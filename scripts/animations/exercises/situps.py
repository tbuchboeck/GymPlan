from rig import *
from exercises._cardio_props import PostTimeline, figure, focus_mid, leg

SLUG = "situps"

# Rückenlage auf der Matte, Kopf links, Knie gebeugt, Füße fix (IK).
# Der Oberkörper rollt Wirbel für Wirbel auf (Wirbelsäule gebeugt, rot
# nimmt ab) und wieder ab. Arme vor der Brust gekreuzt, Nacken locker.

FLOOR_Y = 238                  # Oberkante Matte
PX = 214
PY = FLOOR_Y - 16
ANK = (PX + 82, FLOOR_Y - 8)

ARMS = dict(upperarm_n=20, forearm_n=148, hand_n=12, upperarm_f=26, forearm_f=144, hand_f=12)
LIE = dict(ARMS, x=PX, y=PY, rot=90, neck=-3, head=0)
CURL = dict(ARMS, x=PX, y=PY, rot=66, lumbar=-4, thorax=-14, chest=-16, neck=-20, head=-4)
TOP = dict(ARMS, x=PX + 1, y=PY - 1, rot=16, lumbar=-8, thorax=-10, chest=-10, neck=-12, head=-2)


def post(p):
    p = leg(p, "n", ANK, 0, bend=1)
    p = leg(p, "f", (ANK[0] - 4, ANK[1]), 0, bend=1)
    return p


def build():
    keys = [(0, LIE), (0.6, LIE), (1.4, CURL), (2.1, TOP), (2.6, TOP), (3.5, CURL), (4.3, LIE), (4.9, LIE)]
    tl = PostTimeline(keys, post)

    # Abstandshalter Kinn–Brust: kleiner grüner Punkt "Faust" zwischen Kinn und Brust
    def fist(c):
        P = c["P"]
        cx, cy = pt(P, "neck")
        hx, hy = pt(P, "chest")
        a = math.radians(P["chest"][4] - 90)  # Blickrichtung
        return {"cx": (cx + hx) / 2 + 17 * math.cos(a), "cy": (cy + hy) / 2 - 17 * math.sin(a)}

    prims = [
        mat(FLOOR_Y, 50, 350),
        ghost(figure(), SIDE, post(LIE), 0.13),
        *figure(),
        Prim("circle", {"r": 5.5, "fill": "none", "stroke": GOOD, "stroke-width": 2, "opacity": 0.9,
                        "_show": [(1.2, 3.7)]}, fist),
        focus_mid("thorax", 0.2, 22, 11, show=[(0.6, 3.5)]),
        arrow("M118 196 Q122 140 178 118", show=[(0.6, 2.1)]),
        arrow("M180 110 Q114 128 112 192", show=[(2.6, 4.3)]),
        caption_band(),
        caption("Rückenlage, Knie gebeugt, Füße fest", 0, 0.6),
        caption("Ausatmen – Wirbel für Wirbel aufrollen", 0.6, 2.1),
        caption("Oben kurz halten", 2.1, 2.6),
        caption("Einatmen – langsam abrollen", 2.6, 4.3),
        caption("Kopf ablegen – Nacken locker", 4.3, 4.9),
        static_text("Nacken locker – Kinn faustbreit von der Brust", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Sit-Ups")
