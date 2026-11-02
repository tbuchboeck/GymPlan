"""Einarmiges Rudern am Sling-Trainer – Seitansicht, baut auf face_pulls auf.

Nur die nahe Hand hält einen Griff, die ferne Hand liegt locker an der Hüfte.
Der Ellbogen zieht eng am Körper nach hinten zur Hüfte, der Rumpf dreht
nicht mit (Becken/Brust bleiben zum Anker gerichtet).
"""
from rig import *
from exercises import face_pulls as F

SLUG = "einarm-rudern"

F.EL_PULL = (-16.0, -26.0)    # Ellbogen hinter dem Rumpf, auf Höhe der unteren Rippen
F.HD_PULL = (12.0, -40.0)     # Hand neben dem Bauch


def figure() -> list[Prim]:
    prims: list[Prim] = []
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims.append(F.scapula())
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += F.straps(far=False)
    prims += F.arm_prims(far=False)
    return prims


# ferne Hand an der Hüfte
HIP_HAND = dict(upperarm_f=-28, forearm_f=95, hand_f=0)
START = dict(reach=0.0, scap=0.0, **HIP_HAND)
SET = dict(reach=0.0, scap=1.0, chest=-3, neck=2, **HIP_HAND)
PULL = dict(reach=1.0, scap=1.0, chest=-3, neck=2, **HIP_HAND)


def build():
    tl = F.FaceTimeline([(0, START), (0.8, START), (1.8, SET), (2.2, SET), (3.6, PULL), (4.6, PULL),
                         (6.2, SET), (6.6, START), (7.0, START)], skeleton=SIDE)

    def ctx(t):
        p = tl.at(t)
        return {"P": SIDE.fk(p), "pose": p}

    c_set, c_pull = ctx(2.2), ctx(3.6)
    e0, e1 = F.elbow_pt(c_set), F.elbow_pt(c_pull)
    pull_arrow = arrow(f"M{e0[0] - 6:.0f} {e0[1] + 14:.0f} Q{(e0[0] + e1[0]) / 2:.0f} {e1[1] + 22:.0f} "
                       f"{e1[0] - 12:.0f} {e1[1] + 8:.0f}", show=[(2.2, 3.6)])
    lat = Prim("ellipse", {"rx": 8, "ry": 18, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                           "_show": [(1.8, 6.2)]},
               lambda c: dict(zip(("cx", "cy"), F.body_pt(c, "thorax", 0, 10))))
    post = [
        Prim("rect", {"x": 380, "y": 14, "width": 12, "height": F.FLOOR_Y - 14, "rx": 3, "fill": PROP_DARK}),
        Prim("rect", {"x": 370, "y": F.ANCHOR[1] - 7, "width": 14, "height": 14, "rx": 4, "fill": PROP}),
        Prim("circle", {"cx": F.ANCHOR[0], "cy": F.ANCHOR[1], "r": 4.5, "fill": "none", "stroke": "#d1d5db",
                        "stroke-width": 2.2}),
    ]
    scene = group([floor(F.FLOOR_Y, 60, 394), *post, *figure(), lat, pull_arrow],
                  scale=0.9, origin=(200, F.FLOOR_Y), dy=2)
    prims = [
        scene,
        caption_band(),
        static_text("Nicht mitdrehen – Brust bleibt zum Anker", 200, 24, LEAD_SIZE, MUTED),
        static_text("eine Hand am Griff", 360, 52, 12, MUTED, anchor="end"),
        caption("Ein Griff, Körper gespannt wie ein Brett", 0, 0.8),
        caption("Schulterblatt zurück & runter", 0.8, 2.2),
        caption("Ellbogen eng am Körper nach hinten ziehen", 2.2, 3.6),
        caption("Kurz halten – Becken bleibt gerade", 3.6, 4.6),
        caption("Langsam zurück, dann Seite wechseln", 4.6, 7.0),
    ]
    return render(prims, tl, SIDE, fps=12, title="Einarmiges Rudern (Sling)")
