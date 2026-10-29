"""Bauch- und Rippenatmung – aufrecht sitzend, Frontansicht (Nahansicht Rumpf).

Pose-Skalare: belly (0..1) weitet den Bauch, ribs (0..1) weitet den
Brustkorb seitlich und schiebt die Hand an den Rippen nach außen.
Schultern bleiben unten (feste Schulterlinie als Referenz).
"""
import math

from rig import *
from exercises.ulnaris_glide import SK, hand_prims, limb2, arm2, captions2, HAND_SKIN

SLUG = "bauch-rippenatmung"

IN = "#34d399"     # Einatmen (GOOD)
OUT = "#7dd3fc"    # Ausatmen
DUR = 10.0


def torso_d(c):
    g = c["pose"]
    r, b = g.get("ribs", 0.0), g.get("belly", 0.0)
    fx = 24 + 6 * r          # Rippen-Flanke (halbe Breite)
    wx = 18 + 3.5 * b + 1.5 * r   # Taille / Bauch
    hx = 21 + 1.0 * b

    def side(s):
        X = lambda dx: 200 + s * dx
        return [(X(9), 112), (X(27), 118), (X(34), 131), (X(24), 142), (X(fx), 156), (X(wx), 184), (X(hx), 214)]

    L, R = side(-1), side(1)
    p = lambda q: f"{q[0]:.1f} {q[1]:.1f}"
    d = (f"M{p(L[0])}Q{L[1][0] - 4:.1f} {L[1][1] - 2:.1f} {p(L[1])}Q{L[2][0] - 2:.1f} {L[2][1] - 9:.1f} {p(L[2])}"
         f"L{p(L[3])}Q{L[4][0] - 1:.1f} {L[4][1] - 6:.1f} {p(L[4])}Q{L[4][0] + 1:.1f} {L[5][1] - 14:.1f} {p(L[5])}"
         f"Q{L[5][0] - 0.5:.1f} {L[6][1] - 14:.1f} {p(L[6])}"
         f"L{p(R[6])}Q{R[5][0] + 0.5:.1f} {R[6][1] - 14:.1f} {p(R[5])}"
         f"Q{R[4][0] - 1:.1f} {R[5][1] - 14:.1f} {p(R[4])}Q{R[4][0] + 1:.1f} {R[4][1] - 6:.1f} {p(R[3])}"
         f"L{p(R[2])}Q{R[2][0] + 2:.1f} {R[2][1] - 9:.1f} {p(R[1])}Q{R[1][0] + 4:.1f} {R[1][1] - 2:.1f} {p(R[0])}Z")
    return {"d": d}


def ribs_d(c):
    r = c["pose"].get("ribs", 0.0)
    d = ""
    for y, w in [(136, 15), (146, 18), (156, 19)]:
        ww = w + 5 * r
        d += f"M{200 - ww:.1f} {y + 6:.1f}Q200 {y - 4 - 2 * r:.1f} {200 + ww:.1f} {y + 6:.1f}"
    return {"d": d}


def belly_zone(c):
    b = c["pose"].get("belly", 0.0)
    return {"rx": 11 + 6 * b, "ry": 8 + 5 * b, "opacity": 0.1 + 0.35 * b}


def belly_hand_target(p):
    b = p.get("belly", 0.0)
    return (184 - 1.5 * b, 180)


def rib_hand_target(p):
    r = p.get("ribs", 0.0)
    return (224 + 6.5 * r, 168)


BASE = dict(x=200, y=200, belly=0, ribs=0,
            a_pw=10, a_fang=4, a_flen=1, a_th=-60, a_tlen=0.9,
            b_pw=10, b_fang=-4, b_flen=1, b_th=60, b_tlen=0.9)
EMPTY = dict(BASE)
BELLY = dict(BASE, belly=1, ribs=0.12)
FULL = dict(BASE, belly=1, ribs=1)


def build():
    iks = [
        IK("upperarm_L", "forearm_L", belly_hand_target, bend=-1, end_seg="hand_L", end_abs=-8),
        IK("upperarm_R", "forearm_R", rib_hand_target, bend=1, end_seg="hand_R", end_abs=98),
    ]
    tl = Timeline([(0, EMPTY), (2.2, BELLY), (4.0, FULL), (DUR, EMPTY)], iks=iks, skeleton=SK)

    shoulder_line = [
        Prim("line", {"x1": 152, "y1": 116, "x2": 248, "y2": 116, "stroke": GOOD, "stroke-width": 1.4,
                      "stroke-dasharray": "4 4", "opacity": 0.85}),
    ]
    body = [
        Prim("path", {"fill": TORSO, "stroke": SKIN_LINE, "stroke-width": 3, "stroke-linejoin": "round"}, torso_d),
        Prim("path", {"d": "M193 114Q200 121 207 114", "fill": "none", "stroke": SKIN_LINE,
                      "stroke-width": 1.5, "opacity": 0.7}),
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 1.6, "stroke-linecap": "round",
                      "opacity": 0.45}, ribs_d),
        Prim("ellipse", {"cx": 200, "cy": 186, "fill": GOOD, "stroke": GOOD, "stroke-width": 1}, belly_zone),
    ]
    arms = (arm2(["upperarm_L", "forearm_L"], 11, NEAR) + arm2(["upperarm_R", "forearm_R"], 11, NEAR)
            + hand_prims("hand_L", "a_", scale=1.15) + hand_prims("hand_R", "b_", scale=1.15))
    rib_arrows = [
        arrow("M164 150L156 150", width=2, show=[(2.0, 4.0)]),
        arrow("M252 150L260 150", width=2, show=[(2.0, 4.0)]),
    ]
    fig = group(body + limb2(["neck"], 13, TORSO) + head_front() + shoulder_line + arms + rib_arrows,
                scale=1.55, origin=(200, 140), dx=8, dy=14)
    fig.attrs["clip-path"] = "url(#clipA)"

    # --- Atem-Balken oben: Ein 4 s / Aus 6 s -------------------------------
    X0, BW, BY = 70, 260, 30
    xin = X0 + BW * 0.4
    bar = [
        Prim("rect", {"x": X0, "y": BY, "width": BW, "height": 8, "rx": 4, "fill": FLOOR}),
        Prim("rect", {"x": X0, "y": BY, "height": 8, "rx": 4, "fill": IN},
             lambda c: {"width": max(0.01, BW * 0.4 * min(1.0, c["t"] / 4.0))}),
        Prim("rect", {"x": xin, "y": BY, "height": 8, "rx": 4, "fill": OUT},
             lambda c: {"width": max(0.01, BW * 0.6 * max(0.0, (c["t"] - 4.0) / 6.0))}),
        Prim("line", {"x1": xin, "y1": BY - 2, "x2": xin, "y2": BY + 10, "stroke": BG_BOTTOM, "stroke-width": 2}),
    ]
    for txt, x, col, win in [("Ein 4 s", X0 + BW * 0.2, IN, (0, 4)), ("Aus 6 s", xin + BW * 0.3, OUT, (4, DUR))]:
        bar.append(static_text(txt, x, BY - 6, 12, MUTED))
        on = static_text(txt, x, BY - 6, 12, col, weight="700")
        on.attrs["_show"] = [win]
        bar.append(on)

    # --- Zähler links ----------------------------------------------------
    counter = [Prim("circle", {"cx": 62, "cy": 118, "r": 30, "fill": "#0b1220", "stroke": FLOOR, "stroke-width": 2})]
    for i in range(4):
        counter.append(caption(str(i + 1), i, i + 1, y=128, size=28, color=IN, weight="700"))
    for i in range(6):
        counter.append(caption(str(i + 1), 4 + i, 5 + i, y=128, size=28, color=OUT, weight="700"))
    for p in counter[1:]:
        p.attrs["x"] = 62
    counter.append(caption("einatmen", 0, 4, y=166, size=12, color=IN))
    counter.append(caption("ausatmen", 4, DUR, y=166, size=12, color=OUT))
    for p in counter[-2:]:
        p.attrs["x"] = 62

    labels = [
        static_text("Schultern", 338, 80, 11.5, GOOD, weight="600"),
        static_text("bleiben unten", 338, 94, 11.5, GOOD, weight="600"),
        Prim("line", {"x1": 300, "y1": 88, "x2": 286, "y2": 98, "stroke": GOOD, "stroke-width": 1.2, "opacity": 0.7}),
        static_text("Hand an den Rippen", 338, 140, 11, MUTED),
        static_text("Hand auf dem Bauch", 338, 214, 11, MUTED),
        static_text("aufrecht sitzen", 62, 214, 10.5, MUTED),
        static_text("oder Rückenlage", 62, 227, 10.5, MUTED),
    ]
    prims = [fig, *bar, *counter, *labels, caption_band(),
             *captions2([
                 ("Einatmen durch die Nase – erst in den Bauch", "der Bauch weitet sich unter der Hand", 0, 2.2),
                 ("… dann seitlich in die Rippen", "Hände werden nach außen geschoben", 2.2, 4.0),
                 ("Langsam durch den Mund ausatmen", "Rippen sinken zurück", 4.0, 7.0),
                 ("Nacken und Schultern lösen", "täglich 3–5 Minuten", 7.0, DUR),
             ])]
    clip = '<clipPath id="clipA"><rect x="0" y="0" width="400" height="258"/></clipPath>'
    return render(prims, tl, SK, fps=10, title="Bauch- und Rippenatmung", extra_defs=clip)
