"""Clamshells – Seitlage, Ansicht von vorn (auf den Bauch der Person).
Kopf links auf dem Arm, Hüfte und Knie gebeugt, Fersen bleiben zusammen.
Skalar "open" 0..1 hebt das obere Knie wie eine Muschel."""
from rig import *

SLUG = "clamshells"

FLOOR_Y = 232
HIP = (232.0, FLOOR_Y - 26)
FEET = (258.0, FLOOR_Y - 7)
KNEE_LOW = (296.0, FLOOR_Y - 12)
DUR = 6.0


def knee_top(c):
    o = c["pose"].get("open", 0.0)
    a = math.radians(-13 + 50 * o)        # Winkel um die Hüfte
    L = 60.0
    return HIP[0] + L * math.cos(a), HIP[1] - L * math.sin(a) + 2


def leg(knee_fn, col, w):
    def d(c):
        kx, ky = knee_fn(c)
        return {"d": f"M{HIP[0]:.1f} {HIP[1]:.1f}L{kx:.1f} {ky:.1f}L{FEET[0]:.1f} {FEET[1]:.1f}"}
    return [
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
    ]


def build():
    tl = Timeline([(0, dict(open=0)), (0.6, dict(open=0)), (2.2, dict(open=1)), (3.4, dict(open=1)),
                   (5.2, dict(open=0)), (DUR, dict(open=0))], skeleton=SIDE)
    torso = [
        Prim("path", {"d": f"M96 {FLOOR_Y - 22}L{HIP[0]} {HIP[1]}", "fill": "none", "stroke": SKIN_LINE,
                      "stroke-width": 37, "stroke-linecap": "round"}),
        Prim("path", {"d": f"M96 {FLOOR_Y - 22}L{HIP[0]} {HIP[1]}", "fill": "none", "stroke": TORSO,
                      "stroke-width": 34, "stroke-linecap": "round"}),
    ]
    head = [
        Prim("path", {"d": f"M40 {FLOOR_Y - 6}L96 {FLOOR_Y - 6}", "fill": "none", "stroke": FAR,
                      "stroke-width": 12, "stroke-linecap": "round"}),   # unterer Arm als Kissen
        Prim("circle", {"cx": 62, "cy": FLOOR_Y - 30, "r": 17, "fill": HEAD, "stroke": SKIN_LINE,
                        "stroke-width": 3}),
    ]
    top_arm = [
        Prim("path", {"d": f"M104 {FLOOR_Y - 34}Q150 {FLOOR_Y - 10} 170 {FLOOR_Y - 8}", "fill": "none",
                      "stroke": SKIN_LINE, "stroke-width": 14, "stroke-linecap": "round"}),
        Prim("path", {"d": f"M104 {FLOOR_Y - 34}Q150 {FLOOR_Y - 10} 170 {FLOOR_Y - 8}", "fill": "none",
                      "stroke": NEAR, "stroke-width": 11, "stroke-linecap": "round"}),
    ]
    glute = Prim("ellipse", {"cx": HIP[0] - 4, "cy": HIP[1] - 12, "rx": 16, "ry": 11, "fill": ACCENT,
                             "opacity": 0.35, "_pulse": True, "_show": [(0.6, 5.2)]})
    heels = Prim("circle", {"cx": FEET[0], "cy": FEET[1], "r": 5, "fill": GOOD})
    open_arrow = arrow(f"M{KNEE_LOW[0] + 10} {KNEE_LOW[1] - 18} Q{KNEE_LOW[0] + 14} {KNEE_LOW[1] - 50} "
                       f"{KNEE_LOW[0] - 8} {KNEE_LOW[1] - 64}", show=[(0.6, 2.2)])
    pelvis_line = Prim("line", {"x1": HIP[0] - 30, "y1": HIP[1] - 30, "x2": HIP[0] - 30, "y2": HIP[1] + 20,
                                "stroke": GOOD, "stroke-width": 2, "stroke-dasharray": "4 4", "opacity": 0.8})
    prims = [
        mat(FLOOR_Y, 30, 370),
        *head,
        *torso,
        *leg(lambda c: KNEE_LOW, FAR, 15),
        *leg(knee_top, NEAR, 16),
        *top_arm,
        glute, heels, open_arrow, pelvis_line,
        static_text("Fersen bleiben zusammen", FEET[0] + 10, FLOOR_Y + 18, 12, GOOD, weight="600"),
        Prim("text", {"x": 300, "y": 118, "font-size": 12, "fill": TEXT, "text-anchor": "middle",
                      "_show": [(2.2, 3.4)]}, text="seitliches Gesäß arbeitet"),
        static_text("Becken nicht nach hinten kippen", 200, 24, LEAD_SIZE, MUTED),
        caption_band(),
        caption("Seitlage, Hüfte und Knie gebeugt", 0, 0.6),
        caption("Oberes Knie öffnen wie eine Muschel", 0.6, 2.2),
        caption("Kurz halten", 2.2, 3.4),
        caption("Langsam schließen", 3.4, DUR),
    ]
    return render(prims, tl, SIDE, fps=12, title="Clamshells")
