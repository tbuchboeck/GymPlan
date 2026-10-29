from rig import *

SLUG = "open-book"

# Perspektive: schräg vom Kopfende und leicht von oben. Die Drehachse (Wirbel-
# säule) zeigt damit fast zum Betrachter, der obere Arm beschreibt seinen Bogen
# in der Bildebene – genau das "Aufklappen des Buchs". Becken und Knie bleiben
# sichtbar übereinander, die Schulterlinie dreht sich dagegen.
#
# Kleiner 3D-Rig nur für diese Datei (wird von thread_the_needle wiederverwendet):
# Gelenke als 3D-Punkte (x = Bauchseite, y = oben, z = Richtung Kopf/Betrachter),
# orthografisch projiziert. Zeichenreihenfolge ist fest (hinten -> vorn).


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
        f = lambda c, n=names: {"d": smooth_path([self.P(c, k) for k in n])}
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
            return {"d": "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"}
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

CAM = Cam(yaw=-12, pitch=46, scale=1.3, cx=214, cy=190)
ARM = 81
TH_MAX = 78


def joints(p):
    th = math.radians(p.get("th", 0.0))
    s = math.sin(th)
    J = {}
    # Becken/Beine: bleiben liegen (Knie aufeinander)
    J["hip1"], J["hip0"] = (0, 29, -82), (0, 6, -82)
    J["pelvis"] = (0, 17, -82)
    J["knee1"], J["knee0"] = (46, 24, -80), (46, 8, -80)
    J["foot1"], J["foot0"] = (46, 22, -126), (46, 8, -126)
    J["toe1"], J["toe0"] = (52, 22, -132), (52, 8, -132)
    J["waist"] = (0, 18, -46)
    # Schultern drehen um die Längsachse
    sc = (-12 * s, 26 - 11 * s, 0)
    v = (-math.sin(th) * 19, math.cos(th) * 19, 0)
    J["sc"] = sc
    J["sh1"], J["sh0"] = add(sc, v), add(sc, v, -1)
    # Brustbein-Richtung (Normale der Schulterlinie)
    J["chest_c"] = add(sc, (0, 0, -22))
    J["chest_n"] = add(J["chest_c"], (math.cos(th) * 34, math.sin(th) * 34, 0))
    # unterer Arm liegt nach vorn am Boden
    b = J["sh0"]
    J["el0"] = (b[0] + 36, max(7, b[1] - 1), 2)
    J["wr0"] = (b[0] + 68, 7, 4)
    J["ha0"] = (b[0] + 81, 7, 4)
    # oberer Arm gestreckt, Winkel phi in der Bildebene
    t = J["sh1"]
    phi = math.radians(p.get("phi", -17))
    if t[1] + ARM * math.sin(phi) < 9:           # Hand nicht in den Boden
        phi = math.pi - math.asin((9 - t[1]) / ARM) if math.cos(phi) < 0 else math.asin((9 - t[1]) / ARM)
    d = (math.cos(phi), math.sin(phi), 0)
    J["el1"], J["wr1"], J["ha1"] = add(t, d, 36), add(t, d, 68), add(t, d, 81)
    J["el1"] = add(J["el1"], (0, 0, 2))
    J["wr1"] = add(J["wr1"], (0, 0, 4))
    J["ha1"] = add(J["ha1"], (0, 0, 4))
    # Kopf auf dem Kissen, Blick folgt der Hand
    J["neck"] = add(sc, (0, -1, 12))
    J["head"] = (-6 * s, 26 - 3 * s, 32)
    g = math.radians(p.get("gaze", 0.0))
    J["gaze"] = (math.cos(g), math.sin(g), 0.25)
    return J


START = dict(th=0, phi=-17, gaze=-5)
OPEN = dict(th=TH_MAX, phi=190, gaze=125)


def build():
    rig = Rig3(joints, CAM)
    tl = Timeline([(0, START), (0.8, START), (3.2, OPEN), (5.4, OPEN), (7.4, START), (8.0, START)])

    pil_top = [CAM((-24, 9, 14)), CAM((22, 9, 14)), CAM((22, 9, 52)), CAM((-24, 9, 52))]
    pil_d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pil_top) + "Z"
    pil_front = [CAM((-24, 0, 52)), CAM((22, 0, 52))]
    pillow = [
        Prim("path", {"d": f"M{pil_top[3][0]:.1f} {pil_top[3][1]:.1f}L{pil_top[2][0]:.1f} {pil_top[2][1]:.1f}"
                           f"L{pil_front[1][0]:.1f} {pil_front[1][1]:.1f}L{pil_front[0][0]:.1f} {pil_front[0][1]:.1f}Z",
                      "fill": PROP_DARK, "stroke": PROP_DARK, "stroke-width": 8, "stroke-linejoin": "round"}),
        Prim("path", {"d": pil_d, "fill": PROP, "stroke": PROP, "stroke-width": 8, "stroke-linejoin": "round"}),
    ]

    # Bogen, den die Hand beschreibt (gestrichelt, nur während der Bewegung)
    def hand_arc():
        pts = []
        for i in range(25):
            ph = -17 + (190 + 17) * i / 24
            pts.append(rig.cam(joints(dict(th=TH_MAX * i / 24, phi=ph))["ha1"]))
        return pts
    arc_pts = hand_arc()
    arc_d = smooth_path(arc_pts[1:-1])

    ghost_arm = ghost(rig.limb(["sh1", "el1", "wr1", "ha1"], 12, NEAR), SIDE, START, 0.14)

    prims = [
        *floor_rect(CAM, -108, 78, -136, 54),
        *rig.limb(["hip0", "knee0", "foot0"], 16, FAR),
        *rig.limb(["hip1", "knee1", "foot1"], 16, NEAR),
        Prim("ellipse", {"cx": round(CAM((46, 16, -80))[0], 1), "cy": round(CAM((46, 16, -80))[1], 1),
                         "rx": 16, "ry": 22, "fill": GOOD, "opacity": 0.35, "_pulse": True, "_show": [(0.8, 7.4)]}),
        *rig.slab(["hip1", "sh1", "sh0", "hip0"], TORSO, 18),
        *rig.limb(["hip1", "hip0"], 22, TORSO, outline=False),
        *rig.limb(["pelvis", "waist", "chest_c"], 24, TORSO, outline=False),
        *rig.limb(["sh1", "sh0"], 22, "#8f98fb"),
        *rig.limb(["sh0", "el0", "wr0", "ha0"], 11, FAR),
        *pillow,
        *rig.limb(["sc", "neck", "head"], 12, TORSO),
        ghost_arm,
        Prim("path", {"d": arc_d, "fill": "none", "stroke": ACCENT, "stroke-width": 2, "stroke-dasharray": "4 5",
                      "opacity": 0.75, "_show": [(0.8, 3.2)]}),
        Prim("path", {"fill": "none", "stroke": GOOD, "stroke-width": 2.5, "stroke-linecap": "round",
                      "marker-end": "url(#arrowG)"},
             lambda c: {"d": smooth_path([rig.P(c, "chest_c"), rig.P(c, "chest_n")])}),
        *rig.limb(["sh1", "el1", "wr1", "ha1"], 12, NEAR),
        *rig.head("head", "gaze"),
        caption_band(),
        caption("Seitenlage, Knie 90° aufeinander", 0, 0.8),
        caption("Oberen Arm im Bogen öffnen – Blick folgt", 0.8, 3.2),
        caption("Brust zur Decke – 2 Atemzüge halten", 3.2, 5.4),
        caption("Langsam zurück – Knie bleiben zusammen", 5.4, 8.0),
        static_text("Drehung aus der BWS, nicht aus der Hüfte", 200, 24, 13, MUTED),
    ]
    defs = ('<marker id="arrowG" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" '
            f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{GOOD}"/></marker>')
    return render(prims, tl, SIDE, title="Open Book", extra_defs=defs)
