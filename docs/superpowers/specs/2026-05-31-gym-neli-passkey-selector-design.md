# GymPlan — Neli/Thomas Passkey-Auswahl im AuthScreen

**Datum:** 2026-05-31
**Status:** approved (brainstorming)
**Scope:** rein Client-seitig in `gymplan`. Keine Änderungen an `auth-buchboeck`.

## Problem

GymPlan ist eine geteilte App (primär Nelis, sekundär Thomas) hinter dem
WebAuthn-Passkey-Gate von `auth.apps.buchboeck.at` (app_id `gym`,
rpId `gym.apps.buchboeck.at`).

Der Auth-Server unterstützt mehrere Nutzer bereits vollständig: jeder
Endpoint (`login`, `register`, `recovery-code`, `verify-pin`) nimmt einen
`label`-Parameter, der server-seitig auf `'thomas'` defaultet. Nelis
`auth_users`-Zeile existiert (uuid `920133c9-309c-4a52-b814-c0a7813f0b89`,
angelegt in Commit `92e7a5d`), und `gym_sessions` werden über den JWT-`sub`
pro Person getrennt.

**Lücke:** Der GymPlan-Client sendet nie ein `label` (`auth-service.ts`
schickt nur `app_id: 'gym'`), und `AuthScreen.tsx` hat keinen Personen-
Umschalter. Dadurch kann sich die App ausschließlich als Thomas
anmelden/enrollen — Neli kommt nicht hinein und konnte folglich auch nie
einen Passkey für die `gym`-App registrieren.

## Lösung

### 1. `src/lib/auth-service.ts` — `label` durchreichen
- Neuer exportierter Typ `Person = 'neli' | 'thomas'`.
- `loginWithPasskey(person: Person)` sendet `label: person` im
  `login?step=options`-Body (dort wählt der Server die `auth_users`-Zeile
  und die anzubietenden Passkeys).
- `consumeRecoveryCode(code, person: Person)` sendet `label: person` im
  `recovery-code?action=consume`-Body (dort wird geprüft, dass der Code zu
  dieser Person gehört).
- `enrollWithBootstrapToken` bleibt unverändert — der Register-Flow leitet
  den User server-seitig aus dem Bootstrap-Token ab.

### 2. `src/components/AuthScreen.tsx` — Tabs Neli/Thomas
- Zwei Tabs oben auf der Karte. **Default: Neli** (es ist ihre App).
- Die zuletzt gewählte Person wird in `localStorage` (`gym.auth.person`)
  gemerkt und beim nächsten Start vorausgewählt.
- Die Auswahl wird an `loginWithPasskey` / `consumeRecoveryCode` als
  `person` übergeben. Fehlermeldungen nennen die gewählte Person.

### 3. Bootstrap für Nelis ersten Passkey (operativ, kein Code)
Neli braucht **einen** Recovery-Code für `label='neli'`, um auf ihrem Gerät
einmalig ihren Passkey zu erstellen (Tab „Neli" → „Recovery-Code
verwenden"). Der `generate`-Endpoint erzeugt nur Codes für den bereits
eingeloggten User, daher muss der erste Code als Direct-DB-Insert in
`recovery_codes` (user_id = Nelis uuid, `code_hash` = SHA-256 des per
`lib/crockford.js` erzeugten Codes) angelegt werden — dasselbe Admin-Pattern
wie bei `dogfood`. Benötigt den Supabase-Service-Role-Key.

## Annahme / Risiko
- Nelis `auth_users.label` ist `'neli'`. Falls abweichend, liefert
  `login?step=options` „unknown user" (404) — dann Label anpassen.

## Nicht im Scope
- Keine Änderungen am `auth-buchboeck`-Service.
- Kein PIN-UI (für `gym` bewusst entfernt).
- Kein In-App-Generieren von Recovery-Codes für andere Personen.
