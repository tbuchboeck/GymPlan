from rig import *
from ._hantel_b_props import dumbbell, side_fig, label

SLUG = "situps-hantel"

# Sit-up mit Kurzhantel vor der Brust, Seitansicht (Rückenlage, Kopf links).
# Becken und Füße bleiben fix (IK), der Rumpf rollt Wirbel für Wirbel auf.
# Die Hantel liegt längs vor dem Brustbein, beide Hände halten sie.

MAT_Y = 246
HIP = (214, MAT_Y - 15)
ANK_N = (266, MAT_Y - 8)
ANK_F = (262, MAT_Y - 8)

ARMS = dict(upperarm_n=52, forearm_n=112, hand_n=-10, upperarm_f=48, forearm_f=116, hand_f=-10)
LIE = dict(x=HIP[0], y=HIP[1], rot=90, neck=-6, head=0, **ARMS)
UP = dict(x=HIP[0], y=HIP[1], rot=34, lumbar=-14, thorax=-12, chest=-8, neck=-14, head=-4, **ARMS)


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, LIE), (0.6, LIE), (2.1, UP), (2.7, UP), (4.4, LIE), (4.9, LIE)], iks=iks, skeleton=SIDE)

    def db_center(c):
        P = c["P"]
        x, y = pt(P, "thorax")
        a = math.radians(P["thorax"][4] - 90)           # Bauchseite
        return x + 22 * math.cos(a), y - 22 * math.sin(a)

    def abs_focus(c):
        P = c["P"]
        x, y = pt(P, "lumbar")
        a = math.radians(P["lumbar"][4] - 90)
        return {"cx": x + 9 * math.cos(a), "cy": y - 9 * math.sin(a)}

    def hand_on_db(side):
        """Hände greifen die Hantel: IK-Ziel = Griffmitte."""
        def f(pose):
            P = SIDE.fk(pose)
            x, y = pt(P, "thorax")
            a = math.radians(P["thorax"][4] - 90)
            return x + 13 * math.cos(a), y - 13 * math.sin(a)
        return f

    tl.iks += [IK("upperarm_n", "forearm_n", hand_on_db("n"), bend=1),
               IK("upperarm_f", "forearm_f", hand_on_db("f"), bend=1)]

    db = dumbbell("hand_n", "forearm_n", fore=0.95, size=1.15, center_fn=db_center,
                  ang_fn=lambda c: c["P"]["thorax"][4], fist=False)
    fist = Prim("circle", {"r": 7, "fill": NEAR, "stroke": SKIN_LINE, "stroke-width": 1.5},
                lambda c: (lambda p: {"cx": p[0], "cy": p[1]})(db_center(c)))
    figure = side_fig(db_near=[*db, fist])
    prims = [
        mat(MAT_Y, 40, 360),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side(), SIDE,
              tl.at(2.4), 0.13),
        *figure,
        Prim("ellipse", {"rx": 13, "ry": 13, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                         "_show": [(0.6, 4.4)]}, abs_focus),
        arrow("M118 190 Q132 132 178 116", show=[(0.6, 2.1)]),
        arrow("M176 124 Q128 142 116 196", show=[(2.7, 4.4)]),
        Prim("path", {"d": f"M{ANK_N[0] - 14} {MAT_Y - 1}L{ANK_N[0] + 22} {MAT_Y - 1}", "stroke": GOOD,
                      "stroke-width": 3, "stroke-linecap": "round", "opacity": 0.8}),
        label("Füße bleiben am Boden", 330, 212, 0.0, 4.9, 11, GOOD),
        caption_band(),
        caption("Rückenlage, Knie gebeugt, Hantel vor der Brust", 0, 0.6),
        caption("Ausatmen – Oberkörper aufrollen", 0.6, 2.1),
        caption("Oben kurz halten – Bauch fest", 2.1, 2.7),
        caption("Einatmen – langsam abrollen", 2.7, 4.9),
        static_text("Langsam aufrollen – ohne Schwung", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Sit-ups mit Kurzhantel")
