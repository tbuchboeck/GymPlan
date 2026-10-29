"""Baut alle Übungsanimationen nach public/exercise-images/.

Nutzung:  python3 scripts/animations/build.py [name ...]
Jede Datei in exercises/ definiert SLUG und build() -> svg-String.
"""
import importlib
import pathlib
import sys
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "public" / "exercise-images"
sys.path.insert(0, str(HERE))

names = sys.argv[1:] or sorted(p.stem for p in (HERE / "exercises").glob("*.py") if not p.stem.startswith("_"))
for name in names:
    mod = importlib.import_module(f"exercises.{name}")
    svg = mod.build()
    # Als <img> geladen muss die SVG gültiges XML sein (z. B. kein rohes "&"),
    # sonst zeigt der Browser gar nichts an.
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        sys.exit(f"{name}: ungültiges SVG – {e}")
    path = OUT / f"{mod.SLUG}.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"{path.relative_to(HERE.parents[1])}  {len(svg) / 1024:.1f} KB")
