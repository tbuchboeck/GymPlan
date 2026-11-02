"""Aufstehen über die Seite („en bloc“) – Seitansicht eines Betts, Kante rechts.
Pose aus absoluten Winkeln: ta (Rumpf), th (Oberschenkel), sh (Unterschenkel),
ua/fa (Arme), Becken x/y. Ablauf: Rückenlage Knie auf → zur Seite drehen →
Beine über die Kante, mit den Armen hochdrücken → kurz sitzen → aufstehen."""
from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "aufstehen"

FLOOR_Y = 224
BED_Y = 168
EDGE = 286


def pre(p):
    ta = p.get("ta", 180)
    p["rot"] = ta - 90
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    set_abs(SIDE, p, "neck", ta - 4)
    set_abs(SIDE, p, "head", ta - 8)
    for k in ("n", "f"):
        set_abs(SIDE, p, "thigh_" + k, p.get("th", 0))
        set_abs(SIDE, p, "shin_" + k, p.get("sh", 0))
        set_abs(SIDE, p, "foot_" + k, p.get("sh", 0) + 90)
        set_abs(SIDE, p, "upperarm_" + k, p.get("ua", 0))
        set_abs(SIDE, p, "forearm_" + k, p.get("fa", 0))
        set_abs(SIDE, p, "hand_" + k, p.get("fa", 0))
    return p


Y_LIE = BED_Y - 15
A = dict(x=190, y=Y_LIE, ta=180, th=55, sh=-55, ua=-8, fa=-4)            # Rückenlage, Knie auf
B = dict(x=200, y=Y_LIE, ta=180, th=-8, sh=-70, ua=-8, fa=-4)            # zur Seite, Knie zur Kante
C = dict(x=236, y=Y_LIE - 6, ta=128, th=-6, sh=-96, ua=-112, fa=-96)     # Beine raus, hochdrücken
D = dict(x=246, y=BED_Y - 13, ta=92, th=-4, sh=-92, ua=-100, fa=-92)     # sitzen
E = dict(x=262, y=BED_Y - 13, ta=60, th=-30, sh=-104, ua=-80, fa=-70)    # nach vorn verlagern
F = dict(x=300, y=FLOOR_Y - 104, ta=90, th=-90, sh=-90, ua=-90, fa=-86)  # stehen

KEYS = [(0, A), (1.0, A), (3.0, B), (4.0, B), (6.4, C), (7.2, C), (8.6, D), (10.4, D),
        (11.4, E), (12.6, F), (14.4, F)]


def build():
    tl = FnTimeline(KEYS, skeleton=SIDE, pre=pre)
    dur = KEYS[-1][0]
    bed = [
        Prim("rect", {"x": 30, "y": BED_Y, "width": EDGE - 30, "height": 16, "rx": 6, "fill": "#475569"}),
        Prim("rect", {"x": 30, "y": BED_Y - 4, "width": 40, "height": 8, "rx": 4, "fill": PROP}),   # Kissen
        Prim("rect", {"x": 40, "y": BED_Y + 16, "width": 8, "height": FLOOR_Y - BED_Y - 16, "fill": PROP_DARK}),
        Prim("rect", {"x": EDGE - 18, "y": BED_Y + 16, "width": 8, "height": FLOOR_Y - BED_Y - 16, "fill": PROP_DARK}),
    ]
    core = focus("lumbar", rx=10, ry=14, offset=(0, 0), end=False, show=[(1.0, 12.6)])
    roll = arrow("M176 118 Q206 96 236 118", show=[(1.0, 3.0)])
    push = arrow("M214 160 L214 136", show=[(4.0, 6.4)])
    steps = [("1", 1.0, 4.0), ("2", 4.0, 7.2), ("3", 7.2, 10.4), ("4", 10.4, dur)]
    prims = [
        floor(FLOOR_Y, 20, 380),
        group([*bed, *side_figure(), core, roll, push], scale=0.8, origin=(200, FLOOR_Y), dx=-6),
        *[Prim("text", {"x": 360, "y": 110, "font-size": 30, "fill": ACCENT, "font-weight": "700",
                        "text-anchor": "middle", "_show": [(t0, t1)]}, text=n) for n, t0, t1 in steps],
        static_text("Bauchspannung halten", 80, 64, 12, ACCENT, weight="600"),
        caption_band(),
        static_text("Als Ganzes bewegen – nicht frontal aufsetzen", 200, 24, LEAD_SIZE, MUTED),
        caption("Bauch leicht fest, Knie zusammen", 0, 1.0),
        caption("1  Als Ganzes auf die Seite drehen", 1.0, 4.0),
        caption("2  Beine raus – mit den Armen hochdrücken", 4.0, 7.2),
        caption("3  Kurz auf der Bettkante sitzen", 7.2, 10.4),
        caption("4  Aufstehen – erst ein paar Schritte gehen", 10.4, dur),
    ]
    return render(prims, tl, SIDE, fps=10, title="Aufstehen über die Seite")
