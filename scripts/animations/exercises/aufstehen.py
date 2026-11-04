"""Aufstehen über den Vierfüßlerstand – Seitansicht eines Betts, Kante links.
Ablauf: Rückenlage, Bauch fest → als Ganzes auf die Seite drehen →
Vierfüßlerstand → Po auf die Fersen → vorne abstützen, ein Fuß raus auf den
Boden → zweiter Fuß nach, mit den Händen hochdrücken → stehen.

Zwei Figuren: Rückenlage (Bauch oben) braucht die gespiegelte Figur, der
Vierfüßlerstand (Bauch unten) die normale. Beim Drehen auf die Seite wird
zwischen beiden überblendet. Die Rückenlage hat eine eigene Timeline (_PA).
Posen der Hauptfigur aus absoluten Winkeln: ta (Rumpf), Becken x/y, dazu
Zielpunkte für Knöchel (an*/af*) und Handgelenke (hn*/hf*) per IK."""
from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "aufstehen"

FLOOR_Y = 224
BED_Y = FLOOR_Y - 54   # Matratzenoberkante
EDGE = 120             # linke Bettkante (hier wird ausgestiegen)
BED_R = 352
OX = 200               # Spiegelachse/Ursprung der Gruppen
SCALE = 0.8
K = BED_Y - 6          # Höhe von Knie/Knöchel/Hand auf der Matratze
G = FLOOR_Y - 5        # Knöchel am Boden


# --- Rückenlage (gespiegelte Figur, Kopf in ihrem Rahmen links) -------------

def pre_a(p):
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


A_X = 2 * OX - 214     # Becken im gespiegelten Rahmen, auf dem Bildschirm x≈214
SUP = dict(x=A_X, y=BED_Y - 15, ta=180, th=55, sh=-55, ua=-8, fa=-4)
ROLL = dict(SUP, th=40, sh=-75, ua=40, fa=10)   # Knie kippen, Arm greift hinüber
KEYS_A = [(0, SUP), (1.4, SUP), (2.6, ROLL), (20.0, ROLL)]


# --- Hauptfigur (Bauch unten / stehend), Blick nach rechts ------------------

def pre(p):
    ta = p["ta"]
    p["rot"] = ta - 90
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    set_abs(SIDE, p, "neck", ta - p.get("hd", 4))
    set_abs(SIDE, p, "head", ta - p.get("hd", 4) - 4)
    return p


def post(p):
    set_abs(SIDE, p, "foot_n", p["fn"])
    set_abs(SIDE, p, "foot_f", p["ff"])
    p["_PA"] = SIDE.fk(TL_A.at(p["_t"]))
    return p


IKS = [
    IK("thigh_n", "shin_n", lambda p: (p["anx"], p["any"]), bend=1),
    IK("thigh_f", "shin_f", lambda p: (p["afx"], p["afy"]), bend=1),
    IK("upperarm_n", "forearm_n", lambda p: (p["hnx"], p["hny"]), bend=-1, end_seg="hand_n", end_abs=0),
    IK("upperarm_f", "forearm_f", lambda p: (p["hfx"], p["hfy"]), bend=-1, end_seg="hand_f", end_abs=0),
]


def P(x, y, ta, an, af, hn, hf, fn=180, ff=180, hd=4):
    return dict(x=x, y=y, ta=ta, anx=an[0], any=an[1], afx=af[0], afy=af[1],
                hnx=hn[0], hny=hn[1], hfx=hf[0], hfy=hf[1], fn=fn, ff=ff, hd=hd)


# auf der Seite, zusammengerollt, Hände vor der Brust auf der Matratze
SIDE_LIE = P(214, BED_Y - 17, 2, (140, K - 4), (136, K - 4), (268, K), (264, K), fn=180, ff=180, hd=-2)
# Vierfüßlerstand: Knie unter der Hüfte, Hände unter den Schultern
QUAD = P(214, K - 50, 8, (166, K), (162, K), (290, K), (286, K), hd=14)
# Po auf die Fersen
HEEL = P(170, K - 21, 76, (166, K), (162, K), (226, K - 22), (222, K - 22), hd=6)
# vorne abstützen, Hüfte Richtung Kante
LEAN = P(150, K - 28, 26, (166, K), (142, K), (238, K), (234, K), hd=14)
# naher Fuß hinten über die Kante ...
LIFT_N = P(146, K - 28, 26, (112, BED_Y - 22), (142, K), (238, K), (234, K), fn=250, hd=14)
# ... und auf den Boden
STEP_N = P(144, K - 26, 28, (104, G), (142, K), (236, K), (232, K), fn=360, hd=14)
# ferner Fuß nach
LIFT_F = P(130, K - 30, 30, (104, G), (116, BED_Y - 22), (224, K), (220, K), fn=360, ff=250, hd=14)
BOTH = P(118, FLOOR_Y - 86, 30, (104, G), (112, G), (190, K), (186, K), fn=360, ff=360, hd=12)
# mit den Händen hochdrücken, aufrichten
STAND = P(110, FLOOR_Y - 101, 90, (106, G), (112, G), (114, FLOOR_Y - 112), (110, FLOOR_Y - 112),
          fn=360, ff=360, hd=4)

KEYS = [(0, SIDE_LIE), (2.4, SIDE_LIE), (3.4, SIDE_LIE),
        (5.0, QUAD), (6.2, QUAD),
        (7.8, HEEL), (9.0, HEEL),
        (10.2, LEAN), (11.0, LIFT_N), (11.8, STEP_N), (12.4, STEP_N),
        (13.2, LIFT_F), (14.0, BOTH), (14.6, BOTH),
        (16.0, STAND), (18.0, STAND)]
DUR = KEYS[-1][0]
KEYS_A[-1] = (DUR, ROLL)
TL_A = FnTimeline(KEYS_A, skeleton=SIDE, pre=pre_a)

FADE0, FADE1 = 2.3, 3.0   # Überblendung Rückenlage -> Seite


def _with_pa(p: Prim) -> Prim:
    dyn = p.dyn and (lambda c, f=p.dyn: f(dict(c, P=c["pose"]["_PA"])))
    return Prim(p.tag, dict(p.attrs), dyn, p.text, [_with_pa(ch) for ch in p.children])


def _fade(t, rising):
    u = min(1.0, max(0.0, (t - FADE0) / (FADE1 - FADE0)))
    v = u if rising else 1 - u
    if t >= DUR - 1e-6:   # Loop-Ende: wieder Rückenlage
        v = 0.0 if rising else 1.0
    return {"opacity": round(v, 2)}


def build():
    tl = FnTimeline(KEYS, iks=IKS, skeleton=SIDE, pre=pre, post=post)
    bed = [
        Prim("rect", {"x": EDGE, "y": BED_Y, "width": BED_R - EDGE, "height": 16, "rx": 6, "fill": "#475569"}),
        Prim("rect", {"x": BED_R - 44, "y": BED_Y - 4, "width": 40, "height": 8, "rx": 4, "fill": PROP}),  # Kissen
        Prim("rect", {"x": EDGE + 10, "y": BED_Y + 16, "width": 8, "height": FLOOR_Y - BED_Y - 16, "fill": PROP_DARK}),
        Prim("rect", {"x": BED_R - 18, "y": BED_Y + 16, "width": 8, "height": FLOOR_Y - BED_Y - 16, "fill": PROP_DARK}),
    ]
    supine = Prim("g", {}, lambda c: _fade(c["t"], False),
                  children=[_with_pa(p) for p in side_figure()])
    main = Prim("g", {}, lambda c: _fade(c["t"], True), children=side_figure())
    core = focus("lumbar", rx=10, ry=14, offset=(0, 0), end=False, show=[(3.0, 14.6)])
    scene_a = group([supine], scale=SCALE, origin=(OX, FLOOR_Y), mirror=True)
    scene_b = group([*bed, main, core,
                     arrow("M246 108 Q216 84 186 108", show=[(1.4, 3.4)]),        # drehen
                     arrow("M232 150 L232 122", show=[(3.4, 5.0)]),               # hochdrücken
                     arrow("M206 112 Q184 104 176 124", show=[(6.2, 7.8)]),       # Po zu den Fersen
                     arrow("M110 150 Q96 170 100 196", show=[(10.2, 12.4)]),      # Fuß raus
                     arrow("M196 124 L196 96", show=[(14.6, 16.0)])],             # hochdrücken
                    scale=SCALE, origin=(OX, FLOOR_Y))
    steps = [("1", 1.4, 3.4), ("2", 3.4, 6.2), ("3", 6.2, 9.0), ("4", 9.0, 12.4), ("5", 12.4, 16.0)]
    prims = [
        floor(FLOOR_Y, 20, 380),
        scene_a, scene_b,
        *[Prim("text", {"x": 360, "y": 74, "font-size": 30, "fill": ACCENT, "font-weight": "700",
                        "text-anchor": "middle", "_show": [(t0, t1)]}, text=n) for n, t0, t1 in steps],
        static_text("Bauchspannung halten", 270, 52, 12, ACCENT, weight="600"),
        caption_band(),
        static_text("Als Ganzes bewegen – nicht frontal aufsetzen", 200, 24, LEAD_SIZE, MUTED),
        caption("Rückenlage: Bauch leicht fest", 0, 1.4),
        caption("1  Als Ganzes auf die Seite drehen", 1.4, 3.4),
        caption("2  Hochdrücken in den Vierfüßlerstand", 3.4, 6.2),
        caption("3  Po auf die Fersen setzen", 6.2, 9.0),
        caption("4  Vorne abstützen, ein Fuß raus", 9.0, 12.4),
        caption("5  Zweiter Fuß nach, hochdrücken", 12.4, 16.0),
        caption("Stehen – erst ein paar Schritte gehen", 16.0, DUR),
    ]
    return render(prims, tl, SIDE, fps=10, title="Aufstehen über den Vierfüßlerstand", compact=True)
