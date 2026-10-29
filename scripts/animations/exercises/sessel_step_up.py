import math

from rig import *
from exercises._cardio_props import (ANKLE_UP, PostTimeline, arms_level, bez, chair, figure, focus_mid,
                                     label, leg, scene_group)

SLUG = "sessel-step-up"

# Seitansicht (Blick nach rechts), Stuhl vor der Person, Lehne auf der
# abgewandten Seite. Erst führt das rechte (nahe) Bein, dann das linke.
# Füße per IK fix am Boden bzw. auf der Sitzfläche, Arme waagrecht vorn.

FLOOR_Y = 250
SC = 0.72
AY = FLOOR_Y - ANKLE_UP
SEAT_H = 56
CH_X = 170                     # linke Sitzkante
CH_D = 68
SEAT_Y = FLOOR_Y - SEAT_H      # Oberkante Sitz
SAY = SEAT_Y - 3 - ANKLE_UP    # Knöchelhöhe auf dem Sitz (Sitz ist 9 dick, -3 oben)
X0 = 132                       # Knöchel am Boden (nahes Bein)
SX = CH_X + 16                 # Knöchel auf dem Sitz (Fuß komplett auf der Fläche)
DZ = 4                         # fernes Bein minimal versetzt
SY = AY - 97.4

STAND = dict(x=X0 - 3, y=SY, sn=0, sf=0)
UP_Y = SAY - 97.4


def rep_keys(t0, lead, trail):
    L, T = f"s{lead}", f"s{trail}"
    off = 0 if lead == "n" else -DZ
    place = dict(STAND, x=X0 + 6, y=SY + 3, rot=-4, **{L: 1})
    drive = dict(STAND, x=SX - 8 + off, y=SAY - 92, rot=-12, neck=8, **{L: 1, T: 0.45})
    top = dict(STAND, x=SX - 2 + off, y=UP_Y, rot=0, **{L: 1, T: 1})
    lower = dict(STAND, x=SX - 24 + off, y=SAY - 80, rot=-10, neck=6, **{L: 1, T: 0})
    return [(t0 + 0.3, STAND), (t0 + 1.0, place), (t0 + 1.9, drive), (t0 + 2.4, top), (t0 + 2.8, top),
            (t0 + 3.7, lower), (t0 + 4.4, STAND), (t0 + 4.6, STAND)]


def swing(x_floor, x_seat, s):
    return bez((x_floor, AY), (x_floor + 4, SAY - 34), (x_seat - 14, SAY - 26), (x_seat, SAY), s)


def post(p):
    p = dict(p)
    p = arms_level(p, abs_deg=-6, elbow=4)
    for side, d in (("n", 0), ("f", -DZ)):
        s = p.get(f"s{side}", 0.0)
        ank = swing(X0 + d, SX + d, s)
        fa = 16 * math.sin(math.pi * s)
        p = leg(p, side, ank, fa, bend=1)
    return p


def build():
    keys = [(0, STAND)] + rep_keys(0, "n", "f") + rep_keys(4.6, "f", "n")
    tl = PostTimeline(keys, post)
    dur = keys[-1][0]

    scene = scene_group([
        ghost(figure(), SIDE, post(STAND), 0.12),
        *figure(extras_behind=chair(CH_X, FLOOR_Y, SEAT_H, CH_D, 64)),
        focus("root", rx=13, ry=13, offset=(-8, 2), show=[(1.0, 2.8), (5.6, 7.4)]),
        focus_mid("thigh_n", 0.5, 18, 9, show=[(1.0, 2.4)]),
        focus_mid("thigh_f", 0.5, 18, 9, show=[(5.6, 7.0)]),
        arrow("M100 124 Q94 90 110 66", show=[(1.0, 1.9), (5.6, 6.5)]),
        arrow("M104 96 Q90 128 98 160", show=[(2.8, 4.4), (7.4, 9.0)]),
    ], SC, FLOOR_Y)
    prims = [
        floor(FLOOR_Y, 30, 370),
        scene,
        label("Rechts führt", 344, 60, 0.3, 4.6, 12, ACCENT),
        label("Links führt", 344, 60, 4.9, dur, 12, ACCENT),
        caption_band(),
        caption("Arme vor – Fuß ganz auf den Sessel", 0, 1.0),
        caption("Ausatmen – über die Ferse hochdrücken", 1.0, 2.4),
        caption("Oben aufrichten – Po fest", 2.4, 2.8),
        caption("Langsam zurück – hinteres Bein zuerst", 2.8, 4.6),
        caption("Seitenwechsel – linker Fuß auf den Sessel", 4.6, 5.6),
        caption("Ausatmen – über die Ferse hochdrücken", 5.6, 7.0),
        caption("Oben aufrichten – Po fest", 7.0, 7.4),
        caption("Langsam zurück – hinteres Bein zuerst", 7.4, dur),
        static_text("Ganzen Fuß aufsetzen – über die Ferse hochdrücken", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=10, title="Sessel Step-Up")
