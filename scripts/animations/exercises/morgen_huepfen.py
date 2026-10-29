from rig import *
from exercises._morgen_props import FnTimeline, nose_badge, nose_note, TAU

SLUG = "morgen-huepfen"

# Seitansicht, Blick nach rechts. Lockeres Hüpfen auf den Fußballen: Ballen
# bleiben am Kontaktpunkt (IK), Ferse hebt sich, Knie federn weich. Arme
# hängen locker und pendeln leicht nach. Atem synchron: beim Abdrücken und
# Hochgehen ein, beim Landen/Federn aus – Badge oben rechts.

FLOOR_Y = 250
CX = 190
SC = 0.8
HOP = 1.2                   # ein Hüpfer
DUR = 2 * HOP
TOE_X = CX + 16
TOE_Y = FLOOR_Y - 9         # Ballen (Strichende) liegt auf dem Boden
FOOT = 20
LEG = 98
HEIGHT = 14                 # Flughöhe (px vor Skalierung)
FLIGHT = 0.42               # Anteil Flugphase


def phase(t):
    """-> air (0..1), compress (0..1), foot_angle (abs, Grad)."""
    u = (t % HOP) / HOP
    if u < FLIGHT:
        v = u / FLIGHT
        air = math.sin(math.pi * v)
        comp = 0.0
        ang = -38 - 8 * air                     # Fuß gestreckt in der Luft
    else:
        v = (u - FLIGHT) / (1 - FLIGHT)
        air = 0.0
        comp = math.sin(math.pi * v) ** 1.2     # weich landen ... abdrücken
        ang = -38 + 14 * comp                   # Ferse sinkt etwas, bleibt aber oben
    return u, air, comp, ang


def pose_at(t):
    u, air, comp, ang = phase(t)
    a = math.radians(ang)
    lift = HEIGHT * air
    tx, ty = TOE_X, TOE_Y - lift
    ax, ay = tx - FOOT * math.cos(a), ty + FOOT * math.sin(a)
    # Becken: über dem Knöchel, beim Federn tiefer (Knie weich)
    py = ay - (LEG - 3) + 9 * comp
    px = ax - 6 - 2 * comp
    lag = math.sin(TAU * (t / HOP) - 1.9)          # Arme pendeln nach
    pose = dict(x=px, y=py, rot=-3 - 2 * comp, lumbar=1, thorax=1, chest=1,
                neck=1 + 1.5 * comp, head=1,
                upperarm_n=6 + 5 * lag, forearm_n=12 + 7 * lag, hand_n=6,
                upperarm_f=2 + 4 * lag, forearm_f=10 + 6 * lag, hand_f=6,
                ank_x=ax, ank_y=ay, foot_abs=ang, air=air, comp=comp)
    return pose


def post(p):
    P = SIDE.fk(p)
    p["foot_n"] = p["foot_abs"] - P["shin_n"][4] - 90
    p["foot_f"] = p["foot_abs"] - P["shin_f"][4] - 90
    return p


def build():
    iks = [
        IK("thigh_n", "shin_n", lambda p: (p["ank_x"], p["ank_y"]), bend=1),
        IK("thigh_f", "shin_f", lambda p: (p["ank_x"] - 5, p["ank_y"]), bend=1),
    ]
    tl = FnTimeline(pose_at, DUR, iks=iks, skeleton=SIDE, post=post)
    shadow = Prim("ellipse", {"cy": FLOOR_Y, "ry": 4.5, "fill": "#000", "opacity": 0.3},
                  lambda c: {"cx": TOE_X - 12, "rx": round(30 - 10 * c["pose"].get("air", 0.0), 1)})
    start = pose_at(HOP * (FLIGHT + (1 - FLIGHT) / 2))
    for ik in iks:
        start = solve_ik(SIDE, start, ik)
    start = post(start)
    fig = group([
        shadow,
        ghost(limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR), SIDE, start, 0.16),
        *side_figure(),
        focus("shin_n", rx=8, ry=14, offset=(-8, 22), end=False),
    ], scale=SC, origin=(CX, FLOOR_Y))
    # Fenster: ein = Abdrücken + Steigen, aus = Fallen + Landen/Federn
    rise_end = FLIGHT / 2
    push = FLIGHT + (1 - FLIGHT) / 2
    win_in, win_out = [], []
    for k in range(2):
        o = k * HOP
        win_out.append((o + rise_end * HOP, o + push * HOP))
    win_in = [(0, rise_end * HOP), (push * HOP, HOP + rise_end * HOP), (HOP + push * HOP, DUR)]
    # Auf/Ab-Pfeil neben der Figur
    ax = 120
    prims = [
        floor(FLOOR_Y, 60, 330),
        fig,
        arrow(f"M{ax} 150 L{ax} 128", show=[(a, b) for a, b in win_in]),
        arrow(f"M{ax} 128 L{ax} 150", show=[(a, b) for a, b in win_out]),
        *nose_badge([(a, b, "in") for a, b in win_in] + [(a, b, "out") for a, b in win_out]),
        nose_note(),
        static_text("Schultern locker unten", 270, 112, 11, GOOD, anchor="start"),
        caption_band(),
        *[caption("Hoch – durch die Nase einatmen", a, b) for a, b in win_in],
        *[caption("Weich landen – ausatmen", a, b) for a, b in win_out],
        static_text("Locker auf den Fußballen – Knie bleiben weich", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Lymphatisches Hüpfen", fps=15)
