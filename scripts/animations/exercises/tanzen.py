from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "dancing"

# Frontansicht, fröhliches freies Tanzen: drei Moves im Loop (je 2 s, 120 bpm):
# 1) Step-Touch zur Seite mit Armschwung, 2) Arme hoch und mitwippen,
# 3) Disco-Point (Hand an der Hüfte). Füße bleiben per IK am Boden und
# heben sich nur beim Schritt (Hub aus der Fußgeschwindigkeit).
FLOOR_Y = 250
CX = 200
FOOT_Y = FLOOR_Y - 12
HIP_Y = FLOOR_Y - 108
DIP = 7                         # Knie federn im Takt


def arms(uaL, faL, uaR, faR):
    """ua = Abduktion aus der Hängeposition, fa = Ellbogenbeugung (je Seite)."""
    return dict(upperarm_L=-uaL, forearm_L=-faL, upperarm_R=uaR, forearm_R=faR)


def P(t_x=0, dip=0, fl=-18, fr=18, tilt=0, turn=0.0, wL=0.0, **arm):
    p = dict(x=CX + t_x, y=HIP_Y + dip, fl=CX + fl, fr=CX + fr, lumbar=tilt, thorax=-tilt * 0.4,
             chest=-tilt * 0.3, neck=-tilt * 0.4, turn=turn, wL=wL)
    p.update(arm)
    return p


SWING_A = arms(30, 100, 10, 120)
SWING_B = arms(10, 120, 30, 100)
UP_A = arms(160, 25, 150, 35)
UP_B = arms(150, 35, 160, 25)
POINT_UP = arms(40, 60, 140, 0)
POINT_DN = arms(40, 60, 38, 0)

KEYS = [
    # 1) Step-Touch
    (0.0, P(dip=DIP, fl=-18, fr=18, **SWING_A)),
    (0.5, P(t_x=14, dip=0, fl=2, fr=34, tilt=-4, turn=0.3, **SWING_B)),
    (1.0, P(dip=DIP, fl=-18, fr=18, **SWING_A)),
    (1.5, P(t_x=-14, dip=0, fl=-34, fr=-2, tilt=4, turn=-0.3, **SWING_B)),
    (2.0, P(dip=DIP, fl=-18, fr=18, **SWING_A)),
    # 2) Arme hoch, mitwippen
    (2.5, P(t_x=6, dip=0, fl=-22, fr=22, tilt=-7, turn=0.2, **UP_A)),
    (3.0, P(t_x=0, dip=DIP, fl=-22, fr=22, tilt=0, **UP_B)),
    (3.5, P(t_x=-6, dip=0, fl=-22, fr=22, tilt=7, turn=-0.2, **UP_A)),
    (4.0, P(dip=DIP, fl=-20, fr=20, **SWING_A)),
    # 3) Disco-Point, linke Hand an der Hüfte
    (4.5, P(t_x=8, dip=0, fl=-22, fr=22, tilt=-6, turn=0.5, wL=1, **POINT_UP)),
    (5.0, P(t_x=-6, dip=DIP, fl=-22, fr=22, tilt=5, turn=-0.1, wL=1, **POINT_DN)),
    (5.5, P(t_x=8, dip=0, fl=-22, fr=22, tilt=-6, turn=0.5, wL=1, **POINT_UP)),
    (6.0, P(dip=DIP, fl=-18, fr=18, **SWING_A)),
]
DUR = 6.0


def hip_hand(p):
    Pk = FRONT.fk(p)
    x, y = pt(Pk, "hip_L")
    return x - 14, y - 10


def make_tl():
    holder = {}

    def foot_lift(key, t):
        tl = holder["tl"]
        a = tl._interp(max(0.0, t - 0.04)).get(key, 0)
        b = tl._interp(min(DUR, t + 0.04)).get(key, 0)
        return min(10.0, abs(b - a) * 0.9)

    def post(p):
        t = p["_t"]
        q = dict(p)
        q = solve_ik(FRONT, q, IK("thigh_L", "shin_L", (p["fl"], FOOT_Y - foot_lift("fl", t)), bend=1,
                                  end_seg="foot_L", end_abs=-90))
        q = solve_ik(FRONT, q, IK("thigh_R", "shin_R", (p["fr"], FOOT_Y - foot_lift("fr", t)), bend=-1,
                                  end_seg="foot_R", end_abs=-90))
        q = ik_blend(FRONT, q, IK("upperarm_L", "forearm_L", hip_hand, bend=1), p.get("wL", 0))
        return q

    tl = FnTimeline(KEYS, skeleton=FRONT, post=post)
    holder["tl"] = tl
    return tl


def note(x, y, delay, col, dur=DUR / 2, double=False):
    shape = [Prim("ellipse", {"cx": 0, "cy": 0, "rx": 5, "ry": 3.8, "fill": col, "transform": "rotate(-20)"}),
             Prim("line", {"x1": 4.3, "y1": -1, "x2": 4.3, "y2": -20, "stroke": col, "stroke-width": 2,
                           "stroke-linecap": "round"})]
    if double:
        shape += [Prim("ellipse", {"cx": 15, "cy": -4, "rx": 5, "ry": 3.8, "fill": col, "transform": "rotate(-20 15 -4)"}),
                  Prim("line", {"x1": 19.3, "y1": -5, "x2": 19.3, "y2": -24, "stroke": col, "stroke-width": 2,
                                "stroke-linecap": "round"}),
                  Prim("line", {"x1": 4.3, "y1": -20, "x2": 19.3, "y2": -24, "stroke": col, "stroke-width": 3.5,
                                "stroke-linecap": "round"})]
    else:
        shape.append(Prim("path", {"d": "M4.3 -20 Q12 -16 10 -8", "fill": "none", "stroke": col, "stroke-width": 2,
                                   "stroke-linecap": "round"}))
    anim = [Prim("animateTransform", {"attributeName": "transform", "type": "translate", "additive": "sum",
                                      "values": f"0 0;6 -34", "dur": f"{dur}s", "begin": f"{delay}s",
                                      "repeatCount": "indefinite"}),
            Prim("animate", {"attributeName": "opacity", "values": "0;0.85;0.85;0", "keyTimes": "0;0.2;0.7;1",
                             "dur": f"{dur}s", "begin": f"{delay}s", "repeatCount": "indefinite"})]
    return Prim("g", {"transform": f"translate({x} {y})", "opacity": 0}, children=anim + shape)


def build():
    tl = make_tl()
    S = 0.86
    scene = group([floor(FLOOR_Y, 70, 330), *front_figure()], scale=S, origin=(CX, FLOOR_Y))
    # Takt-Punkte: leuchten auf jedem Schlag
    beats = []
    for i in range(4):
        win = [(t, t + 0.25) for t in [k * 0.5 for k in range(12)] if int(round(t / 0.5)) % 4 == i]
        beats.append(Prim("circle", {"cx": 176 + i * 16, "cy": 46, "r": 3, "fill": FLOOR}))
        beats.append(Prim("circle", {"cx": 176 + i * 16, "cy": 46, "r": 3.5, "fill": ACCENT, "_show": win}))
    prims = [
        note(70, 110, 0.0, GOOD),
        note(318, 96, 1.0, ACCENT, double=True),
        note(92, 170, 1.9, "#f472b6", double=True),
        note(300, 168, 0.6, "#a5b4fc"),
        scene,
        *beats,
        caption_band(),
        caption("Step-Touch – locker zur Seite", 0, 2.0),
        caption("Arme hoch – im Takt mitwippen", 2.0, 4.0),
        caption("Disco-Point – einfach Spaß haben!", 4.0, DUR),
        static_text("Locker bewegen – Musik genießen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Tanzen", fps=15)
