"""Gemeinsame Helfer für die @cardio-Übungen (situps, beine_hoch, bauch_beine_po,
kniebeugen, knie_schritt, sessel_step_up). Unterstrich: build.py lädt das nicht
als Übung."""
from __future__ import annotations

import math

from rig import (IK, PROP, PROP_DARK, SIDE, Prim, Timeline, solve_ik, W)

ANKLE_UP = 8      # Knöchel liegt so weit über dem Boden (halbe Fußbreite)
LEG = 98          # Oberschenkel + Unterschenkel


class PostTimeline(Timeline):
    """Timeline mit eigener Nachbearbeitung pro Frame: post(pose) -> pose.
    Damit lassen sich IK-Ziele und Fußwinkel aus Pose-Skalaren ableiten."""

    def __init__(self, keys, post, skeleton=SIDE):
        super().__init__(keys, iks=[], skeleton=skeleton)
        self.post = post

    def at(self, t):
        return self.post(super().at(t))


def bez(p0, p1, p2, p3, s):
    s = max(0.0, min(1.0, s))
    m = 1 - s
    return (m ** 3 * p0[0] + 3 * m * m * s * p1[0] + 3 * m * s * s * p2[0] + s ** 3 * p3[0],
            m ** 3 * p0[1] + 3 * m * m * s * p1[1] + 3 * m * s * s * p2[1] + s ** 3 * p3[1])


def lerp(a, b, u):
    return a + (b - a) * u


def leg(pose, side, ankle, foot_abs=0.0, bend=1):
    """Knöchel von Bein side ('n'/'f') auf ankle, Fuß mit absolutem Winkel."""
    return solve_ik(SIDE, pose, IK(f"thigh_{side}", f"shin_{side}", ankle, bend=bend,
                                   end_seg=f"foot_{side}", end_abs=foot_abs))


def ankle_for_toe(toe, foot_abs):
    """Knöchelposition, wenn die Zehenspitze auf toe bleiben soll (Ferse hebt)."""
    a = math.radians(foot_abs)
    return (toe[0] - 20 * math.cos(a), toe[1] + 20 * math.sin(a))


def arms_level(pose, abs_deg=0.0, elbow=4.0):
    """Arme nach vorn: Oberarm zeigt absolut auf abs_deg (0 = waagrecht nach vorn).
    Berücksichtigt rot und Wirbelsäulenwinkel."""
    spine = pose.get("rot", 0) + pose.get("lumbar", 0) + pose.get("thorax", 0) + pose.get("chest", 0)
    out = dict(pose)
    for s in ("n", "f"):
        out[f"upperarm_{s}"] = abs_deg - (90 + spine + 180) + (-3 if s == "f" else 0)
        out[f"forearm_{s}"] = elbow
        out[f"hand_{s}"] = 0
    return out


def label(text, x, y, t0, t1, size=12, color="#fbbf24", anchor="middle", weight="500"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": weight,
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def chair(x0, floor_y, seat_h=56, depth=62, back_h=62, back_side="right"):
    """Küchenstuhl in Seitansicht, flach. x0 = linke Sitzkante."""
    seat_y = floor_y - seat_h
    bx = x0 + depth - 7 if back_side == "right" else x0 + 1
    return [
        # ferne Beine (dunkler, leicht versetzt)
        Prim("rect", {"x": x0 + 8, "y": seat_y + 4, "width": 6, "height": seat_h - 4, "rx": 2, "fill": PROP_DARK}),
        Prim("rect", {"x": x0 + depth - 12, "y": seat_y + 4, "width": 6, "height": seat_h - 4, "rx": 2,
                      "fill": PROP_DARK}),
        # Lehne
        Prim("rect", {"x": bx, "y": seat_y - back_h, "width": 7, "height": back_h + 4, "rx": 3, "fill": PROP}),
        Prim("rect", {"x": bx - (2 if back_side == "right" else 0) - 3, "y": seat_y - back_h - 2, "width": 13,
                      "height": 9, "rx": 4, "fill": PROP}),
        Prim("rect", {"x": bx, "y": seat_y - back_h * 0.55, "width": 7, "height": 6, "rx": 2, "fill": PROP_DARK}),
        # nahe Beine
        Prim("rect", {"x": x0 + 3, "y": seat_y + 4, "width": 7, "height": seat_h - 4, "rx": 2, "fill": PROP}),
        Prim("rect", {"x": x0 + depth - 10, "y": seat_y + 4, "width": 7, "height": seat_h - 4, "rx": 2, "fill": PROP}),
        Prim("rect", {"x": x0 + 6, "y": seat_y + 26, "width": depth - 12, "height": 4, "rx": 2, "fill": PROP_DARK}),
        # Sitz
        Prim("rect", {"x": x0 - 2, "y": seat_y - 3, "width": depth + 4, "height": 9, "rx": 4, "fill": PROP}),
        Prim("rect", {"x": x0 - 2, "y": seat_y + 3, "width": depth + 4, "height": 3, "rx": 1.5, "fill": PROP_DARK}),
    ]


def scene_group(children, scale, floor_y, cx=W / 2, dx=0.0):
    """Gruppe um den Bodenpunkt skalieren (Figur bleibt auf dem Boden)."""
    ox, oy = cx, floor_y
    tf = f"translate({ox + dx:.1f} {oy:.1f}) scale({scale:.3f}) translate({-ox:.1f} {-oy:.1f})"
    return Prim("g", {"transform": tf}, children=children)


def figure(extras_behind=(), extras_front=(), torso_w=30, mid=()):
    """Wie rig.side_figure, aber Füße als eigene Striche (deutlich sichtbarer
    Fuß mit Ferse) und optionale Prims zwischen fernen und nahen Gliedern."""
    from rig import FAR, NEAR, TORSO, head_side, limb
    prims = list(extras_behind)
    prims += limb(["thigh_f", "shin_f"], 15, FAR)
    prims += limb(["foot_f"], 12, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += list(mid)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    prims += head_side()
    prims += limb(["thigh_n", "shin_n"], 16, NEAR)
    prims += limb(["foot_n"], 13, NEAR)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(extras_front)
    return prims


def focus_mid(seg, u=0.5, rx=18, ry=9, offset=(0, 0), color="#fbbf24", show=None):
    """Pulsierende Fokuszone an einem Punkt entlang eines Segments, gedreht."""
    def f(c):
        sx, sy, ex, ey, a = c["P"][seg]
        x = sx + (ex - sx) * u + offset[0]
        y = sy + (ey - sy) * u + offset[1]
        r = math.radians(a)
        x1, y1 = x + rx * math.cos(r), y - rx * math.sin(r)
        x2, y2 = x - rx * math.cos(r), y + rx * math.sin(r)
        return {"d": f"M{x1:.1f} {y1:.1f}A{rx} {ry} {-a:.0f} 1 0 {x2:.1f} {y2:.1f}"
                     f"A{rx} {ry} {-a:.0f} 1 0 {x1:.1f} {y1:.1f}Z"}
    p = Prim("path", {"fill": color, "opacity": 0.35, "_pulse": True}, f)
    if show is not None:
        p.attrs["_show"] = show
    return p
