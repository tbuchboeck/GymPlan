"""Gemeinsame Zeichenhelfer für die Gym-Geräte-Animationen (Beinpresse,
Bauchpresse, Adduktion/Abduktion, Rotary Torso, Laufband, Ellipsentrainer).
Unterstrich im Namen: build.py lädt diese Datei nicht als Übung."""

from rig import *


# --- statische Formen -------------------------------------------------------

def rect(x, y, w, h, fill=PROP, r=4, **kw) -> Prim:
    a = {"x": x, "y": y, "width": w, "height": h, "rx": r, "fill": fill}
    a.update(kw)
    return Prim("rect", a)


def line(x1, y1, x2, y2, color=PROP_DARK, w=6, cap="round", **kw) -> Prim:
    a = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": color, "stroke-width": w, "stroke-linecap": cap}
    a.update(kw)
    return Prim("line", a)


def circle(x, y, r, fill=PROP, **kw) -> Prim:
    a = {"cx": x, "cy": y, "r": r, "fill": fill}
    a.update(kw)
    return Prim("circle", a)


def poly(points, color=PROP_DARK, w=6, fill="none", **kw) -> Prim:
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    a = {"d": d, "fill": fill, "stroke": color, "stroke-width": w, "stroke-linecap": "round",
         "stroke-linejoin": "round"}
    a.update(kw)
    return Prim("path", a)


# --- dynamische Formen ------------------------------------------------------

def dline(fn, color=PROP_DARK, w=6, cap="round", **kw) -> Prim:
    """Linie, fn(c) -> ((x1, y1), (x2, y2))."""
    def f(c):
        (x1, y1), (x2, y2) = fn(c)
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    a = {"stroke": color, "stroke-width": w, "stroke-linecap": cap}
    a.update(kw)
    return Prim("line", a, f)


def dpath(fn, color=PROP_DARK, w=6, fill="none", **kw) -> Prim:
    """Polylinie, fn(c) -> [(x, y), ...]."""
    def f(c):
        pts = fn(c)
        return {"d": "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}
    a = {"fill": fill, "stroke": color, "stroke-width": w, "stroke-linecap": "round", "stroke-linejoin": "round"}
    a.update(kw)
    return Prim("path", a, f)


def dcircle(fn, r, fill=PROP, **kw) -> Prim:
    def f(c):
        x, y = fn(c)
        return {"cx": x, "cy": y}
    a = {"r": r, "fill": fill}
    a.update(kw)
    return Prim("circle", a, f)


def moving(children: list[Prim], fn) -> Prim:
    """Gruppe, die per translate verschoben wird: fn(c) -> (dx, dy)."""
    def f(c):
        dx, dy = fn(c)
        return {"transform": f"translate({dx:.1f} {dy:.1f})"}
    return Prim("g", {}, f, children=children)


def pad_stroke(fn, w=13, color=PROP, outline=PROP_DARK) -> list[Prim]:
    """Gepolsterte Rolle/Polster als dicker runder Strich mit Rand."""
    return [dline(fn, outline, w + 3), dline(fn, color, w)]


def focus_mid(seg: str, frac=0.5, rx=14, ry=8, along=0.0, perp=0.0, color=ACCENT, show=None,
              rotate=True) -> Prim:
    """Pulsierende Fokuszone auf der Mitte eines Segments (Muskelbauch),
    entlang des Segments ausgerichtet."""
    def f(c):
        sx, sy, ex, ey, a = c["P"][seg]
        x = sx + (ex - sx) * frac
        y = sy + (ey - sy) * frac
        r = math.radians(a)
        ux, uy = math.cos(r), -math.sin(r)
        nx, ny = -uy, ux
        x += ux * along + nx * perp
        y += uy * along + ny * perp
        out = {"cx": x, "cy": y}
        if rotate:
            out["transform"] = f"rotate({-a:.1f} {x:.1f} {y:.1f})"
        return out
    p = Prim("ellipse", {"rx": rx, "ry": ry, "fill": color, "opacity": 0.35, "_pulse": True}, f)
    if show is not None:
        p.attrs["_show"] = show
    return p


def timed(p: Prim, show) -> Prim:
    p.attrs["_show"] = show
    return p


# --- Gewichtsblock ----------------------------------------------------------

def weight_stack(x, top_y, bottom_y, lift, n=9, sel=3, w=32, plate_h=8, label=None) -> tuple[list[Prim], tuple]:
    """Turm mit Führungsstangen und Gewichtsplatten. lift(c) -> Pixel, um die
    die oberen `sel` Platten (eingesteckt) angehoben werden.
    Rückgabe: (prims, (x, y) der oberen Umlenkrolle)."""
    rods_x = (x - w / 2 + 5, x + w / 2 - 5)
    stack_top = bottom_y - 4 - n * plate_h
    prims = [
        rect(x - w / 2 - 6, top_y - 4, w + 12, 8, PROP_DARK, 3),
        line(x - w / 2 - 3, top_y, x - w / 2 - 3, bottom_y, PROP_DARK, 5),
        line(x + w / 2 + 3, top_y, x + w / 2 + 3, bottom_y, PROP_DARK, 5),
        rect(x - w / 2 - 8, bottom_y - 4, w + 16, 6, PROP_DARK, 2),
    ]
    for rx in rods_x:
        prims.append(line(rx, top_y + 4, rx, bottom_y - 4, "#3a4659", 2))
    # untere, ruhende Platten
    for i in range(n - sel):
        y = bottom_y - 4 - (i + 1) * plate_h
        prims.append(rect(x - w / 2, y + 0.6, w, plate_h - 1.2, PROP, 1.5))
    # obere Platten + Kabel bewegen sich
    moving_plates = []
    for i in range(n - sel, n):
        y = bottom_y - 4 - (i + 1) * plate_h
        moving_plates.append(rect(x - w / 2, y + 0.6, w, plate_h - 1.2, "#7c8aa0", 1.5))
    pin_y = bottom_y - 4 - (n - sel + 0.5) * plate_h
    moving_plates.append(circle(x + w / 2 - 4, pin_y, 2.2, ACCENT))
    prims.append(moving(moving_plates, lambda c: (0, -lift(c))))
    pulley = (x, top_y + 10)
    prims.append(dline(lambda c: ((x, stack_top - lift(c)), (x, pulley[1])), "#cbd5e1", 1.6))
    prims.append(circle(pulley[0], pulley[1], 5, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.5}))
    if label:
        prims.append(static_text(label, x, bottom_y + 0, 10, MUTED))
    return prims, pulley


# --- Figur mit klar sichtbaren Gelenken -------------------------------------

def joint_points(P, names):
    """Wie chain_points, aber innere Gelenke doppelt -> deutlicher Knick
    (Knie/Ellbogen), statt dass smooth_path ihn wegrundet."""
    pts = [pt(P, names[0], end=False)]
    for i, n in enumerate(names):
        pts.append(pt(P, n))
        if i < len(names) - 1:
            pts.append(pt(P, n))
    return pts


def limb_j(names, width, color, outline=True) -> list[Prim]:
    out = []
    f = lambda c, n=names: {"d": smooth_path(joint_points(c["P"], n))}
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    return out


def side_fig(torso_w=30, head=True, extras_behind=(), extras_mid=(), extras_front=(),
             far_leg=True, far_arm=True) -> list[Prim]:
    """side_figure mit sichtbaren Knie-/Ellbogenknicken. extras_mid liegt
    zwischen Rumpf und nahen Gliedern (z. B. Polster an der nahen Seite)."""
    prims: list[Prim] = list(extras_behind)
    if far_leg:
        prims += limb_j(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    if far_arm:
        prims += limb_j(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    if head:
        prims += head_side()
    prims += list(extras_mid)
    prims += limb_j(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += limb_j(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(extras_front)
    return prims


# --- Frontansicht sitzend mit einfacher 3D-Projektion -----------------------
# Welt: x nach rechts (Bildschirm), y nach oben, z zum Betrachter. Die Kamera
# schaut leicht von oben (ELEV), dadurch werden Oberschenkel, die zum
# Betrachter zeigen, sichtbar verkürzt, und Drehungen um die Längsachse
# verkürzen die Schulterbreite.

ELEV = math.radians(22)


def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def v_len(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)


def v_norm(a):
    l = v_len(a) or 1e-9
    return (a[0] / l, a[1] / l, a[2] / l)


def v_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def rot_y(p, deg, about=(0.0, 0.0, 0.0)):
    """Drehung um die senkrechte Achse; +deg = Front dreht nach Bild-rechts."""
    r = math.radians(deg)
    x, y, z = v_sub(p, about)
    return v_add((x * math.cos(r) + z * math.sin(r), y, -x * math.sin(r) + z * math.cos(r)), about)


def ik3(a, t, l1, l2, pole):
    """Zwei-Knochen-IK im Raum: Gelenkpunkt (Knie/Ellbogen) zwischen a und t,
    zur Richtung `pole` hin geknickt."""
    d_vec = v_sub(t, a)
    d = max(1e-6, min(v_len(d_vec), l1 + l2 - 1e-3))
    u = v_norm(d_vec)
    along = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - along * along))
    p = v_sub(pole, v_mul(u, v_dot(pole, u)))
    p = v_norm(p)
    return v_add(v_add(a, v_mul(u, along)), v_mul(p, h))


class Proj3D(Skeleton):
    """Skeleton-Ersatz: joints(pose) -> {name: (x, y, z)}; segs = [(name, a, b)].
    fk liefert das gewohnte {seg: (sx, sy, ex, ey, winkel)} in Bildkoordinaten,
    damit limb(), head_front(), focus(), ghost() unverändert funktionieren."""

    def __init__(self, joints, segs, origin=(200.0, 190.0)):
        super().__init__([])
        self.joints = joints
        self.seglist = segs
        self.origin = origin

    def proj(self, p):
        return (self.origin[0] + p[0],
                self.origin[1] - p[1] * math.cos(ELEV) + p[2] * math.sin(ELEV))

    def fk(self, pose):
        J = self.joints(pose)
        out = {}
        for name, a, b in self.seglist:
            sx, sy = self.proj(J[a])
            ex, ey = self.proj(J[b])
            ang = math.degrees(math.atan2(-(ey - sy), ex - sx))
            out[name] = (sx, sy, ex, ey, ang)
        out["_J"] = J
        return out


def seated_joints(pose, arms):
    """Sitzende Person frontal. pose: yaw (Oberkörperdrehung, Grad), spread
    (Oberschenkel-Abspreizung je Seite, Grad), knee_z/ank (Fußposition),
    arms(J, pose) ergänzt Ellbogen/Hände."""
    yaw = pose.get("yaw", 0.0)
    J = {"root": (0.0, 0.0, 0.0)}
    J["lumbar"] = (0.0, 26.0, 0.0)
    J["thorax"] = (0.0, 52.0, 0.0)
    J["chest"] = (0.0, 78.0, 0.0)
    J["neck"] = (0.0, 95.0, 0.0)
    J["head"] = (0.0, 110.0, 0.0)
    J["clav_L"] = rot_y((-24.0, 77.0, 0.0), yaw)
    J["clav_R"] = rot_y((24.0, 77.0, 0.0), yaw)
    J["waist_L"] = rot_y((-19.0, 30.0, 0.0), yaw * 0.45)
    J["waist_R"] = rot_y((19.0, 30.0, 0.0), yaw * 0.45)
    sp = pose.get("spread", 10.0)
    for side, s in (("L", -1), ("R", 1)):
        hip = (s * 15.0, 0.0, 0.0)
        a = math.radians(sp)
        knee = v_add(hip, (s * 50 * math.sin(a), -4.0, 50 * math.cos(a)))
        ank = v_add(knee, (s * 3.0, -46.0, 8.0))
        J["hip_" + side] = hip
        J["knee_" + side] = knee
        J["ank_" + side] = ank
        J["toe_" + side] = v_add(ank, (s * 1.0, -2.0, 11.0))
    arms(J, pose)
    return J


SEATED_SEGS = [
    ("lumbar", "root", "lumbar"), ("thorax", "lumbar", "thorax"), ("chest", "thorax", "chest"),
    ("neck", "chest", "neck"), ("head", "neck", "head"),
    ("clav_L", "chest", "clav_L"), ("clav_R", "chest", "clav_R"),
    ("upperarm_L", "clav_L", "elb_L"), ("forearm_L", "elb_L", "wri_L"), ("hand_L", "wri_L", "hand_L"),
    ("upperarm_R", "clav_R", "elb_R"), ("forearm_R", "elb_R", "wri_R"), ("hand_R", "wri_R", "hand_R"),
    ("hip_L", "root", "hip_L"), ("thigh_L", "hip_L", "knee_L"), ("shin_L", "knee_L", "ank_L"),
    ("foot_L", "ank_L", "toe_L"),
    ("hip_R", "root", "hip_R"), ("thigh_R", "hip_R", "knee_R"), ("shin_R", "knee_R", "ank_R"),
    ("foot_R", "ank_R", "toe_R"),
    ("waist_L", "lumbar", "waist_L"), ("waist_R", "lumbar", "waist_R"),
]


def arm_to(J, side, hand, pole):
    """Arm von der Schulter zur Hand (3D-IK), Handgelenk auf dem Unterarm."""
    sh = J["clav_" + side]
    elb = ik3(sh, hand, 36.0, 42.0, pole)
    J["elb_" + side] = elb
    J["wri_" + side] = v_add(elb, v_mul(v_norm(v_sub(hand, elb)), 32.0))
    J["hand_" + side] = hand


def seated_front_figure(torso_w=44, extras_after_trunk=(), extras_after_arms=(), legs_front=()) -> list[Prim]:
    """Reihenfolge: Rumpf, Arme, Kopf, dann Beine (die zum Betrachter zeigen)."""
    prims: list[Prim] = []
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], torso_w, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    pelvis = lambda c: {"d": smooth_path([pt(c["P"], "hip_L"), pt(c["P"], "hip_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 33, "stroke-linecap": "round"},
                   pelvis),
              Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 30, "stroke-linecap": "round"}, pelvis),
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    prims += list(extras_after_trunk)
    prims += limb_j(["upperarm_L", "forearm_L", "hand_L"], 12, NEAR)
    prims += limb_j(["upperarm_R", "forearm_R", "hand_R"], 12, NEAR)
    prims += head_front()
    prims += list(extras_after_arms)
    for s in ("L", "R"):
        prims += limb_j(["shin_" + s, "foot_" + s], 15, NEAR)
        prims += limb(["thigh_" + s], 18, NEAR)
    prims += list(legs_front)
    return prims
