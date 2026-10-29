from rig import *
from exercises._hantel_props import DB_EDGE, PLATE_N, _ellipse_d

SLUG = "hantel-butterfly"

# Frontansicht, stehend. Die Arme werden als einfache 3D-Kette gerechnet
# (Elevation e: 0 = hängend, 90 = waagrecht; horizontaler Winkel h: 0 = seitlich,
# 90 = nach vorn zum Betrachter) und orthografisch projiziert – so wirken die
# Arme beim Zusammenführen verkürzt, die Hanteln kommen näher (größer).
# Neutraler Griff: Daumen oben -> Griff steht senkrecht, sobald der Arm
# gehoben ist (hängend: Griff zeigt in die Tiefe = Scheibe von vorn).
# Kleine Draufsicht oben rechts zeigt den Bogen vor der Brust.

FLOOR_Y = 250
SC = 0.86
CX = 168
UA, FA, HD = 36.0, 32.0, 8.0
BEND = 22.0          # Ellbogen leicht gebeugt (horizontal)

BASE = dict(x=CX, y=FLOOR_Y - 103, hip_L=0, hip_R=0, thigh_L=-3, thigh_R=3, shin_L=1, shin_R=-1,
            e=4.0, h=0.0)
T = dict(BASE, e=86.0, h=0.0)
TOGETHER = dict(BASE, e=80.0, h=95.0)


def arm(c, side):
    """Schulter, Ellbogen, Faust (Bildkoordinaten) und Tiefe 0..1 der Faust."""
    P, pose = c["P"], c["pose"]
    sx, sy = pt(P, "clav_L" if side < 0 else "clav_R")
    e, h = math.radians(pose.get("e", 0.0)), pose.get("h", 0.0)
    b = BEND * min(1.0, pose.get("e", 0.0) / 40.0)
    se, ce = math.sin(e), math.cos(e)
    hu, hf = math.radians(h), math.radians(h + b)
    ex = sx + side * UA * se * math.cos(hu)
    ey = sy + UA * ce
    fx = ex + side * (FA + HD) * se * math.cos(hf)
    fy = ey + (FA + HD) * ce
    depth = se * (UA * math.sin(hu) + (FA + HD) * math.sin(hf)) / (UA + FA + HD)
    return (sx, sy), (ex, ey), (fx, fy), max(0.0, depth)


def arm_prims(side, col=NEAR, w=13):
    def d(c):
        s, e, f, _ = arm(c, side)
        return {"d": f"M{s[0]:.1f} {s[1]:.1f}L{e[0]:.1f} {e[1]:.1f}L{f[0]:.1f} {f[1]:.1f}"}

    def dumbbell_parts(c):
        _, _, (fx, fy), dep = arm(c, side)
        k = 1 + 0.45 * dep
        lift = math.sin(math.radians(c["pose"].get("e", 0.0)))
        half = (2.0 + 11.0 * lift) * k
        rx, ry = 8.5 * k, (8.5 - 5.8 * lift) * k
        return fx, fy, half, rx, ry, k

    def handle(c):
        fx, fy, half, *_ = dumbbell_parts(c)
        return {"d": f"M{fx:.1f} {fy - half:.1f}L{fx:.1f} {fy + half:.1f}"}

    def plate(sgn, near):
        def f(c):
            fx, fy, half, rx, ry, _ = dumbbell_parts(c)
            return {"d": _ellipse_d(fx, fy + sgn * half, ry, rx, 90)}
        return Prim("path", {"fill": PLATE_N if near else PROP_DARK, "stroke": DB_EDGE, "stroke-width": 2}, f)

    def fist(c):
        fx, fy, _, _, _, k = dumbbell_parts(c)
        return {"cx": fx, "cy": fy, "r": 6.5 * k}

    return [
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": DB_EDGE, "stroke-width": 6, "stroke-linecap": "round"}, handle),
        Prim("path", {"fill": "none", "stroke": PROP_DARK, "stroke-width": 3.5, "stroke-linecap": "round"}, handle),
        plate(-1, True),
        plate(1, False),
        Prim("circle", {"fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5}, fist),
    ]


# --- Draufsicht -------------------------------------------------------------
IX, IY, IW, IH = 300, 40, 90, 84
OX, OY, IS = IX + IW / 2, IY + 30, 0.42


def top_view():
    def arm_top(side):
        def d(c):
            pose = c["pose"]
            e, h = math.radians(pose.get("e", 0.0)), pose.get("h", 0.0)
            b = BEND * min(1.0, pose.get("e", 0.0) / 40.0)
            se = math.sin(e)
            s = (OX + side * 24 * IS, OY)
            el = (s[0] + side * UA * se * math.cos(math.radians(h)) * IS, s[1] + UA * se * math.sin(math.radians(h)) * IS)
            f = (el[0] + side * (FA + HD) * se * math.cos(math.radians(h + b)) * IS,
                 el[1] + (FA + HD) * se * math.sin(math.radians(h + b)) * IS)
            return {"d": f"M{s[0]:.1f} {s[1]:.1f}L{el[0]:.1f} {el[1]:.1f}L{f[0]:.1f} {f[1]:.1f}"}
        return Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 5, "stroke-linecap": "round",
                             "stroke-linejoin": "round"}, d)

    # Bahn der Hände (statisch, gestrichelt) von seitlich nach vorn
    def track(side):
        pts = []
        for i in range(11):
            h = 95 * i / 10
            b = BEND
            se = math.sin(math.radians(83))
            x = OX + side * (24 + UA * se * math.cos(math.radians(h)) + (FA + HD) * se * math.cos(math.radians(h + b))) * IS
            y = OY + (UA * se * math.sin(math.radians(h)) + (FA + HD) * se * math.sin(math.radians(h + b))) * IS
            pts.append(f"{x:.1f} {y:.1f}")
        return Prim("path", {"d": "M" + "L".join(pts), "fill": "none", "stroke": ACCENT, "stroke-width": 1.3,
                             "stroke-dasharray": "2 3", "opacity": 0.7})

    return [
        Prim("rect", {"x": IX, "y": IY, "width": IW, "height": IH, "rx": 8, "fill": "#0b1220", "opacity": 0.75}),
        track(-1), track(1),
        Prim("rect", {"x": OX - 15, "y": OY - 6, "width": 30, "height": 12, "rx": 6, "fill": TORSO,
                      "stroke": SKIN_LINE, "stroke-width": 1.2}),
        arm_top(-1), arm_top(1),
        Prim("circle", {"cx": OX, "cy": OY, "r": 6.5, "fill": "#4338ca", "stroke": SKIN_LINE, "stroke-width": 1.2}),
        Prim("path", {"d": f"M{OX - 3} {OY + 6}L{OX} {OY + 10}L{OX + 3} {OY + 6}", "fill": HEAD}),
        static_text("von oben", OX, IY + IH - 6, 10, MUTED),
    ]


def front_body(arms):
    """Wie rig.front_figure, aber ohne die 2D-Arme (die rechnen wir in 3D)."""
    prims = limb(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR)
    prims += limb(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, NEAR)
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], 44, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    prims += head_front()
    prims += list(arms)
    return prims


def build():
    tl = Timeline([(0, BASE), (0.5, BASE), (1.7, T), (2.0, T), (3.2, TOGETHER), (3.8, TOGETHER),
                   (5.0, T), (5.3, T), (6.4, BASE), (6.8, BASE)], skeleton=FRONT)

    fig = front_body(arm_prims(-1) + arm_prims(1))
    pecs = [focus("chest", rx=11, ry=9, offset=(dx, 12), show=[(2.0, 3.8)]) for dx in (-13, 13)]
    ghost_t = ghost(arm_prims(-1) + arm_prims(1), FRONT, T, 0.15)
    main = group([
        floor(FLOOR_Y + 1, 40, 300),
        ghost_t,
        *fig,
        *pecs,
    ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        main,
        arrow(f"M{CX - 112} 196 Q{CX - 118} 150 {CX - 96} 116", show=[(0.5, 1.7)]),
        arrow(f"M{CX + 112} 196 Q{CX + 118} 150 {CX + 96} 116", show=[(0.5, 1.7)]),
        *top_view(),
        caption_band(),
        caption("Hanteln seitlich, Daumen nach vorn", 0, 0.5),
        caption("Arme seitlich bis Schulterhöhe heben", 0.5, 2.0),
        caption("Ausatmen – vor der Brust zusammenführen", 2.0, 3.8),
        caption("Einatmen – langsam öffnen", 3.8, 5.3),
        caption("Arme senken", 5.3, 6.8),
        static_text("Ellbogen leicht gebeugt – Brust arbeitet", 150, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Butterfly mit Kurzhanteln", fps=12)
