from rig import *
from exercises._gymgeraete_props import *

SLUG = "ellipsentrainer"

# Seitansicht, Blick nach rechts. Echte Mechanik: hinten dreht eine Kurbel,
# die Pedalarme laufen von der Kurbel nach vorn zum unteren Ende der
# Schwinghebel (Kreis-Kreis-Schnitt pro Frame). Dadurch läuft das Pedal auf
# einer Ellipse, und der Griff oben am selben Hebel bewegt sich gegengleich
# zum Fuß derselben Seite (Fuß vorn -> Hand hinten). Füße stehen flach auf
# den Pedalen, Hände bleiben an den Griffen (IK).

FLOOR_Y = 248
C = (112.0, 214.0)             # Kurbel
RC = 24.0
V = (300.0, 146.0)             # Drehpunkt der Schwinghebel
LL = 58.0                      # Hebel unten (Drehpunkt -> Pedalarm)
LU = 86.0                      # Hebel oben (Drehpunkt -> Griff)
D = 196.0                      # Pedalarmlänge Kurbel -> Hebel
FR = 0.6                       # Pedal sitzt bei 60 % des Pedalarms
CYCLE = 1.6
N_CYC = 3
DUR = CYCLE * N_CYC
HX = 214.0
LEG = 97.0


def linkage(phi):
    """Kurbelwinkel -> (Kurbelpunkt K, Hebel unten L, Griff U, Pedal Pd, Armwinkel)."""
    K = (C[0] + RC * math.cos(phi), C[1] + RC * math.sin(phi))
    # Schnitt Kreis(V, LL) mit Kreis(K, D): unterer/vorderer Punkt
    dx, dy = V[0] - K[0], V[1] - K[1]
    d = math.hypot(dx, dy)
    a = (D * D - LL * LL + d * d) / (2 * d)
    h = math.sqrt(max(0.0, D * D - a * a))
    mx, my = K[0] + a * dx / d, K[1] + a * dy / d
    cands = [(mx + h * dy / d, my - h * dx / d), (mx - h * dy / d, my + h * dx / d)]
    L = max(cands, key=lambda p: p[1])
    U = (V[0] - (L[0] - V[0]) * LU / LL, V[1] - (L[1] - V[1]) * LU / LL)
    Pd = (K[0] + (L[0] - K[0]) * FR, K[1] + (L[1] - K[1]) * FR)
    ang = math.degrees(math.atan2(-(L[1] - K[1]), L[0] - K[0]))
    return K, L, U, Pd, ang


def ankle_on(Pd, ang):
    r = math.radians(ang)
    ux, uy = math.cos(r), -math.sin(r)        # entlang Pedalarm
    nx, ny = uy, -ux                          # senkrecht nach oben
    # Ferse etwas hinter Pedalmitte, Fußgelenk 12 px über dem Pedalarm
    return Pd[0] - 9 * ux + 12 * nx, Pd[1] - 9 * uy + 12 * ny


class EllipseTimeline(Timeline):
    def __init__(self):
        super().__init__([(0, {}), (DUR, {})], skeleton=SIDE)

    def at(self, t):
        phi = 2 * math.pi * t / CYCLE
        n = linkage(phi)
        f = linkage(phi + math.pi)
        an = ankle_on(n[3], n[4])
        af = ankle_on(f[3], f[4])
        hy = (an[1] + af[1]) / 2 - 92
        for ax, ay in (an, af):
            dx = ax - HX
            hy = max(hy, ay - math.sqrt(max(0.0, LEG ** 2 - dx * dx)))
        p = dict(x=HX, y=hy, rot=-3, neck=6, head=0, phi=phi)
        p["thorax"] = 2 * math.cos(phi)
        p = solve_ik(SIDE, p, IK("thigh_n", "shin_n", an, bend=1, end_seg="foot_n", end_abs=n[4]))
        p = solve_ik(SIDE, p, IK("thigh_f", "shin_f", (af[0] - 2, af[1]), bend=1, end_seg="foot_f",
                                 end_abs=f[4]))
        p = solve_ik(SIDE, p, IK("upperarm_n", "forearm_n", n[2], bend=-1))
        p = solve_ik(SIDE, p, IK("upperarm_f", "forearm_f", (f[2][0] - 3, f[2][1] + 1), bend=-1))
        return p


def lk(c, far):
    return linkage(c["pose"]["phi"] + (math.pi if far else 0.0))


def side_parts(far: bool) -> list[Prim]:
    col, w = ("#3a4659", 7) if far else (PROP, 6)
    out_c = "#2b3546" if far else PROP_DARK
    arm = lambda c: (lk(c, far)[0], lk(c, far)[1])
    lever = lambda c: (lk(c, far)[2], lk(c, far)[1])

    def pedal(c):
        K, L, U, Pd, ang = lk(c, far)
        r = math.radians(ang)
        ux, uy = math.cos(r), -math.sin(r)
        return ((Pd[0] - 16 * ux, Pd[1] - 16 * uy - 4), (Pd[0] + 18 * ux, Pd[1] + 18 * uy - 4))

    grip = lambda c: (lk(c, far)[2][0], lk(c, far)[2][1])
    return [
        dline(lever, out_c, w + 3), dline(lever, col, w),
        dline(arm, out_c, w + 3), dline(arm, col, w),
        dline(pedal, out_c, 8), dline(pedal, "#7c8aa0" if not far else "#4b5870", 5),
        dcircle(grip, 4.5, "#1f2937"),
    ]


def machine_back() -> list[Prim]:
    return [
        rect(70, FLOOR_Y - 8, 262, 9, PROP_DARK, 4),
        # Kurbelgehäuse hinten
        circle(C[0], C[1], 34, PROP_DARK),
        circle(C[0], C[1], 30, PROP),
        circle(C[0], C[1], 6, PROP_DARK),
        line(C[0], C[1] + 20, C[0] + 6, FLOOR_Y - 6, PROP_DARK, 12),
        # vordere Säule + Konsole
        line(318, FLOOR_Y - 6, V[0], V[1], PROP_DARK, 11),
        line(V[0], V[1], 310, 62, PROP_DARK, 8),
        poly([(292, 50), (326, 46), (332, 64), (294, 70)], PROP_DARK, 3, fill=PROP),
        rect(298, 53, 24, 9, "#0b1220", 2),
        circle(V[0], V[1], 7, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.5}),
    ]


def build():
    tl = EllipseTimeline()
    crank_dot = dcircle(lambda c: lk(c, False)[0], 4, "#94a3b8")
    figure = side_fig(extras_behind=machine_back() + side_parts(True) + [crank_dot],
                      extras_mid=side_parts(False))
    T = [0, 1.6, 3.2, DUR]
    ell = []
    for i in range(48):
        _, _, _, Pd, _ = linkage(2 * math.pi * i / 48)
        ell.append((Pd[0], Pd[1] - 4))
    path = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in ell) + "Z"
    scene = group([
        Prim("path", {"d": path, "fill": "none", "stroke": ACCENT, "stroke-width": 1.6,
                      "stroke-dasharray": "3 4", "opacity": 0.6, "_show": [(T[1], T[2])]}),
        *figure,
        focus_mid("thigh_n", 0.5, 16, 9, show=[(T[1], T[2])]),
        focus("forearm_n", rx=10, ry=10, end=False, show=[(T[2], T[3])]),
    ], scale=0.8, origin=(200, 248), dx=-4)
    prims = [
        scene,
        caption_band(),
        caption("Aufrecht, ganze Sohle auf den Pedalen", T[0], T[1]),
        caption("Gleichmäßig rund treten", T[1], T[2]),
        caption("Arme schieben & ziehen gegengleich", T[2], T[3]),
        static_text("5 Min locker aufwärmen – Fersen bleiben unten", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, fps=15, title="Ellipsentrainer")
