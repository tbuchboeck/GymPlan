from rig import *

SLUG = "open-book"

# Perspektive: vom Kopfende aus, Kamera knapp über dem Boden, Blick entlang der
# Wirbelsäule zu den Füßen (2D vereinfacht). Die Drehachse zeigt zum Betrachter:
# Schulterlinie dreht von senkrecht (Seitenlage) nach fast waagrecht (Brust zur
# Decke), der obere Arm beschreibt einen Halbkreis von rechts nach links.
# Becken und Knie bleiben dahinter sichtbar übereinander. Ein kleines Inset
# zeigt die Seitenlage mit 90°-Knien von oben.
#
# Die 3D-Helfer unten (Cam, Rig3, spath, floor_rect) nutzt thread_the_needle.py.


class Cam:
    def __init__(self, yaw, pitch, scale, cx, cy):
        self.ya, self.pa = math.radians(yaw), math.radians(pitch)
        self.s, self.cx, self.cy = scale, cx, cy

    def __call__(self, p):
        x, y, z = p
        x1 = x * math.cos(self.ya) + z * math.sin(self.ya)
        z1 = -x * math.sin(self.ya) + z * math.cos(self.ya)
        yu = y * math.cos(self.pa) - z1 * math.sin(self.pa)
        return (self.cx + self.s * x1, self.cy - self.s * yu)

    def dir(self, v):
        """Bildschirmwinkel (math., Grad) eines 3D-Richtungsvektors."""
        a, b = self((0, 0, 0)), self(v)
        return math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0]))


def add(a, b, k=1.0):
    return (a[0] + k * b[0], a[1] + k * b[1], a[2] + k * b[2])


def lerp3(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


def spath(points):
    """Wie smooth_path, aber mit ganzzahligen Koordinaten (kleinere Datei)."""
    r = [(round(x), round(y)) for x, y in points]
    if len(r) == 2:
        return f"M{r[0][0]} {r[0][1]}L{r[1][0]} {r[1][1]}"
    d = f"M{r[0][0]} {r[0][1]}"
    for i in range(1, len(r) - 1):
        (cx, cy), (nx, ny) = r[i], r[i + 1]
        mx, my = ((cx + nx) / 2, (cy + ny) / 2) if i < len(r) - 2 else (nx, ny)
        d += f"Q{cx} {cy} {mx:g} {my:g}"
    return d


class Rig3:
    """Cached Gelenk-Funktion pose -> {name: (x, y, z)}."""
    def __init__(self, fn, cam):
        self.fn, self.cam, self._c = fn, cam, {}

    def J(self, c):
        k = id(c["pose"])
        if k not in self._c:
            self._c[k] = (c["pose"], self.fn(c["pose"]))
        return self._c[k][1]

    def P(self, c, name):
        return self.cam(self.J(c)[name])

    def limb(self, names, width, color, outline=True):
        w = width * self.cam.s
        f = lambda c, n=names: {"d": spath([self.P(c, k) for k in n])}
        out = []
        if outline:
            out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": round(w + 3, 1),
                                     "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
        out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": round(w, 1),
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
        return out

    def slab(self, names, color, round_w=12):
        """Gefülltes Polygon mit runden Ecken (Rumpf, Polster)."""
        w = round_w * self.cam.s
        def f(c, n=names):
            pts = [self.P(c, k) for k in n]
            return {"d": "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + "Z"}
        return [Prim("path", {"fill": SKIN_LINE, "stroke": SKIN_LINE, "stroke-width": round(w + 3, 1),
                              "stroke-linejoin": "round"}, f),
                Prim("path", {"fill": color, "stroke": color, "stroke-width": round(w, 1),
                              "stroke-linejoin": "round"}, f)]

    def head(self, center, gaze, r=17, up=None):
        """Kopf; Nase zeigt in Blickrichtung `gaze` (Name eines 3D-Vektors in J).
        `up` (Vektorname) = Scheitelrichtung für Haare."""
        rr = r * self.cam.s

        def base(c):
            x, y = self.P(c, center)
            fa = self.cam.dir(self.J(c)[gaze])
            return x, y, fa

        def at(c, fwd, side, k=1.0):
            x, y, fa = base(c)
            f, s_ = math.radians(fa), math.radians(fa + 90)
            return (x + rr * k * (fwd * math.cos(f) + side * math.cos(s_)),
                    y - rr * k * (fwd * math.sin(f) + side * math.sin(s_)))

        def skull(c):
            x, y, _ = base(c)
            return {"cx": x, "cy": y}

        def hair(c):
            x, y, fa = base(c)
            def p(deg, k=1.0):
                a = math.radians(fa + deg)
                return x + (rr + 1) * k * math.cos(a), y - (rr + 1) * k * math.sin(a)
            p0, p1, q = p(80), p(-80), p(180, 0.25)
            return {"d": f"M{p0[0]:.1f} {p0[1]:.1f}A{rr + 1:.1f} {rr + 1:.1f} 0 1 0 {p1[0]:.1f} {p1[1]:.1f}"
                         f"Q{q[0]:.1f} {q[1]:.1f} {p0[0]:.1f} {p0[1]:.1f}Z"}

        def nose(c):
            a, b, d = at(c, 0.9, 0.18), at(c, 1.25, -0.02), at(c, 0.9, -0.22)
            return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{d[0]:.1f} {d[1]:.1f}Z"}

        def eye(side):
            return lambda c: dict(zip(("cx", "cy"), at(c, 0.55, side * 0.38)))

        return [
            Prim("circle", {"r": round(rr + 1.5, 1), "fill": SKIN_LINE}, skull),
            Prim("circle", {"r": round(rr, 1), "fill": HEAD}, skull),
            Prim("path", {"fill": "#4338ca"}, hair),
            Prim("path", {"fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linejoin": "round"}, nose),
            Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(1)),
            Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(-1)),
        ]


def floor_rect(cam, x0, x1, z0, z1, y=0.0, color="#3f4a7a", edge=5):
    """Matte als projiziertes Rechteck mit sichtbarer Vorderkante."""
    c = [cam((x0, y, z0)), cam((x1, y, z0)), cam((x1, y, z1)), cam((x0, y, z1))]
    d = "M" + "L".join(f"{x:.1f} {yy:.1f}" for x, yy in c) + "Z"
    front = [cam((x0, y, z1)), cam((x1, y, z1))]
    fd = (f"M{front[0][0]:.1f} {front[0][1]:.1f}L{front[1][0]:.1f} {front[1][1]:.1f}"
          f"L{front[1][0]:.1f} {front[1][1] + edge:.1f}L{front[0][0]:.1f} {front[0][1] + edge:.1f}Z")
    return [Prim("path", {"d": fd, "fill": "#2b3460"}),
            Prim("path", {"d": d, "fill": color, "stroke": "#4b5794", "stroke-width": 1})]



# --------------------------------------------------------------------------
# Open Book: 2D-Ansicht vom Kopfende

FLOOR = 236          # Vorderkante der Matte (Kontakt nahe Objekte)
BACKF = FLOOR - 11   # Kontaktlinie hinten (Becken/Knie, etwas weiter weg)
AX = 188             # Drehachse x in Seitenlage
SW = 34              # halbe Schulterbreite
ARM = 84
TH_MAX = 80


def geo(p):
    th = math.radians(p.get("th", 0.0))
    s, c = math.sin(th), math.cos(th)
    G = {}
    ax, ay = AX - 18 * s, FLOOR - 42 + 22 * s
    G["axis"] = (ax, ay)
    G["sh1"] = (ax - SW * s, ay - SW * c)      # obere Schulter
    G["sh0"] = (ax + SW * s, ay + SW * c)      # untere Schulter
    # unterer Arm liegt nach vorn am Boden
    b = G["sh0"]
    G["el0"], G["wr0"], G["ha0"] = (b[0] + 38, FLOOR - 8), (b[0] + 70, FLOOR - 8), (b[0] + 84, FLOOR - 8)
    # oberer Arm gestreckt
    t = G["sh1"]
    phi = math.radians(p.get("phi", -35.0))
    if t[1] - ARM * math.sin(phi) > FLOOR - 8:           # Hand nicht unter die Matte
        k = max(-1.0, min(1.0, (t[1] - (FLOOR - 8)) / ARM))
        phi = math.pi - math.asin(k) if math.cos(phi) < 0 else math.asin(k)
    d = (math.cos(phi), -math.sin(phi))
    G["el1"], G["wr1"], G["ha1"] = [(t[0] + d[0] * L, t[1] + d[1] * L) for L in (38, 70, ARM)]
    # Brust-Normale (zeigt nach vorn bzw. zur Decke)
    G["chest_a"] = (ax + 20 * c, ay - 20 * s)
    G["chest_b"] = (ax + 46 * c, ay - 46 * s)
    # Kopf auf dem Kissen
    G["head"] = (AX - 8 * s, FLOOR - 33)
    G["gaze"] = p.get("gaze", 0.0)
    # hinten: Becken senkrecht, Oberschenkel nach vorn, Knie übereinander
    G["hip1"], G["hip0"] = (AX + 2, BACKF - 50), (AX + 2, BACKF - 14)
    G["knee1"], G["knee0"] = (AX + 50, BACKF - 25), (AX + 50, BACKF - 9)
    return G


class Rig2:
    def __init__(self):
        self._c = {}

    def G(self, c):
        k = id(c["pose"])
        if k not in self._c:
            self._c[k] = (c["pose"], geo(c["pose"]))
        return self._c[k][1]

    def limb(self, names, width, color, outline=True):
        f = lambda c, n=names: {"d": spath([self.G(c)[k] for k in n])}
        out = []
        if outline:
            out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                     "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
        out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
        return out

    def head(self, r=19):
        def base(c):
            x, y = self.G(c)["head"]
            return x, y, self.G(c)["gaze"]

        def at(c, fwd, side):
            x, y, g = base(c)
            f, s_ = math.radians(g), math.radians(g + 90)
            return (x + r * (fwd * math.cos(f) + side * math.cos(s_)),
                    y - r * (fwd * math.sin(f) + side * math.sin(s_)))

        def skull(c):
            x, y, _ = base(c)
            return {"cx": round(x, 1), "cy": round(y, 1)}

        def hair(c):
            x, y, g = base(c)
            def q(deg, k=1.0):
                a = math.radians(g + deg)
                return x + (r + 1) * k * math.cos(a), y - (r + 1) * k * math.sin(a)
            p0, p1, m = q(100), q(-100), q(180, 0.15)
            return {"d": f"M{p0[0]:.1f} {p0[1]:.1f}A{r + 1} {r + 1} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}"
                         f"Q{m[0]:.1f} {m[1]:.1f} {p0[0]:.1f} {p0[1]:.1f}Z"}

        def nose(c):
            a, b, d = at(c, 0.92, 0.14), at(c, 1.3, -0.04), at(c, 0.92, -0.2)
            return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{d[0]:.1f} {d[1]:.1f}Z"}

        def eye(side):
            return lambda c: dict(zip(("cx", "cy"), (round(v, 1) for v in at(c, 0.5, side * 0.36))))

        def mouth(c):
            a, b = at(c, 0.62, 0.28), at(c, 0.62, -0.28)
            m = at(c, 0.74, 0.0)
            return {"d": f"M{a[0]:.1f} {a[1]:.1f}Q{m[0]:.1f} {m[1]:.1f} {b[0]:.1f} {b[1]:.1f}"}

        return [
            Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
            Prim("circle", {"r": r, "fill": HEAD}, skull),
            Prim("path", {"fill": "#4338ca"}, hair),
            Prim("path", {"fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linejoin": "round"}, nose),
            Prim("circle", {"r": 2.3, "fill": SKIN_LINE}, eye(1)),
            Prim("circle", {"r": 2.3, "fill": SKIN_LINE}, eye(-1)),
        ]


START = dict(th=0, phi=-35, gaze=-8)
OPEN = dict(th=TH_MAX, phi=188, gaze=128)


def inset():
    """Kleine Draufsicht: Seitenlage, Knie 90°, Arme vorn (statisch)."""
    pose = dict(x=200, y=150, rot=90, thigh_n=88, shin_n=-92, foot_n=-80, thigh_f=92, shin_f=-92,
                foot_f=-80, upperarm_n=86, upperarm_f=94, neck=-6, head=-4)
    fig = ghost(side_figure(), SIDE, pose, 1.0)
    box = [Prim("rect", {"x": 292, "y": 40, "width": 100, "height": 76, "rx": 8, "fill": "#0b1220",
                         "opacity": 0.7, "stroke": "#334155", "stroke-width": 1}),
           Prim("rect", {"x": 300, "y": 52, "width": 84, "height": 46, "rx": 4, "fill": "#3f4a7a", "opacity": 0.6})]
    return box + [group([fig], scale=0.4, origin=(200, 150), dx=150, dy=-70),
                  static_text("Seitenlage von oben", 342, 110, 9.5, MUTED)]


def build():
    rig = Rig2()
    tl = Timeline([(0, START), (0.8, START), (3.2, OPEN), (5.4, OPEN), (7.4, START), (8.0, START)])

    # Bogen der Hand (gestrichelt, leicht außerhalb der Hand)
    arc = []
    for i in range(1, 24):
        u = i / 24
        G = geo(dict(th=TH_MAX * smooth(u), phi=-35 + 223 * smooth(u)))
        ax, ay = G["sh1"]
        hx, hy = G["ha1"]
        arc.append((ax + (hx - ax) * 1.12, ay + (hy - ay) * 1.12))

    pillow = [Prim("rect", {"x": AX - 34, "y": FLOOR - 15, "width": 60, "height": 13, "rx": 6,
                            "fill": PROP, "stroke": PROP_DARK, "stroke-width": 2})]
    defs = ('<marker id="arrowG" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" '
            f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{GOOD}"/></marker>')
    k1, k0 = geo(START)["knee1"], geo(START)["knee0"]
    scene = group([
        Prim("rect", {"x": 40, "y": BACKF - 4, "width": 312, "height": FLOOR - BACKF + 6, "rx": 3, "fill": "#3f4a7a"}),
        Prim("rect", {"x": 40, "y": FLOOR + 2, "width": 312, "height": 5, "rx": 2, "fill": "#2b3460"}),
        # hinten: Beine und Becken (dunkler = weiter weg)
        *rig.limb(["hip0", "knee0"], 16, FAR),
        *rig.limb(["hip1", "knee1"], 16, "#7479e8"),
        Prim("ellipse", {"cx": k1[0] + 2, "cy": (k1[1] + k0[1]) / 2, "rx": 14, "ry": 20, "fill": GOOD,
                         "opacity": 0.35, "_pulse": True, "_show": [(0.8, 7.4)]}),
        *rig.limb(["hip1", "hip0"], 30, FAR),
        # Rumpf: Flanke zwischen Becken und Schultern, dann Brustkorb
        Prim("path", {"fill": "#6d72e8", "stroke": SKIN_LINE, "stroke-width": 2, "stroke-linejoin": "round"},
             lambda c: {"d": "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in
                                            [rig.G(c)[k] for k in ("hip1", "sh1", "sh0", "hip0")]) + "Z"}),
        *rig.limb(["sh1", "sh0"], 34, TORSO),
        *rig.limb(["sh0", "el0", "wr0", "ha0"], 12, FAR),
        Prim("path", {"fill": "none", "stroke": GOOD, "stroke-width": 2.5, "stroke-linecap": "round",
                      "marker-end": "url(#arrowG)"},
             lambda c: {"d": spath([rig.G(c)["chest_a"], rig.G(c)["chest_b"]])}),
        ghost(rig.limb(["sh1", "el1", "wr1", "ha1"], 13, NEAR), SIDE, START, 0.16),
        Prim("path", {"d": smooth_path(arc), "fill": "none", "stroke": ACCENT, "stroke-width": 2,
                      "stroke-dasharray": "4 5", "opacity": 0.8, "marker-end": "url(#arrowhead)",
                      "_show": [(0.8, 3.2)]}),
        *rig.limb(["sh1", "el1", "wr1", "ha1"], 13, NEAR),
        *pillow,
        *rig.head(),
    ], scale=1.12, origin=(AX, FLOOR), dx=12)
    prims = [
        scene,
        *inset(),
        caption_band(),
        caption("Seitenlage, Knie 90° aufeinander", 0, 0.8),
        caption("Oberen Arm im Bogen öffnen – Blick folgt", 0.8, 3.2),
        caption("Brust zur Decke – 2 Atemzüge halten", 3.2, 5.4),
        caption("Langsam zurück – Knie bleiben zusammen", 5.4, 8.0),
        static_text("Ansicht vom Kopfende", 16, 24, 12, MUTED, anchor="start"),
        static_text("Drehung aus der BWS", 16, 40, 12, MUTED, anchor="start"),
    ]
    return render(prims, tl, SIDE, title="Open Book", extra_defs=defs)
