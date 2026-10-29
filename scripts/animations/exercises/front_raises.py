from rig import *
from exercises._hantel_props import (arc_d, dumbbell_endon_back, dumbbell_endon_front, fist_prim,
                                     focus_seg, grip_point, side_standing)

SLUG = "front-raises"

# Seitansicht, stehend. Obergriff (Handrücken oben): Griffachse zeigt in die
# Tiefe. Arme fast gestreckt nach vorn bis Schulterhöhe, Rumpf bleibt ruhig.

FLOOR_Y = 251
SC = 0.9
CX = 170
ANKLE_N = (CX + 2, FLOOR_Y - 8)
ANKLE_F = (CX - 4, FLOOR_Y - 8)

BASE = dict(x=CX, y=FLOOR_Y - 107, neck=-4, head=2,
            upperarm_n=10, forearm_n=6, hand_n=-2, upperarm_f=8, forearm_f=6, hand_f=-2)
UP = dict(BASE, upperarm_n=92, forearm_n=5, hand_n=-6, upperarm_f=85, forearm_f=5, hand_f=-6)
DOWN_MID = dict(BASE, upperarm_n=48, upperarm_f=46)

DEPTH = (10.0, -7.0)


def grip(hand):
    return lambda c: grip_point(c["P"], hand)[:2]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANKLE_N, bend=-1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANKLE_F, bend=-1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, BASE), (0.6, BASE), (2.0, UP), (2.6, UP), (3.6, DOWN_MID), (4.5, BASE), (4.9, BASE)],
                  iks=iks, skeleton=SIDE)

    far_db = (dumbbell_endon_back(grip("hand_f"), DEPTH, far_col="#3b4656")
              + [fist_prim(grip("hand_f"), FAR, 5.5)]
              + dumbbell_endon_front(grip("hand_f"), DEPTH, near_col=PROP_DARK))
    near_parts = (dumbbell_endon_back(grip("hand_n"), DEPTH) + [fist_prim(grip("hand_n"), NEAR, 6.5)]
                  + dumbbell_endon_front(grip("hand_n"), DEPTH))

    P0 = SIDE.fk(tl.at(0))
    PU = SIDE.fk(tl.at(2.3))
    sx, sy = pt(P0, "chest")
    hx, _, _ = grip_point(PU, "hand_n")
    ghost_arm = ghost(limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR) + near_parts, SIDE, tl.at(0), 0.16)
    shoulder_line = Prim("line", {"x1": sx - 4, "y1": sy, "x2": hx + 46, "y2": sy, "stroke": GOOD,
                                  "stroke-width": 1.6, "stroke-dasharray": "5 4", "opacity": 0.75})

    fig = side_standing(far_arm_extra=far_db, near_arm_extra=near_parts)
    main = group([
        floor(FLOOR_Y + 1, 50, 330),
        shoulder_line,
        ghost_arm,
        *fig,
        focus_seg("upperarm_n", 0.15, 6, rx=11, ry=8, show=[(0.6, 3.6)]),
        arrow(arc_d(sx, sy, 104, -72, -8), show=[(0.6, 2.0)]),
        arrow(arc_d(sx, sy, 104, -8, -66), color=MUTED, width=2.2, show=[(2.6, 4.5)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    ly = FLOOR_Y + (sy - FLOOR_Y) * SC
    lx = CX + (hx + 46 - CX) * SC
    prims = [
        main,
        static_text("Schulterhöhe", lx + 4, ly + 4, 11, GOOD, anchor="start"),
        caption_band(),
        caption("Hanteln vor den Oberschenkeln", 0, 0.6),
        caption("Ausatmen – Arme nach vorn heben", 0.6, 2.0),
        caption("Auf Schulterhöhe kurz halten", 2.0, 2.6),
        caption("Einatmen – langsam senken", 2.6, 4.9),
        static_text("Arme fast gestreckt – Oberkörper bleibt ruhig", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Front Raises")
