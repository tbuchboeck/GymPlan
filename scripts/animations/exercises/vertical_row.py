from rig import *
from exercises._tb_gym_props import *

SLUG = "vertical-row"

# „Trizepszug“ laut Plan – die Anleitung beschreibt aber ein Rudern an der
# Vertical-Row-Maschine: Brust am Polster, Griffe auf Schulterhöhe, Ellbogen
# nach hinten, Schulterblätter zusammen. Seitansicht, Blick nach rechts.
# Griffe hängen an Hebelarmen (Drehpunkt oben), die beim Ziehen nach hinten
# schwingen; der Gewichtsblock hebt sich mit.

FLOOR_Y = 250
HIP = (150.0, 194.0)
ANK_N, ANK_F = (204.0, FLOOR_Y - 8.0), (198.0, FLOOR_Y - 8.0)
PIV = (205.0, 36.0)
LEVER = 82.0
TH0, TH1 = 6.3, -31.5        # Hebelwinkel (Grad, + = nach vorn) Start/gezogen
GRIP_HALF = 10.0
FAR_OFF = (-5.0, -1.5)       # ferne Seite leicht versetzt


def lever_end(p, far=False):
    th = math.radians(TH0 + (TH1 - TH0) * p)
    x, y = PIV[0] + LEVER * math.sin(th), PIV[1] + LEVER * math.cos(th)
    if far:
        x, y = x + FAR_OFF[0], y + FAR_OFF[1]
    return x, y


def post(pose, P):
    p = pose.get("pull", 0.0)
    scap = min(1.0, p * 1.5)
    out = {"scap": scap}
    s = shoulder_side(P, scap)
    l1 = UA * (1 - 0.47 * p)
    for k, far in (("", False), ("_f", True)):
        lx, ly = lever_end(p, far)
        w = (lx, ly + GRIP_HALF)
        sk = (s[0] + FAR_OFF[0], s[1] + FAR_OFF[1]) if far else s
        w = clamp_reach(sk, w, l1 + FA - 0.5)
        e = ik2(sk, w, l1, FA, bend=-1)
        out.update({"sx" + k: sk[0], "sy" + k: sk[1], "ex" + k: e[0], "ey" + k: e[1],
                    "wx" + k: w[0], "wy" + k: w[1]})
    return out


BASE = dict(x=HIP[0], y=HIP[1], rot=-4, neck=2, head=-2, pull=0.0)
PULL = dict(BASE, pull=1.0, chest=-3, neck=3)


def grip(far):
    def f(c):
        lx, ly = lever_end(c["pose"]["pull"], far)
        return (lx, ly + 1, lx, ly + 2 * GRIP_HALF)
    return grip_line(f, 6, PROP_DARK if far else "#94a3b8")


def lever(far):
    def f(c):
        lx, ly = lever_end(c["pose"]["pull"], far)
        return {"x1": PIV[0] + (FAR_OFF[0] if far else 0), "y1": PIV[1], "x2": lx, "y2": ly + 2}
    col = PROP_DARK if far else PROP
    return [Prim("line", {"stroke": "#0b1220", "stroke-width": 9, "stroke-linecap": "round"}, f),
            Prim("line", {"stroke": col, "stroke-width": 6, "stroke-linecap": "round"}, f)]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
    ]
    T_PULL0, T_PULL1, T_HOLD1, T_BACK1, T_END = 0.8, 2.2, 3.2, 5.0, 5.6
    tl = PostTimeline([(0, BASE), (T_PULL0, BASE), (T_PULL1, PULL), (T_HOLD1, PULL),
                       (T_BACK1, BASE), (T_END, BASE)], iks=iks, skeleton=SIDE, post=post)

    lift = lambda c: 26 * c["pose"]["pull"]
    stack, stack_top = weight_stack(318, FLOOR_Y, 66, lift, n=11, w=34)

    frame = [
        R(288, 34, 12, FLOOR_Y - 34, PROP_DARK, rx=3),            # Säule
        R(196, 30, 168, 10, PROP_DARK, rx=4),                     # Querträger oben
        R(270, FLOOR_Y - 7, 110, 7, PROP_DARK, rx=3),             # Fuß
        L(335, 42, 335, stack_top - 2, "#cbd5e1", 2),             # Seil zum Block
        *pulley(335, 46, 5),
    ]
    cam = [C(PIV[0], PIV[1], 11, PROP_DARK), C(PIV[0], PIV[1], 7.5, PROP), C(PIV[0], PIV[1], 2.5, PROP_DARK)]
    seat = [
        R(112, 202, 70, 10, PROP, rx=5),
        R(140, 212, 12, FLOOR_Y - 216, PROP_DARK, rx=2),
        R(112, FLOOR_Y - 7, 70, 7, PROP_DARK, rx=3),
        R(182, 160, 108, 7, PROP_DARK, rx=3),                     # Polsterträger
    ]
    pad = [R(169, 126, 13, 52, "#0b1220", rx=6.5), R(170.5, 127.5, 10, 49, PROP, rx=5)]

    far_leg, torso, near_leg = side_body(head=False)
    figure = (far_leg + lever(True) + grip(True) + arm_prims("_f", far=True) + torso + [scapula()] + pad + lever(False) + head_side() +
              near_leg)
    front = grip(False) + arm_prims("", far=False) + cam

    c0, c1 = tl.at(0), tl.at(T_PULL1)
    ghost_arm = ghost(arm_prims("", far=False), SIDE, c0, 0.2)
    e0, e1 = (c0["ex"], c0["ey"]), (c1["ex"], c1["ey"])
    pull_arrow = arrow(f"M{e0[0] - 4:.0f} {e0[1] + 16:.0f} Q{(e0[0] + e1[0]) / 2:.0f} {e1[1] + 24:.0f} "
                       f"{e1[0] - 4:.0f} {e1[1] + 12:.0f}", show=[(T_PULL0, T_PULL1)])
    back_arrow = arrow(f"M{e1[0] + 14:.0f} {c1['wy'] - 22:.0f} L{c0['wx'] - 6:.0f} {c0['wy'] - 24:.0f}",
                       color=MUTED, width=2.2, show=[(T_HOLD1, T_BACK1)])
    rhomb = Prim("ellipse", {"rx": 6, "ry": 12, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                             "_show": [(1.3, 3.6)]},
                 lambda c: dict(zip(("cx", "cy"), body_pt(c["P"], "thorax", 17, -10))))

    prims = [
        floor(FLOOR_Y, 40, 380),
        *frame, *stack, *seat,
        *figure,
        ghost_arm,
        *front,
        rhomb,
        pull_arrow,
        caption_band(),
        static_text("Brust bleibt am Polster – Ellbogen nach hinten", 200, 22, LEAD_SIZE, MUTED),
        caption("Brust ans Polster, Griffe auf Schulterhöhe", 0, T_PULL0),
        caption("Ausatmen – Ellbogen nach hinten ziehen", T_PULL0, T_PULL1),
        caption("Schulterblätter zusammen – kurz halten", T_PULL1, T_HOLD1),
        caption("Einatmen – langsam zurück", T_HOLD1, T_END),
    ]
    return render(prims, tl, SIDE, fps=15, title="Vertical Row (Rudern an der Maschine)")
