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
