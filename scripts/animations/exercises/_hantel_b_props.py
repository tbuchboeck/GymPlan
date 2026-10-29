"""Gemeinsame Helfer für die Hantel-Übungen (bizeps_ueber_kopf, kreuzheben,
butterfly_reverse, seitheben_frontheben, butterfly_boden, situps_hantel).

Kurzhantel = Griff + zwei Scheiben. Sie sitzt in der Faust (Griffpunkt auf dem
Hand-Segment) und ist quer zum Unterarm ausgerichtet (Winkel = Unterarm + 90°).
`fore` (0..1) verkürzt den Griff perspektivisch (1 = Griff liegt in der
Bildebene, 0 = Blick genau auf die Stirnseite), die Scheiben werden dabei
dicker gezeichnet, damit die Hantel lesbar bleibt.
"""

from __future__ import annotations

import math

from rig import (SIDE, FRONT, Prim, limb, head_side, head_front, pt, smooth_path, chain_points,
                 NEAR, FAR, TORSO, HEAD, SKIN_LINE, PROP, PROP_DARK, MUTED, ACCENT)

PLATE = PROP
PLATE_EDGE = "#1e293b"
PLATE_FAR = PROP_DARK
HANDLE = "#94a3b8"


def grip_point(P, hand: str, frac=0.45):
    x0, y0, x1, y1, a = P[hand]
    return x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac


def _quad(cx, cy, ux, uy, a, b):
    """Rechteck um (cx, cy): b halbe Tiefe entlang u, a halbe Breite quer."""
    px, py = -uy, ux
    pts = [(cx + ux * b + px * a, cy + uy * b + py * a), (cx + ux * b - px * a, cy + uy * b - py * a),
           (cx - ux * b - px * a, cy - uy * b - py * a), (cx - ux * b + px * a, cy - uy * b + py * a)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def dumbbell_geom(cx, cy, ang, fore=1.0, size=1.0):
    """Liefert d-Strings (plate_a, handle, plate_b) für eine Hantel mit Achse
    `ang` (Grad, mathematisch) durch (cx, cy)."""
    ux, uy = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
    hl = (12.5 * fore + 3.0) * size            # halbe Griff-Länge bis Scheibenmitte
    a = 9.5 * size                             # halbe Scheibenhöhe
    b = (3.0 + 4.5 * (1 - fore)) * size        # halbe Scheibendicke
    pa = _quad(cx + ux * hl, cy + uy * hl, ux, uy, a, b)
    pb = _quad(cx - ux * hl, cy - uy * hl, ux, uy, a, b)
    h = f"M{cx + ux * hl:.1f} {cy + uy * hl:.1f}L{cx - ux * hl:.1f} {cy - uy * hl:.1f}"
    return pa, h, pb


def dumbbell(hand: str, forearm: str, far=False, fore=1.0, size=1.0, off=90.0, frac=0.45,
             fist=True, fist_color=None, pose_fore: str | None = None, center_fn=None, ang_fn=None):
    """Prims für eine Kurzhantel in der Hand `hand`.
    off: Winkel der Griffachse relativ zum Unterarm (90 = quer).
    pose_fore: optionaler Pose-Skalar, der `fore` pro Frame setzt.
    center_fn/ang_fn: optional eigener Griffpunkt / eigene Achse (ctx -> ...)."""
    plate_col = PLATE_FAR if far else PLATE
    fist_col = fist_color or (FAR if far else NEAR)

    def geo(c):
        P = c["P"]
        cx, cy = center_fn(c) if center_fn else grip_point(P, hand, frac)
        ang = ang_fn(c) if ang_fn else P[forearm][4] + off
        f = c["pose"].get(pose_fore, fore) if pose_fore else fore
        return dumbbell_geom(cx, cy, ang, f, size), (cx, cy)

    def plate(i):
        return lambda c: {"d": geo(c)[0][i]}

    prims = [
        Prim("path", {"fill": "none", "stroke": PLATE_EDGE, "stroke-width": 6.5 * size, "stroke-linecap": "round"},
             lambda c: {"d": geo(c)[0][1]}),
        Prim("path", {"fill": "none", "stroke": HANDLE if not far else PROP, "stroke-width": 3.5 * size,
                      "stroke-linecap": "round"}, lambda c: {"d": geo(c)[0][1]}),
        Prim("path", {"fill": plate_col, "stroke": PLATE_EDGE, "stroke-width": 2.2, "stroke-linejoin": "round"},
             plate(0)),
        Prim("path", {"fill": plate_col, "stroke": PLATE_EDGE, "stroke-width": 2.2, "stroke-linejoin": "round"},
             plate(2)),
    ]
    if fist:
        prims.append(Prim("circle", {"r": 6.2 * size, "fill": fist_col, "stroke": SKIN_LINE, "stroke-width": 1.5},
                          lambda c: (lambda p: {"cx": p[0], "cy": p[1]})(geo(c)[1])))
    return prims


def side_fig(db_far=(), db_near=(), torso_w=30, behind=(), front=(), head=True, between=()):
    """Wie rig.side_figure, aber mit Einschubstellen für Hanteln:
    db_far direkt nach dem fernen Arm, db_near nach dem nahen Arm.
    between: nach dem Rumpf/Kopf, vor den nahen Gliedmaßen."""
    prims: list[Prim] = list(behind)
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += list(db_far)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    if head:
        prims += head_side()
    prims += list(between)
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    prims += list(db_near)
    prims += list(front)
    return prims


def front_fig(db_L=(), db_R=(), torso_w=44, behind=(), front=(), head=True, legs=True, head_fn=None):
    prims: list[Prim] = list(behind)
    if legs:
        prims += limb(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR)
        prims += limb(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, NEAR)
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], torso_w, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    if head:
        prims += (head_fn() if head_fn else head_front())
    prims += limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR)
    prims += list(db_L)
    prims += limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR)
    prims += list(db_R)
    prims += list(front)
    return prims


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="middle", weight="500"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": weight,
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def shoe(foot: str, color, w=10):
    """Etwas kräftigerer Fuß (flach auf dem Boden)."""
    return limb([foot], w, color)
