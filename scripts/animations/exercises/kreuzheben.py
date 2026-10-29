from rig import *
from ._hantel_b_props import dumbbell, side_fig, label

SLUG = "kreuzheben"

# Rumänisches Kreuzheben mit Kurzhanteln, Seitansicht (Blick nach rechts).
# Füße bleiben per IK fix am Boden, die Arme hängen immer senkrecht
# (upperarm = -rot), die Hanteln gleiten dicht an Oberschenkel/Schienbein.

FLOOR_Y = 250
SC = 0.9
ANK_N = (196, FLOOR_Y - 8)
ANK_F = (190, FLOOR_Y - 8)


def hang(rot, spine=0.0):
    """Arme senkrecht hängend bei Rumpfneigung rot (und Summe Wirbelsäule)."""
    return dict(upperarm_n=-rot - spine + 3, upperarm_f=-rot - spine + 1, forearm_n=-3, forearm_f=-2)


STAND = dict(x=194, y=FLOOR_Y - 8 - 97, rot=0, neck=2, head=0, **hang(0))
HINGE = dict(x=150, y=FLOOR_Y - 8 - 86, rot=-50, lumbar=2, thorax=-2, chest=0, neck=14, head=4, **hang(-50))


def hand_on_leg(side, reach=64.0, gap=14.0):
    """IK-Ziel für das Handgelenk: Punkt vor der Beinvorderseite im Abstand
    `reach` von der Schulter – so gleiten die Hanteln am Bein entlang."""
    def f(pose):
        P = SIDE.fk(pose)
        sx, sy = pt(P, "chest")
        legs = [pt(P, "thigh_" + side, False), pt(P, "thigh_" + side), pt(P, "shin_" + side)]
        ty = sy + reach * 0.97
        fx = None
        for (x0, y0), (x1, y1) in zip(legs, legs[1:]):
            a = math.atan2(-(y1 - y0), x1 - x0) + math.pi / 2   # Vorderseite
            ox, oy = gap * math.cos(a), -gap * math.sin(a)
            if min(y0, y1) <= ty <= max(y0, y1) and abs(y1 - y0) > 1e-6:
                u = (ty - y0) / (y1 - y0)
                fx = x0 + ox + (x1 - x0) * u
        tx = sx if fx is None else fx
        dx, dy = tx - sx, ty - sy
        d = math.hypot(dx, dy)
        return sx + dx / d * reach, sy + dy / d * reach
    return f


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
        IK("upperarm_n", "forearm_n", hand_on_leg("n"), bend=-1),
        IK("upperarm_f", "forearm_f", hand_on_leg("f", gap=12.0), bend=-1),
    ]
    tl = Timeline([(0, STAND), (0.8, STAND), (2.8, HINGE), (3.5, HINGE), (5.0, STAND), (5.8, STAND)],
                  iks=iks, skeleton=SIDE)

    def back_line(c):
        P = c["P"]
        pts = []
        for n in ("lumbar", "thorax", "chest"):
            for end in ((False, True) if n == "lumbar" else (True,)):
                x, y = pt(P, n, end)
                a = math.radians(P[n][4] + 90)
                pts.append((x + 21 * math.cos(a), y - 21 * math.sin(a)))
        return {"d": smooth_path(pts)}

    def ham(c):
        P = c["P"]
        x0, y0, x1, y1, a = P["thigh_n"]
        r = math.radians(a - 90)          # Rückseite des Oberschenkels
        return {"cx": (x0 + x1) / 2 + 6 * math.cos(r), "cy": (y0 + y1) / 2 - 6 * math.sin(r)}

    def glute(c):
        x, y = pt(c["P"], "lumbar", end=False)
        a = math.radians(c["P"]["lumbar"][4] + 90)
        return {"cx": x + 12 * math.cos(a), "cy": y - 12 * math.sin(a) + 4}

    figure = side_fig(
        db_far=dumbbell("hand_f", "forearm_f", far=True, fore=0.8, size=1.1),
        db_near=dumbbell("hand_n", "forearm_n", fore=0.8, size=1.1),
    )
    stage = [
        Prim("rect", {"x": 120, "y": FLOOR_Y - 2, "width": 160, "height": 5, "rx": 2.5, "fill": "#3f4a7a"}),
        ghost(side_fig(head=True), SIDE, tl.at(0), 0.13),
        *figure,
        Prim("ellipse", {"rx": 9, "ry": 17, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                         "_show": [(0.8, 5.0)]}, ham),
        Prim("ellipse", {"rx": 13, "ry": 11, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                         "_show": [(2.8, 5.8)]}, glute),
        Prim("path", {"fill": "none", "stroke": GOOD, "stroke-width": 2.5, "stroke-dasharray": "5 5",
                      "stroke-linecap": "round", "opacity": 0.9}, back_line),
        arrow("M150 120 L122 120", show=[(0.8, 2.8)]),
        arrow("M126 124 L154 124", show=[(3.5, 5.0)]),
    ]
    prims = [
        floor(FLOOR_Y + 2, 20, 380),
        group(stage, scale=SC, origin=(200, FLOOR_Y + 2)),
        label("Rücken gerade", 300, 92, 2.8, 3.5, 12, GOOD),
        label("Hanteln nah am Bein", 300, 160, 2.0, 3.5, 12, ACCENT),
        caption_band(),
        caption("Stand: Hanteln vor den Oberschenkeln", 0, 0.8),
        caption("Einatmen – Hüfte nach hinten schieben", 0.8, 2.8),
        caption("Dehnung hinten – Rücken bleibt gerade", 2.8, 3.5),
        caption("Ausatmen – Hüfte nach vorn, aufrichten", 3.5, 5.0),
        caption("Oben Gesäß anspannen", 5.0, 5.8),
        static_text("Hüfte nach hinten – Rücken neutral", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Kreuzheben mit Kurzhanteln")
