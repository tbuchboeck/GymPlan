import math

from rig import *
from exercises._cardio_props import (ANKLE_UP, PostTimeline, ankle_for_toe, bez, figure, focus_mid,
                                     label, leg, scene_group)

SLUG = "knie-schritt"

# Ausfallschritt nach vorn, Seitansicht (Blick nach rechts). Erst schreitet das
# nahe Bein vor, dann das ferne. Der hintere Fuß bleibt mit den Zehen am Boden
# (Ferse hebt), der vordere Fuß setzt flach auf. Hände an der Hüfte.

FLOOR_Y = 250
SC = 0.86
AY = FLOOR_Y - ANKLE_UP
X0 = 128                       # Knöchel in der Grundstellung (nahes Bein)
DZ = 5                         # fernes Bein minimal versetzt
STEP = 120                     # Schrittlänge (Knöchel zu Knöchel)
SY = AY - 97.4                 # Beckenhöhe im Stand

HANDS = dict(upperarm_n=-32, forearm_n=80, hand_n=24, upperarm_f=-28, forearm_f=78, hand_f=24)
STAND = dict(HANDS, x=X0 - 3, y=SY, sn=0, sf=0, hn=0, hf=0)


def lunge_keys(t0, front, back):
    """Schlüsselposen eines Ausfallschritts ab t0 mit Bein front vor."""
    s, h = f"s{front}", f"h{back}"
    off = 0 if front == "n" else -DZ
    plant = dict(STAND, x=X0 + 38 + off, y=SY + 6, rot=-2, **{s: 1, h: -22})
    bottom = dict(STAND, x=X0 + STEP - 46 + off, y=AY - 57, rot=-4, neck=2, **{s: 1, h: -58})
    return [(t0 + 0.4, STAND), (t0 + 1.3, plant), (t0 + 2.2, bottom), (t0 + 2.8, bottom),
            (t0 + 3.6, plant), (t0 + 4.4, STAND)]


def swing_ankle(x_from, s):
    p0 = (x_from, AY)
    p3 = (x_from + STEP, AY)
    return bez(p0, (x_from + 20, AY - 26), (p3[0] - 34, AY - 20), p3, s)


def post(p):
    p = dict(p)
    for side, xs in (("n", X0), ("f", X0 - DZ)):
        s = p.get(f"s{side}", 0.0)
        h = p.get(f"h{side}", 0.0)
        if s > 1e-3:   # schwingt / steht vorn
            ank = swing_ankle(xs, s)
            fa = 14 * math.sin(math.pi * min(1.0, s))
            p = leg(p, side, ank, fa, bend=1)
        else:          # hinten bzw. Grundstellung: Zehen bleiben, Ferse hebt
            toe = (xs + 20, AY)
            p = leg(p, side, ankle_for_toe(toe, h), h, bend=1)
    return p


def build():
    keys = [(0, STAND)] + lunge_keys(0, "n", "f") + lunge_keys(4.4, "f", "n")
    keys.append((9.0, STAND))
    tl = PostTimeline(keys, post)

    knee_line = Prim("line", {"stroke": GOOD, "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.75,
                              "_show": [(1.8, 3.0), (6.2, 7.4)]},
                     lambda c: (lambda kx: {"x1": kx, "y1": FLOOR_Y - 4, "x2": kx, "y2": FLOOR_Y - 112})(
                         c["P"]["shin_n" if c["t"] < 4.4 else "shin_f"][2]))
    fig = figure()
    scene = scene_group([
        ghost(figure(), SIDE, post(STAND), 0.12),
        knee_line,
        *fig,
        focus_mid("thigh_n", 0.45, 20, 9, show=[(1.3, 3.6)]),
        focus_mid("thigh_f", 0.45, 20, 9, show=[(5.7, 8.0)]),
        focus("root", rx=12, ry=12, offset=(-8, 2), show=[(2.2, 3.6), (6.6, 8.0)]),
        arrow("M172 196 Q210 180 250 194", show=[(0.4, 1.3), (4.8, 5.7)]),
        arrow("M246 120 L246 148", show=[(1.3, 2.2), (5.7, 6.6)]),
        arrow("M246 150 L246 122", show=[(2.8, 3.6), (7.2, 8.0)]),
    ], SC, FLOOR_Y)
    prims = [
        floor(FLOOR_Y, 30, 370),
        scene,
        label("Rechts", 340, 60, 0.4, 4.4, 12, ACCENT),
        label("Links", 340, 60, 4.8, 8.8, 12, ACCENT),
        label("Knie über", 300, 226, 1.8, 3.0, 12, GOOD, "start"),
        label("dem Knöchel", 300, 240, 1.8, 3.0, 12, GOOD, "start"),
        label("Knie über", 300, 226, 6.2, 7.4, 12, GOOD, "start"),
        label("dem Knöchel", 300, 240, 6.2, 7.4, 12, GOOD, "start"),
        caption_band(),
        caption("Aufrecht stehen, Hände an die Hüfte", 0, 0.4),
        caption("Großer Schritt nach vorn", 0.4, 1.3),
        caption("Absenken – hinteres Knie zum Boden", 1.3, 2.2),
        caption("Kurz halten – Oberkörper aufrecht", 2.2, 2.8),
        caption("Über die vordere Ferse zurück", 2.8, 4.4),
        caption("Seitenwechsel: anderes Bein vor", 4.4, 5.7),
        caption("Absenken – hinteres Knie zum Boden", 5.7, 6.6),
        caption("Kurz halten – Oberkörper aufrecht", 6.6, 7.2),
        caption("Über die vordere Ferse zurück", 7.2, 9.0),
        static_text("Oberkörper aufrecht – vorderes Knie über dem Knöchel", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Knie Schritt (Ausfallschritt)")
