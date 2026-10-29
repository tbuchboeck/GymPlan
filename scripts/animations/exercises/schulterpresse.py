from rig import *
from exercises._tb_gym_props import *

SLUG = "schulterpresse"

# Schulterpresse sitzend, Frontansicht. Griffe laufen an zwei Führungs-
# schienen links/rechts; unten Griffe auf Schulterhöhe mit Ellbogen ~90°,
# oben Arme fast gestreckt (nicht durchgedrückt). Beine sitzend in Front-
# ansicht (Oberschenkel zum Betrachter verkürzt) werden selbst gezeichnet.

FLOOR_Y = 250
HIP = (200.0, 192.0)
RAIL_DX = 86.0
W_LOW = (60.0, -27.0)     # Handgelenk relativ zur Schulterlinie-Mitte (dx, dy) unten
W_HIGH = (47.0, -60.0)    # oben


def wrist(p, side):
    dx = W_LOW[0] + (W_HIGH[0] - W_LOW[0]) * p
    dy = W_LOW[1] + (W_HIGH[1] - W_LOW[1]) * p
    return dx, dy


def post(pose, P):
    p = pose.get("press", 0.0)
    out = {}
    cx, cy = pt(P, "chest")
    for k, side, clav in (("", -1, "clav_L"), ("_f", 1, "clav_R")):
        s = pt(P, clav)
        dx, dy = wrist(p, side)
        w = (cx + side * dx, cy + dy)
        w = clamp_reach(s, w, UA + FA - 1.0)
        e = ik2(s, w, UA, FA, bend=1 if side < 0 else -1)
        out.update({"sx" + k: s[0], "sy" + k: s[1], "ex" + k: e[0], "ey" + k: e[1],
                    "wx" + k: w[0], "wy" + k: w[1]})
    return out


BASE = dict(x=HIP[0], y=HIP[1], press=0.0)
UP = dict(BASE, press=1.0)


def seated_legs():
    """Sitzende Beine frontal: Oberschenkel stark verkürzt (zeigen zum
    Betrachter), Schienbeine senkrecht, Füße flach am Boden."""
    out = []
    for side in (-1, 1):
        hx, hy = HIP[0] + side * 12, HIP[1] + 6
        kx, ky = HIP[0] + side * 25, HIP[1] + 16
        ax, ay = HIP[0] + side * 30, FLOOR_Y - 10
        out += [
            Prim("path", {"d": f"M{kx} {ky}L{ax} {ay}", "fill": "none", "stroke": SKIN_LINE, "stroke-width": 18,
                          "stroke-linecap": "round"}),
            Prim("path", {"d": f"M{kx} {ky}L{ax} {ay}", "fill": "none", "stroke": FAR, "stroke-width": 15,
                          "stroke-linecap": "round"}),
            Prim("ellipse", {"cx": ax + side * 3, "cy": FLOOR_Y - 6, "rx": 11, "ry": 5.5, "fill": FAR,
                             "stroke": SKIN_LINE, "stroke-width": 1.5}),
        ]
    for side in (-1, 1):
        hx, hy = HIP[0] + side * 12, HIP[1] + 6
        kx, ky = HIP[0] + side * 25, HIP[1] + 16
        out += [
            Prim("path", {"d": f"M{hx} {hy}L{kx} {ky}", "fill": "none", "stroke": SKIN_LINE, "stroke-width": 27,
                          "stroke-linecap": "round"}),
            Prim("path", {"d": f"M{hx} {hy}L{kx} {ky}", "fill": "none", "stroke": NEAR, "stroke-width": 24,
                          "stroke-linecap": "round"}),
        ]
    out.append(Prim("path", {"d": f"M{HIP[0] - 12} {HIP[1] + 6}L{HIP[0] + 12} {HIP[1] + 6}", "fill": "none",
                             "stroke": NEAR, "stroke-width": 24, "stroke-linecap": "round"}))
    return out


def carriage(k, side):
    """Schlitten an der Schiene + Griffstange zur Hand."""
    rx = HIP[0] + side * RAIL_DX

    def sleeve(c):
        return {"x": rx - 8, "y": c["pose"]["wy" + k] - 12}

    def bar(c):
        p = c["pose"]
        return {"x1": rx, "y1": p["wy" + k] - 2, "x2": p["wx" + k] - side * 2, "y2": p["wy" + k] - 2}

    return [
        Prim("line", {"stroke": "#0b1220", "stroke-width": 9, "stroke-linecap": "round"}, bar),
        Prim("line", {"stroke": "#94a3b8", "stroke-width": 6, "stroke-linecap": "round"}, bar),
        Prim("rect", {"width": 16, "height": 22, "rx": 4, "fill": PROP, "stroke": "#0b1220",
                      "stroke-width": 1.5}, sleeve),
    ]


def build():
    T0, T1, T2, T3, TE = 0.9, 2.3, 3.0, 4.8, 5.4
    tl = PostTimeline([(0, BASE), (T0, BASE), (T1, UP), (T2, UP), (T3, BASE), (TE, BASE)],
                      skeleton=FRONT, post=post)
    c0, c1 = tl.at(0), tl.at(T1)

    lift = lambda c: 24 * c["pose"]["press"]
    stack, stack_top = weight_stack(330, FLOOR_Y, 70, lift, n=10, w=32)
    rails = []
    for side in (-1, 1):
        rx = HIP[0] + side * RAIL_DX
        rails += [R(rx - 4, 36, 8, FLOOR_Y - 36, PROP_DARK, rx=3)]
    sleeve_top = lambda c: c["pose"]["wy_f"] - 12
    frame = [
        R(104, 28, 270, 8, PROP_DARK, rx=4),
        R(96, FLOOR_Y - 7, 280, 7, PROP_DARK, rx=3),
        Prim("line", {"x1": HIP[0] + RAIL_DX, "x2": HIP[0] + RAIL_DX, "y1": 44, "stroke": "#cbd5e1",
                      "stroke-width": 2}, lambda c: {"y2": sleeve_top(c)}),
        L(HIP[0] + RAIL_DX, 44, 346, 44, "#cbd5e1", 2),
        L(346, 44, 346, stack_top - 2, "#cbd5e1", 2),
        *pulley(HIP[0] + RAIL_DX, 44, 5), *pulley(346, 44, 5),
    ]
    bench = [
        R(166, 60, 68, 136, "#0b1220", rx=10),           # Lehne hinter dem Rücken
        R(168, 62, 64, 132, PROP, rx=9),
        R(146, 196, 108, 10, PROP, rx=5),                # Sitz
        R(194, 206, 12, FLOOR_Y - 212, PROP_DARK, rx=2),
    ]

    # beide Arme nah (Frontansicht): Farbe NEAR
    arms_l = arm_prims("", w=13)
    arms_r = arm_prims("_f", w=13)
    for prim in arms_r:
        for key in ("stroke", "fill"):
            if prim.attrs.get(key) == FAR:
                prim.attrs[key] = NEAR

    figure = front_figure(legs=False)
    # front_figure zeichnet Skelett-Arme – die ersetzen wir durch eigene
    figure = [p for p in figure if not _is_skel_arm(p)]

    delts = [focus("clav_L", rx=11, ry=11, offset=(-2, 2), show=[(T0, T3)]),
             focus("clav_R", rx=11, ry=11, offset=(2, 2), show=[(T0, T3)])]
    # 90°-Marke am linken Ellbogen in der unteren Position
    ex, ey = c0["ex"], c0["ey"]
    ang = Prim("g", {"_show": [(0, T0 + 0.3), (T3 - 0.2, TE)]}, children=[
        Prim("path", {"d": f"M{ex + 1:.1f} {ey - 13:.1f} L{ex + 13:.1f} {ey - 13:.1f} L{ex + 13:.1f} {ey - 1:.1f}",
                      "fill": "none", "stroke": GOOD, "stroke-width": 2}),
    ])
    ang_txt = Prim("text", {"x": ex - 26, "y": ey + 22, "font-size": 12, "fill": GOOD, "font-weight": "600",
                            "text-anchor": "middle", "_show": [(0, T0 + 0.3), (T3 - 0.2, TE)]}, text="90°")
    lock = Prim("text", {"x": c1["wx_f"] + 16, "y": c1["wy_f"] - 4, "font-size": 11, "fill": WARN,
                         "text-anchor": "start", "_show": [(T1, T2)]}, text="nicht durchstrecken")
    neck_ok = Prim("g", {"_show": [(T0, T3)]}, children=[
        Prim("path", {"d": f"M{c0['sx'] + 6:.0f} {c0['sy'] - 12:.0f} Q{c0['sx'] + 12:.0f} {c0['sy'] - 22:.0f} 186 {c0['sy'] - 30:.0f}",
                      "fill": "none", "stroke": GOOD, "stroke-width": 1.6, "stroke-dasharray": "3 3"}),
    ])
    up_l = arrow(f"M{c0['wx'] - 22:.0f} {c0['wy'] - 6:.0f} L{c1['wx'] - 22:.0f} {c1['wy'] + 4:.0f}", show=[(T0, T1)])
    up_r = arrow(f"M{c0['wx_f'] + 22:.0f} {c0['wy_f'] - 6:.0f} L{c1['wx_f'] + 22:.0f} {c1['wy_f'] + 4:.0f}",
                 show=[(T0, T1)])

    prims = [
        floor(FLOOR_Y, 30, 380),
        *frame, *stack, *rails, *bench,
        *figure,
        *seated_legs(),
        *carriage("", -1), *carriage("_f", 1),
        *arms_l, *arms_r,
        *delts,
        ang, ang_txt, up_l, up_r,
        caption_band(),
        static_text("Nacken locker – Schultern bleiben tief", 200, 22, 13, MUTED),
        caption("Griffe auf Schulterhöhe – Ellbogen 90°", 0, T0),
        caption("Ausatmen – kontrolliert nach oben", T0, T1),
        caption("Oben nicht ganz durchstrecken", T1, T2),
        caption("Einatmen – langsam bis 90° zurück", T2, TE),
    ]
    return render(prims, tl, FRONT, fps=15, title="Schulterpresse")


def _is_skel_arm(p):
    """True für die Arm-Pfade aus front_figure (dyn mit Kette upperarm_*)."""
    if p.dyn is None or p.tag != "path":
        return False
    fn = p.dyn
    try:
        names = fn.__defaults__[0]
    except (TypeError, IndexError):
        return False
    return isinstance(names, list) and any(n.startswith("upperarm") for n in names)
