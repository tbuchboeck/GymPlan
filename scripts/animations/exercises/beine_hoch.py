from rig import *
from exercises._cardio_props import figure, focus_mid, label, scene_group

SLUG = "beine-hoch"

# Rückenlage, Kopf links. Gestreckte Beine schweben über der Matte und
# wechseln sich wie eine Schere ab (nahes = rechtes Bein). Becken, Rücken
# und Kopf bleiben ruhig liegen, Arme neben dem Körper.

FLOOR_Y = 238
PX = 220
PY = FLOOR_Y - 16

BASE = dict(x=PX, y=PY, rot=90, neck=-3, upperarm_n=-5, forearm_n=9, hand_n=-28,
            upperarm_f=-3, forearm_f=7, hand_f=-26, foot_n=-72, foot_f=-72, shin_n=-2, shin_f=-2)
HI, LO = 42, 10


def legs(n, f):
    return dict(BASE, thigh_n=n, thigh_f=f)


MID = legs(24, 22)
A = legs(HI, LO)      # rechts hoch
B = legs(LO + 2, HI)  # links hoch


def build():
    keys = [(0, MID), (0.5, MID), (1.2, A), (1.4, A), (2.2, B), (2.4, B), (3.2, A), (3.4, A),
            (4.2, B), (4.4, B), (5.0, MID)]
    tl = Timeline(keys)

    prims = [
        scene_group([
            mat(FLOOR_Y, 36, 352),
            ghost(figure(), SIDE, MID, 0.12),
            *figure(),
            focus_mid("lumbar", 0.3, 20, 10, show=[(0.5, 4.4)]),
            focus("root", rx=26, ry=5, offset=(-30, 14), color=GOOD, show=[(0.5, 4.4)]),
            arrow("M342 150 Q352 128 336 108", show=[(0.5, 1.2), (2.4, 3.2)]),
            arrow("M336 108 Q352 128 342 150", show=[(1.4, 2.2), (3.4, 4.2)]),
        ], 1.12, FLOOR_Y),
        label("Rücken bleibt am Boden", 150, 186, 0.5, 4.4, 11, GOOD),
        caption_band(),
        caption("Rückenlage – Beine gestreckt anheben", 0, 0.5),
        caption("Rechtes Bein hoch, linkes tief", 0.5, 1.4),
        caption("Wechseln – wie eine Schere", 1.4, 2.4),
        caption("Gleichmäßig weiteratmen", 2.4, 3.4),
        caption("Bauch fest – Füße nicht ablegen", 3.4, 5.0),
        static_text("Unterer Rücken bleibt fest auf der Matte", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Beine Hoch (Schere)")
