from rig import *
from exercises._morgen_b_props import nose_hint, front_feet_out, label

SLUG = "ballet-squat"

# Frontansicht, breiter Stand, Füße ~45° nach außen. Langsam tief (Plié) und
# wieder hoch. Knöchel fix (IK), Knie wandern nach außen über die Zehen,
# Becken sinkt senkrecht, Rumpf bleibt lang und aufrecht. Arme in
# zweiter Position (seitlich, weich gerundet).

FLOOR_Y = 252
CX = 200
SC = 0.9
ANK_Y = FLOOR_Y - 12
ANK_L, ANK_R = CX - 64, CX + 64
TOE_OUT = 45

ARMS = dict(upperarm_L=-62, forearm_L=-14, hand_L=-10, upperarm_R=62, forearm_R=14, hand_R=10)
UP = dict(x=CX, y=ANK_Y - 84, neck=0, **ARMS)
DOWN = dict(UP, y=ANK_Y - 46, upperarm_L=-58, upperarm_R=58)


def build():
    iks = [IK("thigh_L", "shin_L", (ANK_L, ANK_Y), bend=-1),
           IK("thigh_R", "shin_R", (ANK_R, ANK_Y), bend=1)]
    keys = [(0, UP), (0.4, UP), (2.6, DOWN), (3.3, DOWN), (5.3, UP), (5.6, UP)]
    tl = Timeline(keys, iks=iks, skeleton=FRONT)
    dur = tl.duration

    legs = (limb(["hip_L", "thigh_L", "shin_L"], 17, NEAR) + limb(["hip_R", "thigh_R", "shin_R"], 17, NEAR))
    # Füße ausgedreht: von der Ferse schräg nach außen-vorn (zum Betrachter)
    def foot(side):
        sgn = -1 if side == "L" else 1
        ax = ANK_L if side == "L" else ANK_R
        d = f"M{ax:.0f} {ANK_Y + 3:.0f}L{ax + sgn * 13:.0f} {ANK_Y + 7:.0f}"
        return [Prim("path", {"d": d, "fill": "none", "stroke": SKIN_LINE, "stroke-width": 14, "stroke-linecap": "round"}),
                Prim("path", {"d": d, "fill": "none", "stroke": NEAR, "stroke-width": 11, "stroke-linecap": "round"})]
    feet = foot("L") + foot("R")
    fig = front_figure(legs=False, extras_behind=[*feet, *legs])

    # Knie-über-Zehen-Linien (unten sichtbar): Knie -> Fußspitze
    def ktl(side):
        sgn = -1 if side == "L" else 1
        ax = ANK_L if side == "L" else ANK_R
        tip = (ax + sgn * 16, FLOOR_Y - 2)

        def f(c):
            kx, ky = pt(c["P"], f"thigh_{side}")
            return {"x1": kx, "y1": ky, "x2": tip[0], "y2": tip[1]}
        return Prim("line", {"stroke": GOOD, "stroke-width": 2, "stroke-dasharray": "4 4",
                             "_show": [(1.6, 4.2)]}, f)

    # Rücken lang: Lot entlang der Wirbelsäule
    def spine(c):
        x0, y0 = pt(c["P"], "root", end=False)
        x1, y1 = pt(c["P"], "head")
        return {"x1": x0, "y1": y0 + 6, "x2": x1, "y2": y1 - 24}
    spine_line = Prim("line", {"stroke": GOOD, "stroke-width": 1.5, "stroke-dasharray": "5 5", "opacity": 0.55},
                      spine)

    P_up, P_dn = FRONT.fk(tl.at(0)), FRONT.fk(tl.at(2.6))
    kL_up, kL_dn = pt(P_up, "thigh_L"), pt(P_dn, "thigh_L")
    knee_arrows = [
        arrow(f"M{kL_up[0] - 6:.0f} {kL_up[1] - 2:.0f} L{kL_dn[0] - 14:.0f} {kL_dn[1] - 10:.0f}", width=2.5,
              show=[(0.4, 2.6)]),
        arrow(f"M{2 * CX - kL_up[0] + 6:.0f} {kL_up[1] - 2:.0f} L{2 * CX - kL_dn[0] + 14:.0f} {kL_dn[1] - 10:.0f}",
              width=2.5, show=[(0.4, 2.6)]),
    ]
    ry_up, ry_dn = pt(P_up, "root", end=False)[1], pt(P_dn, "root", end=False)[1]
    up_arrow = arrow(f"M{CX} {ry_dn + 46:.0f} L{CX} {ry_dn + 12:.0f}", width=3, show=[(3.3, 5.3)])

    main = group([
        ghost(limb(["hip_L", "thigh_L", "shin_L"], 17, NEAR) + limb(["hip_R", "thigh_R", "shin_R"], 17, NEAR)
              + limb(["lumbar", "thorax", "chest"], 44, TORSO), FRONT, tl.at(0), 0.12),
        *fig,
        focus("thigh_L", rx=15, ry=8, offset=(-16, 8), end=False, show=[(1.2, 4.6)]),
        focus("thigh_R", rx=15, ry=8, offset=(16, 8), end=False, show=[(1.2, 4.6)]),
        *knee_arrows, up_arrow,
    ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        floor(FLOOR_Y + 1, 50, 350),
        main,
        caption_band(),
        caption("Langsam tief – Knie nach außen", 0, 2.6),
        caption("Unten kurz halten – Rücken lang", 2.6, 3.3),
        caption("Langsam wieder hoch", 3.3, dur),
        static_text("Knie zeigen Richtung Zehen", 200, 24, 13, MUTED),
        nose_hint(dur=dur),
    ]
    return render(prims, tl, FRONT, title="Ballet Squat", fps=12)
