from rig import *

SLUG = "nackendehnung"

# Frontansicht, Nahansicht Oberkörper, sitzend auf einem Stuhl.
# Person blickt zum Betrachter: anatomisch RECHTS = Bildschirm LINKS (_L).
# Seite 1: rechte Hand (_L) unters Gesäß, Kopf neigt nach links (Bild rechts),
#          Nase Richtung linke Achsel (Bild rechts unten). Dehnung Bild links.
# Seite 2: gespiegelt.

SCALE, ORIGIN, DY = 1.12, (200.0, 150.0), -10.0
ROOT = (200.0, 203.0)            # Becken (Gruppenkoordinaten)
SEAT_Y = ROOT[1] + 3             # Vorderkante der Sitzfläche


def relaxed(side):
    """Hand liegt locker auf dem Oberschenkel."""
    s = "L" if side < 0 else "R"
    k = -side
    return {f"upperarm_{s}": 1 * k, f"forearm_{s}": 26 * k, f"hand_{s}": 16 * k, f"clav_{s}": 0.0}


def fixed(side):
    """Hand unterm Gesäß: Arm gestreckt nach unten, Schulter tief."""
    s = "L" if side < 0 else "R"
    k = -side
    return {f"upperarm_{s}": -17 * k, f"forearm_{s}": 0.0, f"hand_{s}": 2 * k, f"clav_{s}": 8 * k}


BASE = dict(x=ROOT[0], y=ROOT[1], **relaxed(-1), **relaxed(1))


def side_poses(side):
    """side = Bildseite der fixierten Hand (-1 links = anatomisch rechts)."""
    fix = dict(BASE, **fixed(side))
    t = -side   # Neigung zur Gegenseite: Bild rechts bei side=-1
    tilt = dict(fix, neck=-13 * t, head=-13 * t, chest=-2 * t, turn=0.0, nod=0.0)
    turn = dict(tilt, head=-17 * t, turn=0.42 * t, nod=0.38)
    return fix, tilt, turn


def head_custom(r=17) -> list[Prim]:
    """Frontaler Kopf mit Drehung (turn) und leichtem Senken des Blicks (nod)."""
    def base(c):
        x, y = pt(c["P"], "head")
        a = c["P"]["head"][4]
        return x, y, math.radians(a - 90), math.radians(a), c["pose"].get("turn", 0.0), c["pose"].get("nod", 0.0)

    def P(c, off, up):
        x, y, lat, ua, *_ = base(c)
        return (x + r * (off * math.cos(lat) + up * math.cos(ua)),
                y - r * (off * math.sin(lat) + up * math.sin(ua)))

    def skull(c):
        x, y, *_ = base(c)
        return {"cx": x, "cy": y}

    def eye(side):
        def f(c):
            *_, turn, nod = base(c)
            x, y = P(c, side * 0.36 + turn * 0.42, 0.12 - nod * 0.32)
            return {"cx": x, "cy": y}
        return f

    def nose(c):
        *_, turn, nod = base(c)
        o = turn * 0.58
        a = P(c, o, 0.02 - nod * 0.3)
        b = P(c, o + 0.07 * (1 if turn >= 0 else -1) + turn * 0.1, -0.24 - nod * 0.3)
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}"}

    def mouth(c):
        *_, turn, nod = base(c)
        o = turn * 0.5
        a, m, b = P(c, o - 0.2, -0.47 - nod * 0.25), P(c, o, -0.55 - nod * 0.25), P(c, o + 0.2, -0.47 - nod * 0.25)
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}Q{m[0]:.1f} {m[1]:.1f} {b[0]:.1f} {b[1]:.1f}"}

    def hair(c):
        *_, turn, nod = base(c)
        hl = 0.46 - nod * 0.12
        pts = []
        for i in range(13):
            ang = math.radians(8 + 164 * i / 12)
            pts.append(P(c, math.cos(ang) * 1.04, max(hl, math.sin(ang) * 1.04)))
        d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        q = P(c, -turn * 0.3, hl - 0.1)
        return {"d": d + f"Q{q[0]:.1f} {q[1]:.1f} {pts[0][0]:.1f} {pts[0][1]:.1f}Z"}

    def ear(side):
        def f(c):
            *_, turn, nod = base(c)
            x, y = P(c, side * (0.98 - side * turn * 0.18), -0.05 - nod * 0.1)
            return {"cx": x, "cy": y}
        return f

    return [
        Prim("circle", {"r": 5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, ear(-1)),
        Prim("circle", {"r": 5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, ear(1)),
        Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
        Prim("circle", {"r": r, "fill": HEAD}, skull),
        Prim("path", {"fill": "#4338ca"}, hair),
        Prim("circle", {"r": 2.2, "fill": SKIN_LINE}, eye(-1)),
        Prim("circle", {"r": 2.2, "fill": SKIN_LINE}, eye(1)),
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linecap": "round"}, nose),
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.3, "stroke-linecap": "round"}, mouth),
    ]


def legs() -> list[Prim]:
    out = []
    for s, k in (("L", -1), ("R", 1)):
        def thigh(c, s=s, k=k):
            hx, hy = pt(c["P"], f"hip_{s}")
            return {"d": f"M{hx - k * 2:.1f} {hy + 4:.1f}L{hx - k * 1:.1f} {hy + 20:.1f}L{hx:.1f} {hy + 80:.1f}"}
        out += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round",
                              "stroke-linejoin": "round"}, thigh),
                Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 22, "stroke-linecap": "round",
                              "stroke-linejoin": "round"}, thigh)]
    return out


def arm_layer(side) -> list[Prim]:
    s = "L" if side < 0 else "R"
    return limb([f"upperarm_{s}", f"forearm_{s}", f"hand_{s}"], 13, NEAR)


def stretch_band(side) -> Prim:
    """Grüne Dehnzone: seitlicher Nacken auf der Seite der fixierten Hand."""
    s = "L" if side < 0 else "R"

    def f(c):
        P = c["P"]
        hx, hy = pt(P, "head")
        a = math.radians(P["head"][4])
        lat = (math.cos(a - math.pi / 2), -math.sin(a - math.pi / 2))
        up = (math.cos(a), -math.sin(a))
        e = (hx + side * 13 * lat[0] - 12 * up[0], hy + side * 13 * lat[1] - 12 * up[1])
        cx, cy = pt(P, "chest")
        nb = (cx + side * 8, cy - 7)
        sx, sy = pt(P, f"clav_{s}")
        sh = (cx + (sx - cx) * 0.72, cy + (sy - cy) * 0.72 - 9)
        return {"d": smooth_path([e, nb, sh])}

    return Prim("path", {"fill": "none", "stroke": GOOD, "stroke-width": 8, "stroke-linecap": "round",
                         "stroke-linejoin": "round", "opacity": 0.45, "_pulse": True}, f)


def build():
    fixA, tiltA, turnA = side_poses(-1)
    fixB, tiltB, turnB = side_poses(1)
    T = 7.8
    seq = [(0, BASE), (0.5, BASE), (1.5, fixA), (1.8, fixA), (3.2, tiltA), (3.5, tiltA), (4.6, turnA),
           (6.6, turnA), (7.4, fixA), (7.8, BASE)]
    keys = seq + [(T + t, (fixB if p is fixA else tiltB if p is tiltA else turnB if p is turnA else p))
                  for t, p in seq[1:]]
    tl = Timeline(keys, skeleton=FRONT)
    dur = tl.duration

    def P_at(t):
        return FRONT.fk(tl.at(t))

    # Pfeile: Kopf neigen (Bogen über dem Kopf), Nase drehen (kurzer Bogen)
    arrows = []
    for off, k in ((0.0, 1), (T, -1)):
        h0 = pt(P_at(off + 1.8), "head")
        arrows.append(arrow(f"M{h0[0] - k * 6:.0f} {h0[1] - 27:.0f} Q{h0[0] + k * 20:.0f} {h0[1] - 34:.0f} "
                            f"{h0[0] + k * 32:.0f} {h0[1] - 14:.0f}", show=[(off + 1.8, off + 3.2)]))
        h1 = pt(P_at(off + 3.5), "head")
        arrows.append(arrow(f"M{h1[0] + k * 2:.0f} {h1[1] + 24:.0f} Q{h1[0] + k * 18:.0f} {h1[1] + 28:.0f} "
                            f"{h1[0] + k * 26:.0f} {h1[1] + 40:.0f}", width=2.5, show=[(off + 3.5, off + 4.6)]))
        # fixierte Schulter bleibt unten
        Pf = P_at(off + 1.8)
        sx, sy = pt(Pf, "clav_L" if k > 0 else "clav_R")
        arrows.append(arrow(f"M{sx:.0f} {sy - 30:.0f} L{sx:.0f} {sy - 16:.0f}", width=2.5,
                            show=[(off + 0.5, off + 1.8)]))

    bands = [stretch_band(-1), stretch_band(1)]
    bands[0].attrs["_show"] = [(2.4, 7.4)]
    bands[1].attrs["_show"] = [(T + 2.4, T + 7.4)]

    chair = [
        Prim("rect", {"x": ROOT[0] - 38, "y": ROOT[1] - 74, "width": 76, "height": 84, "rx": 6, "fill": PROP_DARK}),
    ]
    seat = [Prim("rect", {"x": ROOT[0] - 50, "y": SEAT_Y, "width": 100, "height": 9, "rx": 4, "fill": PROP}),
            Prim("rect", {"x": ROOT[0] - 44, "y": SEAT_Y + 9, "width": 7, "height": 60, "fill": PROP_DARK}),
            Prim("rect", {"x": ROOT[0] + 37, "y": SEAT_Y + 9, "width": 7, "height": 60, "fill": PROP_DARK})]

    # Sitzkante seitlich vor den Händen: die fixierte Hand verschwindet darunter
    seat_sides = [Prim("rect", {"x": ROOT[0] - 50, "y": SEAT_Y, "width": 26, "height": 9, "rx": 4, "fill": PROP}),
                  Prim("rect", {"x": ROOT[0] + 24, "y": SEAT_Y, "width": 26, "height": 9, "rx": 4, "fill": PROP})]
    trunk = limb(["lumbar", "thorax", "chest"], 44, TORSO)
    shl = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    torso = [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, shl),
             trunk[0],
             Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, shl),
             trunk[1]]
    neck_head = limb(["neck"], 13, TORSO) + head_custom()

    scene = group([
        *chair,
        ghost(neck_head, FRONT, BASE, 0.16),
        *limb(["neck"], 13, TORSO),
        *torso,
        *seat,
        *legs(),
        *arm_layer(-1), *arm_layer(1),
        *seat_sides,
        *head_custom(),
        *bands,
        *arrows,
    ], scale=SCALE, origin=ORIGIN, dy=DY)

    # Halte-Uhr: Ring füllt sich während des Haltens
    R = 15
    circ = 2 * math.pi * R
    holds = [(4.6, 6.6), (T + 4.6, T + 6.6)]

    def ring(c):
        t = c["t"]
        f = 0.0
        for a, b in holds:
            if a <= t <= b:
                f = (t - a) / (b - a)
        return {"stroke-dashoffset": circ * (1 - f)}

    timer = Prim("g", {"_show": holds}, children=[
        Prim("circle", {"cx": 352, "cy": 96, "r": R, "fill": "none", "stroke": FLOOR, "stroke-width": 4}),
        Prim("circle", {"cx": 352, "cy": 96, "r": R, "fill": "none", "stroke": GOOD, "stroke-width": 4,
                        "stroke-dasharray": f"{circ:.1f}", "stroke-linecap": "round",
                        "transform": "rotate(-90 352 96)"}, ring),
        static_text("30 s", 352, 100, 12, TEXT, weight="600"),
        static_text("halten", 352, 126, 12, MUTED),
    ])

    def caps(off, hand, seite, achsel):
        return [
            caption(f"{hand} Hand unters Gesäß – fixiert die Schulter", off, off + 1.8, size=14),
            caption(f"Kopf zur {seite} Seite neigen – Ohr zur Schulter", off + 1.8, off + 3.5, size=14),
            caption(f"Nase leicht Richtung {achsel} Achsel drehen", off + 3.5, off + 4.6, size=14),
            caption("30 s halten – ruhig atmen", off + 4.6, off + 6.6, size=14),
            caption("Lösen – Seite wechseln", off + 6.6, off + T, size=14),
        ]

    # Fixierende Hand: greift seitlich unter dem Gesäß die Sitzkante
    def to_screen(x, y):
        return ORIGIN[0] + (x - ORIGIN[0]) * SCALE, ORIGIN[1] + (y - ORIGIN[1]) * SCALE + DY

    grips = []
    for off, side, seg in ((0.0, -1, "hand_L"), (T, 1, "hand_R")):
        hx, hy = to_screen(*pt(P_at(off + 1.8), seg))
        win = [(off + 1.0, off + 7.4)]
        lx = hx + side * 30
        grips.append(Prim("g", {"_show": win}, children=[
            Prim("circle", {"cx": round(hx, 1), "cy": round(hy - 2, 1), "r": 13, "fill": "none", "stroke": GOOD,
                            "stroke-width": 2.5, "stroke-dasharray": "4 3"}),
            Prim("line", {"x1": round(hx + side * 14, 1), "y1": round(hy - 6, 1), "x2": round(lx, 1),
                          "y2": round(hy - 26, 1), "stroke": GOOD, "stroke-width": 1.5}),
            static_text("Hand hält", lx + side * 4, hy - 42, 12, GOOD, anchor="end" if side < 0 else "start",
                        weight="600"),
            static_text("die Sitzkante", lx + side * 4, hy - 28, 12, GOOD, anchor="end" if side < 0 else "start",
                        weight="600"),
        ]))

    prims = [
        scene,
        *grips,
        caption_band(),
        timer,
        static_text("Nicht am Kopf ziehen – Schulter bleibt unten", 200, 24, LEAD_SIZE, MUTED),
        *caps(0.0, "Rechte", "linken", "linke"),
        *caps(T, "Linke", "rechten", "rechte"),
    ]
    return render(prims, tl, FRONT, fps=8, title="Seitliche Nackendehnung")
