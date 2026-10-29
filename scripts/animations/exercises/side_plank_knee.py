from rig import *
from exercises._ruecken_cardio_props import label, dyn_line

SLUG = "side-plank-knee"

# Frontansicht einer seitlich liegenden Figur (Kopf rechts, Gesicht zum
# Betrachter), als einfache 2D-Geometrie aus dem Skalar "lift" 0..1:
# 0 = Seitlage, auf den Unterarm gestützt, Becken liegt auf der Matte,
# 1 = Knie–Hüfte–Schulter eine Linie. Knie und Ellbogen bleiben fix, der
# Oberarm steht senkrecht unter der Schulter, der Unterarm liegt flach.

FLOOR_Y = 236
KNEE = (116.0, FLOOR_Y - 9)          # unteres Knie
ELBOW = (266.0, FLOOR_Y - 7)
UPPER = 50                           # Oberarm (senkrecht)
SB = (ELBOW[0], ELBOW[1] - UPPER)    # untere Schulter
SC = (SB[0] - 5, SB[1] - 17)         # Schulter-Mitte (Körperlinie)
ST = (SB[0] - 10, SB[1] - 34)        # obere Schulter
THIGH = 50
HALF_W = 10                          # halbe Rumpfbreite (schlank)


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    return dx / n, dy / n


def geo(p):
    lift = p.get("lift", 0.0)
    ux, uy = unit(KNEE, SC)
    up_line = (KNEE[0] + THIGH * ux, KNEE[1] + THIGH * uy)
    down = (KNEE[0] + 47, FLOOR_Y - 13)          # Becken liegt auf
    pc = (down[0] + (up_line[0] - down[0]) * lift, down[1] + (up_line[1] - down[1]) * lift)
    # Taille: abgelegt hängt sie zur Matte durch, oben gerade
    mid = ((pc[0] + SC[0]) / 2, (pc[1] + SC[1]) / 2)
    waist = (mid[0], mid[1] + 13 * (1 - lift))
    vx, vy = unit(pc, SC)
    nx, ny = vy, -vx                              # "oben" (zur Decke)
    G = dict(pc=pc, waist=waist, u=(vx, vy), n=(nx, ny))
    G["hip_t"] = (pc[0] + 9 * nx, pc[1] + 9 * ny)
    G["hip_b"] = (pc[0] - 7 * nx, pc[1] - 7 * ny)
    G["knee_t"] = (KNEE[0] + 4, KNEE[1] - 14)
    # oberer Arm: Hand auf der Hüfte
    hand = (G["hip_t"][0] + 10 * vx, G["hip_t"][1] + 10 * vy)
    m = ((ST[0] + hand[0]) / 2, (ST[1] + hand[1]) / 2)
    G["el_t"] = (m[0] + 30 * nx, m[1] + 30 * ny)       # Ellbogen zeigt zur Decke
    G["hand_t"] = hand
    a = math.degrees(math.atan2(-(SC[1] - pc[1]), SC[0] - pc[0]))
    G["ang"] = a
    G["head"] = (SC[0] + 34 * vx, SC[1] + 34 * vy)
    G["neck"] = (SC[0] + 14 * vx, SC[1] + 14 * vy)
    return G


_cache = {}


def G(c):
    k = id(c["pose"])
    if k not in _cache:
        _cache[k] = (c["pose"], geo(c["pose"]))
    return _cache[k][1]


def path(keys_or_fn, width, color, outline=True, sharp=False):
    def f(c):
        pts = keys_or_fn(c)
        if sharp:
            return {"d": "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}
        return {"d": smooth_path(pts)}
    out = []
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    return out


def static_path(pts, width, color):
    d = smooth_path(pts)
    return [Prim("path", {"d": d, "fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                          "stroke-linecap": "round", "stroke-linejoin": "round"}),
            Prim("path", {"d": d, "fill": "none", "stroke": color, "stroke-width": width,
                          "stroke-linecap": "round", "stroke-linejoin": "round"})]


def head():
    r = 16

    def at(c, fwd, side):
        g = G(c)
        x, y = g["head"]
        ux, uy = g["u"]
        nx, ny = g["n"]
        return x + r * (fwd * ux + side * nx), y + r * (fwd * uy + side * ny)

    def skull(c):
        x, y = G(c)["head"]
        return {"cx": x, "cy": y}

    def eye(s):
        return lambda c: dict(zip(("cx", "cy"), at(c, 0.12, s * 0.36)))

    def mouth(c):
        a, b = at(c, -0.4, 0.22), at(c, -0.4, -0.22)
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}"}

    return [Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
            Prim("circle", {"r": r, "fill": HEAD}, skull),
            Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(1)),
            Prim("circle", {"r": 2.4, "fill": SKIN_LINE}, eye(-1)),
            Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linecap": "round"}, mouth)]


DOWN = dict(lift=0.0)
UP = dict(lift=1.0)
T0, T1, T2, T3, END = 1.0, 3.0, 9.0, 11.0, 12.4


def build():
    tl = Timeline([(0, DOWN), (T0, DOWN), (T1, UP), (T2, UP), (T3, DOWN), (END, DOWN)])
    ex, ey = ELBOW
    fig = [
        # Unterschenkel zeigen nach hinten (verkürzt)
        *static_path([KNEE, (KNEE[0] - 12, KNEE[1] + 3)], 13, FAR),
        *static_path([(KNEE[0] + 4, KNEE[1] - 14), (KNEE[0] - 9, KNEE[1] - 13)], 13, FAR),
        # untere Seite: Oberschenkel, Unterarm flach, Oberarm senkrecht
        *path(lambda c: [KNEE, G(c)["hip_b"]], 17, FAR),
        *static_path([(ex, ey), (ex + 34, ey + 1)], 12, FAR),
        Prim("circle", {"cx": ex + 38, "cy": ey + 1, "r": 7, "fill": FAR, "stroke": SKIN_LINE, "stroke-width": 1.5}),
        *static_path([SB, (ex, ey)], 13, FAR),
        # Rumpf schlank, Schulterlinie senkrecht gestapelt
        *path(lambda c: [G(c)["pc"], G(c)["waist"], SC], 2 * HALF_W + 6, TORSO),
        *static_path([SB, ST], 18, TORSO),
        *path(lambda c: [SC, G(c)["neck"]], 12, TORSO),
        *head(),
        # obere Seite
        *path(lambda c: [G(c)["knee_t"], G(c)["hip_t"]], 17, NEAR),
        *path(lambda c: [ST, G(c)["el_t"], G(c)["hand_t"]], 12, NEAR, sharp=True),
    ]
    p_dn = tl.at(0)
    ghost_body = ghost(path(lambda c: [G(c)["pc"], G(c)["waist"], SC], 2 * HALF_W + 6, TORSO)
                       + path(lambda c: [KNEE, G(c)["hip_b"]], 17, FAR), SIDE, p_dn, 0.16)

    S, OX = 1.2, 200
    gpc_up = geo(UP)["pc"]
    scene = group([
        mat(FLOOR_Y, 50, 350),
        ghost_body,
        *fig,
        dyn_line(lambda c: (KNEE, SC), show=[(T1, T2)]),
        Prim("ellipse", {"rx": 18, "ry": 10, "fill": ACCENT, "opacity": 0.35, "_pulse": True, "_show": [(T0, T2)]},
             lambda c: dict(zip(("cx", "cy"), G(c)["waist"]))),
        arrow(f"M{gpc_up[0] + 22:.0f} {FLOOR_Y - 6} L{gpc_up[0] + 22:.0f} {gpc_up[1] - 18:.0f}", show=[(T0, T1)]),
        arrow(f"M{gpc_up[0] + 22:.0f} {gpc_up[1] - 18:.0f} L{gpc_up[0] + 22:.0f} {FLOOR_Y - 6}", show=[(T2, T3)]),
    ], scale=S, origin=(OX, FLOOR_Y))

    def T(x, y):
        return OX + (x - OX) * S, FLOOR_Y + (y - FLOOR_Y) * S

    lx, ly = T(ex + 22, ey)
    prims = [
        scene,
        label("Ellbogen unter", lx + 2, 186, 0, T1, 12, GOOD, anchor="start"),
        label("der Schulter", lx + 2, 200, 0, T1, 12, GOOD, anchor="start"),
        Prim("path", {"d": f"M{lx + 8:.0f} 206 L{T(ex, ey)[0] + 8:.0f} {T(ex, ey)[1] - 10:.0f}", "stroke": GOOD,
                      "stroke-width": 1.5, "fill": "none", "opacity": 0.8, "_show": [(0, T1)]}),
        label("Schulter weg", 352, 70, T1, T2, 12, ACCENT),
        label("vom Ohr", 352, 84, T1, T2, 12, ACCENT),
        label("eine Linie", 84, 196, T1, T2, 12, GOOD),
        label("20–30 s halten", 110, 84, T1, T2, 16, ACCENT, weight="700"),
        label("ruhig weiter atmen", 110, 104, T1 + 1.5, T2, 12, TEXT),
        caption_band(),
        caption("Seitlage, auf den Unterarm gestützt", 0, T0),
        caption("Becken anheben – Knie, Hüfte, Schulter", T0, T1),
        caption("Halten – Becken nicht kippen", T1, T2),
        caption("Kontrolliert absetzen", T2, T3),
        caption("Seite wechseln – beide Seiten!", T3, END),
        static_text("Schulter–Hüfte–Knie in einer Linie", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Seitstütz (Knie-Variante)", fps=10)
