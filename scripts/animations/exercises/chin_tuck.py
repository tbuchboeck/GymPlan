from rig import *

SLUG = "chin-tuck"

# Sitzend auf Hocker, Seitansicht. Kinn gleitet waagrecht nach hinten.
SIT = dict(x=185, y=200, thigh_n=90, shin_n=-90, thigh_f=88, shin_f=-88,
           upperarm_n=8, forearm_n=70, upperarm_f=8, forearm_f=70)
FWD = dict(SIT, neck=-10, head=4)            # Kopf leicht vorgeschoben (Alltag)
TUCK = dict(SIT, neck=14, head=-16)          # Doppelkinn: Kopf hinten, Blick gerade


def build():
    tl = Timeline([(0, FWD), (1.0, FWD), (2.2, TUCK), (4.6, TUCK), (5.8, FWD), (6.4, FWD)])
    ear_line = Prim("line", {"x1": 205, "y1": 70, "x2": 205, "y2": 205, "stroke": GOOD,
                             "stroke-width": 1.5, "stroke-dasharray": "5 5", "opacity": 0.6})
    stool = [Prim("rect", {"x": 150, "y": 204, "width": 80, "height": 9, "rx": 4, "fill": PROP}),
             Prim("line", {"x1": 162, "y1": 213, "x2": 158, "y2": 262, "stroke": PROP_DARK, "stroke-width": 6}),
             Prim("line", {"x1": 218, "y1": 213, "x2": 222, "y2": 262, "stroke": PROP_DARK, "stroke-width": 6})]
    gaze = Prim("line", {"stroke": ACCENT, "stroke-width": 1.5, "stroke-dasharray": "3 4", "opacity": 0.7},
                lambda c: (lambda x, y, a: {"x1": x + 14, "y1": y - 2, "x2": x + 120, "y2": y - 2 - 106 * math.tan(math.radians(a - 90))})(*pt(c["P"], "head"), c["P"]["head"][4]))
    figure = side_figure(extras_behind=stool)
    # Nahansicht Oberkörper/Kopf, unten abgeschnitten
    head_parts = limb(["neck"], 13, TORSO) + head_side()
    close = group([ear_line, ghost(head_parts, SIDE, FWD, 0.25)] + figure + [
        gaze,
        arrow("M262 96 L236 96", show=[(1.0, 2.4)]),
        focus("neck", rx=8, ry=12, offset=(-7, 2), color=GOOD, end=False, show=[(2.2, 4.6)]),
    ], scale=2.0, origin=(200, 100), dy=20)
    close.attrs["clip-path"] = "url(#clipFig)"
    prims = [close, caption_band(),
        static_text("Blick bleibt waagrecht", 318, 92, 12, ACCENT),
        caption("Kopf locker", 0, 1.0),
        caption("Kinn waagrecht zurückschieben", 1.0, 2.2),
        caption("5 s halten – Nacken wird lang", 2.2, 4.6),
        caption("Locker lösen", 4.6, 6.4),
        static_text("Nicht nicken – gleiten", 200, 24, LEAD_SIZE, MUTED),
    ]
    clip = '<clipPath id="clipFig"><rect x="0" y="0" width="400" height="300"/></clipPath>'
    return render(prims, tl, SIDE, title="Chin Tucks", extra_defs=clip)
