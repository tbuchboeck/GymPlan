from rig import *
from exercises._gymgeraete_props import *

SLUG = "laufband"

# Seitansicht, Blick nach rechts. Echter Gangzyklus: Standbein klebt am Band
# (Fuß wandert mit Bandgeschwindigkeit nach hinten), Ferse setzt auf, Fuß rollt
# ab, Zehen drücken ab; Schwungbein schwingt angehoben nach vorn. Becken
# federt leicht, Arme pendeln gegengleich. Band-Markierungen laufen exakt mit
# der Geschwindigkeit der Standfüße.

DECK_Y = 232                    # Oberkante Band
GY = DECK_Y - 8                 # Höhe der Fußgelenke beim flachen Fuß
HX = 186.0                      # Becken (x fix, Person bleibt am Platz)
CYCLE = 1.2                     # Doppelschritt in s (zügiges Gehen)
N_CYC = 4
DUR = CYCLE * N_CYC
STANCE = 0.6
S = 29.0                        # halbe Schrittlänge (Fußgelenk vor/hinter Becken)
FL = 20.0                       # Fußlänge im Skelett
V = 2 * S / (STANCE * CYCLE)    # Bandgeschwindigkeit px/s
LEG = 97.6


def foot_state(phi):
    """(Fußgelenk x, y, absoluter Fußwinkel) für Phase 0..1 (0 = Fersenkontakt)."""
    phi %= 1.0
    if phi < STANCE:
        s = phi / STANCE
        g = HX + S - 2 * S * s
        if s < 0.12:
            a = 16 * (1 - smooth(s / 0.12))
            return g, GY, a                      # Ferse = Drehpunkt
        if s < 0.62:
            return g, GY, 0.0
        a = -42 * smooth((s - 0.62) / 0.38)       # Ferse hebt ab, Zehen am Band
        tx = g + FL
        r = math.radians(a)
        return tx - FL * math.cos(r), GY + FL * math.sin(r), a
    w = (phi - STANCE) / (1 - STANCE)
    x0, y0, a0 = foot_state(STANCE - 1e-6)
    x1, y1, a1 = HX + S, GY, 16.0
    k = smooth(w)
    x = x0 + (x1 - x0) * k
    y = y0 + (y1 - y0) * k - 15 * math.sin(math.pi * min(1, w * 1.1))
    a = a0 + (a1 - a0) * smooth(min(1, w * 1.25))
    return x, y, a


class GaitTimeline(Timeline):
    def __init__(self):
        super().__init__([(0, {}), (DUR, {})], skeleton=SIDE)

    def at(self, t):
        ph = (t / CYCLE) % 1.0
        n = foot_state(ph)
        f = foot_state(ph + 0.5)
        hy = GY - 94.0 - 2.2 * math.cos(4 * math.pi * (ph - STANCE / 2))
        for ax, ay, _ in (n, f):
            dx = ax - HX
            hy = max(hy, ay - math.sqrt(max(0.0, LEG ** 2 - dx * dx)))
        swing = math.cos(2 * math.pi * ph)        # +1 = nahes Bein vorn
        p = dict(x=HX, y=hy, rot=-4, neck=5, head=1,
                 upperarm_n=-22 * swing + 3, forearm_n=24 + 16 * max(0, -swing),
                 upperarm_f=22 * swing + 3, forearm_f=24 + 16 * max(0, swing),
                 thorax=1.5 * swing, chest=-1.5 * swing)
        for side, (ax, ay, a) in (("n", n), ("f", f)):
            p = solve_ik(SIDE, p, IK(f"thigh_{side}", f"shin_{side}", (ax, ay), bend=1,
                                      end_seg=f"foot_{side}", end_abs=a))
        return p


def treadmill_back() -> list[Prim]:
    return [
        # Seitenwange/Deck
        rect(58, DECK_Y - 2, 280, 14, PROP_DARK, 7),
        # Motorhaube vorn
        rect(300, DECK_Y - 14, 52, 26, PROP, 9),
        # Füße
        rect(70, DECK_Y + 10, 16, 8, PROP_DARK, 3), rect(316, DECK_Y + 10, 22, 8, PROP_DARK, 3),
        # Säule + Konsole
        line(334, DECK_Y - 10, 318, 112, PROP_DARK, 10),
        poly([(300, 96), (340, 92), (346, 112), (300, 118)], PROP_DARK, 3, fill=PROP),
        rect(306, 100, 26, 10, "#0b1220", 2),
        Prim("text", {"x": 319, "y": 108.5, "font-size": 8, "fill": GOOD, "text-anchor": "middle",
                      "font-weight": "700"}, text="5.5"),
        # ferner Handlauf
        poly([(318, 124), (262, 140), (248, 146)], "#3a4659", 6),
    ]


def belt() -> list[Prim]:
    x0, x1 = 70, 326
    return [
        line(x0, DECK_Y + 1, x1, DECK_Y + 1, "#1f2937", 5),
        Prim("line", {"x1": x0, "y1": DECK_Y + 1, "x2": x1, "y2": DECK_Y + 1, "stroke": "#7c8aa0",
                      "stroke-width": 3, "stroke-dasharray": "6 14"},
             lambda c: {"stroke-dashoffset": V * c["t"]}),
        circle(x0, DECK_Y + 5, 6, PROP, stroke=PROP_DARK, **{"stroke-width": 2}),
        circle(x1 - 4, DECK_Y + 5, 6, PROP, stroke=PROP_DARK, **{"stroke-width": 2}),
    ]


def build():
    tl = GaitTimeline()
    near_rail = [poly([(320, 128), (266, 144), (252, 150)], PROP_DARK, 7),
                 poly([(320, 128), (266, 144), (252, 150)], PROP, 3)]
    figure = side_fig(extras_behind=treadmill_back() + belt(), extras_front=near_rail)
    T = [0, 1.6, 3.2, DUR]
    scene = group([
        *figure,
        focus("foot_n", rx=15, ry=8, offset=(6, 2), end=False, show=[(T[1], T[2])]),
        focus("forearm_n", rx=10, ry=10, end=False, show=[(T[2], T[3])]),
    ], scale=0.84, origin=(200, 246), dx=4)
    prims = [
        scene,
        caption_band(),
        caption("Aufrecht gehen, Blick nach vorn", T[0], T[1]),
        caption("Ferse aufsetzen – über den Fuß abrollen", T[1], T[2]),
        caption("Arme schwingen gegengleich mit", T[2], T[3]),
        static_text("20 Min zügig gehen – nicht am Geländer hängen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, fps=15, title="Laufband")
