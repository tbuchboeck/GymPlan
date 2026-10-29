from rig import *

SLUG = "face-pulls"

# Seitansicht, Blick nach rechts zum Anker. Die Person lehnt sich in die
# Schlingen; die Bandlänge bleibt konstant – beim Ziehen richtet sich der
# Körper deshalb auf (Neigung wird pro Frame numerisch gelöst). Füße fix.

FLOOR_Y = 250
ANKLE = (212.0, FLOOR_Y - 5.0)
ANCHOR = (372.0, 46.0)
LEGLEN = 98.0
STRAP = 158.0          # Bandlänge Anker -> Griff
ARM = 36 + 32          # Ober- + Unterarm (Hand am Unterarmende)

# Arm-Geometrie: Die Ellbogen gehen beim Ziehen seitlich nach außen. In der
# Seitansicht wird der Oberarm dadurch verkürzt gesehen – das Skelett kann das
# nicht, daher rechnen wir Ellbogen/Hand selbst und zeichnen die Arme eigens.
EL_PULL = (3.0, 3.0)     # Ellbogen (vor, hoch) relativ zur Schulter: auf Schulterhöhe, außen
HD_PULL = (25.0, 29.0)   # Hand vor dem Gesicht, auf Augenhöhe
UA, FA = 36.0, 34.0


def _body_axes(P):
    """Einheitsvektoren der Brust: up (Richtung Hals) und fwd (Blick)."""
    a = math.radians(P["chest"][4])
    up = (math.cos(a), -math.sin(a))
    fwd = (math.cos(a - math.pi / 2), -math.sin(a - math.pi / 2))
    return up, fwd


def _place(pose: dict, lean: float) -> dict:
    p = dict(pose)
    p["rot"] = lean
    l = math.radians(lean)
    p["x"] = ANKLE[0] - LEGLEN * math.sin(l)
    p["y"] = ANKLE[1] - LEGLEN * math.cos(l)
    p["foot_n"] = -lean          # Füße flach am Boden
    p["foot_f"] = -lean
    return p


def shoulder(P, pose):
    """Schultergelenk: etwas unter dem Halsansatz; wandert mit den
    Schulterblättern nach hinten-unten."""
    x, y = pt(P, "chest")
    up, fwd = _body_axes(P)
    s = pose.get("scap", 0.0)
    a, b = 5 + 2.5 * s, 3.5 * s
    return x - up[0] * a - fwd[0] * b, y - up[1] * a - fwd[1] * b


def _arm(pose: dict, P):
    """Ellbogen und Hand (nahe Seite) für den aktuellen Zug-Anteil."""
    sx, sy = shoulder(P, pose)
    up, fwd = _body_axes(P)
    r = pose.get("reach", 0.0)
    dx, dy = ANCHOR[0] - sx, ANCHOR[1] - sy
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    e0 = (sx + ux * UA, sy + uy * UA)
    h0 = (sx + ux * (UA + FA), sy + uy * (UA + FA))
    loc = lambda v: (sx + v[0] * fwd[0] + v[1] * up[0], sy + v[0] * fwd[1] + v[1] * up[1])
    e1, h1 = loc(EL_PULL), loc(HD_PULL)
    k = r
    lift = math.sin(math.pi * r)
    e = (e0[0] + (e1[0] - e0[0]) * k + up[0] * 8 * lift, e0[1] + (e1[1] - e0[1]) * k + up[1] * 8 * lift)
    h = (h0[0] + (h1[0] - h0[0]) * k + up[0] * 6 * lift, h0[1] + (h1[1] - h0[1]) * k + up[1] * 6 * lift)
    return e, h


class FaceTimeline(Timeline):
    def at(self, t):
        base = self._interp(t)

        def solve(lean):
            p = _place(base, lean)
            P = SIDE.fk(p)
            e, h = _arm(p, P)
            return p, e, h, math.hypot(ANCHOR[0] - h[0], ANCHOR[1] - h[1])

        lo, hi = 0.0, 45.0
        for _ in range(28):       # Neigung so, dass die Bandlänge konstant bleibt
            mid = (lo + hi) / 2
            if solve(mid)[3] > STRAP:
                hi = mid
            else:
                lo = mid
        p, e, h, _ = solve((lo + hi) / 2)
        p.update(ex=e[0], ey=e[1], hx=h[0], hy=h[1])
        return p


def hand_pt(c, far=False):
    x, y = c["pose"]["hx"], c["pose"]["hy"]
    return (x - 5, y + 1) if far else (x, y)


def elbow_pt(c, far=False):
    x, y = c["pose"]["ex"], c["pose"]["ey"]
    return (x - 6, y + 1) if far else (x, y)


def arm_prims(far: bool) -> list[Prim]:
    w, col = (11, FAR) if far else (12, NEAR)

    def d(c):
        s = shoulder(c["P"], c["pose"])
        if far:
            s = (s[0] - 6, s[1] + 1)
        return {"d": smooth_path([s, elbow_pt(c, far), elbow_pt(c, far), hand_pt(c, far)])}

    def fist(c):
        x, y = hand_pt(c, far)
        return {"cx": x, "cy": y}

    return [
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("circle", {"r": w / 2 + 1.5, "fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5}, fist),
    ]


def body_pt(c, seg, along, perp, end=True):
    """Punkt relativ zu einem Segment: along entlang, perp nach hinten (+)."""
    P = c["P"]
    x, y = pt(P, seg, end)
    a = math.radians(P[seg][4])
    ux, uy = math.cos(a), -math.sin(a)
    bx, by = -math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)  # Rücken
    return x + along * ux + perp * bx, y + along * uy + perp * by


def straps(far: bool) -> list[Prim]:
    arm = "f" if far else "n"
    col = "#3b4a63" if far else "#d1d5db"

    def band(c):
        hx, hy = hand_pt(c, far)
        return {"x1": ANCHOR[0], "y1": ANCHOR[1], "x2": hx, "y2": hy}

    def handle(c):
        hx, hy = hand_pt(c, far)
        dx, dy = hx - ANCHOR[0], hy - ANCHOR[1]
        d = math.hypot(dx, dy)
        nx, ny = -dy / d, dx / d
        return {"x1": hx + nx * 11, "y1": hy + ny * 11, "x2": hx - nx * 11, "y2": hy - ny * 11}

    return [
        Prim("line", {"stroke": col, "stroke-width": 3.5 if not far else 3, "stroke-linecap": "round"}, band),
        Prim("line", {"stroke": "#0b1220", "stroke-width": 8, "stroke-linecap": "round"}, handle),
        Prim("line", {"stroke": PROP if not far else PROP_DARK, "stroke-width": 5, "stroke-linecap": "round"}, handle),
    ]


def scapula() -> Prim:
    def f(c):
        s = c["pose"].get("scap", 0.0)
        # Schulterblatt auf dem oberen Rücken: rutscht nach hinten-unten
        pts = [body_pt(c, "thorax", 22 - 7 * s + da, 2 * s + dp) for da, dp in
               ((5, 1), (-18, 6), (3, 14))]
        (ax, ay), (bx, by), (cx, cy) = pts
        return {"d": f"M{ax:.1f} {ay:.1f}Q{(ax + bx) / 2 - 1:.1f} {(ay + by) / 2:.1f} {bx:.1f} {by:.1f}"
                     f"Q{(bx + cx) / 2:.1f} {(by + cy) / 2:.1f} {cx:.1f} {cy:.1f}Z"}
    return Prim("path", {"fill": HEAD, "opacity": 0.55, "stroke": SKIN_LINE, "stroke-width": 1.2,
                         "stroke-linejoin": "round"}, f)


def figure() -> list[Prim]:
    prims: list[Prim] = []
    prims += straps(far=True)
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += arm_prims(far=True)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims.append(scapula())
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += straps(far=False)
    prims += arm_prims(far=False)
    return prims


START = dict(reach=0.0, scap=0.0)
SET = dict(reach=0.0, scap=1.0, chest=-3, neck=2)
PULL = dict(reach=1.0, scap=1.0, chest=-3, neck=2)


def build():
    tl = FaceTimeline([(0, START), (0.8, START), (1.8, SET), (2.2, SET), (3.6, PULL), (4.8, PULL),
                       (6.4, SET), (6.8, START), (7.2, START)], skeleton=SIDE)

    def ctx(t):
        p = tl.at(t)
        return {"P": SIDE.fk(p), "pose": p}

    c_set, c_pull = ctx(2.2), ctx(3.6)
    h0, h1 = hand_pt(c_set), hand_pt(c_pull)
    pull_arrow = arrow(f"M{h0[0] - 4:.0f} {h0[1] - 16:.0f} Q{(h0[0] + h1[0]) / 2:.0f} {h1[1] - 24:.0f} "
                       f"{h1[0] + 16:.0f} {h1[1] - 10:.0f}", show=[(2.2, 3.6)])
    c0 = ctx(1.0)
    b0 = body_pt(c0, "thorax", 26, 24)
    b1 = body_pt(c0, "thorax", 2, 27)
    scap_arrow = arrow(f"M{b0[0]:.0f} {b0[1]:.0f} Q{b0[0] - 9:.0f} {(b0[1] + b1[1]) / 2:.0f} {b1[0]:.0f} {b1[1]:.0f}",
                       show=[(0.8, 2.2)])

    trap_focus = Prim("ellipse", {"rx": 8, "ry": 16, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                                  "_show": [(1.8, 6.4)]},
                      lambda c: dict(zip(("cx", "cy"), body_pt(c, "thorax", 8, 12))))

    post = [
        Prim("rect", {"x": 380, "y": 14, "width": 12, "height": FLOOR_Y - 14, "rx": 3, "fill": PROP_DARK}),
        Prim("rect", {"x": 370, "y": ANCHOR[1] - 7, "width": 14, "height": 14, "rx": 4, "fill": PROP}),
        Prim("circle", {"cx": ANCHOR[0], "cy": ANCHOR[1], "r": 4.5, "fill": "none", "stroke": "#d1d5db",
                        "stroke-width": 2.2}),
    ]
    c_start = ctx(0)
    ghost_parts = limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side()

    scene = group([
        floor(FLOOR_Y, 60, 394),
        *post,
        ghost(ghost_parts, SIDE, c_start["pose"], 0.13),
        *figure(),
        trap_focus,
        scap_arrow,
        pull_arrow,
    ], scale=0.9, origin=(200, FLOOR_Y), dy=2)

    prims = [
        scene,
        caption_band(),
        static_text("Körper gespannt wie ein Brett", 200, 24, 13, MUTED),
        static_text("Anker auf Kopfhöhe", 360, 52, 11, MUTED, anchor="end"),
        caption("Arme lang, Körper gespannt", 0, 0.8),
        caption("Schulterblätter zurück & runter", 0.8, 2.2),
        caption("Griffe zum Gesicht – Ellbogen hoch & außen", 2.2, 3.6),
        caption("Kurz halten – mittlerer/unterer Trapez", 3.6, 4.8),
        caption("Kontrolliert zurück", 4.8, 7.2),
    ]
    return render(prims, tl, SIDE, fps=12, title="Face Pulls (Sling)")
