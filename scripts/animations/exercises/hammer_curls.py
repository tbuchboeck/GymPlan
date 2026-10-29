from rig import *
from exercises._hantel_props import (arc_d, dumbbell_inplane, fist_prim, focus_seg, grip_point,
                                     side_standing, PLATE_F)

SLUG = "hammer-curls"

# Seitansicht, stehend. Neutraler Griff (Daumen zeigt nach vorn bzw. oben):
# die Griffachse liegt in der Bildebene, senkrecht zum Unterarm – die Hantel
# ist als Griff mit zwei Scheiben zu sehen und dreht mit dem Unterarm.

FLOOR_Y = 251
SC = 0.9
CX = 186
ANKLE_N = (CX + 2, FLOOR_Y - 8)
ANKLE_F = (CX - 4, FLOOR_Y - 8)

BASE = dict(x=CX, y=FLOOR_Y - 107, neck=-4, head=2,
            upperarm_n=3, forearm_n=8, hand_n=0, upperarm_f=1, forearm_f=6, hand_f=0)
UP = dict(BASE, lumbar=-1, forearm_n=132, forearm_f=128)
MID = dict(BASE, forearm_n=70, forearm_f=67)


def grip(hand):
    return lambda c: grip_point(c["P"], hand)[:2]


def axis(fore):
    # Griff senkrecht zum Unterarm; Daumenende zeigt in Richtung +90°
    return lambda c: c["P"][fore][4] + 90


def thumb(fore, hand, col):
    def f(c):
        x, y, _ = grip_point(c["P"], hand)
        a = math.radians(c["P"][fore][4] + 90)
        return {"cx": x + 5.5 * math.cos(a), "cy": y - 5.5 * math.sin(a)}
    return Prim("circle", {"r": 3.2, "fill": col, "stroke": SKIN_LINE, "stroke-width": 1.3}, f)


def build():
    iks = [
        IK("thigh_n", "shin_n", ANKLE_N, bend=-1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANKLE_F, bend=-1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, BASE), (0.7, BASE), (1.9, UP), (2.6, UP), (3.7, MID), (4.5, BASE), (4.9, BASE)],
                  iks=iks, skeleton=SIDE)

    def db(hand, fore, col, dark, fcol, fr):
        return (dumbbell_inplane(grip(hand), axis(fore), half=12, plate=17, color=col, dark=dark)
                + [fist_prim(grip(hand), fcol, fr), thumb(fore, hand, fcol)])

    far_db = db("hand_f", "forearm_f", PLATE_F, "#334155", FAR, 5.5)
    near_db = db("hand_n", "forearm_n", PROP, PROP_DARK, NEAR, 6.5)

    P0 = SIDE.fk(tl.at(0))
    ex, ey = pt(P0, "upperarm_n")
    ghost_arm = ghost(limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR) + near_db, SIDE, tl.at(0), 0.16)
    elbow_ring = Prim("circle", {"r": 9, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                                 "stroke-dasharray": "3 3"},
                      lambda c: dict(zip(("cx", "cy"), pt(c["P"], "upperarm_n"))))

    fig = side_standing(far_arm_extra=far_db, near_arm_extra=near_db)
    main = group([
        floor(FLOOR_Y + 1, 60, 320),
        ghost_arm,
        *fig,
        focus_seg("upperarm_n", 0.55, 8, rx=13, ry=7, show=[(0.7, 3.7)]),
        focus_seg("forearm_n", 0.35, 6, rx=10, ry=6, show=[(0.7, 3.7)]),
        elbow_ring,
        arrow(arc_d(ex, ey, 64, -78, 28), show=[(0.7, 1.9)]),
        arrow(arc_d(ex, ey, 64, 28, -68), color=MUTED, width=2.2, show=[(2.6, 4.5)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    PU = SIDE.fk(tl.at(2.2))
    hx, hy, _ = grip_point(PU, "hand_n")
    hx, hy = CX + (hx - CX) * SC, FLOOR_Y + (hy - FLOOR_Y) * SC
    prims = [
        main,
        Prim("g", {"_show": [(1.7, 3.0)]}, children=[
            Prim("path", {"d": f"M{hx + 52:.1f} {hy - 14:.1f}Q{hx + 24:.1f} {hy - 30:.1f} {hx + 4:.1f} {hy - 16:.1f}",
                          "fill": "none", "stroke": ACCENT, "stroke-width": 1.8, "marker-end": "url(#arrowhead)"}),
            Prim("text", {"x": hx + 56, "y": hy - 8, "font-size": 12, "fill": ACCENT, "font-weight": "600"},
                 text="Daumen oben"),
        ]),
        caption_band(),
        caption("Neutraler Griff – Daumen zeigt nach vorn", 0, 0.7),
        caption("Ausatmen – hochbeugen", 0.7, 1.9),
        caption("Oben kurz halten", 1.9, 2.6),
        caption("Einatmen – langsam absenken", 2.6, 4.9),
        static_text("Griff bleibt neutral – Handgelenk nicht drehen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Hammer Curls")
