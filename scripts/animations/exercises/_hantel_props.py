"""Gemeinsame Helfer für die Kurzhantel-Übungen (@hantel-Plan).

Kurzhantel = Griff + zwei Scheiben, folgt pro Frame der Hand und ist mit dem
Unterarm ausgerichtet. Zwei Darstellungen:
* dumbbell_inplane: Griffachse liegt in der Bildebene (z. B. Hammergriff in
  der Seitansicht) – sichtbar als Griff mit zwei Scheiben.
* dumbbell_endon: Griffachse zeigt in die Tiefe (z. B. Untergriff in der
  Seitansicht) – schräg von vorn gesehen: zwei versetzte Scheiben.
"""

from __future__ import annotations

import math

from rig import (FAR, NEAR, PROP, PROP_DARK, SKIN_LINE, Prim, chain_points, limb, head_side, pt,
                 smooth_path, TORSO)

DB_EDGE = "#1e293b"
PLATE_N = "#7c8ba1"   # nahe Scheibe (heller als PROP)
PLATE_F = PROP_DARK


def grip_point(P, hand: str, k=0.55):
    """Griffpunkt in der Faust: Anteil k entlang des Hand-Segments."""
    sx, sy, ex, ey, a = P[hand]
    return sx + (ex - sx) * k, sy + (ey - sy) * k, a


def dumbbell_inplane(center_fn, axis_fn, half=12.0, plate=9.0, color=PROP, dark=PROP_DARK,
                     scale_fn=None, fist=None) -> list[Prim]:
    """center_fn(c)->(x,y), axis_fn(c)->Grad (Griffachse). scale_fn(c)->0..1
    verkürzt die Achse (perspektivisch). fist=(farbe, r) zeichnet die Faust
    über den Griff."""

    def ends(c):
        x, y = center_fn(c)
        a = math.radians(axis_fn(c))
        s = scale_fn(c) if scale_fn else 1.0
        h = max(2.5, half * s)
        ux, uy = math.cos(a), -math.sin(a)
        return x, y, ux, uy, h

    def handle(c):
        x, y, ux, uy, h = ends(c)
        return {"d": f"M{x - ux * h:.1f} {y - uy * h:.1f}L{x + ux * h:.1f} {y + uy * h:.1f}"}

    def plates(c):
        x, y, ux, uy, h = ends(c)
        nx, ny = -uy, ux
        d = ""
        for sgn in (-1, 1):
            px, py = x + sgn * ux * h, y + sgn * uy * h
            d += (f"M{px - nx * plate / 2:.1f} {py - ny * plate / 2:.1f}"
                  f"L{px + nx * plate / 2:.1f} {py + ny * plate / 2:.1f}")
        return {"d": d}

    out = [
        Prim("path", {"fill": "none", "stroke": DB_EDGE, "stroke-width": 6, "stroke-linecap": "round"}, handle),
        Prim("path", {"fill": "none", "stroke": dark, "stroke-width": 3.5, "stroke-linecap": "round"}, handle),
        Prim("path", {"fill": "none", "stroke": DB_EDGE, "stroke-width": 10, "stroke-linecap": "round"}, plates),
        Prim("path", {"fill": "none", "stroke": color, "stroke-width": 7, "stroke-linecap": "round"}, plates),
    ]
    if fist:
        col, r = fist
        out.append(Prim("circle", {"r": r, "fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5},
                        lambda c: dict(zip(("cx", "cy"), center_fn(c)))))
    return out


def _ellipse_d(x, y, rx, ry, tilt):
    """Ellipsen-Pfad (tilt in SVG-Grad, im Uhrzeigersinn)."""
    a = math.radians(tilt)
    vx, vy = -math.sin(a) * ry, math.cos(a) * ry
    return (f"M{x - vx:.1f} {y - vy:.1f}A{rx} {ry} {tilt:.0f} 1 0 {x + vx:.1f} {y + vy:.1f}"
            f"A{rx} {ry} {tilt:.0f} 1 0 {x - vx:.1f} {y - vy:.1f}Z")


def dumbbell_endon_back(center_fn, depth=(7.0, -5.0), ry=11.0, rx=5.5, tilt=-20, far_col=PLATE_F) -> list[Prim]:
    """Hinterer Teil (ferne Scheibe + Griff) einer Hantel, deren Achse in die
    Tiefe zeigt. Danach Faust zeichnen, dann dumbbell_endon_front.
    depth = Bildvektor von der Faust zur fernen Scheibe."""
    dx, dy = depth

    def handle(c):
        x, y = center_fn(c)
        return {"d": f"M{x - dx:.1f} {y - dy:.1f}L{x + dx:.1f} {y + dy:.1f}"}

    def far(c):
        x, y = center_fn(c)
        return {"d": _ellipse_d(x + dx, y + dy, rx, ry, tilt)}

    return [
        Prim("path", {"fill": far_col, "stroke": DB_EDGE, "stroke-width": 2}, far),
        Prim("path", {"fill": "none", "stroke": DB_EDGE, "stroke-width": 6, "stroke-linecap": "round"}, handle),
        Prim("path", {"fill": "none", "stroke": PROP_DARK, "stroke-width": 3.5, "stroke-linecap": "round"}, handle),
    ]


def dumbbell_endon_front(center_fn, depth=(7.0, -5.0), ry=11.0, rx=5.5, tilt=-20, near_col=PLATE_N) -> list[Prim]:
    dx, dy = depth

    def near(c):
        x, y = center_fn(c)
        return {"d": _ellipse_d(x - dx, y - dy, rx, ry, tilt)}

    return [Prim("path", {"fill": near_col, "stroke": DB_EDGE, "stroke-width": 2}, near)]


def fist_prim(center_fn, col=NEAR, r=6.5) -> Prim:
    return Prim("circle", {"r": r, "fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5},
                lambda c: dict(zip(("cx", "cy"), center_fn(c))))


def side_standing(far_arm_extra=(), near_arm_extra=(), behind=(), front=(), torso_w=30) -> list[Prim]:
    """Seitansicht wie rig.side_figure, aber mit Einschüben direkt nach dem
    fernen bzw. nahen Arm (für Hanteln in der Hand)."""
    prims: list[Prim] = list(behind)
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += list(far_arm_extra)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(near_arm_extra)
    prims += list(front)
    return prims


def seg_point(P, seg, k=0.5, side=0.0):
    """Punkt entlang eines Segments (Anteil k) plus seitlicher Versatz
    (side > 0 = links der Laufrichtung, mathematisch)."""
    sx, sy, ex, ey, a = P[seg]
    r = math.radians(a + 90)
    return sx + (ex - sx) * k + side * math.cos(r), sy + (ey - sy) * k - side * math.sin(r)


def focus_seg(seg, k=0.5, side=0.0, rx=12, ry=7, color=None, show=None, rotate=True) -> Prim:
    """Pulsierende Fokuszone entlang eines Segments, mit dem Segment gedreht."""
    from rig import ACCENT

    def f(c):
        x, y = seg_point(c["P"], seg, k, side)
        a = c["P"][seg][4]
        return {"d": _ellipse_d(x, y, ry, rx, -a if rotate else 0)}

    p = Prim("path", {"fill": color or ACCENT, "opacity": 0.35, "_pulse": True}, f)
    if show is not None:
        p.attrs["_show"] = show
    return p


def arc_d(cx, cy, r, a0, a1):
    """Kreisbogen um (cx,cy) von a0 nach a1 (mathematische Grad)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    return f"M{p0[0]:.1f} {p0[1]:.1f}A{r} {r} 0 {large} {sweep} {p1[0]:.1f} {p1[1]:.1f}"


def limb_sharp(names, width, color, outline=True):
    """Wie rig.limb, aber als Polylinie (Knie/Ellbogen nicht verrundet) –
    sinnvoll bei stark gebeugten Gelenken (Sitzen)."""
    def d(c, n=names):
        pts = chain_points(c["P"], n)
        return {"d": "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, d))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}, d))
    return out
