from rig import *
from exercises._bauch_props import FLOOR_Y, PRONE, forearm_iks, mat_layer, stage, figure, legs_sharp

SLUG = "prone-leg-lifts"

# Bauchlage, Unterarmstütz. Beide Beine gestreckt gemeinsam anheben (Hüftstreckung),
# Becken bleibt auf der Matte, Blick zur Matte.
DOWN = PRONE
UP = dict(PRONE, thigh_n=-17, shin_n=1, foot_n=-74, thigh_f=-19, shin_f=1, foot_f=-74,
          lumbar=10)


def build():
    tl = Timeline([(0, DOWN), (0.8, DOWN), (2.0, UP), (3.2, UP), (4.6, DOWN), (5.2, DOWN)],
                  iks=forearm_iks(), skeleton=SIDE)
    legs = legs_sharp()
    prims = [
        *stage([
            *mat_layer(),
            ghost(legs, SIDE, DOWN, 0.16),
            *figure(),
            focus("root", rx=22, ry=9, offset=(-4, -14), end=False, show=[(0.8, 4.6)]),
            arrow("M62 176 Q56 162 62 148", show=[(0.8, 2.0)]),
            arrow("M62 148 Q56 162 62 176", show=[(3.2, 4.6)]),
        ]),
        caption_band(),
        caption("Unterarme stützen, Beine lang", 0, 0.8),
        caption("Ausatmen – beide Beine gestreckt heben", 0.8, 2.0),
        caption("Kurz halten – Po & Bauch fest", 2.0, 3.2),
        caption("Langsam absenken", 3.2, 5.2),
        static_text("Becken bleibt auf der Matte – nur leicht heben", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bauchlage-Beinheben")
