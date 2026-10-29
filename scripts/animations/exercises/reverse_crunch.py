from rig import *
from exercises._bauch_props import FLOOR_Y, PinTimeline, mat_layer, stage, figure, legs_sharp

SLUG = "reverse-crunch"

# Rückenlage, Kopf links. Knie angewinkelt, Füße schweben knapp über der Matte.
# Knie zur Brust ziehen – das Becken rollt leicht ein und hebt ab, Schultern und
# Hände bleiben liegen. Langsam zurück, ohne die Füße abzulegen.
SHOULDER = (160, FLOOR_Y - 15)
WRIST = (227, FLOOR_Y - 8)

START = dict(y=FLOOR_Y - 15, rot=90, neck=-8, head=8,
             **{"thigh_n@": 42, "shin_n@": -44, "foot_n@": 18,
                "thigh_f@": 37, "shin_f@": -40, "foot_f@": 22})
CURL = dict(START, y=FLOOR_Y - 29, lumbar=-10, thorax=-6, chest=-2, neck=-10, head=8,
            **{"thigh_n@": 118, "shin_n@": -10, "foot_n@": 52,
               "thigh_f@": 113, "shin_f@": -6, "foot_f@": 56})


def build():
    iks = [
        IK("upperarm_n", "forearm_n", WRIST, bend=1, end_seg="hand_n", end_abs=0),
        IK("upperarm_f", "forearm_f", (WRIST[0] - 5, WRIST[1]), bend=1, end_seg="hand_f", end_abs=0),
    ]
    keys = [(0, START), (0.8, START), (2.0, CURL), (2.7, CURL), (4.7, START), (5.3, START)]
    tl = PinTimeline(keys, SHOULDER, iks=iks)
    s0 = tl.at(0)
    legs = legs_sharp()
    prims = [
        *stage([
            *mat_layer(),
            ghost(legs, SIDE, s0, 0.16),
            *figure(),
            focus("root", rx=18, ry=9, offset=(-14, -16), end=False, show=[(0.8, 4.7)]),
            arrow("M300 150 Q300 112 262 102", show=[(0.8, 2.0)]),
            arrow("M262 102 Q300 112 300 150", show=[(2.7, 4.7)]),
        ]),
        caption_band(),
        caption("Knie angewinkelt, Füße schweben", 0, 0.8),
        caption("Ausatmen – Knie zur Brust ziehen", 0.8, 2.0),
        caption("Becken rollt leicht ein – halten", 2.0, 2.7),
        caption("Langsam absenken – Füße nicht ablegen", 2.7, 5.3),
        static_text("Aus dem Bauch rollen – nicht mit Schwung", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Reverse Crunch")
