# Übungsanimationen

Animierte SVGs (SMIL, kein JavaScript) für `public/exercise-images/`.
Die App bindet sie per `imageUrl` in `src/data/workoutPlan.ts` als `<img>` ein.

```bash
python3 scripts/animations/build.py              # alle bauen
python3 scripts/animations/build.py chin_tuck    # nur eine
node scripts/animations/preview.cjs public/exercise-images/chin-tuck.svg /tmp/x.png 8   # Kontaktabzug
```

## Aufbau

- `rig.py` – Skelette (`SIDE`, `FRONT`), Timeline mit Schlüsselposen,
  IK/Anchor, Zeichen-Bausteine, Renderer.
- `exercises/<name>.py` – eine Übung: `SLUG` (Dateiname) und `build()`.
- Referenzen: `exercises/chin_tuck.py` (Nahansicht, Geisterpose),
  `exercises/katze_kuh.py` (Ganzkörper, IK hält Hände/Knie am Boden,
  Anchor hält Schultern über den Händen).

## Konventionen

- Leinwand 400×300. Unten ab y=258 liegt das `caption_band()` für die
  Phasentexte (`caption(text, t0, t1)`), oben (y≈24) ein kurzer Leitsatz.
  Kein Titel – die Karte zeigt den Namen schon.
- Winkel mathematisch: 0° = rechts, 90° = oben, positiv = gegen den
  Uhrzeigersinn. Posen enthalten **relative** Winkel (Abweichung von der
  Ruhelage) pro Segment, dazu `x`, `y` (Becken) und `rot` (ganze Figur).
- `SIDE` blickt nach rechts; `_n` = nahe Seite (hell), `_f` = ferne (dunkel).
  Ruhelage: aufrecht stehend, Arme hängen, Füße zeigen nach vorn.
- `FRONT`: `_L`/`_R` = linke/rechte **Bildschirmseite**. Ruhelage: stehend,
  Arme hängen. Kopf-Drehung über den Skalar `turn` (-1..1).
  Liegende Figuren: `rot=-90` (Kopf rechts) bzw. `rot=90` (Kopf links).
- Loops: erste und letzte Schlüsselpose gleich. Halten = Pose zweimal.
- Farben aus `rig.py` verwenden (NEAR/TORSO/FAR/ACCENT/GOOD/WARN/PROP…).
  ACCENT (gelb) = Bewegungspfeile/Fokus, GOOD (grün) = Dehnung/richtig,
  WARN (rot) = Achtung.
- `ghost(...)` zeigt die Startpose blass, `focus(...)` pulsiert dort, wo es
  arbeiten/dehnen soll, `arrow(...)` mit `show=[(t0, t1)]` nur während der
  Bewegung.
- Ziel-Dateigröße < ~120 KB (fps=15 ist Standard; bei langen Loops fps=12).
