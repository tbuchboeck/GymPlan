from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "glute-bridge"

# Rückenlage, Seitansicht, Kopf links (rot≈90 -> Gesicht nach oben).
# Skalar "lift" 0..1: Becken hebt sich um die fixen Schulterblätter,
# Fersen bleiben auf der Matte (IK), Kopf/Arme liegen flach.
FLOOR_Y = 236
C = FLOOR_Y - 16              # Mittellinie des liegenden Rumpfs
SH = (128, C)                 # Schulter-Kontakt (Ende von "chest")
SPINE = 78                    # lumbar + thorax + chest
ALPHA = 22                    # Rumpfwinkel oben (Knie–Hüfte–Schulter Linie)
ANKLE = (262, FLOOR_Y - 7)


def pre(p):
    a = ALPHA * p.get("lift", 0.0)
    r = math.radians(a)
    p["x"] = SH[0] + SPINE * math.cos(r)
    p["y"] = SH[1] - SPINE * math.sin(r)
    p["rot"] = 90 + a
    # Becken leicht nach hinten gekippt (kein Hohlkreuz): Wirbel gerade
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    set_abs(SIDE, p, "neck", 172)
    set_abs(SIDE, p, "head", 176)
    return p


IKS = [
    IK("thigh_n", "shin_n", ANKLE, bend=1, end_seg="foot_n", end_abs=0),
    IK("thigh_f", "shin_f", (ANKLE[0] - 3, ANKLE[1]), bend=1, end_seg="foot_f", end_abs=0),
    IK("upperarm_n", "forearm_n", (SH[0] + 74, FLOOR_Y - 6), bend=1, end_seg="hand_n", end_abs=-2),
    IK("upperarm_f", "forearm_f", (SH[0] + 70, FLOOR_Y - 6), bend=1, end_seg="hand_f", end_abs=-2),
]

DOWN = dict(lift=0.0)
UP = dict(lift=1.0)

# Tempo laut Plan: 2 s hoch / 3–5 s halten (hier 4) / 2 s runter
T_UP0, T_UP1, T_H1, T_DN1, T_END = 0.8, 2.8, 6.8, 8.8, 9.6


def build():
    tl = FnTimeline([(0, DOWN), (T_UP0, DOWN), (T_UP1, UP), (T_H1, UP), (T_DN1, DOWN), (T_END, DOWN)],
                    iks=IKS, skeleton=SIDE, pre=pre)
    p_up = tl.at(T_UP1 + 0.1)
    p_dn = tl.at(0)

    def line_pts(c):
        P = c["P"]
        return pt(P, "chest"), pt(P, "thigh_n")

    fig = side_figure()
    S, OX = 1.32, 196

    def T(x, y):
        return OX + (x - OX) * S, FLOOR_Y + (y - FLOOR_Y) * S

    lx, ly = T(206, 160)
    hx, hy = T(ANKLE[0] - 4, FLOOR_Y)
    scene = group([
        mat(FLOOR_Y, 66, 314),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR),
              SIDE, p_dn, 0.16),
        *fig,
        dyn_line(line_pts, show=[(T_UP1, T_H1)]),
        focus("root", rx=17, ry=12, offset=(4, 8), end=False, show=[(T_UP0, T_H1)]),
        arrow("M206 214 L206 188", show=[(T_UP0, T_UP1)]),
        arrow("M206 188 L206 212", show=[(T_H1, T_DN1)]),
        Prim("circle", {"cx": ANKLE[0] - 4, "cy": FLOOR_Y - 2, "r": 3.5, "fill": GOOD, "_show": [(T_UP0, T_DN1)]}),
    ], scale=S, origin=(OX, FLOOR_Y))
    prims = [
        scene,
        label("Druck über die Fersen", hx + 4, FLOOR_Y + 17, T_UP0, T_UP1, 11, GOOD),
        label("eine Linie", lx - 30, ly - 4, T_UP1, T_H1, 12, GOOD),
        *counter(T_UP1, 4, lx + 2, ly - 34, size=18),
        caption_band(),
        caption("Rückenlage, Knie ca. 90°", 0, T_UP0),
        caption("Ausatmen – Po fest, Becken hoch", T_UP0, T_UP1),
        caption("Oben halten – Knie, Hüfte, Schulter", T_UP1, T_H1),
        caption("Kontrolliert absenken", T_H1, T_END),
        *tempo_chip([("2 s hoch", T_UP0, T_UP1), ("4 s halten", T_UP1, T_H1), ("2 s runter", T_H1, T_DN1)]),
        static_text("Gesäß anspannen – nicht ins Hohlkreuz", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Glute Bridge")
