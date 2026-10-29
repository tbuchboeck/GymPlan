from rig import *
from exercises._bauch_props import FLOOR_Y, PRONE, forearm_iks, mat_layer, stage, figure, legs_sharp

SLUG = "scissor-kicks"

# Bauchlage, Unterarmstütz. Gestreckte Beine schweben knapp über der Matte und
# bewegen sich abwechselnd auf und ab (Schere). Becken bleibt liegen.
HOVER = dict(PRONE, thigh_n=-6, shin_n=0, foot_n=-74, thigh_f=-6, shin_f=0, foot_f=-74)
A = dict(HOVER, thigh_n=-19, thigh_f=1)    # nahes Bein oben
B = dict(HOVER, thigh_n=1, thigh_f=-19)    # fernes Bein oben


def build():
    keys = [(0, PRONE), (0.6, PRONE), (1.3, HOVER),
            (2.0, A), (2.8, B), (3.6, A), (4.4, B), (5.1, HOVER), (5.8, PRONE), (6.2, PRONE)]
    tl = Timeline(keys, iks=forearm_iks(), skeleton=SIDE)
    legs = legs_sharp()
    strokes = [(1.3, 5.1)]
    updown = arrow("M62 150 L62 172", show=strokes)
    updown.attrs["marker-start"] = "url(#arrowhead)"
    prims = [
        *stage([
            *mat_layer(),
            ghost(legs, SIDE, PRONE, 0.14),
            *figure(),
            focus("root", rx=20, ry=7, offset=(-16, 8), end=False, show=strokes),
            updown,
        ]),
        caption_band(),
        caption("Unterarme stützen, Blick zur Matte", 0, 0.6),
        caption("Beine gestreckt leicht abheben", 0.6, 1.3),
        caption("Abwechselnd auf und ab – wie eine Schere", 1.3, 5.1),
        caption("Ablegen, kurz lösen", 5.1, 6.2),
        static_text("Kleine, ruhige Schläge – Becken bleibt liegen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Scissor Kicks (Bauchlage)")
