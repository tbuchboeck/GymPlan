from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "side-plank-knee"

# Frontansicht einer seitlich liegenden Figur (Kopf rechts, Gesicht zum
# Betrachter). R (Bildschirm) = untere Körperseite. Unteres Knie bleibt fix
# am Boden, der Ellenbogen bleibt unter der Schulter. Skalar "lift" 0..1:
# 0 = Becken hängt auf der Matte, 1 = Schulter–Hüfte–Knie eine Linie.
FLOOR_Y = 236
KNEE = (112, FLOOR_Y - 9)        # unteres Knie (fix)
SH_Y = FLOOR_Y - 8 - 36          # Schulterhöhe: Oberarm senkrecht auf Ellenbogen


def d(a, l):
    r = math.radians(a)
    return l * math.cos(r), -l * math.sin(r)


def place(alpha, th):
    """Wurzel so, dass das untere Knie auf KNEE liegt."""
    tx, ty = d(th, 50)
    hx, hy = d(alpha - 90, 15)
    return KNEE[0] - tx - hx, KNEE[1] - ty - hy


def shoulder_y(alpha, th, bend):
    x, y = place(alpha, th)
    p = dict(x=x, y=y, rot=alpha - 90, lumbar=bend, thorax=bend * 0.5)
    P = FRONT.fk(p)
    return pt(P, "clav_R")[1]


def solve_alpha(th, bend):
    lo, hi = 0.0, 80.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if shoulder_y(mid, th, bend) > SH_Y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


TH_UP = None


def pre(p):
    lift = p.get("lift", 0.0)
    # gerade Linie: Oberschenkel in Rumpfrichtung; abgelegt: Oberschenkel flach, Taille knickt
    bend = -14 * (1 - lift)
    th_flat = 186.0
    a_up = solve_alpha(180 + 21, 0)          # Startwert für die Linie
    th = th_flat + (180 + a_up - th_flat) * lift
    a = solve_alpha(th, bend)
    x, y = place(a, th)
    p.update(x=x, y=y, rot=a - 90, lumbar=bend, thorax=bend * 0.5, chest=0)
    # Oberschenkel absolut setzen (Eltern: hip_*)
    set_abs(FRONT, p, "thigh_R", th)
    set_abs(FRONT, p, "thigh_L", th + 2)
    set_abs(FRONT, p, "shin_R", th + 90)   # nach hinten gebeugt (wird kurz gezeichnet)
    set_abs(FRONT, p, "shin_L", th + 90)
    # unterer Arm: Oberarm senkrecht nach unten auf den Ellenbogen
    set_abs(FRONT, p, "upperarm_R", -90)
    set_abs(FRONT, p, "neck", a - 4)
    set_abs(FRONT, p, "head", a - 6)
    p["turn"] = 0.0
    return p


def hand_on_hip(p):
    P = FRONT.fk(p)
    x, y = pt(P, "hip_L")
    return x + 10, y - 6


IKS = [IK("upperarm_L", "forearm_L", hand_on_hip, bend=-1)]

DOWN = dict(lift=0.0)
UP = dict(lift=1.0)
T0, T1, T2, T3, END = 0.8, 2.8, 8.8, 10.8, 12.4


def build():
    tl = FnTimeline([(0, DOWN), (T0, DOWN), (T1, UP), (T2, UP), (T3, DOWN), (END, DOWN)],
                    iks=IKS, skeleton=FRONT, pre=pre)

    def shin_stub(side, col, w):
        # Unterschenkel zeigt nach hinten (vom Betrachter weg): verkürzt
        def f(c):
            P = c["P"]
            kx, ky = pt(P, f"thigh_{side}")
            a = P[f"thigh_{side}"][4]
            ex, ey = d(a + 90 + 180, 0)  # Platzhalter
            dx, dy = d(a + 125, 16)
            return {"d": f"M{kx:.1f} {ky:.1f}L{kx + dx:.1f} {ky + dy:.1f}"}
        return [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round"}, f),
                Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round"}, f)]

    def forearm(c):
        # unterer Unterarm liegt auf der Matte, zeigt schräg nach vorn
        ex, ey = pt(c["P"], "upperarm_R")
        return {"d": f"M{ex:.1f} {ey + 1:.1f}L{ex + 30:.1f} {ey + 3:.1f}"}

    def fist(c):
        ex, ey = pt(c["P"], "upperarm_R")
        return {"cx": ex + 33, "cy": ey + 3}

    fore = [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 16, "stroke-linecap": "round"}, forearm),
            Prim("path", {"fill": "none", "stroke": FAR, "stroke-width": 13, "stroke-linecap": "round"}, forearm)]
    fig = [
        *shin_stub("R", FAR, 14), *limb(["hip_R", "thigh_R"], 16, FAR),
        *fore,
        *limb(["clav_R", "upperarm_R"], 13, FAR),
    ]
    # Rumpf (Front-Figur ohne Beine, eigene Arm-Reihenfolge)
    trunk = limb(["lumbar", "thorax", "chest"], 40, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    fig += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 25, "stroke-linecap": "round"}, sh),
            trunk[0], *limb(["neck"], 13, TORSO),
            Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"}, sh),
            trunk[1]]
    fig += head_front()
    fig += [*shin_stub("L", NEAR, 15), *limb(["hip_L", "thigh_L"], 16, NEAR)]
    fig += limb(["upperarm_L", "forearm_L"], 12, NEAR)

    p_dn = tl.at(0)

    def line_pts(c):
        P = c["P"]
        return pt(P, "thigh_R"), pt(P, "chest")

    S, OX = 1.25, 190
    scene = group([
        mat(FLOOR_Y, 50, 340),
        ghost(limb(["lumbar", "thorax", "chest"], 40, TORSO), FRONT, p_dn, 0.14),
        *fig,
        dyn_line(line_pts, show=[(T1, T2)]),
        focus("lumbar", rx=20, ry=11, offset=(0, 4), show=[(T0, T2)]),
        arrow("M176 222 L176 198", show=[(T0, T1)]),
        arrow("M176 196 L176 220", show=[(T2, T3)]),
    ], scale=S, origin=(OX, FLOOR_Y))

    def T(x, y):
        return OX + (x - OX) * S, FLOOR_Y + (y - FLOOR_Y) * S

    sx, sy = T(258, SH_Y - 26)
    ex, ey = T(256, FLOOR_Y)
    prims = [
        scene,
        label("Schulter weg vom Ohr", sx + 2, sy - 28, T1, T2, 11, ACCENT),
        arrow(f"M{sx + 34} {sy - 18} L{sx + 34} {sy + 2}", width=2.5, show=[(T1, T2)]),
        label("Ellenbogen unter Schulter", ex + 6, FLOOR_Y + 16, 0, T1, 11, GOOD),
        label("eine Linie", 150, 150, T1, T2, 12, GOOD),
        label("20–30 s halten", 150, 96, T1, T2, 16, ACCENT, weight="700"),
        label("ruhig weiter atmen", 150, 116, T1 + 1.5, T2, 12, TEXT),
        caption_band(),
        caption("Seitlage, Knie angewinkelt", 0, T0),
        caption("Becken anheben – Schulter, Hüfte, Knie", T0, T1),
        caption("Halten – Becken nicht kippen", T1, T2),
        caption("Kontrolliert absetzen", T2, T3),
        caption("Seite wechseln – beide Seiten!", T3, END),
        static_text("Schulter–Hüfte–Knie in einer Linie", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Seitstütz (Knie-Variante)", fps=12)
