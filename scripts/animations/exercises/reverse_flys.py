from rig import *

SLUG = "reverse-flys"

# Frontansicht. Sling hängt vorn-oben (zwei Schlaufen an einer Stange), die
# Person lehnt sich leicht in die Bänder. Die Arme zeigen anfangs zum
# Betrachter – dafür rechnen wir eine einfache 3D-Projektion der Arme
# (Ellbogen/Hand) selbst, statt die 2D-Kettenlängen zu verwenden.

# Nahansicht: Gruppe skaliert um ORIGIN, Beine laufen unten aus dem Bild.
SCALE, ORIGIN, DY = 1.1, (200.0, 150.0), 0.0


def to_group(x, y):
    """Bildschirm- -> Gruppenkoordinaten (für Requisiten an fixer Stelle)."""
    return (ORIGIN[0] + (x - ORIGIN[0]) / SCALE, ORIGIN[1] + (y - ORIGIN[1] - DY) / SCALE)


BAR_SCREEN_Y = 42
ANCH = {-1: to_group(146, BAR_SCREEN_Y + 5), 1: to_group(254, BAR_SCREEN_Y + 5)}   # -1 = links (Bild)
UA, FA = 36.0, 32.0
BEND = 20.0       # leicht gebeugte Arme (Grad)
TH0, TH1 = 4.0, 86.0   # Armwinkel in der Horizontalen: vorn -> seitlich


def _shoulder(P, side):
    return pt(P, "clav_L" if side < 0 else "clav_R")


def arm_pts(c, side):
    """(Schulter, Ellbogen, Hand, Tiefe 0..1 [1 = zum Betrachter])."""
    P, pose = c["P"], c["pose"]
    o = pose.get("open", 0.0)
    th = TH0 + (TH1 - TH0) * o
    sx, sy = _shoulder(P, side)
    te, th_ = math.radians(th + BEND), math.radians(th - BEND - 12 * (1 - o))
    lat_e = UA * math.sin(te)
    lat_h = lat_e + FA * math.sin(th_)
    # Höhe: anfangs Griffe auf Brusthöhe, geöffnet etwa auf Schulterhöhe
    dy_e = 5 + 4 * (1 - o)
    dy_h = 3 + 19 * (1 - o) - 4 * math.sin(math.pi * o)
    e = (sx + side * lat_e, sy + dy_e)
    h = (sx + side * lat_h, sy + dy_h)
    depth = math.cos(math.radians(th))
    return (sx, sy), e, h, depth


def arm(side, col=NEAR, w=13) -> list[Prim]:
    def d(c):
        s, e, h, _ = arm_pts(c, side)
        return {"d": smooth_path([s, e, e, h])}

    def fist(c):
        _, _, h, dep = arm_pts(c, side)
        return {"cx": h[0], "cy": h[1], "r": 7 + 3.5 * dep}

    return [
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("circle", {"fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5}, fist),
    ]


def strap(side) -> list[Prim]:
    ax, ay = ANCH[side]

    def band(c):
        _, _, h, _ = arm_pts(c, side)
        return {"x1": ax, "y1": ay, "x2": h[0], "y2": h[1]}

    def handle(c):
        _, _, (hx, hy), dep = arm_pts(c, side)
        dx, dy = hx - ax, hy - ay
        d = math.hypot(dx, dy)
        nx, ny = -dy / d, dx / d
        L = 10 + 5 * dep
        return {"x1": hx + nx * L, "y1": hy + ny * L, "x2": hx - nx * L, "y2": hy - ny * L}

    return [
        Prim("line", {"stroke": "#d1d5db", "stroke-width": 3, "stroke-linecap": "round"}, band),
        Prim("line", {"stroke": "#0b1220", "stroke-width": 8, "stroke-linecap": "round"}, handle),
        Prim("line", {"stroke": MUTED, "stroke-width": 5, "stroke-linecap": "round"}, handle),
    ]


def ear_gap(side) -> Prim:
    """Grüne Linie Ohr–Schulter: Schultern bleiben weg von den Ohren."""
    def f(c):
        P = c["P"]
        hx, hy = pt(P, "head")
        sx, sy = _shoulder(P, side)
        x = hx + side * 21
        return {"x1": x, "y1": hy + 6, "x2": x, "y2": sy - 13}
    return Prim("line", {"stroke": GOOD, "stroke-width": 2.5, "stroke-linecap": "round",
                         "stroke-dasharray": "3 4"}, f)


def back_inset(x0=314, y0=40, w=74, h=84) -> list[Prim]:
    """Kleine Rückenansicht: Schulterblätter gleiten zusammen und nach unten."""
    cx = x0 + w / 2

    def scap(side):
        def f(c):
            p = c["pose"]
            s = p.get("scap", 0.0)
            o = p.get("open", 0.0)
            mx = cx + side * (13 - 4 * s - 4 * o)      # Innenrand
            ty = y0 + 24 + 6 * s + 2 * o
            pts = [(mx, ty), (mx + side * 20, ty - 2), (mx + side * 3, ty + 30)]
            (ax, ay), (bx, by), (qx, qy) = pts
            return {"d": f"M{ax:.1f} {ay:.1f}L{bx:.1f} {by:.1f}Q{bx - side * 6:.1f} {by + 18:.1f} {qx:.1f} {qy:.1f}"
                         f"Q{ax - side * 2:.1f} {(ay + qy) / 2:.1f} {ax:.1f} {ay:.1f}Z"}
        return Prim("path", {"fill": NEAR, "stroke": SKIN_LINE, "stroke-width": 1.2, "stroke-linejoin": "round"}, f)

    trap = Prim("path", {"d": f"M{cx - 9} {y0 + 32}L{cx + 9} {y0 + 32}L{cx} {y0 + 66}Z", "fill": ACCENT,
                         "opacity": 0.35, "_pulse": True, "_show": [(2.0, 6.6)]})
    return [
        Prim("rect", {"x": x0, "y": y0, "width": w, "height": h, "rx": 8, "fill": "#0b1220", "opacity": 0.7,
                      "stroke": FLOOR, "stroke-width": 1}),
        Prim("path", {"d": f"M{x0 + 10} {y0 + 30}Q{cx} {y0 + 12} {x0 + w - 10} {y0 + 30}L{x0 + w - 16} {y0 + h - 6}"
                           f"L{x0 + 16} {y0 + h - 6}Z", "fill": TORSO, "opacity": 0.55}),
        Prim("line", {"x1": cx, "y1": y0 + 18, "x2": cx, "y2": y0 + h - 8, "stroke": SKIN_LINE, "stroke-width": 2,
                      "stroke-dasharray": "2 3"}),
        trap, scap(-1), scap(1),
        static_text("Rücken", cx, y0 + h + 13, 10, MUTED),
    ]


def figure() -> list[Prim]:
    prims: list[Prim] = []
    prims += limb(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR)
    prims += limb(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, NEAR)
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], 44, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    prims += head_front()
    prims += strap(-1) + strap(1)
    prims += arm(-1) + arm(1)
    return prims


BASE = dict(x=200, y=to_group(0, 213)[1], thigh_L=-3, thigh_R=3, open=0.0, scap=0.0)
SET = dict(BASE, scap=1.0, clav_L=5, clav_R=-5)
OPEN = dict(SET, open=1.0)


def build():
    tl = Timeline([(0, BASE), (0.8, BASE), (1.8, SET), (2.0, SET), (3.6, OPEN), (4.8, OPEN),
                   (6.4, SET), (6.8, BASE), (7.2, BASE)], skeleton=FRONT)

    def ctx(t):
        p = tl.at(t)
        return {"P": FRONT.fk(p), "pose": p}

    # Bogenpfeile entlang des Handwegs, etwas nach außen/oben versetzt
    arcs = []
    for side in (-1, 1):
        pts = []
        for i in range(9):
            p = dict(SET, open=0.3 + 0.62 * i / 8)
            _, _, h, _ = arm_pts({"P": FRONT.fk(p), "pose": p}, side)
            pts.append((h[0] + side * 8, h[1] + 22 - 6 * math.sin(math.pi * i / 8)))
        arcs.append(arrow(smooth_path(pts), show=[(2.0, 3.6)]))

    c_set = ctx(1.0)
    down = []
    for side in (-1, 1):
        sx, sy = _shoulder(c_set["P"], side)
        down.append(arrow(f"M{sx - side * 4:.0f} {sy - 30:.0f} L{sx - side * 4:.0f} {sy - 17:.0f}",
                          width=2.5, show=[(0.8, 2.0)]))

    bx0, by0 = to_group(118, BAR_SCREEN_Y - 4)
    bx1, _ = to_group(282, 0)
    bar = [
        Prim("rect", {"x": bx0, "y": by0, "width": bx1 - bx0, "height": 8 / SCALE, "rx": 4, "fill": PROP_DARK}),
        Prim("circle", {"cx": ANCH[-1][0], "cy": ANCH[-1][1], "r": 4.5, "fill": "none", "stroke": "#d1d5db", "stroke-width": 2.2}),
        Prim("circle", {"cx": ANCH[1][0], "cy": ANCH[1][1], "r": 4.5, "fill": "none", "stroke": "#d1d5db", "stroke-width": 2.2}),
    ]
    ghost_arms = arm(-1) + arm(1)
    scene = group([
        *bar,
        *figure(),
        ghost(ghost_arms, FRONT, BASE, 0.2),
        ear_gap(-1), ear_gap(1),
        *down, *arcs,
    ], scale=SCALE, origin=ORIGIN, dy=DY)
    # Ohr-Linien nur in Halte-/Öffnungsphase
    for p in scene.children:
        if p.tag == "line" and p.attrs.get("stroke") == GOOD:
            p.attrs["_show"] = [(2.0, 4.8)]

    prims = [
        scene,
        *back_inset(),
        caption_band(),
        static_text("Schultern bleiben weg von den Ohren", 200, 24, 13, MUTED),
        caption("Griffe vor der Brust, Arme leicht gebeugt", 0, 0.8),
        caption("Schulterblätter zurück & runter", 0.8, 2.0),
        caption("Arme im Bogen seitlich öffnen", 2.0, 3.6),
        caption("Kurz halten – Schulterblätter bleiben unten", 3.6, 4.8),
        caption("Kontrolliert zurück", 4.8, 7.2),
    ]
    return render(prims, tl, FRONT, fps=12, title="Reverse Flys (Sling)")
