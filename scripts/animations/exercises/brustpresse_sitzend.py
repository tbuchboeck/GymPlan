from rig import *
from exercises._tb_gym_props import *

SLUG = "brustpresse-sitzend"

# Brustpresse sitzend, Seitansicht (Blick nach rechts). Rücken am Polster,
# Griffe auf Brusthöhe. Die Griffe hängen an Hebelarmen (Drehpunkt oben),
# die beim Drücken nach vorn schwingen; der Gewichtsblock hinter der Lehne
# hebt sich mit. Schultern bleiben hinten (kein Vorschieben am Ende).

FLOOR_Y = 250
HIP = (150.0, 194.0)
ANK_N, ANK_F = (206.0, FLOOR_Y - 8.0), (200.0, FLOOR_Y - 8.0)
PIV = (190.0, 36.0)
GRIP_HALF = 10.0
W0, W1 = (167.0, 139.0), (211.0, 139.0)      # Handgelenk an der Brust / vorne
FAR_OFF = (-5.0, -1.5)


def _lever_geom():
    gx0, gy0 = W0[0], W0[1] - GRIP_HALF
    gx1, gy1 = W1[0], W1[1] - GRIP_HALF
    r0 = math.hypot(gx0 - PIV[0], gy0 - PIV[1])
    r1 = math.hypot(gx1 - PIV[0], gy1 - PIV[1])
    a0 = math.degrees(math.atan2(gx0 - PIV[0], gy0 - PIV[1]))
    a1 = math.degrees(math.atan2(gx1 - PIV[0], gy1 - PIV[1]))
    return (r0 + r1) / 2, a0, a1


LEVER, TH0, TH1 = _lever_geom()


def lever_end(p, far=False):
    th = math.radians(TH0 + (TH1 - TH0) * p)
    x, y = PIV[0] + LEVER * math.sin(th), PIV[1] + LEVER * math.cos(th)
    if far:
        x, y = x + FAR_OFF[0], y + FAR_OFF[1]
    return x, y


def post(pose, P):
    p = pose.get("push", 0.0)
    out = {"scap": 0.7}
    s = shoulder_side(P, 0.7)
    l1 = UA * (1 - 0.5 * (1 - p))      # Ellbogen seitlich -> Oberarm verkürzt
    for k, far in (("", False), ("_f", True)):
        lx, ly = lever_end(p, far)
        sk = (s[0] + FAR_OFF[0], s[1] + FAR_OFF[1]) if far else s
        w = clamp_reach(sk, (lx, ly + GRIP_HALF), l1 + FA - 0.5)
        e = ik2(sk, w, l1, FA, bend=-1)
        out.update({"sx" + k: sk[0], "sy" + k: sk[1], "ex" + k: e[0], "ey" + k: e[1],
                    "wx" + k: w[0], "wy" + k: w[1]})
    return out


BASE = dict(x=HIP[0], y=HIP[1], rot=2, neck=-1, head=0, push=0.0)
PUSH = dict(BASE, push=1.0)


def grip(far):
    def f(c):
        lx, ly = lever_end(c["pose"]["push"], far)
        return (lx, ly + 1, lx, ly + 2 * GRIP_HALF)
    return grip_line(f, 6, PROP_DARK if far else "#94a3b8")


def lever(far):
    def f(c):
        lx, ly = lever_end(c["pose"]["push"], far)
        return {"x1": PIV[0] + (FAR_OFF[0] if far else 0), "y1": PIV[1], "x2": lx, "y2": ly + 2}
    col = PROP_DARK if far else PROP
    return [Prim("line", {"stroke": "#0b1220", "stroke-width": 9, "stroke-linecap": "round"}, f),
            Prim("line", {"stroke": col, "stroke-width": 6, "stroke-linecap": "round"}, f)]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
    ]
    T0, T1, T2, T3, TE = 0.8, 2.2, 3.0, 4.8, 5.4
    tl = PostTimeline([(0, BASE), (T0, BASE), (T1, PUSH), (T2, PUSH), (T3, BASE), (TE, BASE)],
                      iks=iks, skeleton=SIDE, post=post)

    lift = lambda c: 26 * c["pose"]["push"]
    stack, stack_top = weight_stack(44, FLOOR_Y, 66, lift, n=11, w=34)

    frame = [
        R(36, 30, 172, 10, PROP_DARK, rx=4),                      # Querträger oben
        R(96, 34, 10, FLOOR_Y - 34, PROP_DARK, rx=3),             # Säule hinter der Lehne
        R(30, FLOOR_Y - 7, 120, 7, PROP_DARK, rx=3),
        L(61, 40, 61, stack_top - 2, "#cbd5e1", 2),
        *pulley(61, 44, 5),
    ]
    cam = [C(PIV[0], PIV[1], 11, PROP_DARK), C(PIV[0], PIV[1], 7.5, PROP), C(PIV[0], PIV[1], 2.5, PROP_DARK)]
    seat = [
        R(106, 150, 22, 6, PROP_DARK, rx=2),                      # Lehnenträger
        R(118, 96, 17, 108, "#0b1220", rx=7),                     # Rückenpolster
        R(119.5, 97.5, 14, 105, PROP, rx=6),
        R(112, 202, 70, 10, PROP, rx=5),                          # Sitz
        R(140, 212, 12, FLOOR_Y - 216, PROP_DARK, rx=2),
        R(112, FLOOR_Y - 7, 70, 7, PROP_DARK, rx=3),
    ]

    far_leg, torso, near_leg = side_body(head=False)
    figure = (far_leg + lever(True) + grip(True) + arm_prims("_f", far=True) + torso +
              lever(False) + head_side() + near_leg)
    front = grip(False) + arm_prims("", far=False) + cam

    c0, c1 = tl.at(0), tl.at(T1)
    ghost_arm = ghost(arm_prims("", far=False), SIDE, c0, 0.2)
    y_ar = max(c0["ey"], c1["ey"]) + 22
    push_arrow = arrow(f"M{c0['wx'] + 6:.0f} {y_ar:.0f} L{c1['wx'] + 10:.0f} {y_ar:.0f}", show=[(T0, T1)])
    pec = Prim("ellipse", {"rx": 9, "ry": 12, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                           "_show": [(T0, T3)]},
               lambda c: dict(zip(("cx", "cy"), body_pt(c["P"], "thorax", 16, 9))))
    lock = Prim("text", {"x": c1["wx"] + 14, "y": c1["wy"] - 14, "font-size": 12, "fill": WARN,
                         "text-anchor": "start", "_show": [(T1, T2)]}, text="nicht durchstrecken")

    prims = [
        floor(FLOOR_Y, 24, 380),
        *frame, *stack, *seat,
        *figure,
        ghost_arm,
        *front,
        pec,
        push_arrow, lock,
        caption_band(),
        static_text("Schultern bleiben hinten am Polster", 200, 22, LEAD_SIZE, MUTED),
        caption("Rücken ans Polster, Griffe auf Brusthöhe", 0, T0),
        caption("Ausatmen – nach vorne drücken", T0, T1),
        caption("Arme fast gestreckt – kurz halten", T1, T2),
        caption("Einatmen – kontrolliert zurück", T2, TE),
    ]
    return render(prims, tl, SIDE, fps=15, title="Brustpresse sitzend")
