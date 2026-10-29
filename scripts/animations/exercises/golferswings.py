from rig import *
from exercises._morgen_b_props import nose_hint, front_feet_out

SLUG = "golferswings"

# Frontansicht. Beide Hände gefasst schwingen diagonal von unten-seitlich nach
# oben über die andere Schulter; Seitenwechsel, dann gespiegelt.
# Der FRONT-Rig kann keine Rumpfdrehung – deshalb werden Schulterlinie, Rumpf
# und Arme hier selbst gezeichnet: Pose-Skalar "sy" (Schulterdrehung, Grad,
# >0 = Brust dreht zur rechten Bildseite) verkürzt die Schulterlinie, die
# Arme laufen als (leicht gebeugte) Kette von der Schulter zum gemeinsamen
# Griffpunkt. Becken und Gewicht wandern mit, die hintere Ferse hebt ab.
# Beine per IK, Füße bleiben am Boden.

FLOOR_Y = 252
CX = 200
SC = 0.86
ANK_Y = FLOOR_Y - 12
ANK_L = CX - 30
ANK_R = CX + 30
UA, FA, HA = 36.0, 32.0, 13.0
REACH = UA + FA - 0.5

STAND = dict(x=CX, y=FLOOR_Y - 113, hx=CX, hy=FLOOR_Y - 140, w=0.0, sy=0.0, lift_L=0, lift_R=0)
LOW_L = dict(STAND, x=CX - 7, y=FLOOR_Y - 110, lumbar=7, thorax=4, chest=1, neck=-9, head=-2, hinge=32,
             hx=CX - 50, hy=FLOOR_Y - 116, w=-1, sy=-58, lift_R=4)
HIGH_R = dict(STAND, x=CX + 9, y=FLOOR_Y - 115, lumbar=-5, thorax=-3, chest=-1, neck=6, head=3,
              hx=CX + 60, hy=FLOOR_Y - 232, w=1, sy=62, lift_L=8)
MIR = ("lumbar", "thorax", "chest", "neck", "head", "w", "sy")


def mirror(p):
    q = {k: (2 * CX - v if k in ("x", "hx") else (-v if k in MIR else v)) for k, v in p.items()}
    q["lift_L"], q["lift_R"] = p.get("lift_R", 0), p.get("lift_L", 0)
    return q


LOW_R, HIGH_L = mirror(LOW_L), mirror(HIGH_R)


def shoulders(P, pose):
    """Schulterpunkte (L, R) – Schulterlinie verkürzt sich mit der Drehung."""
    cx_, cy_ = pt(P, "chest")
    k = math.cos(math.radians(pose.get("sy", 0.0)))
    out = []
    for s in ("L", "R"):
        ex, ey = pt(P, f"clav_{s}")
        out.append((cx_ + (ex - cx_) * k, cy_ + (ey - cy_) + 2))
    return out


def grip(P, pose):
    """Griffpunkt (Handgelenke), für beide Schultern erreichbar."""
    sL, sR = shoulders(P, pose)
    tx, ty = pose["hx"], pose["hy"]
    mx, my = (sL[0] + sR[0]) / 2, (sL[1] + sR[1]) / 2
    for _ in range(40):
        if max(math.hypot(tx - sL[0], ty - sL[1]), math.hypot(tx - sR[0], ty - sR[1])) <= REACH:
            break
        tx, ty = mx + (tx - mx) * 0.97, my + (ty - my) * 0.97
    return tx, ty


def arm_chain(S, G, side):
    """Schulter -> Ellbogen -> Handgelenk -> Fingerspitzen. Ellbogen weich
    gebeugt; zeigt der Arm zum Betrachter (kurze Projektion), wird er
    verkürzt statt stark gebeugt."""
    d = max(1e-6, math.hypot(G[0] - S[0], G[1] - S[1]))
    k = min(1.0, max(d / (REACH * 0.96), 0.4))      # zum Betrachter: verkürzt statt geknickt
    l1, l2 = UA * k, FA * k
    dd = min(d, l1 + l2 - 1e-3)
    a = math.acos(max(-1, min(1, (l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd))))
    base = math.atan2(G[1] - S[1], G[0] - S[0])
    ang = base + side * a                       # Ellbogen nach außen
    E = (S[0] + l1 * math.cos(ang), S[1] + l1 * math.sin(ang))
    ux, uy = (G[0] - E[0]), (G[1] - E[1])
    n = math.hypot(ux, uy) or 1
    T = (G[0] + ux / n * HA * k, G[1] + uy / n * HA * k)
    return [S, E, G, T]


UPPER = {"lumbar", "thorax", "chest", "neck", "head", "clav_L", "clav_R", "upperarm_L", "forearm_L", "hand_L",
         "upperarm_R", "forearm_R", "hand_R"}


class HingeFront(Skeleton):
    """FRONT mit Hüftbeuge nach vorn (Pose-Skalar "hinge", Grad): der
    Oberkörper wird in der Frontansicht senkrecht verkürzt gesehen."""

    def __init__(self):
        super().__init__(FRONT.segs)

    def fk(self, pose):
        out = FRONT.fk(pose)
        k = math.cos(math.radians(pose.get("hinge", 0.0)))
        ry = pose.get("y", 200.0)
        for n in UPPER:
            sx, sy, ex, ey, a = out[n]
            out[n] = (sx, ry + (sy - ry) * k, ex, ry + (ey - ry) * k, a)
        return out


HFRONT = HingeFront()


class SwingTimeline(Timeline):
    def at(self, t):
        p = self._interp(t)
        # Hinteres Bein (Ferse hoch) knickt nach innen, Standbein nach außen/gerade
        bl = 1 if p.get("lift_L", 0) > 0.5 else -1
        br = -1 if p.get("lift_R", 0) > 0.5 else 1
        for ik in (IK("thigh_L", "shin_L", (ANK_L, ANK_Y - p.get("lift_L", 0)), bend=bl),
                   IK("thigh_R", "shin_R", (ANK_R, ANK_Y - p.get("lift_R", 0)), bend=br)):
            p = solve_ik(FRONT, p, ik)
        p["turn"] = 0.75 * math.sin(math.radians(p.get("sy", 0.0)))
        return p


def geo(c):
    g = c.get("_g")
    if g is None:
        P, pose = c["P"], c["pose"]
        sL, sR = shoulders(P, pose)
        G = grip(P, pose)
        # Hände leicht versetzt: beide fassen ineinander
        g = {"sL": sL, "sR": sR, "G": G,
             "armL": arm_chain(sL, (G[0] - 1.5, G[1] - 1), -1),
             "armR": arm_chain(sR, (G[0] + 1.5, G[1] + 1), 1)}
        c["_g"] = g
    return g


def stroke(fn, width, color, extra=None, outline=True):
    out = []
    for w, col in (((width + 3, SKIN_LINE),) if outline else ()) + ((width, color),):
        def d(c, f=fn):
            r = {"d": smooth_path(f(c))}
            if extra:
                r.update(extra(c))
            return r
        out.append(Prim("path", {"fill": "none", "stroke": col, "stroke-width": w, "stroke-linecap": "round",
                                 "stroke-linejoin": "round"}, d))
    return out


def figure():
    prims = []
    lift = lambda side, c: min(1.0, c["pose"].get(f"lift_{side}", 0) / 8.0)
    prims += limb(["hip_L", "thigh_L", "shin_L"], 16, NEAR) + limb(["hip_R", "thigh_R", "shin_R"], 16, NEAR)
    prims += front_feet_out(12, lift=lift)
    prims += limb(["neck"], 13, TORSO)

    def trunk(c):
        P = c["P"]
        return chain_points(P, ["lumbar", "thorax", "chest"])

    tw = lambda base: (lambda c: {"stroke-width": round(base - 8 * abs(math.sin(math.radians(c["pose"]["sy"]))), 1)})
    sh = lambda c: [geo(c)["sL"], pt(c["P"], "chest"), geo(c)["sR"]]
    prims += [stroke(sh, 22, TORSO)[0],
              stroke(trunk, 44, TORSO, extra=tw(47))[0],
              stroke(sh, 22, TORSO, outline=False)[0],
              stroke(trunk, 44, TORSO, extra=tw(44), outline=False)[0]]
    # Brustbein-Linie wandert mit der Drehung (zeigt, wohin die Brust zeigt)
    prims.append(Prim("path", {"fill": "none", "stroke": "#6366f1", "stroke-width": 3, "stroke-linecap": "round"},
                      lambda c: (lambda s, ch, th: {"d": f"M{ch[0] + 15 * s:.1f} {ch[1] + 8:.1f}"
                                                         f"L{th[0] + 13 * s:.1f} {th[1] + 4:.1f}"})(
                          math.sin(math.radians(c["pose"]["sy"])), pt(c["P"], "chest"), pt(c["P"], "thorax"))))
    prims += head_front()
    # Arme vor dem Rumpf; der Arm der weggedrehten Schulter liegt unten.
    vis = lambda want: (lambda c: {"opacity": 1 if (c["pose"]["sy"] > 0) == want else 0})
    armL = lambda c: geo(c)["armL"]
    armR = lambda c: geo(c)["armR"]
    prims += stroke(armR, 13, NEAR, extra=vis(True))
    prims += stroke(armL, 13, NEAR)
    prims += stroke(armR, 13, NEAR, extra=vis(False))
    return prims


def build():
    tl = SwingTimeline([(0, LOW_L), (0.35, LOW_L), (1.35, HIGH_R), (1.65, HIGH_R), (2.6, LOW_L),
                        (3.25, LOW_R), (3.6, LOW_R), (4.6, HIGH_L), (4.9, HIGH_L), (5.85, LOW_R),
                        (6.5, LOW_L)], skeleton=HFRONT)
    dur = tl.duration

    def foot_weight(side):
        sgn = -1 if side == "L" else 1
        ax = ANK_L if side == "L" else ANK_R
        return Prim("ellipse", {"cx": ax + sgn * 3, "cy": FLOOR_Y + 1, "rx": 17, "ry": 3.5, "fill": GOOD},
                    lambda c: {"opacity": round(max(0.0, sgn * c["pose"]["w"]) * 0.75, 2)})

    def grip_at(t):
        pose = tl.at(t)
        c = {"P": HFRONT.fk(pose), "pose": pose}
        return geo(c)["armL"][3]

    a0, a1 = grip_at(0.0), grip_at(1.45)
    m = lambda q: (2 * CX - q[0], q[1])

    def bahn(p0, p1, bow, show, dashed):
        mx, my = (p0[0] + p1[0]) / 2 + bow, (p0[1] + p1[1]) / 2 + abs(bow) * 0.35
        d = f"M{p0[0]:.0f} {p0[1]:.0f}Q{mx:.0f} {my:.0f} {p1[0]:.0f} {p1[1]:.0f}"
        if dashed:
            return Prim("path", {"d": d, "fill": "none", "stroke": ACCENT, "stroke-width": 1.6,
                                 "stroke-dasharray": "3 5", "opacity": 0.5, "_show": show})
        return arrow(d, width=3, show=show)

    o0, o1 = (a0[0] - 14, a0[1] + 8), (a1[0] + 16, a1[1] + 2)
    main = group([
        foot_weight("L"), foot_weight("R"),
        bahn(a0, a1, 44, [(0, 2.6)], True),
        bahn(m(a0), m(a1), -44, [(3.25, 5.85)], True),
        *figure(),
        bahn(o0, o1, 62, [(0.35, 1.4)], False),
        bahn(m(o0), m(o1), -62, [(3.6, 4.65)], False),
    ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        floor(FLOOR_Y + 1, 60, 340),
        main,
        caption_band(),
        caption("Von unten-seitlich diagonal hoch", 0, 1.65),
        caption("Locker zurückschwingen", 1.65, 2.6),
        caption("Seite wechseln", 2.6, 3.6),
        caption("Über die andere Schulter – Gewicht mit", 3.6, 4.9),
        caption("Beide Seiten gleich oft", 4.9, dur),
        static_text("Gewicht wandert mit dem Schwung", 200, 24, 13, MUTED),
        nose_hint(),
    ]
    return render(prims, tl, HFRONT, title="Golferswings", fps=15)
