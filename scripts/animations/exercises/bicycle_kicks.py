from rig import *
from exercises._bauch_props import FLOOR_Y, PRONE, forearm_iks, mat_layer, stage

SLUG = "bicycle-kicks-prone"

# Bauchlage, Unterarmstütz. Tretbewegung wie beim Radfahren: ein Bein zieht an
# (Ferse Richtung Po), das andere streckt lang nach hinten – im Wechsel.
# Oberschenkel schweben knapp über der Matte, Becken bleibt liegen.
T0, T1 = 0.9, 5.7      # Tretphase
CYCLE = 2.4
END = 6.6


def leg(phi, side):
    b = 0.5 - 0.5 * math.cos(phi)                 # Kniebeugung 0..1
    h = 0.5 - 0.5 * math.cos(phi - math.pi / 2)   # Oberschenkel heben 0..1
    return {f"thigh_{side}": -3 - 9 * h, f"shin_{side}": -86 * b, f"foot_{side}": -74 + 36 * b}


def cycle_pose(t):
    phi = 2 * math.pi * (t - T0) / CYCLE
    p = dict(PRONE)
    p.update(leg(phi, "n"))
    p.update(leg(phi + math.pi, "f"))
    return p


def env(t):
    if t <= T0 - 0.6 or t >= T1 + 0.6:
        return 0.0
    if t < T0:
        return smooth((t - (T0 - 0.6)) / 0.6)
    if t > T1:
        return 1 - smooth((t - T1) / 0.6)
    return 1.0


def keys():
    out = []
    n = int(END * 15)
    for i in range(n + 1):
        t = END * i / n
        c, e = cycle_pose(max(T0, min(T1, t))), env(t)
        out.append((t, {k: PRONE.get(k, 0.0) + (c.get(k, 0.0) - PRONE.get(k, 0.0)) * e for k in set(c) | set(PRONE)}))
    return out


def build():
    tl = Timeline(keys(), iks=forearm_iks(), skeleton=SIDE)
    # Weg der nahen Ferse als gestrichelte Schleife
    path_pts = []
    for i in range(25):
        P = SIDE.fk(cycle_pose(T0 + CYCLE * i / 24))
        path_pts.append(pt(P, "shin_n"))
    loop = Prim("path", {"d": smooth_path(path_pts + [path_pts[1]]), "fill": "none", "stroke": ACCENT,
                         "stroke-width": 1.5, "stroke-dasharray": "3 4", "opacity": 0.55, "_show": [(T0, T1)]})
    prims = [
        *stage([
            *mat_layer(),
            loop,
            *side_figure(),
            focus("root", rx=20, ry=7, offset=(-16, 8), end=False, show=[(T0, T1)]),
        ]),
        caption_band(),
        caption("Unterarme stützen, Beine lang", 0, T0 - 0.5),
        caption("Ein Bein anziehen, das andere strecken", T0 - 0.5, T0 + CYCLE),
        caption("Im Wechsel treten – wie Radfahren", T0 + CYCLE, T1 + 0.4),
        caption("Beine ablegen, lösen", T1 + 0.4, END),
        static_text("Ruhig treten – Becken bleibt auf der Matte", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, fps=15, title="Bicycle Kicks (Bauchlage)")
