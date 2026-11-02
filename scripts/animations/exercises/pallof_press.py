"""Pallof Press – Draufsicht (von oben), damit Band, Zug und Anti-Rotation
sichtbar sind. Skalar "press" 0..1: Hände von der Brust nach vorn gestreckt.
Das Band zieht seitlich zum Anker (links) – der Rumpf bleibt gerade."""
from rig import *

SLUG = "pallof-press"

CX, CY = 220.0, 168.0          # Mitte zwischen den Schultern
ANCHOR = (34.0, 112.0)
DUR = 8.0


def hands(c):
    p = c["pose"].get("press", 0.0)
    return CX, CY - 26 - 52 * p


def build():
    tl = Timeline([(0, dict(press=0)), (0.8, dict(press=0)), (2.6, dict(press=1)), (4.6, dict(press=1)),
                   (6.6, dict(press=0)), (DUR, dict(press=0))], skeleton=SIDE)
    def arm(side):
        sx = CX + side * 30
        def d(c):
            hx, hy = hands(c)
            p = c["pose"].get("press", 0.0)
            tx, ty = hx + side * 6, hy + 4
            mx, my = (sx + tx) / 2, (CY - 4 + ty) / 2
            # gebeugt: Ellbogen seitlich außen; gestreckt: gerade Linie
            ex, ey = mx + side * 26 * (1 - p), my + 6 * (1 - p)
            return {"d": f"M{sx:.1f} {CY - 4:.1f}L{ex:.1f} {ey:.1f}L{tx:.1f} {ty:.1f}"}
        return [
            Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 15, "stroke-linecap": "round", "stroke-linejoin": "round"}, d),
            Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 12, "stroke-linecap": "round", "stroke-linejoin": "round"}, d),
        ]
    band = Prim("line", {"x1": ANCHOR[0], "y1": ANCHOR[1], "stroke": "#f472b6", "stroke-width": 4,
                         "stroke-linecap": "round"},
                lambda c: dict(zip(("x2", "y2"), hands(c))))
    fist = Prim("ellipse", {"rx": 13, "ry": 9, "fill": NEAR, "stroke": SKIN_LINE, "stroke-width": 2},
                lambda c: dict(zip(("cx", "cy"), hands(c))))
    body = [
        # Füße hüftbreit (von oben unter dem Körper)
        Prim("ellipse", {"cx": CX - 18, "cy": CY + 22, "rx": 8, "ry": 15, "fill": FAR}),
        Prim("ellipse", {"cx": CX + 18, "cy": CY + 22, "rx": 8, "ry": 15, "fill": FAR}),
        # Schultern/Rumpf
        Prim("ellipse", {"cx": CX, "cy": CY, "rx": 44, "ry": 18, "fill": TORSO, "stroke": SKIN_LINE,
                         "stroke-width": 3}),
        *arm(-1), *arm(1),
        Prim("circle", {"cx": CX, "cy": CY + 2, "r": 15, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 3}),
        Prim("path", {"d": f"M{CX - 5} {CY - 11} L{CX} {CY - 19} L{CX + 5} {CY - 11}", "fill": HEAD,
                      "stroke": SKIN_LINE, "stroke-width": 2, "stroke-linejoin": "round"}),   # Nase = Blick
    ]
    # gerade Linie Becken/Schultern nach vorn: bleibt
    guide = Prim("line", {"x1": CX - 70, "y1": CY, "x2": CX + 70, "y2": CY, "stroke": GOOD,
                          "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.8})
    anchor_box = [
        Prim("rect", {"x": 16, "y": ANCHOR[1] - 30, "width": 12, "height": 60, "rx": 3, "fill": PROP_DARK}),
        Prim("circle", {"cx": ANCHOR[0], "cy": ANCHOR[1], "r": 5, "fill": PROP}),
    ]
    pull = arrow(f"M{CX + 64} {CY - 34} Q{CX + 48} {CY - 70} {CX + 10} {CY - 82}", color=WARN, width=2.5,
                 show=[(2.6, 4.6)])
    prims = [
        *anchor_box, band, *body, fist, guide, pull,
        static_text("Ansicht von oben", 330, 60, 12, MUTED),
        static_text("Band zieht zur Seite", 92, 98, 12, "#f472b6"),
        Prim("text", {"x": CX + 96, "y": CY - 64, "font-size": 12, "fill": WARN, "text-anchor": "middle",
                      "_show": [(2.6, 4.6)]}, text="will dich drehen"),
        Prim("text", {"x": CX + 100, "y": CY + 6, "font-size": 12, "fill": GOOD, "font-weight": "600",
                      "text-anchor": "middle"}, text="bleibt gerade"),
        caption_band(),
        static_text("Seitlich zum Anker stehen, Bauch fest", 200, 24, LEAD_SIZE, MUTED),
        caption("Griff mit beiden Händen vor der Brust", 0, 0.8),
        caption("Arme langsam gerade nach vorn strecken", 0.8, 2.6),
        caption("2 s halten – nicht mitdrehen lassen", 2.6, 4.6),
        caption("Zurück zur Brust, später Seite wechseln", 4.6, DUR),
    ]
    return render(prims, tl, SIDE, fps=12, title="Pallof Press")
