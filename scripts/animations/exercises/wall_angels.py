from rig import *

SLUG = "wall-angels"

# Frontansicht vor der Wand + kleine Seitansicht rechts (Kontakt Kopf/Rücken/Gesäß).
# FRONT-Winkel: upperarm_L abs = 270 + rel, upperarm_R abs = -90 + rel.

FLOOR_Y = 250
SC = 0.8                       # Hauptfigur skaliert um (CX, FLOOR_Y)
CX = 160

BASE = dict(x=CX, y=FLOOR_Y - 107, hip_L=0, hip_R=0, thigh_L=-4, thigh_R=4, shin_L=2, shin_R=-2)


def arms(ua, fa, clav=0.0):
    """ua = Abduktion des Oberarms aus der Hängeposition (Grad), fa = Winkel
    Unterarm relativ zum Oberarm (positiv = nach oben/innen geknickt).
    clav > 0 hebt die Schultern, < 0 senkt sie."""
    return dict(upperarm_L=-ua + clav, forearm_L=-fa, upperarm_R=ua - clav, forearm_R=fa,
                clav_L=-clav, clav_R=clav)


U = dict(BASE, **arms(90, 90))                 # U-Form: Ellbogen auf Schulterhöhe
UP = dict(BASE, **arms(150, 20, clav=5))       # hochgleiten
W_ = dict(BASE, **arms(50, 102, clav=-6))      # Ellbogen zu den Rippen, Schulterblätter runter

# Seitansicht-Inset
IN_X, IN_Y, IN_W, IN_H = 290, 42, 98, 168
WALL_X = 318                   # Wandlinie im Inset (Bildschirm)
SIDE_POSE = dict(x=0, y=0, rot=2, neck=-2, head=0, thigh_n=6, thigh_f=4, shin_n=0, shin_f=0,
                 foot_n=-6, foot_f=-4)
IS = 0.6                      # Inset-Maßstab


def stroke(fn, width, color, outline=True):
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"},
                        lambda c: {"d": smooth_path(fn(c))}))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"},
                    lambda c: {"d": smooth_path(fn(c))}))
    return out


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="middle"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": "500",
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def wall_bg():
    return [
        Prim("rect", {"x": 8, "y": 36, "width": 384, "height": FLOOR_Y - 36 + 1, "rx": 6, "fill": "#273449"}),
        Prim("rect", {"x": 8, "y": FLOOR_Y - 8, "width": 384, "height": 9, "fill": PROP_DARK}),
        floor(FLOOR_Y + 1, 8, 392),
    ]


def side_inset():
    """Seitansicht: Figur lehnt an der Wand. Der nahe Arm wird aus der
    Frontpose projiziert (nur die senkrechte Komponente bleibt sichtbar)."""
    P0 = SIDE.fk(SIDE_POSE)
    # Figur so platzieren, dass Gesäß/Rücken die Wand berühren
    feet_y = P0["foot_n"][3]
    ox = WALL_X + 9  # Becken-Mitte knapp vor der Wand
    base_y = IN_Y + IN_H - 10

    def to_inset(x, y):
        return ox + (x - 0) * IS, base_y + (y - feet_y) * IS

    pose = dict(SIDE_POSE)
    P = SIDE.fk(pose)

    def tp(name, end=True):
        return to_inset(*pt(P, name, end))

    def poly(names):
        return [to_inset(*p) for p in chain_points(P, names)]

    def st(pts, w, col, outline=True):
        d = smooth_path(pts)
        out = []
        if outline:
            out.append(Prim("path", {"d": d, "fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 2,
                                     "stroke-linecap": "round", "stroke-linejoin": "round"}))
        out.append(Prim("path", {"d": d, "fill": "none", "stroke": col, "stroke-width": w,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}))
        return out

    hx, hy = tp("head")
    sh = tp("chest")
    # Arm-Projektion aus der Front-Pose (linker Bildschirmarm)
    def arm_pts(c):
        Pf = c["P"]
        s = pt(Pf, "clav_L")
        e = pt(Pf, "upperarm_L")
        h = pt(Pf, "forearm_L")
        f = pt(Pf, "hand_L")
        bx = WALL_X + 5
        return [(bx, sh[1] + (s[1] - s[1]) * IS), (bx, sh[1] + (e[1] - s[1]) * IS),
                (bx, sh[1] + (h[1] - s[1]) * IS), (bx, sh[1] + (f[1] - s[1]) * IS)]

    prims = [
        Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "rx": 8, "fill": "#0b1220",
                      "opacity": 0.75}),
        Prim("rect", {"x": IN_X + 6, "y": IN_Y + 8, "width": WALL_X - IN_X - 6, "height": IN_H - 16,
                      "fill": "#273449"}),
        Prim("line", {"x1": WALL_X, "y1": IN_Y + 8, "x2": WALL_X, "y2": base_y + 2, "stroke": PROP,
                      "stroke-width": 2}),
        Prim("line", {"x1": IN_X + 6, "y1": base_y + 2, "x2": IN_X + IN_W - 6, "y2": base_y + 2,
                      "stroke": FLOOR, "stroke-width": 2}),
    ]
    prims += st(poly(["thigh_f", "shin_f", "foot_f"]), 8, FAR)
    prims += st(poly(["neck"]), 7, TORSO)
    prims += st(poly(["lumbar", "thorax", "chest"]), 15, TORSO)
    prims += [Prim("circle", {"cx": hx, "cy": hy, "r": 9.5, "fill": HEAD, "stroke": SKIN_LINE,
                              "stroke-width": 1.5}),
              Prim("circle", {"cx": hx + 4.5, "cy": hy - 1, "r": 1.3, "fill": SKIN_LINE})]
    prims += st(poly(["thigh_n", "shin_n", "foot_n"]), 8, NEAR)
    prims += stroke(arm_pts, 6, NEAR)
    # Kontaktpunkte an der Wand
    for yy in (hy, sh[1] + 12, to_inset(*pt(P, "root", False))[1]):
        prims.append(Prim("circle", {"cx": WALL_X, "cy": yy, "r": 3, "fill": GOOD}))
    prims.append(Prim("ellipse", {"cx": WALL_X + 7, "cy": sh[1] + 16, "rx": 6, "ry": 11, "fill": ACCENT,
                                  "opacity": 0.5, "_pulse": True, "_show": [(3.8, 7.4)]}))
    prims.append(static_text("Kopf · Rücken · Po", IN_X + IN_W / 2, IN_Y + IN_H + 13, 10, GOOD))
    prims.append(static_text("an der Wand", IN_X + IN_W / 2, IN_Y + IN_H + 25, 10, GOOD))
    return prims


def build():
    tl = Timeline([(0, U), (1.0, U), (3.0, UP), (3.8, UP), (5.8, W_), (7.4, W_), (8.8, U), (9.2, U)],
                  skeleton=FRONT)

    fig = front_figure()
    ghost_u = ghost(limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR)
                    + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR), FRONT, U, 0.16)
    # Schulterblätter runter: kleine Pfeile neben dem Hals
    sh_arrows = [arrow(f"M{x} 40 L{x} 54", width=2.5, show=[(5.8, 7.4)]) for x in (CX - 30, CX + 30)]
    main = group([ghost_u, *fig,
                  arrow(f"M{CX - 96} 92 Q{CX - 104} 60 {CX - 92} 30", show=[(1.0, 3.0)]),
                  arrow(f"M{CX + 96} 92 Q{CX + 104} 60 {CX + 92} 30", show=[(1.0, 3.0)]),
                  arrow(f"M{CX - 104} 40 Q{CX - 110} 90 {CX - 86} 128", show=[(3.8, 5.8)]),
                  arrow(f"M{CX + 104} 40 Q{CX + 110} 90 {CX + 86} 128", show=[(3.8, 5.8)]),
                  *sh_arrows,
                  ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        *wall_bg(),
        main,
        *side_inset(),
        caption_band(),
        caption("Arme in U-Form an der Wand", 0, 1.0),
        caption("Langsam hochgleiten – Kontakt halten", 1.0, 3.8),
        caption("Ellbogen zu den Rippen ziehen", 3.8, 7.4),
        caption("Zurück in die U-Form", 7.4, 9.2),
        label("Schulterblätter", 20, 184, 3.8, 7.4, anchor="start"),
        label("nach unten", 20, 199, 3.8, 7.4, anchor="start"),
        static_text("Rippen unten – kein Hohlkreuz", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Wall Angels", fps=12)
