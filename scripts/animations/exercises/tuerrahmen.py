from rig import *

SLUG = "tuerrahmen-dehnung"

# Seitansicht (Blick nach rechts) + kleine Draufsicht links oben.
# Der nahe Arm liegt mit dem Unterarm senkrecht am Türrahmen. Weil der
# Oberarm dabei zur Seite (zum Betrachter) zeigt, wird er hier aus einem
# kleinen 3D-Modell projiziert: Ellbogen E bleibt fix am Rahmen, die
# Schulter wandert mit dem Körper nach vorn -> Oberarm zeigt nach hinten.

FLOOR_Y = 248
ANK_FRONT = (200, 240)
ANK_BACK = (128, 240)
ELBOW = (157.0, 76.0)          # fix am Rahmen (Schulterhöhe in der Startpose)
POST_X = ELBOW[0] + 6          # Vorderkante des Unterarms liegt an der Rahmen-Rückseite
POST_W = 14
UA, FA, HA = 36.0, 32.0, 13.0  # Oberarm, Unterarm, Hand
HALF_SH = 20.0                 # halbe Schulterbreite (Draufsicht)
EDGE_Z = 50.0                  # Türöffnung: halbe Breite (Draufsicht)

START = dict(x=165, y=152, upperarm_f=4, forearm_f=6, neck=2, head=-2)
LEAN = dict(x=173, y=155, rot=-6, upperarm_f=12, forearm_f=8, neck=6, head=4)
LEAN_IN = dict(LEAN, x=175)  # in der Haltephase minimal tiefer


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="start"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": "500",
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def shoulder(c):
    return pt(c["P"], "chest")


def elbow_z(c):
    """Seitliche Tiefe (z) der nahen Schulter so, dass |S-E| = Oberarmlänge."""
    sx, sy = shoulder(c)
    dx, dy = ELBOW[0] - sx, ELBOW[1] - sy
    dz = math.sqrt(max(0.0, UA * UA - dx * dx - dy * dy))
    return dz


def stroke(fn, width, color, outline=True, **extra):
    """Dicker runder Strich entlang fn(c) -> Punktliste (mit Umriss)."""
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"},
                        lambda c: {"d": smooth_path(fn(c))}))
    attrs = {"fill": "none", "stroke": color, "stroke-width": width,
             "stroke-linecap": "round", "stroke-linejoin": "round"}
    attrs.update(extra)
    out.append(Prim("path", attrs, lambda c: {"d": smooth_path(fn(c))}))
    return out


def near_arm():
    ex, ey = ELBOW
    hand = (ex, ey - FA)
    tip = (ex, ey - FA - HA + 2)
    upper = stroke(lambda c: [shoulder(c), ELBOW], 12, NEAR)
    fore = stroke(lambda c: [ELBOW, hand], 12, NEAR)
    palm = stroke(lambda c: [hand, tip], 10, NEAR)
    return fore + palm + upper


def door():
    """Türrahmen-Pfosten (hinter der Figur) mit angedeuteter Wand."""
    top = 34
    return [
        Prim("rect", {"x": POST_X, "y": top, "width": POST_W, "height": FLOOR_Y - top,
                      "fill": PROP_DARK}),
        Prim("rect", {"x": POST_X + POST_W - 4, "y": top, "width": 4, "height": FLOOR_Y - top,
                      "fill": PROP, "opacity": 0.8}),
        Prim("rect", {"x": POST_X - 3, "y": top - 6, "width": POST_W + 6, "height": 8, "rx": 2,
                      "fill": PROP}),
    ]


def figure():
    prims = []
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += near_arm()
    return prims


# --- Draufsicht --------------------------------------------------------------

IN_X, IN_Y, IN_W, IN_H = 14, 40, 108, 104
K = 1.0


def top_xy(x_fwd, z):
    # vorwärts (x) = nach oben, z (seitlich, Rahmen-Seite) = nach rechts
    return IN_X + 34 + z * K, IN_Y + 74 - (x_fwd - 160) * K


def top_view():
    wall_y0 = top_xy(POST_X + POST_W, 0)[1]
    wall_y1 = top_xy(POST_X, 0)[1]
    edge_x = top_xy(0, EDGE_Z)[0]
    left_edge = top_xy(0, -EDGE_Z)[0]

    def body_c(c):
        sx, _ = shoulder(c)
        zc = EDGE_Z + 6 - elbow_z(c) - HALF_SH  # Körpermitte (z)
        return sx, zc

    def sh_line(c):
        sx, zc = body_c(c)
        return [top_xy(sx, zc - HALF_SH), top_xy(sx, zc + HALF_SH)]

    def uarm(c):
        sx, zc = body_c(c)
        return [top_xy(sx, zc + HALF_SH), top_xy(ELBOW[0], EDGE_Z + 6)]

    def head(c):
        sx, zc = body_c(c)
        x, y = top_xy(sx + 3, zc)
        return {"cx": x, "cy": y}

    def chest_focus(c):
        sx, zc = body_c(c)
        x, y = top_xy(sx + 9, zc + HALF_SH * 0.55)
        return {"cx": x, "cy": y}

    def far_hand(c):
        sx, zc = body_c(c)
        x, y = top_xy(sx + 2, zc - HALF_SH - 2)
        return {"cx": x, "cy": y}

    ex, ey = top_xy(ELBOW[0], EDGE_Z + 6)
    inner = [
        Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "rx": 8, "fill": "#0b1220",
                      "opacity": 0.7}),
        # Wand mit Türöffnung
        Prim("rect", {"x": edge_x, "y": wall_y0, "width": IN_X + IN_W - edge_x, "height": wall_y1 - wall_y0,
                      "fill": PROP_DARK}),
        Prim("rect", {"x": IN_X, "y": wall_y0, "width": left_edge - IN_X, "height": wall_y1 - wall_y0,
                      "fill": PROP_DARK}) if left_edge > IN_X else None,
        Prim("circle", {"r": 4, "fill": FAR}, far_hand),
        *stroke(sh_line, 11, TORSO),
        Prim("ellipse", {"rx": 9, "ry": 6, "fill": GOOD, "opacity": 0.35, "_pulse": True,
                         "_show": [(2.2, 7.6)]}, chest_focus),
        *stroke(uarm, 8, NEAR),
        Prim("circle", {"r": 6, "fill": NEAR, "stroke": SKIN_LINE, "stroke-width": 1.5, "cx": ex, "cy": ey}),
        Prim("circle", {"r": 8, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, head),
        static_text("von oben", IN_X + IN_W / 2, IN_Y + IN_H - 6, 10, MUTED),
    ]
    g = Prim("g", {"clip-path": "url(#clipTop)"}, children=[p for p in inner if p is not None])
    return [g]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_FRONT, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_BACK, bend=1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, START), (1.4, START), (3.4, LEAN), (5.2, LEAN_IN), (7.0, LEAN),
                   (7.6, LEAN), (9.2, START), (9.6, START)],
                  iks=iks, skeleton=SIDE)

    torso_ghost = ghost(limb(["lumbar", "thorax"], 30, TORSO) + limb(["thorax", "chest"], 26, TORSO, False)
                        + limb(["neck"], 13, TORSO) + head_side(), SIDE, tl.at(0), 0.16)

    chest = focus("chest", rx=11, ry=14, offset=(13, 6), color=GOOD, show=[(2.6, 7.6)])
    scene = group([floor(FLOOR_Y, 40, 360), *door(), torso_ghost, *figure(), chest,
                   arrow("M150 120 L176 120", show=[(1.4, 3.2)]),
                   ], scale=0.92, origin=(200, FLOOR_Y))

    prims = [
        scene,
        *top_view(),
        caption_band(),
        caption("Unterarm senkrecht an den Rahmen, Ellbogen 90°", 0, 1.4, size=14),
        caption("Mit dem Körper langsam vorlehnen", 1.4, 3.4),
        caption("Brust zieht – 30 s ruhig atmen", 3.4, 7.6),
        caption("Langsam zurück", 7.6, 9.6),
        label("Schulter bleibt unten", 236, 70, 3.4, 7.6),
        static_text("Kribbeln im Arm? Spannung sofort lösen", 258, 24, 12, MUTED),
    ]
    return render(prims, tl, SIDE, title="Brustdehnung im Türrahmen", fps=12,
                  extra_defs=f'<clipPath id="clipTop"><rect x="{IN_X}" y="{IN_Y}" width="{IN_W}" height="{IN_H}" rx="8"/></clipPath>')
