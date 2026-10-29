from rig import *

SLUG = "bws-rolle"

# Rückenlage, Kopf links, Seitansicht. Die Rolle liegt fest am Boden; pro Frame
# wird die Neigung des Oberkörpers (rot) so gesucht, dass der Rücken genau auf
# der Rolle aufliegt. Becken und Füße bleiben am Boden (Root fix + Bein-IK).

FLOOR_Y = 246
R_ROLL = 10
BACK = 16.5                      # halbe Rumpfbreite inkl. Kontur
HIP = (236, FLOOR_Y - 16.5)      # Gesäß liegt auf
ANKLE_N = (304, FLOOR_Y - 9.5)
ANKLE_F = (300, FLOOR_Y - 9.5)
POS1, POS2 = 184, 173            # Rollenmitte x: mittlere BWS, eine Handbreit höher


def _quad(p0, p1, p2, n=10):
    return [((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * p1[0] + s * s * p2[0],
             (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * p1[1] + s * s * p2[1])
            for s in (i / n for i in range(n + 1))]


def back_curve(P):
    """Mittellinie des Rumpfs so, wie limb() sie zeichnet."""
    r, l, t, c = pt(P, "root"), pt(P, "lumbar"), pt(P, "thorax"), pt(P, "chest")
    return _quad(r, l, t) + _quad(l, t, c)


def clearance(pose):
    P = SIDE.fk(pose)
    cx, cy = pose["roll"], FLOOR_Y - R_ROLL
    return min(math.hypot(x - cx, y - cy) for x, y in back_curve(P)) - (R_ROLL + BACK)


def fit_roll(pose):
    lo, hi = 40.0, 95.0          # kleiner rot = steiler aufgerichtet
    for _ in range(26):
        mid = (lo + hi) / 2
        if clearance(dict(pose, rot=mid)) > 0:
            lo = mid
        else:
            hi = mid
    return dict(pose, rot=lo)


def _head_pts(pose):
    P = SIDE.fk(pose)
    x, y = pt(P, "head")
    a = math.radians(P["head"][4])
    up = (math.cos(a), -math.sin(a))                     # Scheitel
    back = (math.cos(a + math.pi / 2), -math.sin(a + math.pi / 2))  # Hinterkopf
    return x, y, up, back


def hand_target(dx):
    def f(pose):
        x, y, up, back = _head_pts(pose)
        return (x + back[0] * 15 - up[0] * 9 + dx, y + back[1] * 15 - up[1] * 9)
    return f


class RollTimeline(Timeline):
    def at(self, t):
        pose = fit_roll(self._interp(t))
        for ik in self.iks:
            if ik.end_seg and ik.end_seg.startswith("hand"):
                P = SIDE.fk(pose)
                ik = IK(ik.upper, ik.lower, ik.target, ik.bend, ik.end_seg, P["head"][4] + 25)
            pose = solve_ik(SIDE, pose, ik)
        return pose


BASE = dict(x=HIP[0], y=HIP[1], chest=-6, neck=-10, head=-8)
EXT = dict(BASE, thorax=6, chest=30, neck=-30, head=-10)   # BWS sinkt über die Rolle, Kopf bleibt gestützt in Verlängerung


def roll_prims():
    cy = FLOOR_Y - R_ROLL
    cx = lambda c: {"cx": c["pose"]["roll"]}
    return [
        Prim("circle", {"cy": cy, "r": R_ROLL + 1.5, "fill": "#1e293b"}, cx),
        Prim("circle", {"cy": cy, "r": R_ROLL, "fill": PROP}, cx),
        Prim("circle", {"cy": cy, "r": R_ROLL - 3.5, "fill": "none", "stroke": "#94a3b8", "stroke-width": 1.2,
                        "stroke-dasharray": "2.5 2.5"}, cx),
        Prim("circle", {"cy": cy, "r": 2.6, "fill": PROP_DARK}, cx),
    ]


def figure():
    """Wie side_figure, aber der nahe Arm liegt hinter dem Kopf (Hände am Hinterkopf)."""
    prims = []
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    return prims


def build():
    tl_keys = [
        (0.0, dict(BASE, roll=POS1)), (0.9, dict(BASE, roll=POS1)),
        (2.6, dict(EXT, roll=POS1)), (4.8, dict(EXT, roll=POS1)),
        (6.0, dict(BASE, roll=POS1)), (6.4, dict(BASE, roll=POS1)),
        (7.6, dict(BASE, roll=POS2)), (8.1, dict(BASE, roll=POS2)),
        (9.8, dict(EXT, roll=POS2)), (12.0, dict(EXT, roll=POS2)),
        (13.2, dict(BASE, roll=POS2)), (13.6, dict(BASE, roll=POS2)),
        (14.6, dict(BASE, roll=POS1)),
    ]
    iks = [
        IK("thigh_f", "shin_f", ANKLE_F, bend=1, end_seg="foot_f", end_abs=0),
        IK("thigh_n", "shin_n", ANKLE_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("upperarm_f", "forearm_f", hand_target(-3), bend=-1, end_seg="hand_f", end_abs=0),
        IK("upperarm_n", "forearm_n", hand_target(0), bend=-1, end_seg="hand_n", end_abs=0),
    ]
    tl = RollTimeline(tl_keys, iks=iks, skeleton=SIDE)
    start = tl.at(0)
    scene = group([
        mat(FLOOR_Y, 92, 342),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side(),
              SIDE, start, 0.14),
        Prim("circle", {"cx": POS1, "cy": FLOOR_Y - R_ROLL, "r": R_ROLL, "fill": "none", "stroke": MUTED,
                        "stroke-width": 1.2, "stroke-dasharray": "3 3", "_show": [(7.0, 13.6)]}),
        *roll_prims(),
        *figure(),
        arrow("M150 150 Q138 166 140 186", width=2.2, show=[(0.9, 2.6), (8.1, 9.8)]),
        focus("thorax", rx=16, ry=9, offset=(-2, 7), color=GOOD, show=[(2.6, 4.8), (9.8, 12.0)]),
        arrow(f"M{POS1 - R_ROLL - 3} {FLOOR_Y - R_ROLL} L{POS2 - R_ROLL - 10} {FLOOR_Y - R_ROLL}", width=2,
              show=[(6.4, 7.6)]),
    ], scale=1.4, origin=(230, FLOOR_Y), dx=-20)
    prims = [
        scene,
        caption_band(),
        caption("Rolle quer unter der mittleren BWS", 0, 0.9),
        caption("Ausatmen – über die Rolle sinken", 0.9, 2.6),
        caption("2–3 Atemzüge halten, kein Hohlkreuz", 2.6, 4.8),
        caption("Langsam zurück", 4.8, 6.4),
        caption("Rolle eine Handbreit nach oben", 6.4, 8.1),
        caption("Absinken – LWS bleibt am Boden", 8.1, 9.8),
        caption("Halten und ruhig atmen", 9.8, 12.0),
        caption("Zurück – Segment für Segment höher", 12.0, 13.6),
        caption("Neuer Durchgang: mittlere BWS", 13.6, 14.6),
        static_text("Nur BWS über die Rolle – nie unter den Nacken", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Extension über die Rolle")
