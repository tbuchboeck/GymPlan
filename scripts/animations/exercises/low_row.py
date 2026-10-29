from rig import *
from exercises._tb_gym_props import *

SLUG = "low-row"

# Low Row am Kabelzug: Seilrolle unten (Adjustable Pulley), sitzend auf
# niedriger Bank, Füße an der Fußplatte, Knie leicht gebeugt. Seitansicht,
# Blick zur Rolle. Aus leichter Vorlage mit geradem Rücken aufrichten und
# den Griff zur Hüfte rudern, Schulterblätter zusammen.

FLOOR_Y = 250
HIP = (128.0, 208.0)
ANK_N, ANK_F = (228.0, 204.0), (224.0, 205.0)
PULLEY = (302.0, 230.0)
FAR_OFF = (-4.0, -1.0)


def post(pose, P):
    p = pose.get("pull", 0.0)
    scap = min(1.0, max(0.0, (p - 0.4) / 0.5))
    s = shoulder_side(P, scap)
    # Start: Arme lang Richtung Rolle; Ende: Hände am Bauch, Ellbogen hinten
    d = math.radians(-27)
    w0 = (s[0] + 66 * math.cos(d), s[1] - 66 * math.sin(d))
    w1 = body_pt(P, "lumbar", -2, 11)
    w = (w0[0] + (w1[0] - w0[0]) * p, w0[1] + (w1[1] - w0[1]) * p)
    out = {"scap": scap}
    for k, far in (("", False), ("_f", True)):
        sk = (s[0] + FAR_OFF[0], s[1] + FAR_OFF[1]) if far else s
        wk = (w[0] + FAR_OFF[0], w[1] + FAR_OFF[1]) if far else w
        wk = clamp_reach(sk, wk, UA + FA - 1.0)
        e = ik2(sk, wk, UA, FA, bend=-1)
        out.update({"sx" + k: sk[0], "sy" + k: sk[1], "ex" + k: e[0], "ey" + k: e[1],
                    "wx" + k: wk[0], "wy" + k: wk[1]})
    return out


START = dict(x=HIP[0], y=HIP[1], rot=-15, neck=8, head=4, pull=0.0)
PULL = dict(START, rot=1, neck=2, head=0, chest=-3, pull=1.0)


def _dir(c):
    p = c["pose"]
    dx, dy = PULLEY[0] - p["wx"], PULLEY[1] - p["wy"]
    d = math.hypot(dx, dy)
    return dx / d, dy / d


def handle():
    """V-Griff, Spitze zeigt zum Seil."""
    def bar(c):
        p = c["pose"]
        x, y = p["wx"], p["wy"]
        ux, uy = _dir(c)
        nx, ny = -uy, ux
        tip = (x + ux * 11, y + uy * 11)
        a = (x + nx * 8 - ux, y + ny * 8 - uy)
        b = (x - nx * 8 - ux, y - ny * 8 - uy)
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{tip[0]:.1f} {tip[1]:.1f}L{b[0]:.1f} {b[1]:.1f}"}
    return [Prim("path", {"fill": "none", "stroke": "#0b1220", "stroke-width": 8, "stroke-linejoin": "round",
                          "stroke-linecap": "round"}, bar),
            Prim("path", {"fill": "none", "stroke": "#94a3b8", "stroke-width": 5, "stroke-linejoin": "round",
                          "stroke-linecap": "round"}, bar)]


def cable():
    def f(c):
        p = c["pose"]
        ux, uy = _dir(c)
        return {"x2": p["wx"] + ux * 11, "y2": p["wy"] + uy * 11}
    return Prim("line", {"x1": PULLEY[0], "y1": PULLEY[1], "stroke": "#e2e8f0", "stroke-width": 2.2}, f)


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=78),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=78),
    ]
    T0, T1, T2, T3, TE = 0.8, 2.3, 3.1, 4.9, 5.5
    tl = PostTimeline([(0, START), (T0, START), (T1, PULL), (T2, PULL), (T3, START), (TE, START)],
                      iks=iks, skeleton=SIDE, post=post)
    c0, c1 = tl.at(0), tl.at(T1)
    lift = lambda c: 0.5 * math.hypot(c0["wx"] - c["pose"]["wx"], c0["wy"] - c["pose"]["wy"])

    stack, stack_top = weight_stack(326, FLOOR_Y, 64, lift, n=11, w=34)
    tower = [
        R(296, 40, 14, FLOOR_Y - 40, PROP_DARK, rx=4),
        R(296, 36, 94, 10, PROP_DARK, rx=4),
        R(232, FLOOR_Y - 7, 156, 7, PROP_DARK, rx=3),             # Bodenrahmen
        L(343, 50, 343, stack_top - 2, "#cbd5e1", 2),
        *pulley(343, 48, 5),
        R(290, PULLEY[1] - 11, 24, 22, PROP, rx=5),               # Schlitten unten
        *pulley(PULLEY[0], PULLEY[1], 6),
    ]
    plate = [
        R(240, 176, 10, 60, "#0b1220", rx=4), R(241.5, 177.5, 7, 57, PROP, rx=3),     # Fußplatte
        L(245, 236, 245, FLOOR_Y - 6, PROP_DARK, 6),
    ]
    bench = [
        R(70, 216, 96, 10, PROP, rx=5),
        R(80, 226, 10, FLOOR_Y - 228, PROP_DARK, rx=2),
        R(146, 226, 10, FLOOR_Y - 228, PROP_DARK, rx=2),
    ]

    far_leg, torso, near_leg = side_body()
    figure = (far_leg + arm_prims("_f", far=True) + torso + [scapula()] + [cable()] + near_leg + handle() +
              arm_prims("", far=False))

    back_line = Prim("line", {"stroke": GOOD, "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.75,
                              "stroke-linecap": "round"},
                     lambda c: dict(zip(("x1", "y1", "x2", "y2"),
                                        body_pt(c["P"], "lumbar", -18, -21, end=False) +
                                        body_pt(c["P"], "chest", 2, -21))))
    ghost_parts = limb(["lumbar", "thorax"], 30, TORSO) + limb(["thorax", "chest"], 26, TORSO, outline=False) + \
        limb(["neck"], 13, TORSO) + head_side()
    e0, e1 = (c0["ex"], c0["ey"]), (c1["ex"], c1["ey"])
    pull_arrow = arrow(f"M{c0['wx'] - 4:.0f} {c0['wy'] + 18:.0f} Q{(c0['wx'] + c1['wx']) / 2:.0f} "
                       f"{c1['wy'] + 30:.0f} {c1['wx'] - 6:.0f} {c1['wy'] + 18:.0f}", show=[(T0, T1)])
    rhomb = Prim("ellipse", {"rx": 6, "ry": 12, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                             "_show": [(1.6, T3 - 0.6)]},
                 lambda c: dict(zip(("cx", "cy"), body_pt(c["P"], "thorax", 17, -10))))

    prims = [
        floor(FLOOR_Y, 40, 388),
        *tower, *stack, *plate, *bench,
        ghost(ghost_parts, SIDE, c0, 0.14),
        *figure,
        back_line, rhomb, pull_arrow,
        caption_band(),
        static_text("Rücken bleibt gerade – zur Hüfte rudern", 200, 22, 13, MUTED),
        caption("Knie leicht gebeugt, Rücken gerade, Arme lang", 0, T0),
        caption("Ausatmen – Griff zur Hüfte rudern", T0, T1),
        caption("Schulterblätter zusammenziehen", T1, T2),
        caption("Einatmen – kontrolliert nach vorn", T2, TE),
    ]
    return render(prims, tl, SIDE, fps=15, title="Low Row am Kabelzug")
