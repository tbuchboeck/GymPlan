from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "curl-up"

# McGill Curl-up: Rückenlage, ein Bein aufgestellt (nah), das andere gestreckt
# (fern), Hände unter der Lende. Skalar "lift" 0..1 hebt nur Kopf und
# Schultern ein kleines Stück – als Block, ohne das Kinn zur Brust zu ziehen.
FLOOR_Y = 236
C = FLOOR_Y - 16
SEG = 26
HIP = (128 + 3 * SEG, C)
ANKLE_N = (262, FLOOR_Y - 7)


def pre(p):
    lift = p.get("lift", 0.0)
    p["x"], p["y"] = HIP
    p["rot"] = 90
    p["lumbar"] = 0.0
    p["thorax"] = -4 * lift
    p["chest"] = -14 * lift
    # Kopf/Nacken bleiben in Verlängerung des Brustkorbs (kein Kinn zur Brust)
    P = SIDE.fk(p)
    ca = P["chest"][4]
    set_abs(SIDE, p, "neck", ca - 8)
    set_abs(SIDE, p, "head", ca - 4)
    return p


IKS = [
    IK("thigh_n", "shin_n", ANKLE_N, bend=1, end_seg="foot_n", end_abs=0),
    IK("thigh_f", "shin_f", (HIP[0] + 96, FLOOR_Y - 8), bend=1, end_seg="foot_f", end_abs=80),
    # Hände unter der Lende
    IK("upperarm_n", "forearm_n", (HIP[0] - 12, FLOOR_Y - 4), bend=1, end_seg="hand_n", end_abs=0),
    IK("upperarm_f", "forearm_f", (HIP[0] - 16, FLOOR_Y - 4), bend=1, end_seg="hand_f", end_abs=0),
]

DOWN = dict(lift=0.0)
UP = dict(lift=1.0)
T_UP0, T_UP1, T_H1, T_DN1, T_END = 0.8, 2.3, 10.3, 11.8, 12.8


def build():
    tl = FnTimeline([(0, DOWN), (T_UP0, DOWN), (T_UP1, UP), (T_H1, UP), (T_DN1, DOWN), (T_END, DOWN)],
                    iks=IKS, skeleton=SIDE, pre=pre)
    p_dn = tl.at(0)
    fig = side_figure()
    S, OX = 1.32, 196
    scene = group([
        mat(FLOOR_Y, 50, 330),
        ghost(limb(["thorax", "chest"], 26, TORSO) + limb(["neck"], 13, TORSO), SIDE, p_dn, 0.16),
        *fig,
        focus("lumbar", rx=22, ry=9, offset=(0, 4), end=True, show=[(T_UP0, T_H1)]),
        arrow("M122 200 L122 184", show=[(T_UP0, T_UP1)]),
        arrow("M122 184 L122 200", show=[(T_H1, T_DN1)]),
    ], scale=S, origin=(OX, FLOOR_Y))
    prims = [
        scene,
        label("nur wenige cm", 96, 132, T_UP0, T_H1, 12, GOOD),
        label("Bauch fest, Lende neutral", 210, 168, T_UP1, T_H1, 12, ACCENT),
        *counter(T_UP1, 8, 318, 120, size=18),
        caption_band(),
        caption("Ein Bein auf, eins lang, Hände unter die Lende", 0, T_UP0),
        caption("Kopf und Schultern als Block leicht abheben", T_UP0, T_UP1),
        caption("8–10 s halten – ruhig weiteratmen", T_UP1, T_H1),
        caption("Ablegen, Bein wechseln", T_H1, T_END),
        static_text("Kinn nicht zur Brust ziehen – Blick zur Decke", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Curl-up")
