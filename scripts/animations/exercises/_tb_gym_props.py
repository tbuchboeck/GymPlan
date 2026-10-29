"""Gemeinsame Helfer für Geräteübungen (Rudern, Pressen) und Gehen.

Arme werden hier selbst gerechnet (2-Knochen-IK in der Bildebene mit
optional verkürztem Oberarm), weil die Oberarme bei Rudern/Pressen oft
seitlich aus der Bildebene zeigen. Die Pose trägt dann Schulter-, Ellbogen-
und Handpunkte (sx/sy, ex/ey, wx/wy und *_f für die ferne Seite).
"""
from rig import *

UA, FA = 36.0, 32.0


# --------------------------------------------------------------------------
# Geometrie
# --------------------------------------------------------------------------

def ik2(s, w, l1, l2, bend=1):
    """Ellbogen für Schulter s, Handgelenk w (SVG-Koordinaten).
    bend=+1: Ellbogen links der Linie s->w (im mathematischen Sinn)."""
    dx, dy = w[0] - s[0], -(w[1] - s[1])
    d = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
    base = math.atan2(dy, dx)
    ca = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    a = math.acos(max(-1.0, min(1.0, ca)))
    ang = base + bend * a
    return (s[0] + l1 * math.cos(ang), s[1] - l1 * math.sin(ang))


def clamp_reach(s, w, reach):
    dx, dy = w[0] - s[0], w[1] - s[1]
    d = math.hypot(dx, dy)
    if d <= reach:
        return w
    return (s[0] + dx / d * reach, s[1] + dy / d * reach)


def axes(P, seg="chest"):
    """Einheitsvektoren (up, fwd) eines Segments in SVG-Koordinaten."""
    a = math.radians(P[seg][4])
    up = (math.cos(a), -math.sin(a))
    fwd = (math.cos(a - math.pi / 2), -math.sin(a - math.pi / 2))
    return up, fwd


def body_pt(P, seg, along, fwd_off, end=True):
    """Punkt relativ zu einem Segment: along entlang (ab Ende/Start),
    fwd_off nach vorn (+) bzw. hinten (-)."""
    x, y = pt(P, seg, end)
    up, fw = axes(P, seg)
    return (x + along * up[0] + fwd_off * fw[0], y + along * up[1] + fwd_off * fw[1])


def shoulder_side(P, scap=0.0):
    """Schultergelenk in Seitansicht, wandert bei Retraktion nach hinten."""
    return body_pt(P, "chest", -6 - 1.0 * scap, -1 - 4.0 * scap)


class PostTimeline(Timeline):
    """Timeline, die nach IK pro Frame eine Funktion post(pose, P) aufruft,
    deren Ergebnis (dict) in die Pose übernommen wird."""

    def __init__(self, keys, iks=None, skeleton=None, post=None):
        super().__init__(keys, iks or [], skeleton)
        self.post = post

    def at(self, t):
        pose = super().at(t)
        if self.post:
            pose.update(self.post(pose, self.skeleton.fk(pose)))
        return pose


# --------------------------------------------------------------------------
# Figur-Bausteine
# --------------------------------------------------------------------------

def _stroke(fn, w, col, outline=True):
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, fn))
    out.append(Prim("path", {"fill": "none", "stroke": col, "stroke-width": w,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}, fn))
    return out


def arm_prims(suffix="", far=False, w=None, fist_r=None):
    """Arm aus pose-Punkten s{suffix}, e{suffix}, w{suffix}."""
    w = w or (11 if far else 12)
    col = FAR if far else NEAR
    k = suffix

    def d(c):
        p = c["pose"]
        s, e, h = (p["sx" + k], p["sy" + k]), (p["ex" + k], p["ey" + k]), (p["wx" + k], p["wy" + k])
        return {"d": smooth_path([s, e, e, h])}

    def fist(c):
        p = c["pose"]
        return {"cx": p["wx" + k], "cy": p["wy" + k]}

    r = fist_r or (w / 2 + 1.5)
    return _stroke(d, w, col) + [
        Prim("circle", {"r": r, "fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5}, fist)]


def grip_line(get_pts, w=6, col=PROP, dark="#0b1220"):
    """Griffstange: get_pts(c) -> (x1, y1, x2, y2)."""
    def f(c):
        x1, y1, x2, y2 = get_pts(c)
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    return [Prim("line", {"stroke": dark, "stroke-width": w + 3, "stroke-linecap": "round"}, f),
            Prim("line", {"stroke": col, "stroke-width": w, "stroke-linecap": "round"}, f)]


def scapula(key="scap", seg="thorax"):
    """Schulterblatt auf dem oberen Rücken, rutscht bei Retraktion nach
    hinten-unten (sichtbare Zusatzinfo, sehr dezent)."""
    def f(c):
        P = c["P"]
        s = c["pose"].get(key, 0.0)
        pts = [body_pt(P, seg, 20 - 4 * s + da, -(dp + 2.5 * s)) for da, dp in
               ((5, 1), (-17, 5), (3, 13))]
        (ax, ay), (bx, by), (cx, cy) = pts
        return {"d": f"M{ax:.1f} {ay:.1f}Q{(ax + bx) / 2 - 1:.1f} {(ay + by) / 2:.1f} {bx:.1f} {by:.1f}"
                     f"Q{(bx + cx) / 2:.1f} {(by + cy) / 2:.1f} {cx:.1f} {cy:.1f}Z"}
    return Prim("path", {"fill": HEAD, "opacity": 0.5, "stroke": SKIN_LINE, "stroke-width": 1.2,
                         "stroke-linejoin": "round"}, f)


def side_body(head=True, torso_w=30, far_leg=True, near_leg=True):
    """Rumpf/Kopf/Beine in Seitansicht (ohne Arme), in Reihenfolge:
    returns (far_leg, torso_and_head, near_leg)."""
    far = limb(["thigh_f", "shin_f", "foot_f"], 15, FAR) if far_leg else []
    mid = limb(["neck"], 13, TORSO) + limb(["lumbar", "thorax"], torso_w, TORSO) + \
        limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    if head:
        mid += head_side()
    near = limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR) if near_leg else []
    return far, mid, near


# --------------------------------------------------------------------------
# Geräte
# --------------------------------------------------------------------------

def R(x, y, w, h, fill=PROP, rx=3, **kw):
    a = {"x": x, "y": y, "width": w, "height": h, "rx": rx, "fill": fill}
    a.update(kw)
    return Prim("rect", a)


def L(x1, y1, x2, y2, col=PROP_DARK, w=6, **kw):
    a = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": col, "stroke-width": w, "stroke-linecap": "round"}
    a.update(kw)
    return Prim("line", a)


def C(cx, cy, r, fill=PROP, **kw):
    a = {"cx": cx, "cy": cy, "r": r, "fill": fill}
    a.update(kw)
    return Prim("circle", a)


def pulley(cx, cy, r=7):
    return [C(cx, cy, r + 2, PROP_DARK), C(cx, cy, r, PROP), C(cx, cy, 2.2, PROP_DARK)]


def weight_stack(x, floor_y, top_y, lift, n=10, w=36, label=True, moving=4):
    """Gewichtsblock: Rahmen, Führungsstangen, Platten. lift(c) -> px nach
    oben für die obersten `moving` Platten (der Rest bleibt liegen)."""
    ph, gap = 8.0, 2.0
    out = [
        R(x - 6, top_y, 6, floor_y - top_y, PROP_DARK, rx=2),
        R(x + w, top_y, 6, floor_y - top_y, PROP_DARK, rx=2),
        R(x - 10, floor_y - 6, w + 20, 6, PROP_DARK, rx=2),
        L(x + 8, top_y + 4, x + 8, floor_y - 6, "#3b4658", 2),
        L(x + w - 8, top_y + 4, x + w - 8, floor_y - 6, "#3b4658", 2),
    ]
    y_bottom = floor_y - 6
    for i in range(n):
        y = y_bottom - (i + 1) * (ph + gap) + gap
        idx_from_top = n - 1 - i
        col = "#7c8aa0" if idx_from_top < moving else PROP
        p = R(x + 1, y, w - 2, ph, col, rx=2)
        if idx_from_top < moving:
            p.dyn = (lambda c, y=y: {"y": y - lift(c)})
        out.append(p)
    top_plate_y = y_bottom - n * (ph + gap) + gap
    # Hubstange über dem Block
    rod = Prim("line", {"x1": x + w / 2, "x2": x + w / 2, "stroke": "#9aa6b8", "stroke-width": 3,
                        "stroke-linecap": "round"},
               lambda c: {"y1": top_y + 14 - lift(c) * 0.0, "y2": top_plate_y - lift(c) + 1})
    out.insert(5, rod)
    # Steckstift an der untersten bewegten Platte
    pin_y = top_plate_y + (moving - 1) * (ph + gap) + ph / 2
    out.append(Prim("circle", {"cx": x + w + 1, "r": 2.6, "fill": ACCENT, "opacity": 0.85},
                    lambda c: {"cy": pin_y - lift(c)}))
    return out, top_plate_y


def floor_and_shadow(y, x0=20, x1=380):
    return [floor(y, x0, x1)]
