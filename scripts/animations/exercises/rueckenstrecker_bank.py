"""Rückenstrecker-Bank (45°) – isometrisch halten. Seitansicht, Kopf rechts,
Gesicht zum Boden. Hüfte am Polster, Fersen unter der Rolle. Skalar "lift"
0..1: Oberkörper hängt (0) bzw. bildet eine Linie mit den Beinen (1)."""
from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "rueckenstrecker-bank"

FLOOR_Y = 248
HIP = (196.0, 140.0)
LEG_A = 225.0              # Beine schräg nach hinten-unten (45°)
UP_A, DOWN_A = 45.0, -30.0


def pre(p):
    a = DOWN_A + (UP_A - DOWN_A) * p.get("lift", 0.0)
    p["x"], p["y"] = HIP
    p["rot"] = a - 90
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    set_abs(SIDE, p, "neck", a)
    set_abs(SIDE, p, "head", a)
    for k in ("n", "f"):
        set_abs(SIDE, p, "thigh_" + k, LEG_A)
        set_abs(SIDE, p, "shin_" + k, LEG_A)
        set_abs(SIDE, p, "foot_" + k, LEG_A + 90)
    # Arme vor der Brust verschränkt
    for k in ("n", "f"):
        set_abs(SIDE, p, "upperarm_" + k, a - 150)
        set_abs(SIDE, p, "forearm_" + k, a + 10)
        set_abs(SIDE, p, "hand_" + k, a + 10)
    return p


def build():
    T0, T1, T2, T3, END = 0.6, 2.6, 12.6, 14.6, 15.2
    tl = FnTimeline([(0, dict(lift=0)), (T0, dict(lift=0)), (T1, dict(lift=1)), (T2, dict(lift=1)),
                     (T3, dict(lift=0)), (END, dict(lift=0))], skeleton=SIDE, pre=pre)
    r = math.radians(LEG_A)
    ux, uy = math.cos(r), -math.sin(r)
    ankle = (HIP[0] + 98 * ux, HIP[1] + 98 * uy)
    # Polster vor der Hüfte (unter dem Körper), Rolle hinter den Fersen
    nx, ny = uy, -ux                       # Normale Richtung Bauchseite? -> unten rechts
    pad_c = (HIP[0] - 4 * ux + 18 * uy, HIP[1] - 4 * uy - 18 * ux)   # Bauchseite
    bench = [
        Prim("line", {"x1": pad_c[0], "y1": pad_c[1], "x2": pad_c[0] + 10, "y2": FLOOR_Y, "stroke": PROP_DARK,
                      "stroke-width": 8, "stroke-linecap": "round"}),
        Prim("line", {"x1": ankle[0] - 6, "y1": ankle[1] + 8, "x2": ankle[0] - 2, "y2": FLOOR_Y,
                      "stroke": PROP_DARK, "stroke-width": 8, "stroke-linecap": "round"}),
        Prim("line", {"x1": ankle[0] - 2, "y1": FLOOR_Y - 4, "x2": pad_c[0] + 10, "y2": FLOOR_Y - 4,
                      "stroke": PROP_DARK, "stroke-width": 7, "stroke-linecap": "round"}),
        Prim("rect", {"x": pad_c[0] - 24, "y": pad_c[1] - 8, "width": 48, "height": 16, "rx": 7, "fill": PROP,
                      "transform": f"rotate(-45 {pad_c[0]:.1f} {pad_c[1]:.1f})"}),
        Prim("circle", {"cx": ankle[0] - 9, "cy": ankle[1] - 8, "r": 8, "fill": PROP}),
    ]

    def line_pts(c):
        P = c["P"]
        return pt(P, "shin_n"), pt(P, "head")

    scene = group([
        floor(FLOOR_Y, 40, 360),
        *bench,
        *side_figure(),
        dyn_line(line_pts, show=[(T1, T2)]),
        focus("lumbar", rx=10, ry=16, offset=(-6, -6), end=False, show=[(T0, T2)]),
        arrow("M262 206 Q292 170 276 122", show=[(T0, T1)]),
    ], scale=1.0, origin=(200, FLOOR_Y))
    prims = [
        scene,
        label("eine Linie – nicht höher", 318, 200, T1, T2, 12, GOOD),
        *counter(T1, 10, 330, 170, size=20),
        caption_band(),
        static_text("Kein Hohlkreuz – Gesäß mit anspannen", 200, 24, LEAD_SIZE, MUTED),
        caption("Hüfte am Polster, Fersen unter der Rolle", 0, T0),
        caption("Oberkörper heben bis zur geraden Linie", T0, T1),
        caption("10 s halten – Kopf in Verlängerung", T1, T2),
        caption("Kurz absenken – 5–6×", T2, END),
    ]
    return render(prims, tl, SIDE, fps=8, title="Rückenstrecker-Bank")
