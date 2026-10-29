# GymPlan

Progressive Web App (PWA) für geführtes Training – für **Neli** und **Thomas**, mit den Trainingsplänen von Trainer Martin Schiendorfer und eigenen Physio-Routinen. Deutschsprachig, dunkles Design, für das Handy gebaut und auch offline nutzbar.

## Funktionen

- **Login mit Passkey** (Fingerabdruck/Face ID) über `auth.apps.buchboeck.at`, Person wählbar (Neli/Thomas). Der Login bleibt **7 Tage gültig** – auch offline und nach Neustart der App. „Abmelden“ auf der Startseite beendet die Sitzung (z. B. um die Person zu wechseln).
- **Plan-Auswahl** bei jedem Start: zeigt pro Plan „heute erledigt“ und „diese Woche x/y“. Der zuletzt gewählte Plan steht oben und ist hervorgehoben; bei Thomas steht vor 11 Uhr `@morgen` ganz oben, solange er heute noch nicht erledigt ist.
- **Startseite**: Wochenübersicht Mo–So (Punkte für erledigte Tage, „x / Einheiten pro Woche“ für den aktuellen Plan), „Weitermachen bei Übung X/Y“ für ein angefangenes Training, Plan-Hinweis (z. B. wann ärztlich abklären), Übungsliste zum direkten Einstieg.
- **Geführtes Training** Übung für Übung mit Satz-Abhaken, Pausen-Timer und animierten Übungsbildern (SVG).
- **Befinden & Vorsicht** (nur Thomas, `@rücken`/`@nacken`): Abfrage „besser/gleich/schlechter“ und Kribbeln nach dem Training, „Kribbelt – abbrechen“ bei Nerven-Übungen.
- **Statistiken**: Verlauf, Serien (Streak), Wochentage, Diagramme; Export/Import als JSON/CSV.
- **Synchronisation** der Trainings mit Supabase (lokal zuerst, Server im Hintergrund).
- **Offline**: Service Worker speichert die App inkl. aller Übungsbilder.

Erinnerungen per Push gibt es bewusst **nicht** (die frühere Einstellung war eine Attrappe ohne echte Benachrichtigungen). Stattdessen zeigt die Plan-Auswahl, was heute bzw. diese Woche noch offen ist.

## Pläne und Personen

| Plan | Kennung | Übungen | Einheiten/Woche | Für |
|------|---------|---------|-----------------|-----|
| Ganzkörper-Trainingsplan | `@gym` | 12 | 2 | Neli, Thomas |
| Hanteltraining | `@hantel` | 12 | 2 | Neli, Thomas |
| Cardio | `@cardio` | 15 | 2 | Neli, Thomas |
| Rücken-Aufbau | `@rücken` | 6 | 4 | Thomas |
| Nacken, Schulter & BWS | `@nacken` | 14 | 4 | Thomas |
| Morgen-Reset | `@morgen` | 10 | 7 | Thomas |

Die Pläne stehen in `src/data/workoutPlan.ts`, die Sichtbarkeit pro Person (`onlyFor`) in `src/components/LocationSelector.tsx`. Neli soll nichts eintragen müssen – für sie bleibt alles so einfach wie möglich.

## Entwicklung

```bash
npm install
cp .env.example .env.local   # VITE_SUPABASE_URL und VITE_SUPABASE_ANON_KEY eintragen
npm run dev                  # http://localhost:5173
npm run build                # Typprüfung + Produktions-Build nach dist/
npm run preview              # Build lokal ansehen
npm run lint
```

Ohne Supabase-Variablen läuft die App rein lokal (keine Synchronisation).

### Übungsanimationen

Die animierten SVGs in `public/exercise-images/` werden mit einem Python-Generator unter `scripts/animations/` erzeugt (Skelett-Rig, Schlüsselposen, SMIL-Animation ohne JavaScript):

```bash
python3 scripts/animations/build.py              # alle bauen
python3 scripts/animations/build.py chin_tuck    # nur eine Übung
```

Details und Konventionen: `scripts/animations/README.md`.

### Version

Die Version kommt aus `package.json` (`version`), dazu Commit-Kürzel und Build-Zeitpunkt. Sie werden beim Build eingebacken und zusätzlich als `/version.json` ausgeliefert. Login-Seite und Plan-Auswahl zeigen die Version an und bieten „neu laden“, wenn online schon eine neuere Version liegt. Bei inhaltlichen Änderungen `version` in `package.json` erhöhen.

## Als App installieren

- **iPhone (Safari):** Teilen → „Zum Home-Bildschirm“.
- **Android (Chrome):** Menü → „Zum Startbildschirm hinzufügen“ bzw. „App installieren“.

## Technik

React 19, TypeScript, Vite 7, Tailwind CSS 4, vite-plugin-pwa (Workbox), Recharts (nachgeladen), Lucide-Icons, Supabase. Gehostet auf Vercel (`vercel.json`: SPA-Rewrite und Sicherheits-Header inkl. CSP).

Mehr Details (Architektur, Speicher-Schlüssel, Sicherheit): [DOCUMENTATION.md](DOCUMENTATION.md).

## Lizenz

Privates Projekt für persönliche Nutzung.
