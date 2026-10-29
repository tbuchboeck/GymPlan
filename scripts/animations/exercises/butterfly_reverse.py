from rig import *
from ._hantel_b_props import dumbbell, front_fig, label

SLUG = "butterfly-reverse"

# Vorgebeugtes Reverse Butterfly. Hauptbild: Frontansicht der vorgebeugten
# Person (Rumpf/Hals perspektivisch verkürzt, Kopf blickt zum Boden), Arme
# heben seitlich bis Schulterhöhe. Kleines Inset rechts oben zeigt die
# Seitansicht der Haltung (Hüfte gebeugt, Rücken gerade); dort wird der Arm
# als Projektion mitbewegt.

FLOOR_Y = 250
LEAN = 50.0                                  # Rumpfneigung aus der Senkrechten
K = math.cos(math.radians(LEAN))
_LEN = {"lumbar": 26 * K, "thorax": 26 * K, "chest": 26 * K, "neck": 17 * K, "head": 15 * K,
        "thigh_L": 47, "thigh_R": 47}
BENT = Skeleton([Seg(s.name, s.parent, _LEN.get(s.name, s.length), s.rest) for s in FRONT.segs])

CX = 172
LEGS = dict(hip_L=0, hip_R=0, thigh_L=-5, thigh_R=5, shin_L=4, shin_R=-4)
BASE = dict(x=CX, y=FLOOR_Y - 104, **LEGS)


def arms(ua, fa=14.0, clav=0.0):
    """ua = Abduktion aus der Hängeposition, fa = leichte Ellbogenbeugung."""
    return dict(upperarm_L=-ua, forearm_L=fa, upperarm_R=ua, forearm_R=-fa, clav_L=-clav, clav_R=clav,
                ua=ua)


DOWN = dict(BASE, **arms(6, 18))
UP = dict(BASE, **arms(84, 12, clav=-3))


def head_down(r=17.0):
    """Kopf von vorn, Blick zum Boden: viel Haar oben, Augen tief."""
    def c(cc):
        x, y = pt(cc["P"], "head")
        return x, y + 4

    def skull(cc):
        x, y = c(cc)
        return {"cx": x, "cy": y}

    def hair(cc):
        x, y = c(cc)
        return {"d": f"M{x - r - 1:.1f} {y + 4:.1f}A{r + 1} {r + 1} 0 0 1 {x + r + 1:.1f} {y + 4:.1f}"
                     f"Q{x:.1f} {y - 2:.1f} {x - r - 1:.1f} {y + 4:.1f}Z"}

    def eye(side):
        return lambda cc: (lambda x, y: {"cx": x + side * 6, "cy": y + 9})(*c(cc))

    def brow(cc):
        x, y = c(cc)
        return {"d": f"M{x - 2:.1f} {y + 13:.1f}L{x + 2:.1f} {y + 13:.1f}"}

    return [
        Prim("circle", {"r": r + 1.5, "fill": SKIN_LINE}, skull),
        Prim("circle", {"r": r, "fill": HEAD}, skull),
        Prim("path", {"fill": "#4338ca"}, hair),
        Prim("circle", {"r": 2.0, "fill": SKIN_LINE}, eye(-1)),
        Prim("circle", {"r": 2.0, "fill": SKIN_LINE}, eye(1)),
        Prim("path", {"stroke": SKIN_LINE, "stroke-width": 1.5, "stroke-linecap": "round"}, brow),
    ]


# --- Seitansicht-Inset --------------------------------------------------------
IN_X, IN_Y, IN_W, IN_H = 300, 40, 92, 110
IS = 0.42
SIDE_POSE = dict(x=0, y=0, rot=-LEAN, neck=12, head=4, thigh_n=34, shin_n=-30, foot_n=-4,
                 thigh_f=32, shin_f=-28, foot_f=-4, upperarm_n=LEAN, upperarm_f=LEAN)


def side_inset():
    P = SIDE.fk(SIDE_POSE)
    foot_y = max(P["foot_n"][3], P["shin_n"][3])
    ox, oy = IN_X + 34, IN_Y + IN_H - 12 - (foot_y - 0) * IS

    def tr(p):
        return ox + p[0] * IS, oy + p[1] * IS

    def st(names, w, col):
        d = smooth_path([tr(p) for p in chain_points(P, names)])
        return [Prim("path", {"d": d, "fill": "none", "stroke": SKIN_LINE, "stroke-width": w + 2,
                              "stroke-linecap": "round", "stroke-linejoin": "round"}),
                Prim("path", {"d": d, "fill": "none", "stroke": col, "stroke-width": w,
                              "stroke-linecap": "round", "stroke-linejoin": "round"})]

    sx, sy = tr(pt(P, "chest"))
    hx, hy = tr(pt(P, "head"))
    L = 70 * IS

    def arm_d(c):
        ua = c["pose"].get("ua", 0.0)
        ln = L * math.cos(math.radians(ua))      # Projektion: Arm kommt zum Betrachter
        return {"d": f"M{sx:.1f} {sy:.1f}L{sx:.1f} {sy + max(ln, 0.5):.1f}"}

    def db(c):
        ua = c["pose"].get("ua", 0.0)
        ln = L * math.cos(math.radians(ua))
        return {"cx": sx, "cy": sy + ln}

    floor_y = IN_Y + IN_H - 12
    a = math.radians(P["chest"][4] + 90)
    back = [tr(pt(P, "lumbar", False)), tr(pt(P, "chest"))]
    back = [(x + 8 * math.cos(a), y - 8 * math.sin(a)) for x, y in back]
    prims = [Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "rx": 8, "fill": "#0b1220",
                           "opacity": 0.7}),
             Prim("line", {"x1": IN_X + 8, "y1": floor_y, "x2": IN_X + IN_W - 8, "y2": floor_y,
                           "stroke": FLOOR, "stroke-width": 2})]
    prims += st(["thigh_f", "shin_f", "foot_f"], 6, FAR)
    prims += st(["neck"], 5, TORSO)
    prims += st(["lumbar", "thorax", "chest"], 12, TORSO)
    prims += [Prim("circle", {"cx": hx, "cy": hy, "r": 7.5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5})]
    prims += st(["thigh_n", "shin_n", "foot_n"], 7, NEAR)
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 8, "stroke-linecap": "round"}, arm_d),
              Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 6, "stroke-linecap": "round"}, arm_d),
              Prim("circle", {"r": 4.5, "fill": PROP, "stroke": "#1e293b", "stroke-width": 1.5}, db),
              Prim("line", {"x1": back[0][0], "y1": back[0][1], "x2": back[1][0], "y2": back[1][1], "stroke": GOOD,
                            "stroke-width": 1.8, "stroke-dasharray": "3 3"}),
              static_text("~45° vorgebeugt", IN_X + IN_W / 2, IN_Y + 14, 10, MUTED)]
    return prims


def build():
    tl = Timeline([(0, DOWN), (0.6, DOWN), (1.9, UP), (2.6, UP), (4.1, DOWN), (4.6, DOWN)], skeleton=BENT)
    P_up = BENT.fk(UP)
    P_dn = BENT.fk(DOWN)
    lh, rh = pt(P_dn, "hand_L"), pt(P_dn, "hand_R")
    lu, ru = pt(P_up, "hand_L"), pt(P_up, "hand_R")

    figure = front_fig(
        db_L=dumbbell("hand_L", "forearm_L", fore=0.9, size=1.05),
        db_R=dumbbell("hand_R", "forearm_R", fore=0.9, size=1.05),
        head_fn=head_down,
    )
    prims = [
        floor(FLOOR_Y + 2, 20, 290),
        ghost(limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR) + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR),
              BENT, DOWN, 0.15),
        *figure,
        focus("clav_L", rx=10, ry=9, offset=(2, 0), show=[(0.6, 4.1)]),
        focus("clav_R", rx=10, ry=9, offset=(-2, 0), show=[(0.6, 4.1)]),
        arrow(f"M{lh[0] - 22:.0f} {lh[1] - 6:.0f} Q{lu[0] - 6:.0f} {lh[1] - 4:.0f} {lu[0] - 6:.0f} {lu[1] + 22:.0f}",
              show=[(0.6, 1.9)]),
        arrow(f"M{rh[0] + 22:.0f} {rh[1] - 6:.0f} Q{ru[0] + 6:.0f} {rh[1] - 4:.0f} {ru[0] + 6:.0f} {ru[1] + 22:.0f}",
              show=[(0.6, 1.9)]),
        label("Schulterblätter zusammen", CX, 62, 1.9, 2.6, 12, GOOD),
        *side_inset(),
        caption_band(),
        caption("Vorgebeugt, Rücken gerade, Arme hängen", 0, 0.6),
        caption("Ausatmen – Arme seitlich anheben", 0.6, 1.9),
        caption("Oben kurz halten", 1.9, 2.6),
        caption("Einatmen – langsam senken", 2.6, 4.6),
        static_text("Nur bis Schulterhöhe – Ellbogen leicht gebeugt", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, BENT, title="Butterfly reverse (vorgebeugt)")
