from rig import *
from exercises._morgen_props import (FnTimeline, Front3D, nose_badge, nose_note, top_inset, TAU)

SLUG = "hip-twist-hops"

# Frontansicht. Kleine Hopser: in der Luft drehen Hüfte/Beine (Fußspitzen,
# Gürtellinie, Nabel) zur einen Seite, der Oberkörper (Schulterlinie,
# Brustbein) zur anderen. Weich landen, kurz federn. Draufsicht-Inset zeigt
# die Gegenrotation.

FLOOR_Y = 250
CX = 186
SC = 0.8
HALF = 1.2                  # ein Hopser
DUR = 2 * HALF
ANK_Y = FLOOR_Y - 15
PEL_Y = ANK_Y - 95
HIP = 34                    # Beckendrehung
SHO = 26                    # Gegendrehung Schultern
HOP = 13                    # Sprunghöhe (px, vor Skalierung)
FLY = 0.5                   # Anteil Flugphase


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def hop_state(t):
    """-> (air 0..1, side -1..1 aktuelle Drehung, knee 0..1 Federn)."""
    k = int(t // HALF) % 2
    u = (t % HALF) / HALF
    frm, to = (-1, 1) if k == 0 else (1, -1)
    if u < FLY:
        v = u / FLY
        air = math.sin(math.pi * v)
        side = frm + (to - frm) * smooth((v - 0.1) / 0.8)
        knee = max(0.0, 1 - v * 3) * 0.5     # Absprung aus leichter Beuge
    else:
        v = (u - FLY) / (1 - FLY)
        air = 0.0
        side = to
        knee = math.sin(math.pi * min(1.0, v * 1.25))  # weich landen, federn
        if v > 0.8:
            knee = max(knee, 0.5 * (v - 0.8) / 0.2)    # Ausholen zum nächsten Hopser
    return air, side, knee


def pose_at(t):
    air, side, knee = hop_state(t)
    hy, sy = HIP * side, -SHO * side
    lift = air * HOP
    drop = knee * 9
    pose = dict(x=CX, y=PEL_Y - lift + drop, hy=hy, sy=sy, toe_out=6, toe_len=22,
                ank_y=ANK_Y - lift, turn=0.35 * math.sin(math.radians(sy)) * 2)
    for key, s in (("L", -1), ("R", 1)):
        dx = s * 16 * math.cos(math.radians(hy))
        pose["ank%s_x" % key] = CX + dx
        pose["ank%s_z" % key] = -s * 16 * math.sin(math.radians(hy))
        # Arme locker angewinkelt vor dem Körper, leicht mitschwingend
        pose["ab%s1" % key] = 16 + 8 * air
        pose["fl%s1" % key] = 20
        pose["ab%s2" % key] = 34 + 10 * air
        pose["fl%s2" % key] = 60
    pose["air"] = air
    return pose


FIG = Front3D()


def build():
    tl = FnTimeline(pose_at, DUR, skeleton=FRONT)
    shadow = Prim("ellipse", {"cx": CX, "cy": FLOOR_Y, "ry": 5, "fill": "#000", "opacity": 0.28},
                  lambda c: {"rx": round(44 - 12 * c["pose"].get("air", 0.0), 1)})
    fig = group([shadow, *FIG.prims()], scale=SC, origin=(CX, FLOOR_Y))
    # Pfeile: Hüfte (unten) und Schultern (oben) gegenläufig, nur im Flug
    hip_y, sh_y = 150, 96
    w1 = [(0.05, HALF * FLY)]
    w2 = [(HALF + 0.05, HALF + HALF * FLY)]
    prims = [
        floor(FLOOR_Y, 40, 300),
        fig,
        arrow(f"M{CX - 34} {hip_y} Q{CX} {hip_y + 12} {CX + 34} {hip_y}", show=w1),
        arrow(f"M{CX + 34} {sh_y} Q{CX} {sh_y + 12} {CX - 34} {sh_y}", show=w1),
        arrow(f"M{CX + 34} {hip_y} Q{CX} {hip_y + 12} {CX - 34} {hip_y}", show=w2),
        arrow(f"M{CX - 34} {sh_y} Q{CX} {sh_y + 12} {CX + 34} {sh_y}", show=w2),
        *top_inset(342, 160, 38, lambda p: (p.get("hy", 0.0), p.get("sy", 0.0)),
                   hip_color=GOOD, sh_color=ACCENT, nose_color=TEXT, bar_w=1.4),
        Prim("line", {"x1": 300, "y1": 220, "x2": 314, "y2": 220, "stroke": ACCENT, "stroke-width": 7,
                      "stroke-linecap": "round"}),
        static_text("Oberkörper", 320, 224, 12, ACCENT, anchor="start", weight="600"),
        Prim("line", {"x1": 300, "y1": 238, "x2": 314, "y2": 238, "stroke": GOOD, "stroke-width": 7,
                      "stroke-linecap": "round"}),
        static_text("Hüfte/Beine", 320, 242, 12, GOOD, anchor="start", weight="600"),
        *nose_badge([(0, HALF, "in"), (HALF, DUR, "out")]),
        nose_note(),
        caption_band(),
        caption("Hüfte nach links – Oberkörper nach rechts", 0, HALF),
        caption("Hüfte nach rechts – Oberkörper nach links", HALF, DUR),
        static_text("Kleine Hopser – leichtfüßig landen, Knie weich", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, FRONT, title="Hip Twist Hops", fps=15)
