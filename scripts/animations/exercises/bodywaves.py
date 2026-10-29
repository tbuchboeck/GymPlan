from rig import *
from exercises._morgen_props import FnTimeline, nose_badge, nose_note, TAU

SLUG = "bodywaves"

# Seitansicht, Blick nach rechts. Eine Welle läuft von unten nach oben:
# Becken -> LWS -> BWS -> Brust -> Hals. Jedes Segment schwingt mit
# Phasenversatz (absolute Neigung = A_i * sin(phi - i*delta)), die BWS-Segmente
# mit der größten Amplitude. Der Kopf bleibt fast waagrecht (kein Nicken).
# Füße flach am Boden (IK), Knie federn mit dem Becken, Arme hängen locker.

FLOOR_Y = 250
CX = 186
SC = 0.9
DUR = 4.0
ANKLE = (CX + 2, FLOOR_Y - 8)
DELTA = 1.0                         # Phasenversatz je Segment (rad)
# absolute Neigungs-Amplituden: Becken, LWS, BWS unten, BWS oben/Brust, Hals, Kopf
AMP = [10, 14, 24, 20, 9, 3]
NSEG = len(AMP)


def thetas(t):
    ph = TAU * t / DUR
    return [a * math.sin(ph - i * DELTA) for i, a in enumerate(AMP)], ph


def pose_at(t):
    th, ph = thetas(t)
    # positiver Winkel = gegen den Uhrzeigersinn = oberes Ende nach hinten.
    # Welle "schiebt nach vorn" => negativ.
    th = [-v for v in th]
    shift = 10 * math.sin(ph)                    # Becken vor/zurück
    pose = dict(x=ANKLE[0] - 4 + shift, y=ANKLE[1] - 92 + 2.5 * (1 + math.sin(ph)),
                rot=th[0], lumbar=th[1] - th[0], thorax=th[2] - th[1], chest=th[3] - th[2],
                neck=th[4] - th[3], head=th[5] - th[4] - 2)
    lag = math.sin(ph - 4 * DELTA)
    pose["upperarm_n"] = -th[3] + 5 * lag
    pose["forearm_n"] = 10 + 4 * lag
    pose["upperarm_f"] = -th[3] + 4 * lag - 3
    pose["forearm_f"] = 9 + 3 * lag
    pose["phase"] = ph
    return pose


def crest(t):
    """Segment-Index (kontinuierlich) des Wellenbergs, 0..2pi/DELTA."""
    ph = TAU * t / DUR
    return ((ph - math.pi / 2) % TAU) / DELTA


def t_of(i):
    return ((math.pi / 2 + i * DELTA) / TAU * DUR) % DUR


SPINE = ["lumbar", "thorax", "chest", "neck"]


def build():
    iks = [
        IK("thigh_n", "shin_n", ANKLE, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", (ANKLE[0] - 5, ANKLE[1]), bend=1, end_seg="foot_f", end_abs=0),
    ]
    tl = FnTimeline(pose_at, DUR, iks=iks, skeleton=SIDE)

    def wave_dot(c):
        """Leuchtpunkt am Rücken, der mit dem Wellenberg nach oben wandert."""
        i = crest(c["t"])
        P = c["P"]
        pts = chain_points(P, SPINE)            # 5 Punkte: Becken .. Kopfansatz
        k = min(max((i - 0.5) / (NSEG - 1) * (len(pts) - 1), 0), len(pts) - 1.001)
        j = int(k)
        f = k - j
        x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f
        y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f
        a = math.radians(P["thorax"][4] + 90)   # nach hinten (Rückenseite)
        vis = 1 if 0.3 <= i <= NSEG + 0.2 else 0
        return {"cx": x + 15 * math.cos(a), "cy": y - 15 * math.sin(a), "opacity": vis * 0.9}

    back_line = Prim("path", {"fill": "none", "stroke": ACCENT, "stroke-width": 2, "stroke-dasharray": "4 5",
                              "opacity": 0.7},
                     lambda c: {"d": smooth_path([(x - 14, y) for x, y in chain_points(c["P"], SPINE)])})
    neutral = dict(x=ANKLE[0] - 4, y=ANKLE[1] - 94)
    for ik in iks:
        neutral = solve_ik(SIDE, neutral, ik)
    # Blicklinie: Kopf bleibt ruhig
    gaze = Prim("line", {"stroke": GOOD, "stroke-width": 1.5, "stroke-dasharray": "3 4", "opacity": 0.7},
                lambda c: (lambda x, y, a: {"x1": x + 20, "y1": y - 1, "x2": x + 62,
                                            "y2": y - 1 - 42 * math.tan(math.radians(a - 90))})(
                    *pt(c["P"], "head"), c["P"]["head"][4]))
    fig = group([
        Prim("ellipse", {"cx": ANKLE[0] + 2, "cy": FLOOR_Y, "rx": 30, "ry": 4.5, "fill": "#000", "opacity": 0.28}),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO), SIDE, neutral, 0.13),
        *side_figure(),
        back_line,
        Prim("circle", {"r": 6, "fill": ACCENT}, wave_dot),
        gaze,
        focus("thorax", rx=10, ry=18, offset=(-10, 0), show=[(t_of(2), t_of(4))]),
    ], scale=SC, origin=(CX, FLOOR_Y))

    # Phasen nach Lage des Wellenbergs
    def win(i0, i1):
        a, b = t_of(i0), t_of(i1)
        return [(a, b)] if a < b else [(a, DUR), (0, b)]

    labels = [
        (0.0, 1.0, "Becken schiebt nach vorn"),
        (1.0, 2.0, "Welle über den Bauch …"),
        (2.0, 4.0, "… durch den mittleren Rücken"),
        (4.0, 5.2, "Brust – Nacken folgt locker"),
        (5.2, TAU / DELTA, "Kopf ruhig – kein Nicken"),
    ]
    caps = []
    for i0, i1, txt in labels:
        for a, b in win(i0, i1):
            caps.append(caption(txt, a, b))
    br_in = win(0.0, 3.2)
    br_out = win(3.2, TAU / DELTA)
    prims = [
        floor(FLOOR_Y, 60, 320),
        fig,
        static_text("Blick bleibt ruhig", 300, 92, 11, GOOD, anchor="middle"),
        *nose_badge([(a, b, "in") for a, b in br_in] + [(a, b, "out") for a, b in br_out]),
        nose_note(),
        caption_band(),
        *caps,
        static_text("Welle vor allem durch die BWS – kein Kopfnicken", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bodywaves", fps=15)
