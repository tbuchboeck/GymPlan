from rig import *

SLUG = "ytw"

# Bauchlage von oben (FRONT-Skelett, rot=-90 -> Kopf rechts, wir sehen den
# Rücken). L-Arm = obere Bildhälfte, R-Arm = untere. Unten links eine kleine
# Seitansicht: Stirn auf dem Handtuch, Arm hebt nur 2–3 cm ab.
# Pose-Skalare: lift (0..1) = Arme angehoben, sq (0..1) = Schulterblätter
# zurück & runter.

CX, CY = 196, 140              # Becken (unskaliert)
GS = 0.92                      # Gruppen-Skalierung um (230, CY)
GO = (230, CY)

BASE = dict(x=CX, y=CY, rot=-90, thigh_L=-3, thigh_R=3, shin_L=1, shin_R=-1)


def letter(ua, fa=0.0, **kw):
    p = dict(BASE)
    p["upperarm_L"] = ua - 180
    p["upperarm_R"] = 180 - ua
    p["forearm_L"] = -fa
    p["forearm_R"] = fa
    p.update(kw)
    return p


Y0 = letter(28)                      # Arme schräg vorn (Y)
T0 = letter(90)                      # seitlich (T)
W0 = letter(135, 75)                 # Ellbogen an den Rippen, Hände neben den Schultern


def up(p):
    return dict(p, lift=1.0, sq=1.0)


def sq(p):
    return dict(p, sq=1.0)


# --- Zeitplan --------------------------------------------------------------
SEQ = [("Y", Y0), ("T", T0), ("W", W0)]
TRANS, PREP, LIFT, HOLD, DOWN = 1.1, 0.5, 0.6, 2.0, 0.7
BLOCK = TRANS + PREP + LIFT + HOLD + DOWN


def timeline():
    keys = [(0.0, Y0)]
    t = 0.0
    for i, (_, p) in enumerate(SEQ):
        t += TRANS                 # Übergang (bzw. beim Y: kurz ruhig liegen)
        t = round(t, 3)
        keys.append((t, p))
        t += PREP
        t = round(t, 3)
        keys.append((t, sq(p)))
        t += LIFT
        t = round(t, 3)
        keys.append((t, up(p)))
        t += HOLD
        t = round(t, 3)
        keys.append((t, up(p)))
        t += DOWN
        t = round(t, 3)
        keys.append((t, p))
    t += TRANS
    keys.append((round(t, 3), Y0))
    return Timeline(keys, skeleton=FRONT)


def windows(i):
    return i * BLOCK + TRANS


# --- Zeichnen ---------------------------------------------------------------


def axis(c):
    a = math.radians(c["P"]["chest"][4])
    u = (math.cos(a), -math.sin(a))          # Richtung Kopf
    v = (math.cos(a + math.pi / 2), -math.sin(a + math.pi / 2))  # Richtung L-Seite
    return u, v


def body_pt(c, along, lat):
    """Punkt relativ zum Schulter-Mittelpunkt (Ende 'chest')."""
    x, y = pt(c["P"], "chest")
    u, v = axis(c)
    return x + along * u[0] + lat * v[0], y + along * u[1] + lat * v[1]


def arm_chain(c, side):
    P = c["P"]
    return chain_points(P, [f"upperarm_{side}", f"forearm_{side}", f"hand_{side}"])


def arm_prims(side):
    def d(c):
        return {"d": smooth_path(arm_chain(c, side)), "stroke-width": 13 + 2.2 * c["pose"].get("lift", 0)}

    def d_out(c):
        r = d(c)
        r["stroke-width"] += 3
        return r

    def shadow(c):
        lf = c["pose"].get("lift", 0)
        pts = [(x + 5 * lf, y + 8 * lf) for x, y in arm_chain(c, side)]
        return {"d": smooth_path(pts), "opacity": 0.15 + 0.4 * lf}

    return (
        Prim("path", {"fill": "none", "stroke": "#0b1220", "stroke-width": 14, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, shadow),
        [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-linecap": "round", "stroke-linejoin": "round"}, d_out),
         Prim("path", {"fill": "none", "stroke": NEAR, "stroke-linecap": "round", "stroke-linejoin": "round"}, d)],
    )


def scapula(side):
    s = 1 if side == "L" else -1

    def f(c):
        k = c["pose"].get("sq", 0.0)
        m = 9 - 5 * k            # Abstand zur Wirbelsäule (zurück = näher)
        sh = -7 * k               # runter = Richtung Füße
        a = body_pt(c, -2 + sh, s * m)            # oberer Innenwinkel
        b = body_pt(c, -4 + sh, s * (m + 16))     # Schulterecke
        e = body_pt(c, -25 + sh, s * (m + 3))     # unterer Winkel
        q2 = body_pt(c, -17 + sh, s * (m + 14))
        q3 = body_pt(c, -13 + sh, s * (m - 1.5))
        return {"d": f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}"
                     f"Q{q2[0]:.1f} {q2[1]:.1f} {e[0]:.1f} {e[1]:.1f}"
                     f"Q{q3[0]:.1f} {q3[1]:.1f} {a[0]:.1f} {a[1]:.1f}Z"}

    return Prim("path", {"fill": "#7078ea", "stroke": "#4b4fc4", "stroke-width": 1.5,
                         "stroke-linejoin": "round"}, f)


def spine():
    def f(c):
        P = c["P"]
        a = pt(P, "lumbar", end=False)
        b = pt(P, "chest")
        return {"x1": a[0], "y1": a[1], "x2": b[0], "y2": b[1]}
    return Prim("line", {"stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-dasharray": "3 4", "opacity": 0.6}, f)


def head_back(r=17):
    def c_(c):
        x, y = pt(c["P"], "head")
        return {"cx": x, "cy": y}

    def ears(side):
        def f(c):
            x, y = pt(c["P"], "head")
            u, v = axis(c)
            s = 1 if side == "L" else -1
            return {"cx": x + s * v[0] * (r + 1) - u[0] * 1, "cy": y + s * v[1] * (r + 1)}
        return f

    return [
        Prim("ellipse", {"rx": 3.2, "ry": 5.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, ears("L")),
        Prim("ellipse", {"rx": 3.2, "ry": 5.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5}, ears("R")),
        Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, c_),
        Prim("circle", {"r": r, "fill": "#4338ca"}, c_),
        Prim("circle", {"r": r * 0.55, "fill": "#3b32b8"}, c_),
    ]


def figure():
    shL, armL = arm_prims("L")
    shR, armR = arm_prims("R")
    trunk_focus = Prim("ellipse", {"rx": 14, "ry": 7, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                                   "_show": [(windows(i) + PREP, windows(i) + PREP + LIFT + HOLD) for i in range(3)]},
                       lambda c: dict(zip(("cx", "cy"), body_pt(c, -17 - 5 * c["pose"].get("sq", 0), 0))))
    prims = [shL, shR]
    prims += limb(["hip_L", "thigh_L", "shin_L", "foot_L"], 16, FAR)
    prims += limb(["hip_R", "thigh_R", "shin_R", "foot_R"], 16, FAR)
    prims += limb(["neck"], 13, TORSO)
    trunk = limb(["lumbar", "thorax", "chest"], 52, TORSO)
    sh = lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])}
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 29, "stroke-linecap": "round"}, sh),
              trunk[0],
              Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 26, "stroke-linecap": "round"}, sh),
              trunk[1]]
    prims += [spine(), scapula("L"), scapula("R"), trunk_focus]
    prims += armL + armR
    prims += head_back()
    return prims


def props():
    # Matte (von oben) und Handtuch unter der Stirn
    hx = CX + 78 + 17 + 15
    return [
        Prim("rect", {"x": CX - 125, "y": CY - 46, "width": 290, "height": 92, "rx": 8, "fill": "#3f4a7a"}),
        Prim("rect", {"x": CX - 125, "y": CY - 46, "width": 290, "height": 92, "rx": 8, "fill": "none",
                      "stroke": "#4f5b92", "stroke-width": 2}),
        Prim("rect", {"x": hx - 10, "y": CY - 22, "width": 34, "height": 44, "rx": 5, "fill": "#94a3b8",
                      "opacity": 0.75}),
        Prim("line", {"x1": hx + 18, "y1": CY - 22, "x2": hx + 18, "y2": CY + 22, "stroke": "#cbd5e1",
                      "stroke-width": 2, "opacity": 0.6}),
    ]


# --- Seitansicht-Inset -----------------------------------------------------
IX, IY, IW, IH = 10, 190, 222, 64
S_ = 0.55
MAT_Y = IY + IH - 12


def side_inset():
    foot_x = IX + 22
    sh_x = foot_x + (107 + 78) * S_
    head_x = sh_x + 32 * S_ + 4

    def arm(c):
        P = c["P"]
        lf = c["pose"].get("lift", 0)
        s = pt(P, "clav_R")
        e = pt(P, "upperarm_R")
        h = pt(P, "forearm_R")
        f = pt(P, "hand_R")
        k = S_ / 1.0
        y_low = MAT_Y - 3 - lf * 4.5
        return [(sh_x, MAT_Y - 7), (sh_x + (e[0] - s[0]) * k, y_low - 0.5),
                (sh_x + (h[0] - s[0]) * k, y_low), (sh_x + (f[0] - s[0]) * k, y_low)]

    def arm_d(c):
        return {"d": smooth_path(arm(c))}

    def gap(c):
        lf = c["pose"].get("lift", 0)
        x = arm(c)[-1][0] + 8
        return {"x1": x, "y1": MAT_Y - 1, "x2": x, "y2": MAT_Y - 3 - lf * 4.5, "opacity": lf}

    prims = [
        Prim("rect", {"x": IX, "y": IY, "width": IW, "height": IH, "rx": 8, "fill": "#0b1220", "opacity": 0.75}),
        Prim("rect", {"x": IX + 8, "y": MAT_Y, "width": IW - 16, "height": 4, "rx": 2, "fill": "#3f4a7a"}),
        # Handtuch unter der Stirn
        Prim("rect", {"x": head_x - 2, "y": MAT_Y - 4, "width": 13, "height": 4, "rx": 1.5, "fill": "#94a3b8"}),
        # Beine + Rumpf
        Prim("path", {"d": f"M{foot_x:.1f} {MAT_Y - 4}L{sh_x - 2:.1f} {MAT_Y - 7}", "stroke": SKIN_LINE,
                      "stroke-width": 11, "stroke-linecap": "round", "fill": "none"}),
        Prim("path", {"d": f"M{foot_x:.1f} {MAT_Y - 4}L{foot_x + 107 * S_:.1f} {MAT_Y - 5}", "stroke": FAR,
                      "stroke-width": 7, "stroke-linecap": "round", "fill": "none"}),
        Prim("path", {"d": f"M{foot_x + 107 * S_:.1f} {MAT_Y - 6}L{sh_x - 2:.1f} {MAT_Y - 8}", "stroke": TORSO,
                      "stroke-width": 10, "stroke-linecap": "round", "fill": "none"}),
        Prim("circle", {"cx": head_x, "cy": MAT_Y - 11, "r": 7.5, "fill": HEAD, "stroke": SKIN_LINE,
                        "stroke-width": 1.5}),
        Prim("path", {"d": f"M{head_x - 7:.1f} {MAT_Y - 14}A7.5 7.5 0 0 1 {head_x + 3:.1f} {MAT_Y - 18.3}"
                           f"L{head_x - 2:.1f} {MAT_Y - 12}Z", "fill": "#4338ca"}),
        # Linie Kopf–Wirbelsäule (neutral)
        Prim("line", {"x1": foot_x + 60, "y1": MAT_Y - 16, "x2": head_x + 12, "y2": MAT_Y - 16,
                      "stroke": GOOD, "stroke-width": 1.2, "stroke-dasharray": "3 3", "opacity": 0.7}),
        Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 8.5, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, arm_d),
        Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 6, "stroke-linecap": "round",
                      "stroke-linejoin": "round"}, arm_d),
        Prim("line", {"stroke": ACCENT, "stroke-width": 2}, gap),
        static_text("Kopf bleibt in", IX + 10, IY + 15, 10, GOOD, anchor="start"),
        static_text("Verlängerung", IX + 10, IY + 27, 10, GOOD, anchor="start"),
    ]
    return prims


def build():
    tl = timeline()
    dur = tl.duration
    big = []
    caps = []
    texts = {
        "Y": ("Y: Arme schräg nach vorn, Daumen hoch", "Schulterblätter runter, Arme 2–3 cm heben"),
        "T": ("T: Arme seitlich, Daumen hoch", "Erst Schulterblätter, dann Arme heben"),
        "W": ("W: Ellbogen an die Rippen", "Ellbogen & Hände heben – 2 s halten"),
    }
    for i, (name, _) in enumerate(SEQ):
        b0 = i * BLOCK
        t_set = b0 + TRANS
        t_end = b0 + BLOCK
        big.append(Prim("text", {"x": 56, "y": 86, "font-size": 64, "font-weight": "800", "fill": ACCENT,
                                 "text-anchor": "middle", "_show": [(b0 + 0.4 if i else 0, t_end + 0.4)]},
                        text=name))
        a, b = texts[name]
        caps.append(caption(a, b0 if i else 0, t_set, size=14))
        caps.append(caption(b, t_set, t_end, size=14))
    caps.append(caption("Zurück zum Y", 3 * BLOCK, dur, size=14))
    big[0].attrs["_show"] = [(0, BLOCK + 0.4), (3 * BLOCK + 0.4, dur)]

    def lbl_pos(c):
        P = c["P"]
        sx = pt(P, "clav_R")[0]
        fx = pt(P, "hand_R")[0]
        foot_x = IX + 22
        sh_x = foot_x + (107 + 78) * S_
        return {"x": sh_x + (fx - sx) * S_ + 8}

    lift_lbl = Prim("text", {"y": MAT_Y - 26, "font-size": 10, "fill": ACCENT,
                             "text-anchor": "middle", "font-weight": "600",
                             "_show": [(i * BLOCK + TRANS + PREP + 0.3, i * BLOCK + TRANS + PREP + LIFT + HOLD)
                                       for i in range(3)]}, lbl_pos, text="2–3 cm")

    scene = group([*props(), *figure()], scale=GS, origin=GO)
    prims = [
        scene,
        *side_inset(),
        lift_lbl,
        *big,
        caption_band(),
        *caps,
    ]
    return render(prims, tl, FRONT, title="Y-T-W in Bauchlage", fps=10)
