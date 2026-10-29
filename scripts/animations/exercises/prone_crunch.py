from rig import *
from exercises._bauch_props import limb_sharp, poly_path

SLUG = "prone-crunch"

# Draufsicht (von oben auf den Rücken): Bauchlage, Oberkörper auf die
# Unterarme gestützt, Becken bleibt auf der Matte. Ein Knie wird angewinkelt
# seitlich über die Matte Richtung Brust/Ellbogen gezogen, dann zurück – im Wechsel.
CY = 150
BASE = dict(x=160, y=CY, rot=-90,
            thigh_L=-4, shin_L=1, thigh_R=4, shin_R=-1)
KNEE_L = dict(BASE, thigh_L=-138, shin_L=150, lumbar=2, thorax=1)
KNEE_R = dict(BASE, thigh_R=138, shin_R=-150, lumbar=-2, thorax=-1)

HEAD_R = 16


def top_arm(side):
    """Arm von oben: Ellbogen knapp vor/außen der Schulter (Oberarm steht
    senkrecht, wirkt von oben kurz), Unterarm flach nach vorn."""
    s = 1 if side == "L" else -1

    def pts(c):
        P = c["P"]
        sx, sy = pt(P, f"clav_{side}")
        ex, ey = sx + 12, sy - s * 8
        wx, wy = ex + 34, ey + s * 6
        hx, hy = wx + 13, wy + s * 1
        return [(sx, sy), (ex, ey), (wx, wy), (hx, hy)]

    f = lambda c: {"d": poly_path(pts(c))}
    return [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 16, "stroke-linecap": "round",
                          "stroke-linejoin": "round"}, f),
            Prim("path", {"fill": "none", "stroke": NEAR if side == "L" else FAR, "stroke-width": 13,
                          "stroke-linecap": "round", "stroke-linejoin": "round"}, f)]


def head_top():
    """Hinterkopf von oben: Haarschopf, Ohren seitlich."""
    def c0(c):
        x, y = pt(c["P"], "head")
        return {"cx": x, "cy": y}

    def hair(c):
        x, y = pt(c["P"], "head")
        return {"cx": x - 3, "cy": y}

    def ear(s):
        def f(c):
            x, y = pt(c["P"], "head")
            return {"cx": x + 2, "cy": y - s * (HEAD_R - 1)}
        return f

    return [Prim("circle", {"r": HEAD_R + 1.5, "fill": SKIN_LINE}, c0),
            Prim("ellipse", {"rx": 3.5, "ry": 2.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1}, ear(1)),
            Prim("ellipse", {"rx": 3.5, "ry": 2.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1}, ear(-1)),
            Prim("circle", {"r": HEAD_R, "fill": HEAD}, c0),
            Prim("circle", {"r": HEAD_R - 2.5, "fill": "#4338ca"}, hair)]


def top_figure():
    prims = []
    prims += limb_sharp(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, FAR)
    prims += limb_sharp(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR)
    prims += top_arm("R") + top_arm("L")
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], 42, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
              trunk[1]]
    # Wirbelsäule als feine Linie (zeigt Seitneigung)
    prims.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.5, "opacity": 0.5,
                               "stroke-linecap": "round"},
                      lambda c: {"d": smooth_path(chain_points(c["P"], ["lumbar", "thorax", "chest"]))}))
    prims += head_top()
    return prims


def build():
    keys = [(0, BASE), (0.8, BASE), (2.0, KNEE_L), (2.7, KNEE_L), (3.7, BASE),
            (4.1, BASE), (5.3, KNEE_R), (6.0, KNEE_R), (7.0, BASE), (7.4, BASE)]
    tl = Timeline(keys, skeleton=FRONT)
    mat_top = Prim("rect", {"x": 16, "y": CY - 72, "width": 368, "height": 144, "rx": 10, "fill": "#3f4a7a",
                            "opacity": 0.55})
    legs0 = limb_sharp(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, NEAR) + \
        limb_sharp(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, FAR)
    prims = [
        mat_top,
        group([
            ghost(legs0, FRONT, BASE, 0.16),
            *top_figure(),
            focus("lumbar", rx=9, ry=14, offset=(2, -24), show=[(0.8, 3.7)]),
            focus("lumbar", rx=9, ry=14, offset=(2, 24), show=[(4.1, 7.0)]),
            arrow("M70 122 Q120 100 168 104", show=[(0.8, 2.0)]),
            arrow("M70 178 Q120 200 168 196", show=[(4.1, 5.3)]),
        ], scale=1.15, origin=(196, CY)),
        caption_band(),
        static_text("Ansicht von oben", 30, 248, 11, MUTED, anchor="start"),
        caption("Unterarme stützen, Becken liegt", 0, 0.8),
        caption("Knie seitlich zur Brust ziehen", 0.8, 2.0),
        caption("Kurz halten – Bauch fest", 2.0, 2.7),
        caption("Bein lang zurückschieben", 2.7, 4.1),
        caption("Andere Seite – Knie zur Brust", 4.1, 5.3),
        caption("Kurz halten – Bauch fest", 5.3, 6.0),
        caption("Bein lang zurückschieben", 6.0, 7.4),
        static_text("Knie gleitet über die Matte – Becken bleibt unten", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Bauchlage-Crunch")
