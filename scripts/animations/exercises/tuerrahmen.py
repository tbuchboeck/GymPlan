from rig import *

SLUG = "tuerrahmen-dehnung"

# Hauptansicht: Draufsicht (vorwärts = nach oben). Wand mit Türöffnung, die
# Person steht in der Öffnung, rechter Unterarm senkrecht an der Wand direkt
# neben der Rahmenkante (von oben: kurzer Block). Der Ellbogen E bleibt fix;
# die nahe Schulter S bewegt sich auf einem Kreis (Oberarmlänge) um E nach
# vorn -> der Oberarm zeigt immer weiter nach hinten = Brustdehnung.
# Zusätzlich dreht die Schulterlinie leicht auf (ferne Schulter geht vor).
# Inset rechts oben: Armhaltung 90/90 am Pfosten (FRONT-Skelett, statisch).

WALL_Y0, WALL_Y1 = 122, 140          # Wand (Vorder-/Rückseite)
OPEN_X0, OPEN_X1 = 104, 260          # Türöffnung
ELBOW = (267.0, 148.0)               # Unterarm-Block an der Wand-Rückseite, neben der Kante
UA = 57.0                            # Oberarm (Draufsicht)
HS = 37.0                            # halbe Schulterbreite
ALPHA, PHI = 40.0, 12.0              # max. Oberarm-Winkel nach hinten / Aufdrehen
FOOT_FRONT = (196, 62)
FOOT_BACK = (150, 188)

START = dict(lean=0.0)
LEAN = dict(lean=1.0)
LEAN_IN = dict(lean=1.06)            # in der Haltephase minimal tiefer


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="start"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": "500",
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


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


def body(lean):
    """Draufsicht-Geometrie aus dem Skalar lean (0..1)."""
    a = math.radians(ALPHA * lean)
    f = math.radians(PHI * lean)
    S = (ELBOW[0] - UA * math.cos(a), ELBOW[1] - UA * math.sin(a))     # nahe Schulter
    u = (math.cos(f), math.sin(f))                                     # fern -> nah
    F = (S[0] - 2 * HS * u[0], S[1] - 2 * HS * u[1])                   # ferne Schulter
    C = ((S[0] + F[0]) / 2, (S[1] + F[1]) / 2)
    n = (u[1], -u[0])                                                  # vorwärts
    return S, F, C, u, n


def B(c):
    return body(c["pose"].get("lean", 0.0))


def off(p, u, n, a=0.0, b=0.0):
    return (p[0] + a * u[0] + b * n[0], p[1] + a * u[1] + b * n[1])


def scene_static():
    wall = "#3b4a63"
    return [
        # Boden beider Räume, Schwelle in der Öffnung
        Prim("rect", {"x": OPEN_X0, "y": WALL_Y0, "width": OPEN_X1 - OPEN_X0, "height": WALL_Y1 - WALL_Y0,
                      "fill": "#26324a"}),
        Prim("rect", {"x": 8, "y": WALL_Y0, "width": OPEN_X0 - 8, "height": WALL_Y1 - WALL_Y0, "fill": wall}),
        Prim("rect", {"x": OPEN_X1, "y": WALL_Y0, "width": 392 - OPEN_X1, "height": WALL_Y1 - WALL_Y0, "fill": wall}),
        # Türzarge (Rahmenkanten)
        Prim("rect", {"x": OPEN_X0 - 5, "y": WALL_Y0 - 3, "width": 5, "height": WALL_Y1 - WALL_Y0 + 6, "rx": 1.5,
                      "fill": PROP}),
        Prim("rect", {"x": OPEN_X1, "y": WALL_Y0 - 3, "width": 5, "height": WALL_Y1 - WALL_Y0 + 6, "rx": 1.5,
                      "fill": "#94a3b8"}),
    ]


def feet():
    out = []
    for (x, y) in (FOOT_FRONT, FOOT_BACK):
        d = f"M{x - 9} {y + 12}L{x - 9} {y - 8}"
        d2 = f"M{x + 9} {y + 14}L{x + 9} {y - 6}" if (x, y) == FOOT_BACK else f"M{x + 9} {y + 12}L{x + 9} {y - 8}"
        for dd in ((d,) if (x, y) == FOOT_FRONT else (d2,)):
            out.append(Prim("path", {"d": dd, "stroke": SKIN_LINE, "stroke-width": 15, "stroke-linecap": "round",
                                     "fill": "none"}))
            out.append(Prim("path", {"d": dd, "stroke": FAR, "stroke-width": 12, "stroke-linecap": "round",
                                     "fill": "none"}))
    return out


def person(frozen_lean=None):
    def g(c):
        return body(frozen_lean) if frozen_lean is not None else B(c)

    def trunk(c):
        S, F, C, u, n = g(c)
        return [off(F, u, n, 6, -4), off(S, u, n, -6, -4)]

    def shoulders(c):
        S, F, C, u, n = g(c)
        return [F, S]

    def far_arm(c):
        S, F, C, u, n = g(c)
        x, y = off(F, u, n, -7, 4)
        return {"cx": x, "cy": y}

    def head(c):
        S, F, C, u, n = g(c)
        x, y = off(C, u, n, 0, 6)
        return {"cx": x, "cy": y}

    def nose(c):
        S, F, C, u, n = g(c)
        x, y = off(C, u, n, 0, 22)
        return {"cx": x, "cy": y}

    def uarm(c):
        S, F, C, u, n = g(c)
        return [S, ELBOW]

    prims = [Prim("circle", {"r": 10, "fill": FAR, "stroke": SKIN_LINE, "stroke-width": 1.5}, far_arm)]
    prims += stroke(trunk, 40, TORSO)
    prims += stroke(shoulders, 22, TORSO)
    prims += stroke(uarm, 15, NEAR)
    prims += [Prim("circle", {"r": 17.5, "fill": SKIN_LINE}, head),
              Prim("circle", {"r": 16, "fill": "#4338ca"}, head),
              Prim("circle", {"r": 8, "fill": "#3b32b8"}, head),
              Prim("ellipse", {"rx": 4, "ry": 3.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, nose)]
    return prims


def forearm_block():
    ex, ey = ELBOW
    return [Prim("rect", {"x": ex - 7.5, "y": ey - 7.5, "width": 15, "height": 15, "rx": 4, "fill": NEAR,
                          "stroke": SKIN_LINE, "stroke-width": 1.5}),
            Prim("rect", {"x": ex - 4, "y": ey - 4, "width": 8, "height": 8, "rx": 2, "fill": HEAD})]


# --- Inset: Armhaltung 90/90 (statisch) ----------------------------------------
IN_X, IN_Y, IN_W, IN_H = 280, 164, 112, 88


def arm_inset():
    pose = dict(x=0, y=0, upperarm_R=90, forearm_R=90, upperarm_L=4, forearm_L=-4)
    parts = (limb(["neck"], 13, TORSO) + limb(["lumbar", "thorax", "chest"], 44, TORSO)
             + [Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"},
                     lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])})]
             + limb(["upperarm_L", "forearm_L", "hand_L"], 13, FAR)
             + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR) + head_front())
    P = FRONT.fk(pose)
    ex, ey = pt(P, "upperarm_R")
    frozen = ghost(parts, FRONT, pose, opacity=1.0)
    post = Prim("rect", {"x": ex + 7, "y": ey - 52, "width": 12, "height": 120, "fill": "#94a3b8"})
    ang = Prim("path", {"d": f"M{ex - 14} {ey}L{ex - 14} {ey - 14}L{ex} {ey - 14}", "fill": "none",
                        "stroke": ACCENT, "stroke-width": 2.5})
    sh_y = pt(P, "clav_R")[1]
    level = Prim("line", {"x1": pt(P, "clav_L")[0] - 20, "y1": sh_y, "x2": ex + 30, "y2": sh_y, "stroke": GOOD,
                          "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.8})
    cx, cy = pt(P, "chest")
    g = group([post, frozen, level, ang], scale=0.66, origin=(cx, cy),
              dx=IN_X + 40 - cx, dy=IN_Y + 66 - cy)
    clip = Prim("g", {"clip-path": "url(#clipArm)"}, children=[
        Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "fill": "#0b1220", "opacity": 0.8}), g])
    return [clip, static_text("Ellbogen auf Schulterhöhe", IN_X + IN_W / 2, IN_Y + 12, 9, GOOD),
            static_text("Unterarm senkrecht", IN_X + IN_W / 2, IN_Y + 23, 9, GOOD)]


def build():
    tl = Timeline([(0, START), (1.4, START), (3.4, LEAN), (5.2, LEAN_IN), (7.0, LEAN),
                   (7.6, LEAN), (9.2, START), (9.6, START)], skeleton=SIDE)

    def chest(c):
        S, F, C, u, n = B(c)
        x, y = off(S, u, n, -17, 9)
        return {"cx": x, "cy": y}

    focus_chest = Prim("ellipse", {"rx": 15, "ry": 10, "fill": GOOD, "opacity": 0.35, "_pulse": True,
                                   "_show": [(2.4, 7.8)]}, chest)
    start_ghost = ghost(person(0.0), SIDE, START, 0.16)
    main = group([*scene_static(), start_ghost, *person(), *forearm_block(), focus_chest],
                 scale=1.3, origin=(182, 140), dx=-12)
    prims = [
        main,
        arrow("M160 238 L160 208", show=[(1.4, 3.4)]),
        *arm_inset(),
        caption_band(),
        caption("Unterarm senkrecht an den Rahmen, Ellbogen 90°", 0, 1.4, size=14),
        caption("Mit dem Körper langsam vorlehnen", 1.4, 3.4),
        caption("Brust zieht – 30 s ruhig atmen", 3.4, 7.6),
        caption("Langsam zurück", 7.6, 9.6),
        label("Schulter bleibt unten", 16, 238, 3.4, 7.6),
        static_text("Wand", 24, 111, 10, MUTED, anchor="start"),
        static_text("Türrahmen", 302, 111, 10, MUTED, anchor="start"),
        static_text("von oben", 16, 46, 11, MUTED, anchor="start"),
        static_text("Kribbeln im Arm? Spannung sofort lösen", 200, 22, 12, MUTED),
    ]
    clip = (f'<clipPath id="clipArm"><rect x="{IN_X}" y="{IN_Y}" width="{IN_W}" height="{IN_H}" rx="8"/>'
            '</clipPath>')
    return render(prims, tl, SIDE, title="Brustdehnung im Türrahmen", fps=12, extra_defs=clip)
