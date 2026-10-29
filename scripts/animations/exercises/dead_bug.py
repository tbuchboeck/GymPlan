from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "dead-bug"

# Rückenlage, Seitansicht, Kopf links (rot=90 -> Gesicht oben).
# Nahe Seite = rechte Körperseite. Seite 1: rechtes Bein + linker (ferner)
# Arm, Seite 2: linkes Bein + rechter Arm. Rücken bleibt flach liegen.
FLOOR_Y = 238
C = FLOOR_Y - 16
HIP_X = 222

BASE = dict(x=HIP_X, y=C, rot=90, neck=-8, head=4,
            # Tischposition: Oberschenkel senkrecht, Unterschenkel waagrecht
            thigh_n=90, shin_n=-90, foot_n=-15, thigh_f=88, shin_f=-88, foot_f=-15,
            # Arme zur Decke
            upperarm_n=90, upperarm_f=86, forearm_n=0, forearm_f=0, hand_n=0, hand_f=0)

LEG_LONG = dict(thigh=10, shin=0, foot=-8)
ARM_BACK = dict(upperarm=163, forearm=0, hand=4)


def ext(base, leg, arm):
    p = dict(base)
    for k, v in LEG_LONG.items():
        p[f"{k}_{leg}"] = v
    for k, v in ARM_BACK.items():
        p[f"{k}_{arm}"] = v
    return p


S1 = ext(BASE, "n", "f")      # rechtes Bein + linker Arm
S2 = ext(BASE, "f", "n")      # linkes Bein + rechter Arm

# Tempo laut Plan: 3 s raus / 1 s halten / 3 s zurück, dann Seite wechseln
A0 = 0.8
A1, A2, A3 = A0 + 3, A0 + 4, A0 + 7
B0 = A3 + 0.6
B1, B2, B3 = B0 + 3, B0 + 4, B0 + 7
END = B3 + 0.6


def build():
    tl = FnTimeline([(0, BASE), (A0, BASE), (A1, S1), (A2, S1), (A3, BASE), (B0, BASE),
                     (B1, S2), (B2, S2), (B3, BASE), (END, BASE)], skeleton=SIDE)
    S, OX = 1.22, 200

    def T(x, y):
        return OX + (x - OX) * S, FLOOR_Y + (y - FLOOR_Y) * S

    back = Prim("path", {"d": f"M{HIP_X - 58} {FLOOR_Y - 1} L{HIP_X - 4} {FLOOR_Y - 1}", "stroke": GOOD,
                         "stroke-width": 3.5, "stroke-linecap": "round", "fill": "none", "opacity": 0.9})
    out1 = [(A0, A1)]
    out2 = [(B0, B1)]
    scene = group([
        mat(FLOOR_Y, 62, 330),
        *side_figure_r(r=9, round_arms=False),
        back,
        focus("lumbar", rx=22, ry=9, offset=(-4, -6), show=[(A0, A3), (B0, B3)]),
        # Bein raus (nach rechts unten), Arm nach hinten (über Kopf)
        arrow(f"M{HIP_X + 60} {C - 70} Q{HIP_X + 100} {C - 52} {HIP_X + 106} {C - 26}", show=out1 + out2),
        arrow(f"M{HIP_X - 70} {C - 92} Q{HIP_X - 128} {C - 82} {HIP_X - 146} {C - 40}", show=out1 + out2),
    ], scale=S, origin=(OX, FLOOR_Y))

    bx, by = T(HIP_X - 30, FLOOR_Y)
    prims = [
        scene,
        label("Rücken bleibt flach am Boden", bx, by + 15, A0, B3, 11, GOOD),
        label("rechtes Bein + linker Arm", 200, 66, A0, A3, 12, TEXT),
        label("linkes Bein + rechter Arm", 200, 66, B0, B3, 12, TEXT),
        caption_band(),
        caption("Tischposition – Bauch fest", 0, A0),
        caption("Ausatmen – gegengleich lang machen", A0, A1),
        caption("Kurz halten", A1, A2),
        caption("Langsam zurück zur Mitte", A2, A3),
        caption("Seite wechseln", A3, B0),
        caption("Ausatmen – andere Seite lang", B0, B1),
        caption("Kurz halten", B1, B2),
        caption("Langsam zurück zur Mitte", B2, END),
        *tempo_chip([("3 s raus", [(A0, A1), (B0, B1)], None), ("1 s halten", [(A1, A2), (B1, B2)], None),
                     ("3 s zurück", [(A2, A3), (B2, B3)], None)]),
        static_text("Lendenwirbel drückt in die Matte", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Dead Bug", fps=10)
