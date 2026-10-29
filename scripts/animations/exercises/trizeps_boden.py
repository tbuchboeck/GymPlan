from rig import *
from exercises._hantel_props import focus_seg

SLUG = "trizeps-boden"

# Seitansicht, Kopf rechts. Trizeps-Liegestütz auf den Zehen: Hände unter den
# Schultern, Ellbogen beugen eng am Körper nach hinten. Der Körper bleibt ein
# Brett und kippt um die Zehen (Schlüssel "tilt" = Neigung in Grad). Zehen und
# Hände per IK fix am Boden.

FLOOR_Y = 238
TOE = (95.0, FLOOR_Y - 4.0)
HAND_N = (258.0, FLOOR_Y - 5.0)   # unter der Schulter in der Startpose
HAND_F = (254.0, FLOOR_Y - 5.0)

BODY = dict(neck=-4, head=-12, foot_n=6, foot_f=6, thigh_f=-1, shin_f=1)
TOP = dict(BODY, tilt=16.0)
LOW = dict(BODY, tilt=3.8, neck=-2, head=-10)


def place(pose):
    """Becken so setzen, dass der Körper mit Neigung tilt an den Zehen hängt."""
    p = dict(pose)
    p["rot"] = -90 + p.get("tilt", 0.0)
    p["x"], p["y"] = 0.0, 0.0
    P = SIDE.fk(p)
    tx, ty = P["foot_n"][2], P["foot_n"][3]
    p["x"], p["y"] = TOE[0] - tx, TOE[1] - ty
    return p


class PlankTimeline(Timeline):
    def at(self, t):
        pose = place(self._interp(t))
        for ik in self.iks:
            pose = solve_ik(self.skeleton, pose, ik)
        return pose


def build():
    iks = [
        IK("upperarm_n", "forearm_n", HAND_N, bend=-1, end_seg="hand_n", end_abs=0),
        IK("upperarm_f", "forearm_f", HAND_F, bend=-1, end_seg="hand_f", end_abs=0),
    ]
    tl = PlankTimeline([(0, TOP), (0.6, TOP), (2.0, LOW), (2.5, LOW), (3.7, TOP), (4.3, TOP)],
                       iks=iks, skeleton=SIDE)

    body_line = Prim("path", {"fill": "none", "stroke": GOOD, "stroke-width": 1.8, "stroke-dasharray": "5 5",
                              "opacity": 0.75},
                     lambda c: (lambda a, b: {"d": f"M{a[0]:.1f} {a[1] - 14:.1f}L{b[0]:.1f} {b[1] - 14:.1f}"})(
                         pt(c["P"], "shin_n"), pt(c["P"], "chest")))
    P0 = SIDE.fk(tl.at(0))
    PL = SIDE.fk(tl.at(2.2))
    ex, ey = pt(PL, "upperarm_n")
    prims = [
        mat(FLOOR_Y, 50, 350),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side()
              + limb(["thigh_n", "shin_n"], 16, NEAR), SIDE, tl.at(0), 0.13),
        *side_figure(),
        body_line,
        focus_seg("upperarm_n", 0.5, -7, rx=12, ry=7, show=[(0.6, 3.7)]),
        arrow("M352 112 L352 142", show=[(0.6, 2.0)]),
        arrow("M352 150 L352 120", show=[(2.5, 3.7)]),
        Prim("g", {"_show": [(1.6, 3.0)]}, children=[
            Prim("path", {"d": f"M{ex + 12:.1f} {ey - 66:.1f}Q{ex - 8:.1f} {ey - 44:.1f} {ex - 2:.1f} {ey - 12:.1f}",
                          "fill": "none", "stroke": ACCENT, "stroke-width": 1.8, "marker-end": "url(#arrowhead)"}),
            Prim("text", {"x": ex + 34, "y": ey - 72, "font-size": 12, "fill": ACCENT, "font-weight": "600",
                          "text-anchor": "middle"}, text="Ellbogen eng nach hinten"),
        ]),
        static_text("Körper bleibt gerade", 62, 150, 12, GOOD, anchor="start"),
        caption_band(),
        caption("Liegestütz – Hände unter den Schultern", 0, 0.6),
        caption("Einatmen – langsam absenken", 0.6, 2.0),
        caption("Arme eng am Körper", 2.0, 2.5),
        caption("Ausatmen – hochdrücken", 2.5, 4.3),
        static_text("Ellbogen streifen die Rippen – nicht nach außen", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Trizeps-Liegestütze")
