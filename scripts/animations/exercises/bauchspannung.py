"""Bauchspannung – Rückenlage, Knie angewinkelt (wie Shakti-Matte/Becken kippen).
Nabel sanft einziehen, Rumpf leicht anspannen (etwa ein Viertel), weiteratmen."""
from rig import *
from exercises._ruecken_cardio_props import *
from exercises.shakti_matte import pre, IKS, FLOOR_Y

SLUG = "bauchspannung"
DUR = 9.0


def build():
    tl = FnTimeline([(0, dict(breath=0)), (2.0, dict(breath=0.2)), (DUR, dict(breath=0))],
                    iks=IKS, skeleton=SIDE, pre=pre)
    S, OX = 1.32, 196
    belly = Prim("ellipse", {"rx": 22, "ry": 9, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                             "_show": [(1.2, DUR)]},
                 lambda c: dict(zip(("cx", "cy"), (pt(c["P"], "lumbar")[0] + 4, pt(c["P"], "lumbar")[1] - 12))))
    corset = Prim("rect", {"width": 52, "height": 30, "rx": 8, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                           "stroke-dasharray": "4 3", "_show": [(3.0, DUR)]},
                  lambda c: {"x": pt(c["P"], "lumbar")[0] - 22, "y": pt(c["P"], "lumbar")[1] - 22})
    scene = group([mat(FLOOR_Y, 40, 330), *side_figure(), belly, corset,
                   arrow("M196 176 L196 194", show=[(0.6, 3.0)])],
                  scale=S, origin=(OX, FLOOR_Y))
    # Kraft-Anzeige: etwa 25 %
    bar = [
        Prim("rect", {"x": 300, "y": 70, "width": 70, "height": 9, "rx": 4.5, "fill": FLOOR}),
        Prim("rect", {"x": 300, "y": 70, "height": 9, "rx": 4.5, "fill": GOOD},
             lambda c: {"width": max(0.01, 70 * 0.25 * min(1.0, max(0.0, (c["t"] - 0.6) / 2.0)))}),
        static_text("Kraft ≈ 25 %", 335, 64, 12, MUTED),
    ]
    prims = [
        scene, *bar,
        label("weiter normal atmen", 200, 120, 3.0, DUR, 13, GOOD, weight="700"),
        caption_band(),
        static_text("Nicht pressen, nicht die Luft anhalten", 200, 24, LEAD_SIZE, MUTED),
        caption("Nabel sanft nach innen ziehen", 0, 3.0),
        caption("Rumpf leicht fest – wie ein Korsett", 3.0, 6.0),
        caption("Spannung halten und so aufstehen", 6.0, DUR),
    ]
    return render(prims, tl, SIDE, fps=8, title="Bauchspannung")
