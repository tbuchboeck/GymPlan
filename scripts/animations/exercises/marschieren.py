from rig import *

SLUG = "marschieren"

# Aufwärmen: am Stand marschieren, Seitansicht (Blick nach rechts).
# Abwechselnd ein Knie locker anheben, der gegengleiche Arm schwingt nach
# vorn. Standbein bleibt gestreckt und der Fuß fix am Boden; Becken ruhig.

FLOOR_Y = 246
CX = 196.0
PELVIS_Y = FLOOR_Y - 8.0 - 98.0
SCALE = 0.84

STAND = dict(x=CX, y=PELVIS_Y, rot=-1, neck=3, head=-1,
             upperarm_n=2, forearm_n=12, upperarm_f=2, forearm_f=12)


def lift(k):
    o = "f" if k == "n" else "n"
    return dict(STAND, y=PELVIS_Y - 1.5, **{
        "thigh_" + k: 68, "shin_" + k: -84, "foot_" + k: -14,
        "upperarm_" + o: 30, "forearm_" + o: 34,       # Gegenarm vorn
        "upperarm_" + k: -24, "forearm_" + k: 14,      # gleichseitiger Arm hinten
        "chest": -1})


N_UP, F_UP = lift("n"), lift("f")


def build():
    keys = []
    t = 0.0
    for _ in range(2):
        keys += [(t, STAND), (t + 0.55, N_UP), (t + 0.85, N_UP), (t + 1.4, STAND),
                 (t + 1.95, F_UP), (t + 2.25, F_UP)]
        t += 2.8
    keys.append((t, STAND))
    tl = Timeline(keys, skeleton=SIDE)
    dur = tl.duration

    kn = pt(SIDE.fk(N_UP), "thigh_n")
    kf = pt(SIDE.fk(F_UP), "thigh_f")
    a_n = arrow(f"M{kn[0] + 4:.0f} {kn[1] + 44:.0f} Q{kn[0] + 20:.0f} {kn[1] + 26:.0f} {kn[0] + 16:.0f} {kn[1] - 2:.0f}",
                show=[(0.05, 0.6), (2.85, 3.4)])
    a_f = arrow(f"M{kf[0] + 4:.0f} {kf[1] + 44:.0f} Q{kf[0] + 20:.0f} {kf[1] + 26:.0f} {kf[0] + 16:.0f} {kf[1] - 2:.0f}",
                show=[(1.45, 2.0), (4.25, 4.8)])
    relax = focus("lumbar", rx=8, ry=12, offset=(-10, 0), color=GOOD, end=False, show=[(2.8, dur)])
    shadow = Prim("ellipse", {"cx": CX + 6, "cy": FLOOR_Y + 1, "rx": 30, "ry": 4, "fill": "#0b1220",
                              "opacity": 0.5})

    scene = group([shadow, *side_figure(), relax, a_n, a_f], scale=SCALE, origin=(CX, FLOOR_Y))
    prims = [
        floor(FLOOR_Y, 40, 360),
        scene,
        caption_band(),
        static_text("Locker marschieren – ruhig atmen", 200, 22, LEAD_SIZE, MUTED),
        caption("Knie locker anheben", 0, 1.4),
        caption("Gegenarm schwingt mit", 1.4, 2.8),
        caption("Aufrecht, Rücken entspannt", 2.8, 4.2),
        caption("Ruhig atmen – im eigenen Tempo", 4.2, dur),
    ]
    return render(prims, tl, SIDE, fps=15, title="Am Stand marschieren")
