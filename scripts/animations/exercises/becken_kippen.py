from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "becken-kippen"

# Rückenlage, Seitansicht, Kopf links. Skalar "tilt" -1..1:
# -1 = leichtes Hohlkreuz (Lende hebt ab), +1 = Becken sanft zurückgekippt (Lende flach
# am Boden). Bewegung klein und schmerzfrei, Schultern und Füße bleiben liegen.
FLOOR_Y = 236
C = FLOOR_Y - 16
SH = (128, C)
SEG = 26
ANKLE = (262, FLOOR_Y - 7)


def pre(p):
    t = p.get("tilt", 0.0)
    # Hohlkreuz: Lende wölbt sich nach oben (Becken kippt nach vorn),
    # eingerollt: Lende flach, Becken hebt hinten minimal an.
    arch = max(0.0, -t) * 20.0
    roll = max(0.0, t) * 6.0
    # Becken liegt fest, die Lende wölbt sich nach oben, Brustkorb liegt.
    a_lumbar = 180 - arch
    a_thorax = 180 + arch * 0.55
    a_chest = 180 + arch * 0.45
    p["x"], p["y"] = SH[0] + 3 * SEG, C - roll
    p["rot"] = a_lumbar - 90
    p["lumbar"] = 0.0
    p["thorax"] = a_thorax - a_lumbar
    p["chest"] = a_chest - a_thorax
    set_abs(SIDE, p, "neck", 172)
    set_abs(SIDE, p, "head", 176)
    return p


IKS = [
    IK("thigh_n", "shin_n", ANKLE, bend=1, end_seg="foot_n", end_abs=0),
    IK("thigh_f", "shin_f", (ANKLE[0] - 3, ANKLE[1]), bend=1, end_seg="foot_f", end_abs=0),
    IK("upperarm_n", "forearm_n", (SH[0] + 74, FLOOR_Y - 6), bend=1, end_seg="hand_n", end_abs=-2),
    IK("upperarm_f", "forearm_f", (SH[0] + 70, FLOOR_Y - 6), bend=1, end_seg="hand_f", end_abs=-2),
]

MID = dict(tilt=0.0)
HOLLOW = dict(tilt=-1.0)
FLAT = dict(tilt=1.0)

T = [0, 0.6, 2.6, 3.6, 6.0, 7.4, 8.4]


def gap(c):
    t = c["pose"].get("tilt", 0.0)
    a = max(0.0, -t)
    P = c["P"]
    x0, _ = pt(P, "lumbar")
    return {"cx": x0 - 4, "rx": 18, "ry": 0.5 + 5 * a, "opacity": 0.9 * a}


def build():
    keys = [(T[0], MID), (T[1], MID), (T[2], HOLLOW), (T[3], HOLLOW), (T[4], FLAT), (T[5], FLAT), (T[6], MID)]
    tl = FnTimeline(keys, iks=IKS, skeleton=SIDE, pre=pre)
    fig = side_figure()
    S, OX = 1.32, 196
    scene = group([
        mat(FLOOR_Y, 66, 314),
        Prim("ellipse", {"cy": FLOOR_Y - 4, "fill": ACCENT}, gap),
        *fig,
        focus("root", rx=16, ry=10, offset=(-6, 2), end=False, show=[(T[3], T[5])]),
        arrow("M150 214 C160 198 176 198 186 210", show=[(T[1], T[2])]),
        arrow("M186 214 C176 224 160 224 150 218", color=GOOD, show=[(T[3], T[4])]),
    ], scale=S, origin=(OX, FLOOR_Y))
    prims = [
        scene,
        label("kleines Hohlkreuz", 186, 168, T[1], T[3], 12, ACCENT),
        label("Lende sanft in die Matte", 196, 168, T[3], T[5], 12, GOOD),
        caption_band(),
        caption("Rückenlage, Knie aufgestellt", 0, T[1]),
        caption("Becken nach vorn kippen – kleines Hohlkreuz", T[1], T[3]),
        caption("Ausatmen – Becken sanft zurückkippen", T[3], T[5]),
        caption("Locker lösen – im Atemrhythmus wiederholen", T[5], T[6]),
        static_text("Kleine Bewegung, nur so weit es angenehm ist", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Becken kippen")
