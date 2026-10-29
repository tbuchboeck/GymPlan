from rig import *
from ._hantel_b_props import dumbbell, side_fig, label

SLUG = "bizeps-ueber-kopf"

# Seitansicht (Blick nach rechts). Bizeps-Curl mit fixem Ellbogen, dann
# Hanteln vor die Schultern und senkrecht über Kopf drücken, kontrolliert
# zurück. Ganze Figur verkleinert, damit die gestreckten Arme ins Bild passen.

FLOOR_Y = 250
SC = 0.8
LEGS = dict(thigh_n=3, shin_n=-3, thigh_f=-3, shin_f=3)
BASE = dict(x=200, y=FLOOR_Y - 8 - 98, **LEGS)


def arms(ua, fa, ua_f=None, fa_f=None, **kw):
    return dict(BASE, upperarm_n=ua, forearm_n=fa,
                upperarm_f=ua - 3 if ua_f is None else ua_f,
                forearm_f=fa if fa_f is None else fa_f, **kw)


HANG = arms(4, 8)
CURL = arms(6, 138, neck=0)
RACK = arms(32, 146)                       # Hanteln vor den Schultern, Unterarme senkrecht
PRESS = arms(176, 4, ua_f=172, fa_f=6, neck=-4, head=2, lumbar=-1)   # Arme lang über Kopf


def build():
    tl = Timeline([
        (0, HANG), (0.5, HANG),
        (1.5, CURL), (1.9, RACK), (2.2, RACK),
        (3.3, PRESS), (3.8, PRESS),
        (5.0, RACK), (5.3, CURL),
        (6.5, HANG), (6.9, HANG),
    ], skeleton=SIDE)

    def biceps(c):
        x0, y0, x1, y1, a = c["P"]["upperarm_n"]
        r = math.radians(a + 90)
        return {"cx": (x0 + x1) / 2 + 5 * math.cos(r), "cy": (y0 + y1) / 2 - 5 * math.sin(r)}

    def delt(c):
        x, y = pt(c["P"], "chest")
        return {"cx": x + 2, "cy": y + 4}

    P0 = SIDE.fk(HANG)
    ex, ey = pt(P0, "upperarm_n")
    sx, sy = pt(P0, "chest")
    figure = side_fig(
        db_far=dumbbell("hand_f", "forearm_f", far=True, fore=0.8, size=1.3),
        db_near=dumbbell("hand_n", "forearm_n", fore=0.8, size=1.3),
    )
    elbow_fix = Prim("circle", {"cx": ex, "cy": ey, "r": 11, "fill": "none", "stroke": GOOD, "stroke-width": 2,
                                "stroke-dasharray": "3 3", "_show": [(0.4, 1.6), (5.2, 6.6)]})
    stage = [
        Prim("rect", {"x": 140, "y": FLOOR_Y - 2, "width": 120, "height": 5, "rx": 2.5, "fill": "#3f4a7a"}),
        *figure,
        Prim("ellipse", {"rx": 7, "ry": 13, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                         "_show": [(0.5, 2.0), (5.2, 6.6)]}, biceps),
        Prim("ellipse", {"rx": 12, "ry": 11, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                         "_show": [(2.0, 5.1)]}, delt),
        elbow_fix,
        arrow(f"M{ex + 40:.0f} {ey + 30:.0f} Q{ex + 58:.0f} {ey - 18:.0f} {ex + 30:.0f} {ey - 44:.0f}",
              show=[(0.5, 1.5)]),
        arrow(f"M{sx + 48:.0f} {sy - 6:.0f} L{sx + 48:.0f} {sy - 78:.0f}", show=[(2.2, 3.3)]),
        arrow(f"M{sx + 48:.0f} {sy - 78:.0f} L{sx + 48:.0f} {sy - 6:.0f}", show=[(3.8, 5.0)]),
    ]
    prims = [
        floor(FLOOR_Y + 2, 20, 380),
        group(stage, scale=SC, origin=(200, FLOOR_Y + 2)),
        label("Ellbogen bleibt am Körper", 312, 196, 0.5, 1.6, 12, GOOD),
        label("Rumpf fest, kein Hohlkreuz", 312, 150, 3.0, 3.9, 12, ACCENT),
        caption_band(),
        caption("Arme locker, Handflächen nach vorn", 0, 0.5),
        caption("Ausatmen – Curl nach oben", 0.5, 1.5),
        caption("Hanteln vor die Schultern", 1.5, 2.2),
        caption("Ausatmen – über Kopf drücken", 2.2, 3.8),
        caption("Langsam zurück zur Schulter", 3.8, 5.3),
        caption("Kontrolliert ablassen", 5.3, 6.9),
        static_text("Curl mit fixem Ellbogen, dann gerade nach oben", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bizeps-Curl plus Überkopfdrücken")
