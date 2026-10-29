from rig import *
from exercises.face_pulls import _body_axes, _place, shoulder, body_pt, scapula, ANKLE, FLOOR_Y

SLUG = "reverse-flys"

# Seitansicht wie face_pulls: Schlingentrainer vorn an Tür/Stange auf
# Brusthöhe, die Person lehnt sich leicht zurück in die Bänder. Die Arme
# (leicht gebeugt, auf Schulterhöhe) öffnen von vorn nach seitlich – in der
# Seitansicht wird der nahe Arm dabei kürzer und kommt zum Betrachter (Hand
# größer). Die Bandlänge bleibt konstant, darum richtet sich der Körper beim
# Öffnen auf. Inset links oben: dieselbe Bewegung von oben.

ANCHOR = (372.0, 104.0)      # Brust-/Kopfhöhe, vor der Person
STRAP = 200.0
L_ARM = 64.0                 # Schulter -> Hand (leicht gebeugt)
TH_OPEN = 84.0               # Armwinkel: 0 = nach vorn, 90 = seitlich


def arm3(pose, P, far=False):
    """Ellbogen, Hand und Tiefe (1 = ganz zum Betrachter) der nahen/fernen Seite."""
    sx, sy = shoulder(P, pose)
    up, fwd = _body_axes(P)
    th = math.radians(TH_OPEN * pose.get("open", 0.0))
    # Richtung zum Anker als "vorn" der Arme (senkrecht zur Brust wäre zu steil)
    dx, dy = ANCHOR[0] - sx, ANCHOR[1] - sy
    d = math.hypot(dx, dy)
    ax, ay = dx / d, dy / d
    sgn = -1 if far else 1
    lat = math.sin(th)
    # schräge Projektion der Tiefe: zum Betrachter = etwas nach links unten
    ox, oy = -0.32 * sgn, 0.22 * sgn

    def at(k, bend):
        f = k * math.cos(th)
        l = k * lat
        return (sx + ax * f + ox * l + up[0] * bend, sy + ay * f + oy * l + up[1] * bend)

    e = at(34, -4)
    h = at(L_ARM, 2 * lat)
    if far:
        e, h = (e[0] - 6, e[1] + 1), (h[0] - 6, h[1] + 1)
    return e, h, lat * sgn


class FlyTimeline(Timeline):
    def at(self, t):
        base = self._interp(t)

        def solve(lean):
            p = _place(base, lean)
            P = SIDE.fk(p)
            e, h, dep = arm3(p, P)
            return p, P, math.hypot(ANCHOR[0] - h[0], ANCHOR[1] - h[1])

        lo, hi = 0.0, 45.0
        for _ in range(28):
            mid = (lo + hi) / 2
            if solve(mid)[2] > STRAP:
                hi = mid
            else:
                lo = mid
        p, P, _ = solve((lo + hi) / 2)
        for far, k in ((False, "n"), (True, "f")):
            e, h, dep = arm3(p, P, far)
            p.update({f"ex_{k}": e[0], f"ey_{k}": e[1], f"hx_{k}": h[0], f"hy_{k}": h[1], f"dep_{k}": dep})
        return p


def arm_prims(far):
    k = "f" if far else "n"
    w, col = (11, FAR) if far else (12, NEAR)

    def d(c):
        p = c["pose"]
        s = shoulder(c["P"], p)
        if far:
            s = (s[0] - 6, s[1] + 1)
        return {"d": smooth_path([s, (p[f"ex_{k}"], p[f"ey_{k}"]), (p[f"ex_{k}"], p[f"ey_{k}"]),
                                  (p[f"hx_{k}"], p[f"hy_{k}"])])}

    def fist(c):
        p = c["pose"]
        return {"cx": p[f"hx_{k}"], "cy": p[f"hy_{k}"], "r": round(w / 2 + 1.5 + 3 * p[f"dep_{k}"], 1)}

    return [
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 3, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, d),
        Prim("circle", {"fill": col, "stroke": SKIN_LINE, "stroke-width": 1.5}, fist),
    ]


def straps(far):
    k = "f" if far else "n"
    col = "#3b4a63" if far else "#d1d5db"

    def band(c):
        p = c["pose"]
        return {"x1": ANCHOR[0], "y1": ANCHOR[1], "x2": p[f"hx_{k}"], "y2": p[f"hy_{k}"]}

    return [Prim("line", {"stroke": col, "stroke-width": 3 if far else 3.5, "stroke-linecap": "round"}, band)]


def figure():
    prims = []
    prims += straps(True)
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += arm_prims(True)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims.append(scapula())
    prims += head_side()
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += straps(False)
    prims += arm_prims(False)
    return prims


IN_X, IN_Y, IN_W, IN_H = 10, 36, 92, 92


def top_inset():
    """Draufsicht: Brust nach rechts (zum Anker), Arme öffnen von vorn zur Seite."""
    cx, cy = IN_X + 40, IN_Y + IN_H / 2
    out = [Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "rx": 8, "fill": "#0b1220",
                         "opacity": 0.75, "stroke": FLOOR, "stroke-width": 1}),
           Prim("circle", {"cx": IN_X + IN_W - 8, "cy": cy, "r": 4, "fill": "none", "stroke": "#d1d5db",
                           "stroke-width": 2})]

    def arm_line(side):
        def f(c):
            th = math.radians(TH_OPEN * c["pose"].get("open", 0.0))
            sx, sy = cx, cy + side * 13
            hx, hy = sx + 34 * math.cos(th), sy + side * 34 * math.sin(th)
            return {"x1": sx, "y1": sy, "x2": hx, "y2": hy}
        return Prim("line", {"stroke": NEAR if side > 0 else FAR, "stroke-width": 7, "stroke-linecap": "round"}, f)

    def strap_line(side):
        def f(c):
            th = math.radians(TH_OPEN * c["pose"].get("open", 0.0))
            sx, sy = cx, cy + side * 13
            return {"x1": sx + 34 * math.cos(th), "y1": sy + side * 34 * math.sin(th),
                    "x2": IN_X + IN_W - 8, "y2": cy}
        return Prim("line", {"stroke": "#d1d5db", "stroke-width": 1.5, "opacity": 0.8}, f)

    out += [strap_line(-1), strap_line(1), arm_line(-1), arm_line(1),
            Prim("ellipse", {"cx": cx, "cy": cy, "rx": 9, "ry": 17, "fill": TORSO, "stroke": SKIN_LINE,
                             "stroke-width": 1.5}),
            Prim("circle", {"cx": cx - 1, "cy": cy, "r": 8, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.2}),
            Prim("path", {"d": f"M{cx + 7} {cy - 3}L{cx + 11} {cy}L{cx + 7} {cy + 3}", "fill": HEAD,
                          "stroke": SKIN_LINE, "stroke-width": 1}),
            static_text("von oben", IN_X + IN_W / 2, IN_Y + IN_H + 14, 12, MUTED)]
    return out


BASE = dict(open=0.0, scap=0.0)
SET = dict(open=0.0, scap=1.0, chest=-3, neck=2)
OPEN = dict(SET, open=1.0)


def build():
    tl = FlyTimeline([(0, BASE), (0.8, BASE), (1.8, SET), (2.0, SET), (3.6, OPEN), (4.8, OPEN),
                      (6.4, SET), (6.8, BASE), (7.2, BASE)], skeleton=SIDE)

    def ctx(t):
        p = tl.at(t)
        return {"P": SIDE.fk(p), "pose": p}

    c_set, c_open = ctx(2.0), ctx(3.6)
    h0 = (c_set["pose"]["hx_n"], c_set["pose"]["hy_n"])
    h1 = (c_open["pose"]["hx_n"], c_open["pose"]["hy_n"])
    open_arrow = arrow(f"M{h0[0] - 6:.0f} {h0[1] + 16:.0f} Q{(h0[0] + h1[0]) / 2 + 4:.0f} {h1[1] + 30:.0f} "
                       f"{h1[0] + 12:.0f} {h1[1] + 18:.0f}", show=[(2.0, 3.6)])
    c0 = ctx(1.0)
    b0 = body_pt(c0, "thorax", 26, 24)
    b1 = body_pt(c0, "thorax", 2, 27)
    scap_arrow = arrow(f"M{b0[0]:.0f} {b0[1]:.0f} Q{b0[0] - 9:.0f} {(b0[1] + b1[1]) / 2:.0f} {b1[0]:.0f} {b1[1]:.0f}",
                       show=[(0.8, 2.0)])
    trap_focus = Prim("ellipse", {"rx": 8, "ry": 16, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                                  "_show": [(1.8, 6.4)]},
                      lambda c: dict(zip(("cx", "cy"), body_pt(c, "thorax", 8, 12))))
    post = [
        Prim("rect", {"x": 380, "y": 30, "width": 12, "height": FLOOR_Y - 30, "rx": 3, "fill": PROP_DARK}),
        Prim("rect", {"x": 370, "y": ANCHOR[1] - 7, "width": 14, "height": 14, "rx": 4, "fill": PROP}),
        Prim("circle", {"cx": ANCHOR[0], "cy": ANCHOR[1], "r": 4.5, "fill": "none", "stroke": "#d1d5db",
                        "stroke-width": 2.2}),
    ]
    ghost_parts = limb(["lumbar", "thorax", "chest"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side()
    scene = group([
        floor(FLOOR_Y, 60, 394),
        *post,
        ghost(ghost_parts, SIDE, ctx(0)["pose"], 0.13),
        *figure(),
        trap_focus,
        scap_arrow,
        open_arrow,
    ], scale=0.9, origin=(200, FLOOR_Y), dy=2)
    ay = FLOOR_Y + (ANCHOR[1] - FLOOR_Y) * 0.9 + 2
    prims = [
        scene,
        *top_inset(),
        caption_band(),
        static_text("Schultern bleiben weg von den Ohren", 200, 24, LEAD_SIZE, MUTED),
        static_text("Anker vorn", 362, ay - 14, 12, MUTED, anchor="end"),
        static_text("auf Brusthöhe", 362, ay - 0.5 + 18, 12, MUTED, anchor="end"),
        caption("Leicht zurücklehnen, Arme nach vorn", 0, 0.8),
        caption("Schulterblätter zurück & runter", 0.8, 2.0),
        caption("Arme im Bogen seitlich öffnen", 2.0, 3.6),
        caption("Kurz halten – Schulterblätter bleiben unten", 3.6, 4.8),
        caption("Kontrolliert zurück", 4.8, 7.2),
    ]
    return render(prims, tl, SIDE, fps=12, title="Reverse Flys (Sling)")
