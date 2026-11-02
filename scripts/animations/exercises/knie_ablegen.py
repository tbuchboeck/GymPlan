"""Knie seitlich ablegen – Rückenlage, Blick vom Fußende.
Füße und Knie geschlossen, Schultern liegen flach. Skalar "a" = Neigung der
Knie in Grad (+ rechts, - links). Klein anfangen, dann etwas weiter."""
from rig import *

SLUG = "knie-ablegen"

FLOOR_Y = 236
FEET = (200.0, FLOOR_Y - 6)
SHIN = 82.0
HIP_Y = FLOOR_Y - 34


def knee(c, side):
    a = math.radians(c["pose"].get("a", 0.0))
    kx = FEET[0] + SHIN * math.sin(a) + side * 9 * math.cos(a)
    ky = FEET[1] - SHIN * math.cos(a) + side * 9 * math.sin(a)
    return kx, ky


def foot(c, side):
    a = math.radians(c["pose"].get("a", 0.0))
    return FEET[0] + side * 8 * math.cos(a * 0.6), FEET[1] + side * 8 * math.sin(a * 0.6) * 0.3


def hip(c, side):
    a = c["pose"].get("a", 0.0)
    tilt = math.radians(a * 0.25)          # Becken rollt etwas mit
    return 200 + side * 22 * math.cos(tilt), HIP_Y + side * 22 * math.sin(tilt)


def seg(fn, col, w):
    def d(c):
        (x1, y1), (x2, y2) = fn(c)
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    return [Prim("line", {"stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round"}, d),
            Prim("line", {"stroke": col, "stroke-width": w, "stroke-linecap": "round"}, d)]


def build():
    K = [(0, 0), (0.6, 0), (2.2, 22), (3.2, 22), (4.6, 0), (6.2, -22), (7.2, -22), (8.6, 0),
         (10.4, 42), (11.6, 42), (13.0, 0), (14.8, -42), (16.0, -42), (17.4, 0), (18.0, 0)]
    tl = Timeline([(t, dict(a=a)) for t, a in K], skeleton=SIDE)
    dur = 18.0
    # Perspektive vom Fußende (leicht erhöht): Oberkörper und Kopf liegen
    # weiter weg und erscheinen daher höher im Bild, hinter den Knien.
    SY = FLOOR_Y - 100
    back = [
        Prim("polygon", {"points": f"170,{HIP_Y} 230,{HIP_Y} 244,{SY} 156,{SY}", "fill": TORSO,
                         "stroke": SKIN_LINE, "stroke-width": 3, "stroke-linejoin": "round"}),
        Prim("line", {"x1": 92, "y1": SY + 2, "x2": 308, "y2": SY + 2, "stroke": FAR,
                      "stroke-width": 10, "stroke-linecap": "round"}),             # Arme ausgebreitet
        Prim("ellipse", {"cx": 200, "cy": SY, "rx": 46, "ry": 11, "fill": TORSO, "stroke": SKIN_LINE,
                         "stroke-width": 3}),
        Prim("circle", {"cx": 200, "cy": SY - 22, "r": 13, "fill": HEAD, "stroke": SKIN_LINE,
                        "stroke-width": 3}),
        Prim("line", {"x1": 132, "y1": SY - 12, "x2": 268, "y2": SY - 12, "stroke": GOOD,
                      "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.9}),
    ]
    pelvis = Prim("ellipse", {"rx": 30, "ry": 13, "fill": TORSO, "stroke": SKIN_LINE, "stroke-width": 3},
                  lambda c: {"cx": 200, "cy": HIP_Y,
                             "transform": f"rotate({c['pose'].get('a', 0) * 0.25:.1f} 200 {HIP_Y})"})
    legs = []
    for side in (-1, 1):
        legs += seg(lambda c, s=side: (hip(c, s), knee(c, s)), FAR, 14)
    for side in (-1, 1):
        legs += seg(lambda c, s=side: (foot(c, s), knee(c, s)), NEAR, 15)
    knees = [Prim("circle", {"r": 7.5, "fill": NEAR, "stroke": SKIN_LINE, "stroke-width": 2},
                  lambda c, s=s: dict(zip(("cx", "cy"), knee(c, s)))) for s in (-1, 1)]
    scene = group([*back, pelvis, *legs, *knees], scale=1.2, origin=(200, FLOOR_Y))
    prims = [
        mat(FLOOR_Y, 20, 380),
        scene,
        static_text("Schultern bleiben liegen", 200, 66, 12, GOOD, weight="600"),
        static_text("Blick vom Fußende", 340, 60, 12, MUTED),
        caption_band(),
        static_text("Knie und Füße geschlossen – langsam wie ein Pendel", 200, 24, LEAD_SIZE, MUTED),
        caption("Klein anfangen: Knie zu einer Seite sinken lassen", 0, 4.6),
        caption("… und zur anderen Seite, 2 Atemzüge", 4.6, 8.6),
        caption("Dann etwas weiter – nur so weit es angenehm ist", 8.6, dur),
    ]
    return render(prims, tl, SIDE, fps=10, title="Knie seitlich ablegen")
