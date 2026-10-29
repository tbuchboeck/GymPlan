from rig import *
from exercises._tb_gym_props import *

SLUG = "ruderzug"

# Rudern am Kabelturm, stehend, Seitansicht (Blick zum Turm nach rechts).
# Seilrolle etwa auf Brusthöhe, ein Griff mit beiden Händen. Ellbogen
# ziehen eng am Körper nach hinten bis zur Hüfte, die Schulterblätter
# drücken hinten zusammen („Nussknacker“). Füße fix, Knie locker.

FLOOR_Y = 250
HIP = (182.0, 149.0)
ANK_N, ANK_F = (192.0, FLOOR_Y - 8.0), (180.0, FLOOR_Y - 8.0)
PULLEY = (338.0, 108.0)
FAR_OFF = (-4.0, -1.0)
SCALE = 0.86


def post(pose, P):
    p = pose.get("pull", 0.0)
    scap = min(1.0, max(0.0, (p - 0.35) / 0.55))
    s = shoulder_side(P, scap)
    # Handgelenk: vorne (Arme lang, Richtung Seilrolle) -> am Bauch
    belly = body_pt(P, "lumbar", 2, 25)
    w0 = (s[0] + 61, s[1] + 22)
    w1 = (belly[0] + 6, belly[1] - 2)
    u = p
    w = (w0[0] + (w1[0] - w0[0]) * u, w0[1] + (w1[1] - w0[1]) * u - 5 * math.sin(math.pi * u))
    out = {"scap": scap}
    for k, far in (("", False), ("_f", True)):
        sk = (s[0] + FAR_OFF[0], s[1] + FAR_OFF[1]) if far else s
        wk = (w[0] + FAR_OFF[0], w[1] + FAR_OFF[1]) if far else w
        wk = clamp_reach(sk, wk, UA + FA - 1.0)
        e = ik2(sk, wk, UA, FA, bend=-1)
        out.update({"sx" + k: sk[0], "sy" + k: sk[1], "ex" + k: e[0], "ey" + k: e[1],
                    "wx" + k: wk[0], "wy" + k: wk[1]})
    return out


BASE = dict(x=HIP[0], y=HIP[1], rot=-8, lumbar=0, thorax=2, neck=4, head=2, pull=0.0)
PULL = dict(BASE, pull=1.0, chest=-3, neck=5)


def handle():
    """V-Griff: Querstück in den Fäusten, Öse vorne fürs Seil."""
    def bar(c):
        p = c["pose"]
        x, y = p["wx"], p["wy"]
        return {"d": f"M{x - 1:.1f} {y - 8:.1f}L{x + 10:.1f} {y:.1f}L{x - 1:.1f} {y + 8:.1f}"}
    return [Prim("path", {"fill": "none", "stroke": "#0b1220", "stroke-width": 8, "stroke-linejoin": "round",
                          "stroke-linecap": "round"}, bar),
            Prim("path", {"fill": "none", "stroke": "#94a3b8", "stroke-width": 5, "stroke-linejoin": "round",
                          "stroke-linecap": "round"}, bar)]


def cable():
    return Prim("line", {"x1": PULLEY[0], "y1": PULLEY[1] + 6, "stroke": "#e2e8f0", "stroke-width": 2.2},
                lambda c: {"x2": c["pose"]["wx"] + 10, "y2": c["pose"]["wy"]})


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
    ]
    T0, T1, T2, T3, TE = 0.8, 2.2, 3.1, 4.9, 5.5
    tl = PostTimeline([(0, BASE), (T0, BASE), (T1, PULL), (T2, PULL), (T3, BASE), (TE, BASE)],
                      iks=iks, skeleton=SIDE, post=post)
    c0, c1 = tl.at(0), tl.at(T1)
    travel = c0["wx"] - c1["wx"]
    lift = lambda c: 0.55 * (c0["wx"] - c["pose"]["wx"])

    stack, stack_top = weight_stack(366, FLOOR_Y, 40, lift, n=12, w=34)
    tower = [
        R(330, 18, 16, FLOOR_Y - 18, PROP_DARK, rx=4),            # Turm
        R(352, 14, 64, 10, PROP_DARK, rx=4),
        R(320, FLOOR_Y - 7, 104, 7, PROP_DARK, rx=3),
        R(324, PULLEY[1] - 11, 24, 22, PROP, rx=5),               # verstellbarer Schlitten
        *pulley(PULLEY[0], PULLEY[1], 6),
        L(383, 30, 383, stack_top - 2, "#cbd5e1", 2),
        *pulley(383, 26, 5),
    ]
    for i in range(8):                                            # Lochraster der Höhenverstellung
        tower.append(C(338, 34 + i * 26, 2.2, "#3b4658"))

    far_leg, torso, near_leg = side_body()
    figure = (far_leg + arm_prims("_f", far=True) + torso + [scapula()] + near_leg + [cable()] + handle() +
              arm_prims("", far=False))

    ghost_arm = ghost(arm_prims("", far=False) + handle(), SIDE, c0, 0.18)
    e0, e1 = (c0["ex"], c0["ey"]), (c1["ex"], c1["ey"])
    pull_arrow = arrow(f"M{e0[0] - 2:.0f} {e0[1] + 18:.0f} Q{(e0[0] + e1[0]) / 2:.0f} {e1[1] + 26:.0f} "
                       f"{e1[0] - 10:.0f} {e1[1] + 12:.0f}", show=[(T0, T1)])
    rhomb = Prim("ellipse", {"rx": 6, "ry": 12, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                             "_show": [(1.5, T3 - 0.6)]},
                 lambda c: dict(zip(("cx", "cy"), body_pt(c["P"], "thorax", 17, -10))))
    hip_mark = Prim("g", {"_show": [(T1 - 0.3, T2 + 0.2)]}, children=[
        Prim("circle", {"cx": e1[0], "cy": e1[1], "r": 9, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                        "stroke-dasharray": "3 3"})])

    scene = group([
        floor(FLOOR_Y, 40, 430),
        *tower, *stack,
        ghost_arm,
        *figure,
        hip_mark, rhomb, pull_arrow,
    ], scale=SCALE, origin=(200, FLOOR_Y), dy=2)

    prims = [
        scene,
        caption_band(),
        static_text("Ellbogen eng am Körper zur Hüfte", 200, 22, 13, MUTED),
        caption("Knie locker, Rücken gerade, Arme lang", 0, T0),
        caption("Ausatmen – Ellbogen zur Hüfte ziehen", T0, T1),
        caption("„Nussknacker“ – Schulterblätter zusammen", T1, T2),
        caption("Einatmen – Arme langsam lang lassen", T2, TE),
    ]
    return render(prims, tl, SIDE, fps=15, title="Ruderzug am Kabelturm")
