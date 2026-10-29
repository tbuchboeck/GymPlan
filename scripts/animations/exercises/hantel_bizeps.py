from rig import *
from exercises._hantel_props import (arc_d, dumbbell_endon_back, dumbbell_endon_front, fist_prim,
                                     focus_seg, grip_point, side_standing)

SLUG = "hantel-bizeps"

# Seitansicht, stehend. Untergriff (Handflächen vorn): die Griffachse zeigt in
# die Tiefe, die Hantel ist schräg von vorn zu sehen. Oberarme bleiben senkrecht
# am Rumpf, nur die Unterarme beugen. Füße per IK fix.

FLOOR_Y = 251
SC = 0.9
CX = 186
ANKLE_N = (CX + 2, FLOOR_Y - 8)
ANKLE_F = (CX - 4, FLOOR_Y - 8)

BASE = dict(x=CX, y=FLOOR_Y - 107, neck=-4, head=2,
            upperarm_n=3, forearm_n=10, hand_n=4, upperarm_f=1, forearm_f=8, hand_f=4)
UP = dict(BASE, y=FLOOR_Y - 106.5, lumbar=-1, forearm_n=138, hand_n=-12, forearm_f=134, hand_f=-12)
MID = dict(BASE, forearm_n=74, forearm_f=71, hand_n=-4, hand_f=-4)

DEPTH = (10.0, -7.0)


def grip(hand):
    return lambda c: grip_point(c["P"], hand)[:2]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANKLE_N, bend=-1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANKLE_F, bend=-1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, BASE), (0.7, BASE), (1.9, UP), (2.5, UP), (3.6, MID), (4.4, BASE), (4.8, BASE)],
                  iks=iks, skeleton=SIDE)

    far_db = (dumbbell_endon_back(grip("hand_f"), DEPTH, far_col="#3b4656")
              + [fist_prim(grip("hand_f"), FAR, 5.5)]
              + dumbbell_endon_front(grip("hand_f"), DEPTH, near_col=PROP_DARK))
    near_db = (dumbbell_endon_back(grip("hand_n"), DEPTH)
               + [fist_prim(grip("hand_n"), NEAR, 6.5)]
               + dumbbell_endon_front(grip("hand_n"), DEPTH))

    P0 = SIDE.fk(tl.at(0))
    ex, ey = pt(P0, "upperarm_n")
    elbow_ring = Prim("circle", {"r": 9, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                                 "stroke-dasharray": "3 3"},
                      lambda c: dict(zip(("cx", "cy"), pt(c["P"], "upperarm_n"))))
    ghost_arm = ghost(limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
                      + dumbbell_endon_back(grip("hand_n"), DEPTH)
                      + [fist_prim(grip("hand_n"), NEAR, 6.5)]
                      + dumbbell_endon_front(grip("hand_n"), DEPTH), SIDE, tl.at(0), 0.16)

    fig = side_standing(far_arm_extra=far_db, near_arm_extra=near_db)
    main = group([
        floor(FLOOR_Y + 1, 60, 320),
        ghost_arm,
        *fig,
        focus_seg("upperarm_n", 0.5, 8, rx=13, ry=7, show=[(0.7, 3.6)]),
        elbow_ring,
        arrow(arc_d(ex, ey, 62, -80, 30), show=[(0.7, 1.9)]),
        arrow(arc_d(ex, ey, 62, 30, -70), color=MUTED, width=2.2, show=[(2.5, 4.4)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    gx, gy = CX + (ex - CX) * SC, FLOOR_Y + (ey - FLOOR_Y) * SC
    prims = [
        main,
        Prim("line", {"x1": gx - 12, "y1": gy, "x2": 92, "y2": gy, "stroke": GOOD, "stroke-width": 1.2,
                      "stroke-dasharray": "2 3", "opacity": 0.8}),
        static_text("Ellbogen", 62, gy - 4, 12, GOOD),
        static_text("bleibt fix", 62, gy + 9, 12, GOOD),
        caption_band(),
        caption("Arme lang, Handflächen nach vorn", 0, 0.7),
        caption("Ausatmen – hochcurlen", 0.7, 1.9),
        caption("Oben kurz anspannen", 1.9, 2.5),
        caption("Einatmen – langsam absenken", 2.5, 4.8),
        static_text("Ellbogen am Körper – nicht schwingen", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bizeps Curls mit Kurzhanteln")
