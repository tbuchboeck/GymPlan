from rig import *

SLUG = "open-book"

# Perspektive: schräg von oben (fast Draufsicht von der Decke). Person liegt
# auf der rechten Seite, Kopf links, Knie 90° übereinander nach vorn (unten im
# Bild). Der obere Arm schwingt im Halbkreis über den Körper nach hinten auf
# die Matte, der Brustkorb dreht dabei zur Decke (Schultern werden breit).
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
# Open Book: 3D-Mini-Rig, x = Richtung Füße, y = oben, z = Bauchseite

CAM = Cam(yaw=0, pitch=68, scale=1.0, cx=200, cy=152)
SH_X, HIP_X = -52, 40
SW = 19            # halbe Schulterbreite
ARM_UP, ARM_LO, ARM_HA = 36, 32, 13
TH_MAX = 80


def joints(p):
    th = math.radians(p.get("th", 0.0))
    J = {}
    cy = 20 - 7 * math.sin(th)
    c = (SH_X, cy, 0)
    v = (0, SW * math.cos(th), -SW * math.sin(th))        # zur oberen Schulter
    J["sh_c"] = c
    J["sh1"], J["sh0"] = add(c, v), add(c, v, -1)
    J["chest"] = add(c, (0, 14 * math.sin(th), 14 * math.cos(th)))
    # Becken und Beine bleiben liegen: Knie 90°, übereinander
    J["hip1"], J["hip0"] = (HIP_X, 27, 0), (HIP_X, 3, 0)
    J["knee1"], J["knee0"] = (HIP_X + 4, 25, 50), (HIP_X + 2, 4, 50)
    J["foot1"], J["foot0"] = (HIP_X + 52, 23, 52), (HIP_X + 50, 4, 52)
    J["waist"] = (-6, 15 - 2 * math.sin(th), 0)
    J["hip_c"] = (HIP_X, 15, 0)
    # unterer Arm liegt gestreckt nach vorn
    b = J["sh0"]
    J["el0"] = (b[0] + 2, 6, b[2] + ARM_UP)
    J["wr0"] = (b[0] + 3, 5, b[2] + ARM_UP + ARM_LO)
    J["ha0"] = (b[0] + 3, 5, b[2] + ARM_UP + ARM_LO + ARM_HA)
    # oberer Arm gestreckt, Winkel psi in der Querebene (0 = nach vorn, 90 = Decke)
    t = J["sh1"]
    L = ARM_UP + ARM_LO + ARM_HA
    psi = math.radians(p.get("psi", -12.0))
    lo = 10.0
    if t[1] + L * math.sin(psi) < lo:                      # Hand nicht in die Matte
        k = max(-1.0, min(1.0, (lo - t[1]) / L))
        psi = math.asin(k) if math.cos(psi) > 0 else math.pi - math.asin(k)
    d = (0.03, math.sin(psi), math.cos(psi))
    J["el1"], J["wr1"], J["ha1"] = add(t, d, ARM_UP), add(t, d, ARM_UP + ARM_LO), add(t, d, L)
    # Kopf auf dem Kissen, Blick folgt der Hand
    J["neck"] = add(c, (-16, -2 * math.cos(th), 2))
    J["head"] = (SH_X - 36, 17 - 3 * math.sin(th), 2 - 4 * math.sin(th))
    g = math.radians(p.get("gaze", 0.0))
    J["gaze"] = (0, math.sin(g), math.cos(g))
    return J


START = dict(th=0, psi=-12, gaze=0)
OPEN = dict(th=TH_MAX, psi=192, gaze=135)


def build():
    rig = Rig3(joints, CAM)
    tl = Timeline([(0, START), (0.8, START), (3.2, OPEN), (5.4, OPEN), (7.4, START), (8.0, START)])

    # Weg der Hand: neben dem Arm, leicht gewölbt (der Arm geht über den Körper)
    arc = []
    for i in range(2, 23):
        u = i / 24
        J = joints(dict(th=TH_MAX * smooth(u), psi=-12 + 204 * smooth(u)))
        hx, hy = CAM(J["ha1"])
        arc.append((hx + 16 + 22 * math.sin(math.pi * u), hy))

    pillow = CAM((SH_X - 38, 6, 2))
    sx = CAM.s
    k1 = CAM((HIP_X + 4, 25, 50))
    prims = [
        *floor_rect(CAM, -136, 118, -110, 104),
        Prim("ellipse", {"cx": round(pillow[0]), "cy": round(pillow[1]), "rx": round(30 * sx), "ry": round(16 * sx),
                         "fill": PROP, "stroke": PROP_DARK, "stroke-width": 2}),
        # unten liegende Seite (dunkler)
        *rig.limb(["hip0", "knee0", "foot0"], 15, FAR),
        *rig.limb(["sh0", "el0", "wr0", "ha0"], 11, FAR),
        # Rumpf: von oben schmal (Seitenlage), Schulterlinie wird beim Aufdrehen breit
        *rig.limb(["hip_c", "waist", "sh_c"], 30, TORSO),
        *rig.limb(["hip1", "hip0"], 26, TORSO, outline=False),
        *rig.limb(["sh1", "sh0"], 24, "#8f98fb"),
        Prim("ellipse", {"rx": round(13 * sx), "ry": round(9 * sx), "fill": GOOD, "opacity": 0.35, "_pulse": True,
                         "_show": [(1.6, 6.6)]},
             lambda c: dict(zip(("cx", "cy"), (round(v) for v in rig.P(c, "chest"))))),
        *rig.limb(["sh_c", "neck", "head"], 12, TORSO),
        *rig.head("head", "gaze"),
        # oben liegendes Bein, Knie bleiben aufeinander
        *rig.limb(["hip1", "knee1", "foot1"], 16, NEAR),
        Prim("ellipse", {"cx": round(k1[0]), "cy": round(k1[1]), "rx": 15, "ry": 12, "fill": GOOD,
                         "opacity": 0.3, "_pulse": True, "_show": [(0.8, 7.4)]}),
        ghost(rig.limb(["sh1", "el1", "wr1", "ha1"], 12, NEAR), SIDE, START, 0.16),
        # Schatten der Hand auf der Matte: zeigt, wie hoch der Arm gerade ist
        Prim("ellipse", {"rx": round(9 * sx), "ry": round(5 * sx), "fill": "#000", "opacity": 0.3},
             lambda c: (lambda h: dict(zip(("cx", "cy"), (round(v) for v in CAM((h[0], 0, h[2]))))))(rig.J(c)["ha1"])),
        Prim("path", {"d": smooth_path(arc), "fill": "none", "stroke": ACCENT, "stroke-width": 2.5,
                      "stroke-dasharray": "5 5", "opacity": 0.9, "marker-end": "url(#arrowhead)",
                      "_show": [(0.8, 3.2)]}),
        *rig.limb(["sh1", "el1", "wr1", "ha1"], 12, NEAR),
        caption_band(),
        caption("Seitenlage, Knie 90° aufeinander", 0, 0.8),
        caption("Oberen Arm im Bogen öffnen – Blick folgt", 0.8, 3.2),
        caption("Brust zur Decke – 2 Atemzüge halten", 3.2, 5.4),
        caption("Langsam zurück – Knie bleiben zusammen", 5.4, 8.0),
        static_text("Von oben gesehen – Drehung aus der BWS", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Open Book")
