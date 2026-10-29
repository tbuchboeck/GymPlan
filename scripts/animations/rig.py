"""
Kleiner 2D-Rig für animierte Übungs-SVGs (SMIL, ohne JavaScript).

Idee
----
Eine Figur ist ein Skelett aus Segmenten (Baum). Jede Pose legt relative
Gelenkwinkel fest. Zwischen Schlüsselposen wird weich interpoliert
(smoothstep), die Vorwärtskinematik wird pro Frame in Python gerechnet und
als <animate values="..."> ausgegeben. Dadurch bleiben Knochenlängen exakt,
die Zeichenreihenfolge (vorne/hinten) ist frei wählbar, und Requisiten
(Sling, Rolle, Wand) können an Gelenke gekoppelt werden.

Konventionen
------------
* Koordinaten: SVG (x nach rechts, y nach unten), Winkel in Grad, aber
  mathematisch: 0 = rechts, 90 = oben, positiv = gegen den Uhrzeigersinn.
* Pose = dict. Schlüssel "x", "y" (Position der Wurzel/Becken), "rot"
  (Drehung der ganzen Figur, 0 = aufrecht), dazu relative Winkel je Segment
  (Abweichung von der Ruhelage) und beliebige weitere Skalare (z. B.
  "breath", "turn"), die Zeichenfunktionen lesen können.
* Fehlende Schlüssel = 0 (Ruhelage).

Siehe poses.py für anatomische Helfer und exercises/ für Beispiele.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

# --------------------------------------------------------------------------
# Skelett
# --------------------------------------------------------------------------


@dataclass
class Seg:
    name: str
    parent: str | None
    length: float
    rest: float  # Ruhewinkel relativ zum Eltern-Segment


class Skeleton:
    def __init__(self, segs: list[Seg]):
        self.segs = segs
        self.by_name = {s.name: s for s in segs}

    def fk(self, pose: dict) -> dict:
        """Liefert dict name -> (x_start, y_start, x_end, y_end, abs_angle)."""
        out: dict[str, tuple] = {}
        root_rot = pose.get("rot", 0.0)
        rx, ry = pose.get("x", 200.0), pose.get("y", 200.0)
        for s in self.segs:  # Eltern stehen immer vor Kindern
            if s.parent is None:
                sx, sy, pa = rx, ry, root_rot
            else:
                p = out[s.parent]
                sx, sy, pa = p[2], p[3], p[4]
            a = pa + s.rest + pose.get(s.name, 0.0)
            ex = sx + s.length * math.cos(math.radians(a))
            ey = sy - s.length * math.sin(math.radians(a))
            out[s.name] = (sx, sy, ex, ey, a)
        return out


# Seitansicht, Blick nach rechts. Arme/Beine mit Suffix _n (nah) und _f (fern).
SIDE = Skeleton([
    Seg("root", None, 0, 90),
    Seg("lumbar", "root", 26, 0),
    Seg("thorax", "lumbar", 26, 0),
    Seg("chest", "thorax", 26, 0),
    Seg("neck", "chest", 19, 0),
    Seg("head", "neck", 14, 0),
    Seg("upperarm_n", "chest", 36, 180),
    Seg("forearm_n", "upperarm_n", 32, 0),
    Seg("hand_n", "forearm_n", 13, 0),
    Seg("upperarm_f", "chest", 36, 180),
    Seg("forearm_f", "upperarm_f", 32, 0),
    Seg("hand_f", "forearm_f", 13, 0),
    Seg("thigh_n", "root", 50, 180),
    Seg("shin_n", "thigh_n", 48, 0),
    Seg("foot_n", "shin_n", 20, 90),
    Seg("thigh_f", "root", 50, 180),
    Seg("shin_f", "thigh_f", 48, 0),
    Seg("foot_f", "shin_f", 20, 90),
])

# Frontansicht (Blick zum Betrachter). L/R = Bildschirmseite, nicht anatomisch.
FRONT = Skeleton([
    Seg("root", None, 0, 90),
    Seg("lumbar", "root", 26, 0),
    Seg("thorax", "lumbar", 26, 0),
    Seg("chest", "thorax", 26, 0),
    Seg("neck", "chest", 17, 0),
    Seg("head", "neck", 15, 0),
    Seg("clav_L", "chest", 24, 90),
    Seg("upperarm_L", "clav_L", 36, 90),
    Seg("forearm_L", "upperarm_L", 32, 0),
    Seg("hand_L", "forearm_L", 13, 0),
    Seg("clav_R", "chest", 24, -90),
    Seg("upperarm_R", "clav_R", 36, -90),
    Seg("forearm_R", "upperarm_R", 32, 0),
    Seg("hand_R", "forearm_R", 13, 0),
    Seg("hip_L", "root", 15, 90),
    Seg("thigh_L", "hip_L", 50, 90),
    Seg("shin_L", "thigh_L", 48, 0),
    Seg("foot_L", "shin_L", 9, 0),
    Seg("hip_R", "root", 15, -90),
    Seg("thigh_R", "hip_R", 50, -90),
    Seg("shin_R", "thigh_R", 48, 0),
    Seg("foot_R", "shin_R", 9, 0),
])

# --------------------------------------------------------------------------
# Farben / Stil
# --------------------------------------------------------------------------

BG_TOP = "#1e293b"
BG_BOTTOM = "#0f172a"
NEAR = "#a5b4fc"      # nahe Gliedmaßen
TORSO = "#818cf8"     # Rumpf
FAR = "#5b5fd6"       # ferne Gliedmaßen (dunkler)
HEAD = "#c7d2fe"
SKIN_LINE = "#312e81"
ACCENT = "#fbbf24"    # Pfeile, Fokus, Hinweise
GOOD = "#34d399"
WARN = "#f87171"
PROP = "#64748b"
PROP_DARK = "#475569"
FLOOR = "#334155"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"

W, H = 400, 300

# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------


def smooth(t: float) -> float:
    return t * t * (3 - 2 * t)


@dataclass
class IK:
    """Hält das Ende einer 2-Knochen-Kette auf einem Zielpunkt (z. B. Hand am
    Boden). bend=+1/-1 wählt die Knickrichtung. end_seg/end_abs setzt optional
    den absoluten Winkel des dritten Segments (Hand/Fuß flach)."""
    upper: str
    lower: str
    target: tuple[float, float] | Callable[[dict], tuple[float, float]]
    bend: int = 1
    end_seg: str | None = None
    end_abs: float | None = None


@dataclass
class Anchor:
    """Dreht die ganze Figur um die Wurzel, sodass `joint` auf der Linie
    Wurzel→target liegt (z. B. Schultern bleiben über den Händen, während
    sich die Wirbelsäule krümmt). In iks= mit aufnehmen, vor den IKs."""
    joint: str
    target: tuple[float, float]


def solve_anchor(skel: "Skeleton", pose: dict, an: Anchor) -> dict:
    P = skel.fk(pose)
    rx, ry = pose.get("x", 200.0), pose.get("y", 200.0)
    jx, jy = P[an.joint][2], P[an.joint][3]
    cur = math.degrees(math.atan2(-(jy - ry), jx - rx))
    want = math.degrees(math.atan2(-(an.target[1] - ry), an.target[0] - rx))
    out = dict(pose)
    out["rot"] = pose.get("rot", 0.0) + (want - cur)
    return out


def solve_ik(skel: "Skeleton", pose: dict, ik: IK) -> dict:
    P = skel.fk(pose)
    sx, sy, _, _, ua = P[ik.upper]
    parent_abs = ua - skel.by_name[ik.upper].rest - pose.get(ik.upper, 0.0)
    l1 = skel.by_name[ik.upper].length
    l2 = skel.by_name[ik.lower].length
    tx, ty = ik.target(pose) if callable(ik.target) else ik.target
    dx, dy = tx - sx, -(ty - sy)  # mathematisch (y nach oben)
    d = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
    base = math.degrees(math.atan2(dy, dx))
    cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    a = math.degrees(math.acos(max(-1, min(1, cos_a))))
    upper_abs = base + ik.bend * a
    cos_b = (l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2)
    b = math.degrees(math.acos(max(-1, min(1, cos_b))))
    lower_rel_abs = upper_abs - ik.bend * (180 - b)
    out = dict(pose)
    out[ik.upper] = upper_abs - parent_abs - skel.by_name[ik.upper].rest
    out[ik.lower] = lower_rel_abs - upper_abs - skel.by_name[ik.lower].rest
    if ik.end_seg and ik.end_abs is not None:
        out[ik.end_seg] = ik.end_abs - lower_rel_abs - skel.by_name[ik.end_seg].rest
    return out


@dataclass
class Timeline:
    """Schlüsselposen [(sekunde, pose), ...]. Erste und letzte sollten für
    einen sauberen Loop gleich sein. Zwischen Keys: smoothstep.
    iks: Liste von IK-Constraints, die nach dem Interpolieren pro Frame
    angewendet werden (braucht skeleton)."""
    keys: list[tuple[float, dict]]
    iks: list[IK] = field(default_factory=list)
    skeleton: "Skeleton | None" = None

    def at(self, t: float) -> dict:
        pose = self._interp(t)
        for ik in self.iks:
            if isinstance(ik, Anchor):
                pose = solve_anchor(self.skeleton, pose, ik)
            else:
                pose = solve_ik(self.skeleton, pose, ik)
        return pose

    @property
    def duration(self) -> float:
        return self.keys[-1][0]

    def _interp(self, t: float) -> dict:
        ks = self.keys
        if t <= ks[0][0]:
            return dict(ks[0][1])
        for (t0, p0), (t1, p1) in zip(ks, ks[1:]):
            if t0 <= t <= t1:
                u = 0 if t1 == t0 else smooth((t - t0) / (t1 - t0))
                names = set(p0) | set(p1)
                return {n: p0.get(n, 0.0) + (p1.get(n, 0.0) - p0.get(n, 0.0)) * u for n in names}
        return dict(ks[-1][1])


# --------------------------------------------------------------------------
# Primitive: statische Attribute + optionale Funktion für dynamische
# --------------------------------------------------------------------------

Ctx = dict  # {"P": fk-Ergebnis, "pose": pose, "t": sekunde, "u": 0..1}


@dataclass
class Prim:
    tag: str
    attrs: dict = field(default_factory=dict)
    dyn: Callable[[Ctx], dict] | None = None
    text: str | None = None
    children: list["Prim"] = field(default_factory=list)


def fmt(v) -> str:
    if isinstance(v, float):
        s = f"{v:.1f}"
        return s[:-2] if s.endswith(".0") else s
    return str(v)


def pt(P, name, end=True):
    s = P[name]
    return (s[2], s[3]) if end else (s[0], s[1])


def smooth_path(points: list[tuple[float, float]]) -> str:
    """Glatte Kurve durch Punkte (quadratische Bézier über Mittelpunkte)."""
    if len(points) == 2:
        (x0, y0), (x1, y1) = points
        return f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}"
    d = f"M{points[0][0]:.1f} {points[0][1]:.1f}"
    for i in range(1, len(points) - 1):
        cx, cy = points[i]
        nx, ny = points[i + 1]
        mx, my = ((cx + nx) / 2, (cy + ny) / 2) if i < len(points) - 2 else (nx, ny)
        d += f"Q{cx:.1f} {cy:.1f} {mx:.1f} {my:.1f}"
    return d


def chain_points(P, names: list[str]) -> list[tuple[float, float]]:
    pts = [pt(P, names[0], end=False)]
    pts += [pt(P, n) for n in names]
    return pts


# --- Bausteine für Figuren -------------------------------------------------


def limb(names: list[str], width: float, color: str, outline=True) -> list[Prim]:
    """Gliedmaße als dicker, runder Strich durch eine Segmentkette."""
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"},
                        lambda c, n=names: {"d": smooth_path(chain_points(c["P"], n))}))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"},
                    lambda c, n=names: {"d": smooth_path(chain_points(c["P"], n))}))
    return out


def joint_dot(name: str, r: float, color: str, end=True) -> Prim:
    def f(c):
        x, y = pt(c["P"], name, end)
        return {"cx": x, "cy": y}
    return Prim("circle", {"r": r, "fill": color}, f)


def head_side(r=17) -> list[Prim]:
    """Kopf in Seitansicht mit Auge, Nase und Kinn – zeigt Blickrichtung."""
    def center(c):
        x, y = pt(c["P"], "head")
        return x, y, c["P"]["head"][4]

    def face_pt(c, fwd, up):
        x, y, a = center(c)
        fa = math.radians(a - 90)  # Blickrichtung = senkrecht zum Hals
        ua = math.radians(a)
        return (x + r * (fwd * math.cos(fa) + up * math.cos(ua)),
                y - r * (fwd * math.sin(fa) + up * math.sin(ua)))

    def skull(c):
        x, y, _ = center(c)
        return {"cx": x, "cy": y}

    def nose(c):
        a = face_pt(c, 0.9, 0.15)
        b = face_pt(c, 1.28, -0.1)
        d = face_pt(c, 0.92, -0.28)
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{d[0]:.1f} {d[1]:.1f}Z"}

    def eye(c):
        x, y = face_pt(c, 0.5, 0.18)
        return {"cx": x, "cy": y}

    def ear(c):
        x, y = face_pt(c, -0.12, 0.0)
        return {"cx": x, "cy": y}

    def hair(c):
        # Kappe über Hinterkopf und Scheitel: von Stirn bis Nacken
        x, y, a = center(c)
        def at(deg, rr=r + 1):
            ang = math.radians(a - 90 + deg)
            return x + rr * math.cos(ang), y - rr * math.sin(ang)
        p0, p1 = at(78), at(218)
        q = at(150, r * 0.35)
        return {"d": f"M{p0[0]:.1f} {p0[1]:.1f}A{r + 1} {r + 1} 0 0 0 {p1[0]:.1f} {p1[1]:.1f}"
                     f"Q{q[0]:.1f} {q[1]:.1f} {p0[0]:.1f} {p0[1]:.1f}Z"}

    return [
        Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
        Prim("circle", {"r": r, "fill": HEAD}, skull),
        Prim("path", {"fill": "#4338ca"}, hair),
        Prim("path", {"fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linejoin": "round"}, nose),
        Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye),
        Prim("circle", {"r": 3.5, "fill": "none", "stroke": TORSO, "stroke-width": 1.5}, ear),
    ]


def head_front(r=17) -> list[Prim]:
    """Kopf frontal. Pose-Skalar "turn" (-1..1) dreht das Gesicht seitlich."""
    def base(c):
        x, y = pt(c["P"], "head")
        return x, y, c["P"]["head"][4], c["pose"].get("turn", 0.0)

    def eye(side):
        def f(c):
            x, y, a, turn = base(c)
            lat = math.radians(a - 90)
            ua = math.radians(a)
            off = side * 0.38 + turn * 0.45
            return {"cx": x + r * (off * math.cos(lat) + 0.15 * math.cos(ua)),
                    "cy": y - r * (off * math.sin(lat) + 0.15 * math.sin(ua))}
        return f

    def nose(c):
        x, y, a, turn = base(c)
        lat = math.radians(a - 90)
        ua = math.radians(a)
        def p(off, up):
            return (x + r * (off * math.cos(lat) + up * math.cos(ua)),
                    y - r * (off * math.sin(lat) + up * math.sin(ua)))
        o = turn * 0.6
        p1, p2 = p(o, 0.05), p(o + 0.08 * (1 if turn >= 0 else -1), -0.25)
        return {"d": f"M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}"}

    def skull(c):
        x, y, *_ = base(c)
        return {"cx": x, "cy": y}

    return [
        Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
        Prim("circle", {"r": r, "fill": HEAD}, skull),
        Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(-1)),
        Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(1)),
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linecap": "round"}, nose),
    ]


def side_figure(far_first=True, torso_w=30, head=True, extras_behind=(), extras_front=()) -> list[Prim]:
    """Komplette Figur in Seitansicht: ferne Glieder, Rumpf, Kopf, nahe Glieder."""
    prims: list[Prim] = []
    prims += list(extras_behind)
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    if head:
        prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(extras_front)
    return prims


def front_figure(torso_w=44, head=True, extras_behind=(), extras_front=(), legs=True) -> list[Prim]:
    prims: list[Prim] = list(extras_behind)
    if legs:
        prims += limb(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR)
        prims += limb(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, NEAR)
    prims += limb(["neck"], 13, TORSO)
    # Rumpf + Schulterlinie: erst beide Umrisse, dann beide Füllungen
    trunk = limb(["lumbar", "thorax", "chest"], torso_w, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    prims += limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR)
    prims += limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR)
    if head:
        prims += head_front()
    prims += list(extras_front)
    return prims


def group(children: list[Prim], scale=1.0, origin=(200, 150), dx=0.0, dy=0.0, mirror=False) -> Prim:
    """Skaliert/verschiebt eine Gruppe um origin (z. B. Nahansicht vom Kopf)."""
    ox, oy = origin
    sx = -scale if mirror else scale
    tf = f"translate({ox + dx:.1f} {oy + dy:.1f}) scale({sx:.3f} {scale:.3f}) translate({-ox:.1f} {-oy:.1f})"
    return Prim("g", {"transform": tf}, children=children)


# --- Overlays ----------------------------------------------------------------


def arrow(d: str, color=ACCENT, width=3.0, show: list[tuple[float, float]] | None = None) -> Prim:
    """Gebogener Pfeil (Pfadangabe), optional nur in Zeitfenstern sichtbar."""
    p = Prim("path", {"d": d, "fill": "none", "stroke": color, "stroke-width": width,
                      "stroke-linecap": "round", "marker-end": "url(#arrowhead)"})
    if show is not None:
        p.attrs["_show"] = show
    return p


def focus(joint: str, rx=16, ry=10, offset=(0, 0), color=ACCENT, end=True, show=None) -> Prim:
    """Pulsierende Fokuszone (Muskel, der arbeiten soll) an einem Gelenk."""
    def f(c):
        x, y = pt(c["P"], joint, end)
        return {"cx": x + offset[0], "cy": y + offset[1]}
    p = Prim("ellipse", {"rx": rx, "ry": ry, "fill": color, "opacity": 0.35, "_pulse": True}, f)
    if show is not None:
        p.attrs["_show"] = show
    return p


def caption_band(y=258) -> Prim:
    """Dunkles Band unten, damit Phasentexte nie die Figur überdecken."""
    return Prim("rect", {"x": 0, "y": y, "width": W, "height": H - y, "fill": "#0b1220", "opacity": 0.85})


def ghost(prims: list[Prim], skeleton: "Skeleton", pose: dict, opacity=0.18) -> Prim:
    """Statische, blasse Kopie von Figurteilen in einer festen Pose
    (z. B. Startposition), damit der Bewegungsweg sichtbar wird."""
    ctx = {"P": skeleton.fk(pose), "pose": pose, "t": 0.0, "u": 0.0}

    def freeze(p: Prim) -> Prim:
        attrs = {k: v for k, v in p.attrs.items() if k not in ("_show", "_pulse")}
        if p.dyn is not None:
            attrs.update(p.dyn(ctx))
        return Prim(p.tag, attrs, None, p.text, [freeze(c) for c in p.children])

    return Prim("g", {"opacity": opacity}, children=[freeze(p) for p in prims])


def caption(text: str, t0: float, t1: float, y=284, size=15, color=TEXT, weight="600") -> Prim:
    return Prim("text", {"x": W / 2, "y": y, "font-size": size, "fill": color, "font-weight": weight,
                         "text-anchor": "middle", "_show": [(t0, t1)]}, text=text)


def static_text(text, x, y, size=12, color=MUTED, anchor="middle", weight="400") -> Prim:
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color,
                         "text-anchor": anchor, "font-weight": weight}, text=text)


def floor(y: float, x0=20, x1=380) -> Prim:
    return Prim("line", {"x1": x0, "y1": y, "x2": x1, "y2": y, "stroke": FLOOR, "stroke-width": 3,
                         "stroke-linecap": "round"})


def mat(y: float, x0=40, x1=360) -> Prim:
    return Prim("rect", {"x": x0, "y": y, "width": x1 - x0, "height": 6, "rx": 3, "fill": "#3f4a7a"})


# --------------------------------------------------------------------------
# Rendern
# --------------------------------------------------------------------------


def _show_anim(windows, dur) -> str:
    """Opacity 0/1 diskret je nach Zeitfenstern."""
    times, vals = [0.0], ["0"]
    for t0, t1 in windows:
        times += [t0 / dur, min(t1 / dur, 1.0)]
        vals += ["1", "0"]
    # deduplizieren / sortieren
    pairs = []
    for t, v in zip(times, vals):
        if pairs and abs(pairs[-1][0] - t) < 1e-6:
            pairs[-1] = (t, v)
        else:
            pairs.append((t, v))
    if pairs[-1][0] < 1.0:
        pairs.append((1.0, pairs[-1][1]))
    kt = ";".join(f"{t:.4f}" for t, _ in pairs)
    vs = ";".join(v for _, v in pairs)
    return (f'<animate attributeName="opacity" values="{vs}" keyTimes="{kt}" calcMode="discrete" '
            f'dur="{dur}s" repeatCount="indefinite"/>')


def render(prims: list[Prim], timeline: Timeline, skeleton: Skeleton, fps=15,
           title: str = "", extra_defs: str = "", background: list[Prim] | None = None) -> str:
    dur = timeline.duration
    n = max(2, int(round(dur * fps)))
    frames = []
    for i in range(n + 1):
        t = dur * i / n
        pose = timeline.at(t)
        frames.append({"P": skeleton.fk(pose), "pose": pose, "t": t, "u": t / dur})

    def emit(p: Prim) -> str:
        attrs = {k: v for k, v in p.attrs.items() if not k.startswith("_")}
        anims = []
        if p.dyn is not None:
            series = [p.dyn(f) for f in frames]
            for key in series[0]:
                vals = [fmt(s[key]) for s in series]
                if len(set(vals)) == 1:
                    attrs[key] = vals[0]
                else:
                    attrs.pop(key, None)
                    anims.append(f'<animate attributeName="{key}" values="{";".join(vals)}" '
                                 f'dur="{dur}s" repeatCount="indefinite"/>')
        if p.attrs.get("_pulse"):
            anims.append('<animate attributeName="opacity" values="0.15;0.5;0.15" dur="1.6s" '
                         'repeatCount="indefinite"/>')
        a = " ".join(f'{k}="{fmt(v)}"' for k, v in attrs.items())
        inner = "".join(anims) + (p.text or "") + "".join(emit(c) for c in p.children)
        el = f"<{p.tag} {a}>{inner}</{p.tag}>" if inner else f"<{p.tag} {a}/>"
        if "_show" in p.attrs:
            el = f'<g opacity="0">{_show_anim(p.attrs["_show"], dur)}{el}</g>'
        return el

    body = "\n".join(emit(p) for p in (background or []) + prims)
    head = (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="system-ui,-apple-system,sans-serif">\n'
        f'<title>{title}</title>\n'
        '<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/>'
        f'<stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>'
        '<marker id="arrowhead" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" '
        f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{ACCENT}"/></marker>'
        f'{extra_defs}</defs>\n'
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>\n'
    )
    return head + body + "\n</svg>\n"
