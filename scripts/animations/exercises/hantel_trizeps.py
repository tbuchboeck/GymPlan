from rig import *
from exercises._hantel_props import arc_d, dumbbell_inplane, fist_prim, focus_seg, grip_point, limb_sharp
from rig import Seg, Skeleton

SLUG = "hantel-trizeps"

# Seitansicht, sitzend auf einer Bank, einarmig (naher Arm). Neutraler Griff:
# Griffachse in der Bildebene, senkrecht zum Unterarm. Der Oberarm zeigt nach
# oben (Ellbogen fix), nur der Unterarm senkt sich hinter den Kopf und streckt
# wieder. Die andere Hand liegt auf dem Oberschenkel. Füße/Gesäß fix.

FLOOR_Y = 251
SC = 0.9
CX = 182
SEAT_Y = FLOOR_Y - 49                     # Oberkante Bank
ROOT = (CX, SEAT_Y - 8)
ANKLE_N = (CX + 52, FLOOR_Y - 8)
ANKLE_F = (CX + 47, FLOOR_Y - 8)

TOP = dict(x=ROOT[0], y=ROOT[1], neck=-8, head=4, lumbar=1,
           upperarm_n=-176, forearm_n=-2, hand_n=0, 
           thigh_n=90, shin_n=-90, thigh_f=90, shin_f=-90)
LOW = dict(TOP, upperarm_n=-175, forearm_n=140, hand_n=6)
MID = dict(TOP, forearm_n=72)

HALF = 13.0

# Eigenes Skelett: In rig.SIDE reicht der Oberarm (36) nur bis zur Kopfmitte;
# real liegt der Ellbogen über Kopf etwa auf Scheitelhöhe. Daher hier längere
# Oberarme (51) – sonst identisch zu SIDE.
TRI = Skeleton([Seg(s.name, s.parent, 51 if s.name.startswith("upperarm") else s.length, s.rest)
                for s in SIDE.segs])


def figure(dbell, behind):
    prims = list(behind)
    prims += limb_sharp(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims += head_side()
    prims += limb_sharp(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(dbell)
    return prims


def grip(c):
    return grip_point(c["P"], "hand_n")[:2]


def db_axis(c):
    return c["P"]["forearm_n"][4] + 90


def thigh_rest(pose):
    """Ziel für die ferne Hand: auf dem Oberschenkel, kurz vor dem Knie."""
    P = TRI.fk(pose)
    sx, sy, ex, ey, _ = P["thigh_f"]
    return sx + (ex - sx) * 0.62, sy + (ey - sy) * 0.62 - 9


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
        IK("upperarm_f", "forearm_f", thigh_rest, bend=1, end_seg="hand_f", end_abs=-10),
    ]
    tl = Timeline([(0, TOP), (0.6, TOP), (2.2, LOW), (2.7, LOW), (3.4, MID), (4.0, TOP), (4.6, TOP)],
                  iks=iks, skeleton=TRI)

    dbell = dumbbell_inplane(grip, db_axis, half=HALF, plate=16) + [fist_prim(grip, NEAR, 6.5)]
    fig = figure(dbell, bench())

    P0 = TRI.fk(tl.at(0))
    ex, ey = pt(P0, "upperarm_n")
    elbow_ring = Prim("circle", {"r": 9, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                                 "stroke-dasharray": "3 3"},
                      lambda c: dict(zip(("cx", "cy"), pt(c["P"], "upperarm_n"))))
    ghost_arm = ghost(limb(["forearm_n", "hand_n"], 12, NEAR) + dbell, TRI, tl.at(0), 0.15)
    main = group([
        floor(FLOOR_Y + 1, 60, 330),
        ghost_arm,
        *fig,
        focus_seg("upperarm_n", 0.5, 7, rx=13, ry=7, show=[(0.6, 4.0)]),
        elbow_ring,
        arrow(arc_d(ex, ey, 54, 112, 205), color=MUTED, width=2.2, show=[(0.6, 2.2)]),
        arrow(arc_d(ex, ey, 54, 200, 114), show=[(2.7, 4.0)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    gx, gy = CX + (ex - CX) * SC, FLOOR_Y + (ey - FLOOR_Y) * SC
    prims = [
        main,
        Prim("line", {"x1": gx + 10, "y1": gy, "x2": 292, "y2": gy, "stroke": GOOD, "stroke-width": 1.2,
                      "stroke-dasharray": "2 3", "opacity": 0.8}),
        static_text("Ellbogen zeigt", 298, gy - 3, 11, GOOD, anchor="start"),
        static_text("nach oben", 298, gy + 10, 11, GOOD, anchor="start"),
        caption_band(),
        caption("Hantel über Kopf, Arm lang", 0, 0.6),
        caption("Einatmen – hinter den Kopf senken", 0.6, 2.2),
        caption("Unten kurz halten", 2.2, 2.7),
        caption("Ausatmen – Unterarm nach oben strecken", 2.7, 4.6),
        static_text("Ellbogen fix – nur der Unterarm bewegt sich", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, TRI, title="Trizeps-Strecken über Kopf")
