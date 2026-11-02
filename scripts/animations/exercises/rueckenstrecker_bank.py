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
    # Reine Halteübung: Körper bleibt in der geraden Linie, kein Auf und Ab.
    # Nur der Atem bewegt sich minimal; die Fokuszone pulsiert (Spannung baut sich auf).
    DUR = 12.0
    keys = [(0, dict(lift=1.0)), (3.0, dict(lift=0.985)), (6.0, dict(lift=1.0)), (9.0, dict(lift=0.985)),
            (DUR, dict(lift=1.0))]
    tl = FnTimeline(keys, skeleton=SIDE, pre=pre)
    r = math.radians(LEG_A)
    ux, uy = math.cos(r), -math.sin(r)
    ankle = (HIP[0] + 98 * ux, HIP[1] + 98 * uy)
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
        dyn_line(line_pts),
        focus("lumbar", rx=10, ry=16, offset=(-6, -6), end=False),
    ], scale=1.0, origin=(200, FLOOR_Y))
    # Uhr: 3 Minuten durchgehend
    clock = [
        Prim("circle", {"cx": 330, "cy": 150, "r": 26, "fill": "none", "stroke": FLOOR, "stroke-width": 6}),
        Prim("circle", {"cx": 330, "cy": 150, "r": 26, "fill": "none", "stroke": GOOD, "stroke-width": 6,
                        "stroke-dasharray": "163.4", "stroke-linecap": "round",
                        "transform": "rotate(-90 330 150)"},
             lambda c: {"stroke-dashoffset": 163.4 * (1 - c["t"] / DUR)}),
        static_text("3 Min", 330, 156, 15, TEXT, weight="700"),
        static_text("durchgehend", 330, 194, 12, MUTED),
    ]
    prims = [
        scene, *clock,
        static_text("eine Linie – nicht höher", 300, 226, 12, GOOD, weight="600"),
        caption_band(),
        static_text("Halten – kein Auf und Ab", 200, 24, LEAD_SIZE, MUTED),
        caption("Fersen bis Kopf eine gerade Linie", 0, 4.0),
        caption("Ruhig atmen – Spannung baut sich langsam auf", 4.0, 8.0),
        caption("Tut es weh: sofort aufhören", 8.0, DUR, color=WARN),
    ]
    return render(prims, tl, SIDE, fps=6, title="Hyperextension-Bank halten")
