from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "shakti-matte"

# Entspannen auf der Akupressurmatte: Rückenlage, Knie aufgestellt (oder
# Kissen unter den Knien), Arme locker. Nur der Atem bewegt sich:
# Skalar "breath" 0..1 hebt den Brustkorb minimal, Wellen zeigen das Lösen.
FLOOR_Y = 236
C = FLOOR_Y - 16
SEG = 26
HIP = (128 + 3 * SEG, C)
ANKLE = (262, FLOOR_Y - 7)
DUR = 10.0


def pre(p):
    b = p.get("breath", 0.0)
    p["x"], p["y"] = HIP
    p["rot"] = 90
    p["lumbar"] = 0.0
    p["thorax"] = -1.5 * b
    p["chest"] = 1.5 * b
    set_abs(SIDE, p, "neck", 172)
    set_abs(SIDE, p, "head", 176)
    return p


IKS = [
    IK("thigh_n", "shin_n", ANKLE, bend=1, end_seg="foot_n", end_abs=0),
    IK("thigh_f", "shin_f", (ANKLE[0] - 3, ANKLE[1]), bend=1, end_seg="foot_f", end_abs=0),
    IK("upperarm_n", "forearm_n", (128 + 70, FLOOR_Y - 6), bend=1, end_seg="hand_n", end_abs=-2),
    IK("upperarm_f", "forearm_f", (128 + 66, FLOOR_Y - 6), bend=1, end_seg="hand_f", end_abs=-2),
]


def spikes():
    out = [Prim("rect", {"x": 60, "y": FLOOR_Y - 3, "width": 180, "height": 7, "rx": 2, "fill": "#7c3a5a"})]
    d = "".join(f"M{x} {FLOOR_Y - 3}l2 -3l2 3" for x in range(62, 238, 6))
    out.append(Prim("path", {"d": d, "fill": "#f9a8d4", "stroke": "none"}))
    return out


def waves():
    out = []
    for i, x in enumerate((110, 150, 190)):
        out.append(Prim("path", {"d": f"M{x - 10} {FLOOR_Y - 34}q5 -6 10 0t10 0", "fill": "none", "stroke": GOOD,
                                 "stroke-width": 2, "stroke-linecap": "round",
                                 "_show": [(4.0 + i * 0.6, DUR - 0.5)]}))
    return out


def build():
    tl = FnTimeline([(0, dict(breath=0)), (4.0, dict(breath=1)), (DUR, dict(breath=0))],
                    iks=IKS, skeleton=SIDE, pre=pre)
    S, OX = 1.32, 196
    scene = group([mat(FLOOR_Y + 2, 40, 330), *spikes(), *side_figure(), *waves()],
                  scale=S, origin=(OX, FLOOR_Y))
    prims = [
        scene,
        label("einatmen", 200, 120, 0, 4.0, 13, GOOD, weight="700"),
        label("lang ausatmen – loslassen", 200, 120, 4.0, DUR, 13, "#7dd3fc", weight="700"),
        caption_band(),
        caption("Langsam auf die Matte legen, Knie aufgestellt", 0, 4.0),
        caption("Ruhig atmen, Rückenmuskeln weich werden lassen", 4.0, DUR),
        static_text("10–20 Minuten – angenehm, nicht schmerzhaft", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=10, title="Shakti-Matte")
