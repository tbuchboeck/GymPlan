# GymPlan – Technische Dokumentation

## Überblick

GymPlan ist eine PWA für geführtes Training mit zwei Personen:

- **Neli** – Pläne `@gym`, `@hantel`, `@cardio`. Grundsatz: Sie trägt nichts ein, alles bleibt einfach.
- **Thomas** – zusätzlich die Physio-Routinen `@rücken`, `@nacken`, `@morgen` (mit Befindens-Abfrage bei `@rücken`/`@nacken` und „Kribbelt – abbrechen“ bei Nerven-Übungen).

Die Daten liegen lokal (localStorage, primär) und werden im Hintergrund mit der Supabase-Tabelle `gym_sessions` abgeglichen. Gehostet auf Vercel als statischer Vite-Build.

## Ablauf und Architektur

```
main.tsx
└── ErrorBoundary            Chunk-Ladefehler → 1× neu laden, sonst Fehlerseite
    └── App
        ├── AuthScreen       Passkey / Recovery-Code (wenn keine gültige Sitzung)
        └── PersonApp        (pro Person, key = person)
            ├── LocationSelector   Plan-Auswahl, „heute erledigt“, „diese Woche x/y“, Version
            ├── Home               Wochenpunkte Mo–So, Weitermachen, Plan-Hinweis, Übungsliste, Abmelden
            ├── WorkoutView        Übung für Übung (ExerciseCard, RestTimer)
            ├── WorkoutSummary     Abschluss, ggf. Befinden
            └── WorkoutHistory     Statistiken/Diagramme/Export (lazy geladen)
```

Kein Router: `App.tsx` schaltet per `useState` zwischen Ansichten.

### Login (Passkey, 7 Tage gültig)

- `src/lib/auth-service.ts` spricht mit `https://auth.apps.buchboeck.at/api/auth` (app_id `gym`, `label` = Person). Ergebnis ist ein JWT, dessen `sub` die Nutzer-UUID ist.
- Nach erfolgreichem Login wird `{ token, person, expiresAt }` unter `gym.auth.session` in localStorage gespeichert. `expiresAt = min(JWT-exp, Login-Zeit + 7 Tage)`.
- Beim Start liest `App` die Sitzung (`authService.getSession()`); ist sie gültig, ist die App sofort entsperrt – auch offline. Abgelaufene Sitzungen werden gelöscht.
- `getCurrentUserId()` liefert das `sub` nur bei gültiger Sitzung; ohne Sitzung wird nicht synchronisiert (lokal geht trotzdem alles).
- „Abmelden“ auf der Startseite löscht die Sitzung und führt zurück zum Login (Personenwechsel).
- Der früher verwendete Schlüssel `gym.auth.session.v1` in sessionStorage wird nicht mehr gelesen und beim Login/Abmelden entfernt.

### Synchronisation

`src/lib/session-sync.ts`: Nach dem Entsperren werden alle lokalen Sessions hochgeladen (`upsert` nach `id`) und die entfernten Sessions des Nutzers geholt (`pushAllAndPull`), dann funktional zusammengeführt (`mergeSessions`). Neue Sessions werden einzeln „fire-and-forget“ gepusht. Befinden, Kribbeln und abgebrochene Übungen werden – ohne DB-Änderung – als JSON mit Präfix `gp:` in der Spalte `notes` abgelegt.

### Lokale Speicher-Schlüssel

| Schlüssel | Inhalt |
|-----------|--------|
| `gym.auth.session` | Login-Sitzung (Token, Person, Ablauf) |
| `gym.auth.person` | zuletzt gewählte Person im Login |
| `workoutSessions.<person>` | Trainings der Person (Altbestand `workoutSessions` wird einmalig übernommen) |
| `workoutInProgress.<person>` | angefangenes Training (Fortsetzen, max. 12 h) |
| `lastPlan.<person>` | zuletzt gewählter Plan (Vorreihung in der Plan-Auswahl) |
| `gym.chunkReloaded` (sessionStorage) | Schutz gegen Neulade-Schleifen der ErrorBoundary |

### Zeit und Wochen

Alle Tages- und Wochenberechnungen (`src/utils/statistics.ts`) laufen in **Ortszeit**: Tagesschlüssel `YYYY-MM-DD` aus `getFullYear/getMonth/getDate` (nie `toISOString`), Woche = Montag 00:00 bis Sonntag. Serien beginnen heute oder gestern. Hilfsfunktionen: `localDayKey`, `startOfWeek`, `isInWeekOf`, `isSameLocalDay`, `weekdayIndex`, `formatDayCount` („1 Tag“/„n Tage“).

## Pläne

| Variable (`src/data/workoutPlan.ts`) | Plan | Übungen | Einheiten/Woche |
|---|---|---|---|
| `gymWorkoutPlan` | Ganzkörper-Trainingsplan (@gym) | 12 | 2 |
| `homeWorkoutPlan` | Hanteltraining (@hantel) | 12 | 2 |
| `homeWorkoutPlan2` | Cardio (@cardio) | 15 | 2 |
| `backWorkoutPlan` | Rücken-Aufbau (@rücken) | 6 | 4 |
| `neckWorkoutPlan` | Nacken, Schulter & BWS (@nacken) | 14 | 4 |
| `morningWorkoutPlan` | Morgen-Reset (@morgen) | 10 | 7 |

Sessions werden über `planName` dem Plan zugeordnet – Plan-Namen daher nicht leichtfertig umbenennen (sonst passen Wochen-/Tagesanzeigen alter Trainings nicht mehr). Ein Plan kann einen `notice` (Warnhinweis) haben, der auf der Startseite in einer gelben, aufklappbaren Box vor den Übungen steht; Übungen mit `caution` bekommen im Training den Abbrechen-Knopf.

## Übungsanimationen

`scripts/animations/` erzeugt die SVGs in `public/exercise-images/` (SMIL, kein JavaScript): `rig.py` (Skelette, Posen-Timeline, IK, Renderer), `exercises/<name>.py` je Übung, `build.py` baut alle oder einzelne, `preview.cjs` erstellt Kontaktabzüge. Konventionen siehe `scripts/animations/README.md`.

## Versionierung

- `package.json` → `version` ist die fachliche Version; bei Änderungen erhöhen.
- `vite.config.ts` bäckt `{ version, sha, builtAt }` als `__BUILD_INFO__` ein (Commit aus `VERCEL_GIT_COMMIT_SHA` bzw. lokal `git`) und schreibt `/version.json`.
- `VersionBadge` zeigt die Version im Login und unten in der Plan-Auswahl und vergleicht mit `/version.json`; bei Abweichung gibt es „neu laden“ (inkl. Service-Worker-Update).

## PWA und Hosting

- **Manifest**: nur noch das von vite-plugin-pwa erzeugte `manifest.webmanifest` (konfiguriert in `vite.config.ts`: PNG-Icons inkl. maskable, `lang: de`, Theme/Hintergrund `#0f172a`). `public/manifest.json` gibt es nicht mehr.
- **Service Worker**: `registerType: 'autoUpdate'`, Precache aller Build-Dateien inkl. Übungsbilder. Registrierung über die externe Datei `/registerSW.js` – kein Inline-Script, daher mit `script-src 'self'` verträglich.
- **Chunk-Fehler nach Deploys**: Die `ErrorBoundary` erkennt „Failed to fetch dynamically imported module“ / „Importing a module script failed“ / `ChunkLoadError` und lädt einmal neu.
- **vercel.json**: SPA-Rewrite nur für Pfade ohne Dateiendung und außerhalb `assets/` bzw. `exercise-images/` (fehlende Dateien liefern so 404 statt `index.html`). Header: `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Permissions-Policy` (Kamera/Mikrofon/Standort aus), CSP:
  `default-src 'self'; connect-src 'self' https://auth.apps.buchboeck.at https://*.supabase.co; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; frame-ancestors 'none'; manifest-src 'self'; worker-src 'self'`.
  `style-src 'unsafe-inline'` ist für Inline-Styles von React/Recharts nötig.
- Vercel-Umgebungsvariablen: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`.

## Entwicklung

```bash
npm install
cp .env.example .env.local
npm run dev       # Entwicklungsserver
npm run build     # tsc -b + vite build
npm run preview   # Build ansehen (Service Worker aktiv)
npm run lint
```

## Sicherheit Supabase

### Ist-Zustand

`gym_sessions` (Spalten u. a. `id text`, `user_id uuid not null`, `date`, `plan_name`, …, `notes`) hat RLS aktiviert, die Policies erlauben aber laut bisheriger Einrichtung **alles für `anon`**:

```sql
CREATE POLICY "Allow anon read"   ON gym_sessions FOR SELECT USING (true);
CREATE POLICY "Allow anon insert" ON gym_sessions FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon update" ON gym_sessions FOR UPDATE USING (true);
```

Die App filtert zwar per `.eq('user_id', …)`, das ist aber nur Client-Logik: Wer den (öffentlich im Bundle stehenden) anon-Key kennt, kann alle Trainings beider Personen lesen und beliebige Zeilen schreiben oder überschreiben. Der Passkey-JWT wird an Supabase derzeit **nicht** mitgeschickt.

### ToDo (bewusst noch nicht im App-Code umgesetzt)

Ziel: Supabase soll den JWT des Auth-Service prüfen und Zeilen nur für `user_id = sub` freigeben. Zwei Wege:

1. **JWT direkt an Supabase (bevorzugt, wenig Code):**
   - Der Auth-Service muss einen Token ausstellen, den Supabase akzeptiert: entweder als *Third-Party Auth*-Anbieter (Supabase prüft per JWKS/OIDC-Discovery des Auth-Service) oder signiert mit dem JWT-Schlüssel des Supabase-Projekts. Der Token braucht `sub` (UUID), `role: "authenticated"` und passende `aud`/`iss`/`exp`.
   - In der App: `createClient(url, anonKey, { accessToken: async () => authService.getSession()?.token ?? null })`.
   - Achtung: Offline-Sitzungen gelten bis zu 7 Tage, der JWT ggf. kürzer – abgelaufene Tokens führen dann zu 401 beim Sync (die App arbeitet lokal weiter, Sync erst nach erneutem Login). Ggf. Token-Refresh im Auth-Service vorsehen.
2. **Supabase Edge Function als Gateway:** Funktion prüft den Auth-Service-JWT (JWKS), schreibt/liest mit Service-Role-Key ausschließlich Zeilen mit `user_id = sub`. Danach den anon-Zugriff auf `gym_sessions` komplett sperren.

### SQL-Entwurf (für Weg 1)

```sql
-- Alte, offene Policies entfernen
DROP POLICY IF EXISTS "Allow anon read"   ON gym_sessions;
DROP POLICY IF EXISTS "Allow anon insert" ON gym_sessions;
DROP POLICY IF EXISTS "Allow anon update" ON gym_sessions;

ALTER TABLE gym_sessions ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON gym_sessions FROM anon;

-- Nur eigene Zeilen (sub aus dem geprüften JWT)
CREATE POLICY "own rows select" ON gym_sessions
  FOR SELECT TO authenticated
  USING (user_id::text = auth.jwt() ->> 'sub');

CREATE POLICY "own rows insert" ON gym_sessions
  FOR INSERT TO authenticated
  WITH CHECK (user_id::text = auth.jwt() ->> 'sub');

CREATE POLICY "own rows update" ON gym_sessions
  FOR UPDATE TO authenticated
  USING (user_id::text = auth.jwt() ->> 'sub')
  WITH CHECK (user_id::text = auth.jwt() ->> 'sub');

-- Löschen bei Bedarf analog (die App löscht derzeit nichts)
```

Hinweis: `upsert` auf eine fremde `id` scheitert danach an der UPDATE-Policy – gewollt. Reihenfolge beim Umstellen: erst Auth-Service/Token und App-Client (`accessToken`) ausrollen und prüfen, dann die Policies tauschen.

## Erkenntnisse

- Tagesgrenzen nie über `toISOString()` bilden – in Österreich verschiebt das Trainings nach 22/23 Uhr bzw. vor 1/2 Uhr auf den falschen Tag.
- Nach Deploys fehlen alte Chunks im Cache → ErrorBoundary mit einmaligem Neuladen.
- Nur ein Manifest verwenden (vite-plugin-pwa), sonst widersprüchliche Icons/Farben.
- Nicht auf bereits gemergte Branches pushen; Commits gehen sonst verloren.
- `.toSorted()` statt `.sort()` auf Props/State.
