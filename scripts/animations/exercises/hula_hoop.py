from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "hula-hoop"

# Frontansicht, stehend. Becken kreist (seitlich + vor/zurück), Füße bleiben
# fix (IK), Oberkörper gleicht aus und bleibt ruhig. Reifen = Ellipse um die
# Taille: Mittelpunkt läuft dem Becken gegenüber (Kontaktpunkt am Körper),
# hintere Hälfte hinter, vordere Hälfte vor der Figur.
FLOOR_Y = 250
CX = 196
PERIOD = 1.2                    # s pro Reifen-Umdrehung
DUR = PERIOD * 4
ANK_L = (CX - 22, FLOOR_Y - 12)
ANK_R = (CX + 22, FLOOR_Y - 12)
HIP_Y = FLOOR_Y - 109


def arms():
    # Arme angewinkelt seitlich hoch, aus dem Weg des Reifens
    ua, fa = 78, 95
    return dict(upperarm_L=-ua, forearm_L=-fa, upperarm_R=ua, forearm_R=fa, hand_L=-10, hand_R=10)


def pre(p):
    t = p["_t"]
    ph = 2 * math.pi * t / PERIOD
    sx = math.sin(ph)
    p.update(arms())
    p["x"] = CX + 13 * sx
    p["y"] = HIP_Y + 1.5 * math.cos(2 * ph)
    # Oberkörper gleicht seitlich aus
    p["lumbar"] = 9 * sx
    p["thorax"] = -5 * sx
    p["chest"] = -4 * sx
    p["neck"] = -1 * sx
    p["turn"] = 0.0
    p["ph"] = ph
    return p


IKS = [IK("thigh_L", "shin_L", ANK_L, bend=1, end_seg="foot_L", end_abs=-90),
       IK("thigh_R", "shin_R", ANK_R, bend=-1, end_seg="foot_R", end_abs=-90)]

RX, RY = 64, 13


def hoop_geom(c):
    P = c["P"]
    ph = c["pose"]["ph"]
    wx, wy = pt(P, "lumbar")   # Taille
    # Reifenmitte läuft gegenüber vom Becken-Ausschlag (Kontakt an der Hüfte)
    off = RX - 26
    cx = wx - off * math.sin(ph)
    cy = wy + 6 + 5 * math.cos(ph)       # vorn tiefer (Perspektive)
    tilt = -6 * math.sin(ph)
    return cx, cy, tilt


def hoop_half(front):
    def f(c):
        cx, cy, tilt = hoop_geom(c)
        a = math.radians(tilt)
        def q(ang):
            x, y = RX * math.cos(ang), RY * math.sin(ang)
            return cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)
        (x0, y0), (x1, y1) = q(math.pi), q(0)
        sweep = 0 if front else 1
        # vordere Hälfte = unterer Bogen (sweep 0 von links nach rechts)
        return {"d": f"M{x0:.1f} {y0:.1f}A{RX} {RY} {tilt:.1f} 0 {sweep} {x1:.1f} {y1:.1f}"}
    return f


def hoop(front):
    f = hoop_half(front)
    col = "#94a3b8" if front else "#64748b"
    return [Prim("path", {"fill": "none", "stroke": "#0b1220", "stroke-width": 8, "stroke-linecap": "round"}, f),
            Prim("path", {"fill": "none", "stroke": col, "stroke-width": 5, "stroke-linecap": "round"}, f),
            Prim("path", {"fill": "none", "stroke": ACCENT, "stroke-width": 5, "stroke-dasharray": "4 14",
                          "opacity": 0.8 if front else 0.4},
                 lambda c: {**f(c), "stroke-dashoffset": (-1 if front else 1) * 36 * c["t"] / PERIOD * 4 % 18}),]


def build():
    tl = FnTimeline([(0, {}), (DUR, {})], iks=IKS, skeleton=FRONT, pre=pre)
    fig = front_figure(extras_behind=hoop(False), extras_front=hoop(True))
    S = 0.86
    scene = group([floor(FLOOR_Y, 60, 340), *fig,
                   focus("root", rx=26, ry=10, offset=(0, -2))],
                  scale=S, origin=(CX, FLOOR_Y))

    # Draufsicht-Inset: Becken kreist
    ix, iy, ir = 346, 96, 22
    def dot(c):
        ph = c["pose"]["ph"]
        return {"cx": ix + ir * math.sin(ph), "cy": iy + ir * 0.75 * math.cos(ph)}
    inset = [
        Prim("rect", {"x": ix - 38, "y": iy - 44, "width": 76, "height": 92, "rx": 8, "fill": "#0b1220", "opacity": 0.6}),
        Prim("ellipse", {"cx": ix, "cy": iy, "rx": ir, "ry": ir * 0.75, "fill": "none", "stroke": ACCENT,
                         "stroke-width": 1.5, "stroke-dasharray": "3 4", "opacity": 0.7}),
        Prim("ellipse", {"cx": ix, "cy": iy, "rx": 10, "ry": 6, "fill": TORSO, "stroke": SKIN_LINE, "stroke-width": 1.5}),
        Prim("circle", {"r": 4.5, "fill": ACCENT}, dot),
        static_text("Hüfte kreist", ix, iy - 30, 12, MUTED),
        static_text("vorn", ix, iy + 38, 12, MUTED),
    ]
    half = DUR / 2
    prims = [
        scene,
        *inset,
        caption_band(),
        caption("Hüfte kreist – vor, seitlich, zurück", 0, half),
        caption("Reifen in Bewegung halten", half, DUR),
        static_text("Kreisen aus der Hüfte – Oberkörper bleibt ruhig", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, FRONT, title="Hula Hoop", fps=15)
