from rig import *
from exercises._hantel_props import arc_d, dumbbell_inplane, focus_seg, side_standing

SLUG = "hantel-trizeps"

# Seitansicht, sitzend auf einer Bank. Eine Kurzhantel, beide Handflächen
# unter der oberen Scheibe – die Hantel hängt längs zum Unterarm. Oberarme
# zeigen nach oben (Ellbogen fix), nur die Unterarme senken sich hinter den
# Kopf und strecken wieder. Füße/Gesäß fix.

FLOOR_Y = 251
SC = 0.9
CX = 182
SEAT_Y = FLOOR_Y - 49                     # Oberkante Bank
ROOT = (CX, SEAT_Y - 8)
ANKLE_N = (CX + 52, FLOOR_Y - 8)
ANKLE_F = (CX + 47, FLOOR_Y - 8)

TOP = dict(x=ROOT[0], y=ROOT[1], neck=-2, head=0, lumbar=1,
           upperarm_n=-183, forearm_n=4, hand_n=0, upperarm_f=-181, forearm_f=4, hand_f=0,
           thigh_n=90, shin_n=-90, thigh_f=90, shin_f=-90)
LOW = dict(TOP, upperarm_n=-182, forearm_n=138, hand_n=6, upperarm_f=-180, forearm_f=136, hand_f=6,
           neck=-6, head=2)
MID = dict(TOP, forearm_n=72, forearm_f=71)

HALF = 13.0


def db_center(c):
    P = c["P"]
    _, _, ex, ey, a = P["hand_n"]
    r = math.radians(P["forearm_n"][4])
    k = 1.5 - HALF
    return ex + k * math.cos(r), ey - k * math.sin(r)


def db_axis(c):
    return c["P"]["forearm_n"][4]


def bench():
    x0, x1 = CX - 46, CX + 30
    return [
        Prim("rect", {"x": x0 + 8, "y": SEAT_Y + 8, "width": 8, "height": FLOOR_Y - SEAT_Y - 8, "rx": 2,
                      "fill": PROP_DARK}),
        Prim("rect", {"x": x1 - 16, "y": SEAT_Y + 8, "width": 8, "height": FLOOR_Y - SEAT_Y - 8, "rx": 2,
                      "fill": PROP_DARK}),
        Prim("rect", {"x": x0, "y": SEAT_Y, "width": x1 - x0, "height": 10, "rx": 4, "fill": PROP}),
    ]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANKLE_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANKLE_F, bend=1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, TOP), (0.6, TOP), (2.2, LOW), (2.7, LOW), (3.4, MID), (4.0, TOP), (4.6, TOP)],
                  iks=iks, skeleton=SIDE)

    dbell = dumbbell_inplane(db_center, db_axis, half=HALF, plate=17)
    fig = side_standing(far_arm_extra=dbell, behind=bench())

    P0 = SIDE.fk(tl.at(0))
    ex, ey = pt(P0, "upperarm_n")
    elbow_ring = Prim("circle", {"r": 9, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                                 "stroke-dasharray": "3 3"},
                      lambda c: dict(zip(("cx", "cy"), pt(c["P"], "upperarm_n"))))
    ghost_arm = ghost(limb(["forearm_n", "hand_n"], 12, NEAR) + dbell, SIDE, tl.at(0), 0.15)
    main = group([
        floor(FLOOR_Y + 1, 60, 330),
        ghost_arm,
        *fig,
        focus_seg("upperarm_n", 0.5, 7, rx=13, ry=7, show=[(0.6, 4.0)]),
        elbow_ring,
        arrow(arc_d(ex, ey, 60, 108, 205), color=MUTED, width=2.2, show=[(0.6, 2.2)]),
        arrow(arc_d(ex, ey, 60, 200, 102), show=[(2.7, 4.0)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    gx, gy = CX + (ex - CX) * SC, FLOOR_Y + (ey - FLOOR_Y) * SC
    prims = [
        main,
        Prim("line", {"x1": gx + 10, "y1": gy, "x2": 292, "y2": gy, "stroke": GOOD, "stroke-width": 1.2,
                      "stroke-dasharray": "2 3", "opacity": 0.8}),
        static_text("Ellbogen zeigt", 298, gy - 3, 11, GOOD, anchor="start"),
        static_text("nach oben", 298, gy + 10, 11, GOOD, anchor="start"),
        caption_band(),
        caption("Hantel über Kopf, Arme lang", 0, 0.6),
        caption("Einatmen – hinter den Kopf senken", 0.6, 2.2),
        caption("Kurz halten", 2.2, 2.7),
        caption("Ausatmen – Unterarme nach oben strecken", 2.7, 4.6),
        static_text("Oberarme bleiben neben dem Kopf", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Trizeps-Strecken über Kopf")
