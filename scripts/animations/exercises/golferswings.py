from rig import *
from exercises._morgen_b_props import nose_hint, front_feet_out, label

SLUG = "golferswings"

# Frontansicht. Beide Hände gefasst schwingen diagonal von unten-seitlich nach
# oben über die andere Schulter. Becken und Gewicht wandern zur Zielseite,
# das hintere Knie dreht ein, die Ferse hebt leicht ab. Dann Seitenwechsel.
# Hände: beide Arme per IK auf denselben Griffpunkt (wird bei Bedarf so weit
# zur Schultermitte gezogen, dass beide Arme ihn erreichen).

FLOOR_Y = 252
CX = 200
SC = 0.86
ANK_Y = FLOOR_Y - 12
ANK_L = CX - 30
ANK_R = CX + 30
REACH = 36 + 32 - 1.0

STAND = dict(x=CX, y=FLOOR_Y - 115, hx=CX, hy=FLOOR_Y - 120, w=0.0, turn=0.0, lift_L=0, lift_R=0)
# Unten links: Becken/Gewicht links, Rumpf neigt sich zur Seite, Knie weich
LOW_L = dict(STAND, x=CX - 8, y=FLOOR_Y - 111, lumbar=4, thorax=4, chest=2, neck=-6,
             hx=CX - 52, hy=FLOOR_Y - 118, w=-1, turn=-0.55, lift_R=5)
HIGH_R = dict(STAND, x=CX + 9, y=FLOOR_Y - 116, lumbar=-4, thorax=-3, chest=-2, neck=6,
              hx=CX + 44, hy=FLOOR_Y - 230, w=1, turn=0.5, lift_L=7)
LOW_R = {k: (2 * CX - v if k in ("x", "hx") else (-v if k in ("lumbar", "thorax", "chest", "neck", "w", "turn")
                                                     else v)) for k, v in LOW_L.items()}
LOW_R["lift_L"], LOW_R["lift_R"] = LOW_L["lift_R"], LOW_L["lift_L"]
HIGH_L = {k: (2 * CX - v if k in ("x", "hx") else (-v if k in ("lumbar", "thorax", "chest", "neck", "w", "turn")
                                                      else v)) for k, v in HIGH_R.items()}
HIGH_L["lift_L"], HIGH_L["lift_R"] = HIGH_R["lift_R"], HIGH_R["lift_L"]
MID_LOW = dict(STAND, y=FLOOR_Y - 110, hy=FLOOR_Y - 112)


def grip(P, pose):
    """Griffpunkt (Handgelenke) – erreichbar für beide Schultern."""
    sL, sR = pt(P, "clav_L"), pt(P, "clav_R")
    tx, ty = pose["hx"], pose["hy"]
    mx, my = (sL[0] + sR[0]) / 2, (sL[1] + sR[1]) / 2
    for _ in range(30):
        if max(math.hypot(tx - sL[0], ty - sL[1]), math.hypot(tx - sR[0], ty - sR[1])) <= REACH:
            break
        tx, ty = mx + (tx - mx) * 0.96, my + (ty - my) * 0.96
    return tx, ty


class SwingTimeline(Timeline):
    def at(self, t):
        p = self._interp(t)
        P = FRONT.fk(p)
        gx, gy = grip(P, p)
        # Handrichtung: vom Brustbein weg zum Griff
        cx_, cy_ = pt(P, "thorax")
        ha = math.degrees(math.atan2(-(gy - cy_), gx - cx_))
        p["_gx"], p["_gy"] = gx, gy
        iks = [
            IK("thigh_L", "shin_L", (ANK_L, ANK_Y - p.get("lift_L", 0)), bend=-1),
            IK("thigh_R", "shin_R", (ANK_R, ANK_Y - p.get("lift_R", 0)), bend=1),
            IK("upperarm_L", "forearm_L", (gx - 2, gy), bend=1, end_seg="hand_L", end_abs=ha),
            IK("upperarm_R", "forearm_R", (gx + 2, gy), bend=-1, end_seg="hand_R", end_abs=ha),
        ]
        for ik in iks:
            p = solve_ik(FRONT, p, ik)
        return p


def build():
    tl = SwingTimeline([(0, LOW_L), (0.3, LOW_L), (1.3, HIGH_R), (1.6, HIGH_R), (2.6, LOW_L),
                        (3.2, LOW_R), (3.5, LOW_R), (4.5, HIGH_L), (4.8, HIGH_L), (5.8, LOW_R),
                        (6.4, LOW_L)], skeleton=FRONT)
    dur = tl.duration

    def foot_weight(side):
        sgn = -1 if side == "L" else 1
        ax = ANK_L if side == "L" else ANK_R
        return Prim("ellipse", {"cx": ax + sgn * 2, "cy": FLOOR_Y + 1, "rx": 16, "ry": 3.5, "fill": GOOD},
                    lambda c: {"opacity": round(max(0.0, sgn * c["pose"]["w"]) * 0.7, 2)})

    legs = (limb(["hip_L", "thigh_L", "shin_L"], 16, NEAR) + limb(["hip_R", "thigh_R", "shin_R"], 16, NEAR)
            + front_feet_out(12))
    fig = front_figure(legs=False, extras_behind=[foot_weight("L"), foot_weight("R"), *legs])
    ghost_low = ghost(limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR)
                      + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR), FRONT, tl.at(0), 0.13)

    # Schwungbahnen (diagonal), jeweils nur die aktive Diagonale
    PA = tl.at(0.0)
    PB = tl.at(1.3)
    a0, a1 = (PA["_gx"], PA["_gy"]), (PB["_gx"], PB["_gy"])
    def diag(p0, p1, bow, show):
        mx, my = (p0[0] + p1[0]) / 2 + bow, (p0[1] + p1[1]) / 2 + abs(bow) * 0.5
        return arrow(f"M{p0[0]:.0f} {p0[1] + 6:.0f} Q{mx:.0f} {my:.0f} {p1[0]:.0f} {p1[1] - 4:.0f}",
                     width=3, show=show)
    trail = lambda p0, p1, bow, show: Prim("path", {
        "d": f"M{p0[0]:.0f} {p0[1]:.0f} Q{(p0[0] + p1[0]) / 2 + bow:.0f} {(p0[1] + p1[1]) / 2 + abs(bow) * 0.5:.0f}"
             f" {p1[0]:.0f} {p1[1]:.0f}",
        "fill": "none", "stroke": ACCENT, "stroke-width": 1.5, "stroke-dasharray": "3 5", "opacity": 0.45,
        "_show": show})
    m = lambda p: (2 * CX - p[0], p[1])
    off = 30   # Pfeil außen neben der Bahn
    s0, s1 = (a0[0] - off * 0.6, a0[1]), (a1[0] + off * 0.6, a1[1] - 6)
    main = group([
        trail(a0, a1, 40, [(0, 2.6)]),
        trail(m(a0), m(a1), -40, [(3.2, 5.8)]),
        ghost_low,
        *fig,
        diag(s0, s1, 58, [(0.3, 1.3)]),
        diag(m(s0), m(s1), -58, [(3.5, 4.5)]),
        focus("lumbar", rx=20, ry=12, offset=(0, -4), show=[(0.3, 1.6), (3.5, 4.8)]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        floor(FLOOR_Y + 1, 60, 340),
        main,
        caption_band(),
        caption("Diagonal hoch über die andere Schulter", 0, 1.6),
        caption("Locker zurückschwingen", 1.6, 2.6),
        caption("Seite wechseln", 2.6, 3.5),
        caption("Diagonal hoch – Gewicht geht mit", 3.5, 4.8),
        caption("Beide Seiten gleich oft", 4.8, dur),
        static_text("Schwung aus Hüfte & Rumpf – Gewicht verlagern", 196, 24, 13, MUTED),
        nose_hint(),
    ]
    return render(prims, tl, FRONT, title="Golferswings", fps=15)
