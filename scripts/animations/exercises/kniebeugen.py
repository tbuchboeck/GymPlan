from rig import *
from exercises._cardio_props import (ANKLE_UP, PostTimeline, arms_level, figure, focus_mid, label, leg,
                                     scene_group)

SLUG = "kniebeugen"

# Seitansicht, Blick nach rechts. Füße fix (IK), Becken wandert nach hinten
# unten, Oberkörper neigt sich mit geradem Rücken vor, Arme bleiben waagrecht.

FLOOR_Y = 250
SC = 0.86
ANK_X = 210
ANK = (ANK_X, FLOOR_Y - ANKLE_UP)
TOE_X = ANK_X + 22             # Zehenspitze (Fußlänge + Rundung)

STAND = dict(x=ANK_X - 4, y=FLOOR_Y - ANKLE_UP - 97.4, rot=0, neck=0, head=0, arm=-70)
DEEP = dict(x=ANK_X - 34, y=FLOOR_Y - 106 + 50, rot=-40, neck=24, head=8, arm=0)


def post(p):
    p = dict(p)
    # Arme: in der Startpose hängend (arm=-70 -> ~ -90°), sonst waagrecht vorn
    a = p.get("arm", 0)
    p = arms_level(p, abs_deg=a * 90 / 70 if a < 0 else 0, elbow=4)
    p = leg(p, "n", ANK, 0, bend=1)
    p = leg(p, "f", (ANK[0] - 5, ANK[1]), 0, bend=1)
    return p


def build():
    keys = [(0, STAND), (0.7, STAND), (1.3, dict(STAND, arm=0)),
            (2.9, DEEP), (3.5, DEEP),
            (5.0, dict(STAND, arm=0)), (5.4, dict(STAND, arm=0)), (6.0, STAND)]
    tl = PostTimeline(keys, post)

    toe_line = Prim("line", {"x1": TOE_X, "y1": FLOOR_Y - 2, "x2": TOE_X, "y2": FLOOR_Y - 118,
                             "stroke": GOOD, "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.75})
    deep_ghost = ghost(figure(), SIDE, post(dict(STAND, arm=0)), 0.12)
    fig = figure()
    scene = scene_group([
        toe_line,
        deep_ghost,
        *fig,
        focus_mid("thigh_n", 0.5, 20, 10, show=[(1.3, 5.0)]),
        focus("root", rx=13, ry=13, offset=(-6, 2), show=[(2.9, 5.0)]),
        arrow("M150 168 Q138 186 146 206", show=[(1.3, 2.9)]),
        arrow("M152 214 Q140 196 148 176", show=[(3.5, 5.0)]),
    ], SC, FLOOR_Y)
    prims = [
        floor(FLOOR_Y, 40, 360),
        scene,
        label("Knie bleibt hinter", 262, 214, 1.3, 5.0, 11, GOOD, "start"),
        label("der Zehenlinie", 262, 228, 1.3, 5.0, 11, GOOD, "start"),
        caption_band(),
        caption("Hüftbreit stehen, Arme nach vorn", 0, 1.3),
        caption("Einatmen – Po nach hinten absenken", 1.3, 2.9),
        caption("Kurz halten – Rücken gerade", 2.9, 3.5),
        caption("Ausatmen – über die Fersen hoch", 3.5, 5.0),
        caption("Aufrecht – nächste Wiederholung", 5.0, 6.0),
        static_text("Hüfte nach hinten – Fersen bleiben am Boden", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Kniebeugen")
