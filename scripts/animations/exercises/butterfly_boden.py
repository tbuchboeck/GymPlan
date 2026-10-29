from rig import *
from ._hantel_b_props import dumbbell, label

SLUG = "butterfly-boden"

# Butterfly am Boden (Floor Fly). Blick vom Fußende, Kamera leicht erhöht:
# Person liegt auf der Matte (Kopf hinten, Knie angewinkelt vorn), die Arme
# öffnen sich in der Bildebene bis die Ellbogen den Boden berühren und
# kommen im Bogen über der Brust zusammen. Der Körper bleibt ruhig – nur
# die Arme sind ein Rig (FRONT mit breiteren Schultern). Die Hanteln liegen
# im neutralen Griff (Handflächen zueinander) und zeigen daher zum
# Betrachter – perspektivisch verkürzt. Inset: Seitansicht der Lage.

SH_Y = 156                          # Schulterhöhe (Bildschirm)
CX = 186
_LEN = {"clav_L": 33, "clav_R": 33}
ARMS = Skeleton([Seg(s.name, s.parent, _LEN.get(s.name, s.length), s.rest) for s in FRONT.segs])
BASE = dict(x=CX, y=SH_Y + 78)


def arms(ua_abs, fa_rel):
    """ua_abs: absoluter Winkel des linken Oberarms (180 = waagrecht nach
    links, 90 = senkrecht hoch); rechts gespiegelt. fa_rel: Ellbogenbeugung
    (positiv = Unterarm dreht Richtung Decke/Mitte)."""
    return dict(BASE, upperarm_L=ua_abs - 270, forearm_L=-fa_rel, upperarm_R=(180 - ua_abs) + 90,
                forearm_R=fa_rel)


UP = arms(84, 22)          # Hanteln über der Brust zusammen
OPEN = arms(190, 26)       # Ellbogen auf der Matte, Unterarme leicht hoch


def body():
    """Statischer Körper aus Sicht vom Fußende."""
    sx_l, sx_r = CX - 34, CX + 34
    mat = Prim("path", {"d": f"M{CX - 92} 140L{CX + 92} 140L{CX + 150} 246L{CX - 150} 246Z", "fill": "#3f4a7a"})
    mat_edge = Prim("path", {"d": f"M{CX - 150} 246L{CX + 150} 246L{CX + 150} 250L{CX - 150} 250Z",
                             "fill": "#2f3866"})
    head = [Prim("circle", {"cx": CX, "cy": SH_Y - 20, "r": 17.5, "fill": SKIN_LINE}),
            Prim("circle", {"cx": CX, "cy": SH_Y - 20, "r": 16, "fill": HEAD}),
            Prim("path", {"d": f"M{CX - 16} {SH_Y - 24}A16 16 0 0 1 {CX + 16} {SH_Y - 24}Q{CX} {SH_Y - 32} {CX - 16} {SH_Y - 24}Z",
                          "fill": "#4338ca"}),
            Prim("circle", {"cx": CX - 6, "cy": SH_Y - 19, "r": 2.1, "fill": SKIN_LINE}),
            Prim("circle", {"cx": CX + 6, "cy": SH_Y - 19, "r": 2.1, "fill": SKIN_LINE}),
            Prim("path", {"d": f"M{CX} {SH_Y - 16}L{CX} {SH_Y - 11}", "stroke": SKIN_LINE, "stroke-width": 1.5,
                          "stroke-linecap": "round"})]
    trunk_d = (f"M{sx_l - 4} {SH_Y - 4}Q{CX} {SH_Y - 14} {sx_r + 4} {SH_Y - 4}"
               f"L{CX + 26} {SH_Y + 52}Q{CX} {SH_Y + 58} {CX - 26} {SH_Y + 52}Z")
    trunk = [Prim("path", {"d": trunk_d, "fill": TORSO, "stroke": SKIN_LINE, "stroke-width": 3,
                           "stroke-linejoin": "round"})]
    # Knie angewinkelt (zum Betrachter hin), Füße auf der Matte
    legs = []
    for side in (-1, 1):
        hip = (CX + side * 14, SH_Y + 50)
        knee = (CX + side * 24, SH_Y + 60)
        foot = (CX + side * 30, 236)
        for w, col in ((19, SKIN_LINE), (16, NEAR)):
            legs.append(Prim("path", {"d": f"M{hip[0]} {hip[1]}L{knee[0]} {knee[1]}L{foot[0]} {foot[1]}",
                                      "fill": "none", "stroke": col, "stroke-width": w,
                                      "stroke-linecap": "round", "stroke-linejoin": "round"}))
        legs.append(Prim("circle", {"cx": knee[0], "cy": knee[1], "r": 10.5, "fill": NEAR, "stroke": SKIN_LINE,
                                    "stroke-width": 1.5}))
    shoulders = [Prim("circle", {"cx": x, "cy": SH_Y, "r": 9, "fill": TORSO}) for x in (sx_l + 1, sx_r - 1)]
    return [mat, mat_edge, *head, *trunk, *shoulders, *legs]


IN_X, IN_Y, IN_W, IN_H = 300, 38, 92, 84
IS = 0.42
LIE = dict(x=0, y=0, rot=90, neck=-6, head=2, thigh_n=48, shin_n=-118, thigh_f=46, shin_f=-114,
           foot_n=-20, foot_f=-22, upperarm_n=0, upperarm_f=0)


def side_inset():
    P = SIDE.fk(LIE)
    floor_y = IN_Y + IN_H - 12
    ox = IN_X + 56
    oy = floor_y - 13 * IS * 1.8

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

    def arm_len(c):
        Pm = c["P"]
        return max(0.5, (pt(Pm, "clav_L")[1] - grip(Pm)[1]) * IS * 0.95)

    def grip(Pm):
        x0, y0, x1, y1, _ = Pm["hand_L"]
        return x0 + (x1 - x0) * 0.45, y0 + (y1 - y0) * 0.45

    arm = lambda c: {"d": f"M{sx:.1f} {sy:.1f}L{sx:.1f} {sy - arm_len(c):.1f}"}
    prims = [Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "rx": 8, "fill": "#0b1220",
                           "opacity": 0.7}),
             Prim("rect", {"x": IN_X + 8, "y": floor_y - 2, "width": IN_W - 16, "height": 3, "rx": 1.5,
                           "fill": "#3f4a7a"})]
    prims += st(["thigh_f", "shin_f", "foot_f"], 6, FAR)
    prims += st(["neck"], 5, TORSO)
    prims += st(["lumbar", "thorax", "chest"], 12, TORSO)
    prims += [Prim("circle", {"cx": hx, "cy": hy, "r": 7, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1.5})]
    prims += st(["thigh_n", "shin_n", "foot_n"], 7, NEAR)
    prims += [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 8, "stroke-linecap": "round"}, arm),
              Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 6, "stroke-linecap": "round"}, arm),
              Prim("rect", {"width": 10, "height": 5, "rx": 2, "fill": PROP, "stroke": "#1e293b", "stroke-width": 1.2},
                   lambda c: {"x": sx - 5, "y": sy - arm_len(c) - 2.5}),
              static_text("Seitansicht", IN_X + 8, IN_Y + 14, 12, MUTED, anchor="start")]
    return prims


def build():
    tl = Timeline([(0, UP), (0.5, UP), (2.1, OPEN), (2.6, OPEN), (3.9, UP), (4.6, UP)], skeleton=ARMS)
    Pu, Po = ARMS.fk(UP), ARMS.fk(OPEN)
    lo, ro = pt(Po, "hand_L"), pt(Po, "hand_R")
    lu, ru = pt(Pu, "hand_L"), pt(Pu, "hand_R")
    arms_p = []
    for s in ("L", "R"):
        arms_p += limb([f"upperarm_{s}", f"forearm_{s}", f"hand_{s}"], 13, NEAR)
        arms_p += dumbbell(f"hand_{s}", f"forearm_{s}", fore=0.5, size=1.1, ang_fn=lambda c: 90.0)
    prims = [
        *body(),
        Prim("ellipse", {"cx": CX - 17, "cy": SH_Y + 8, "rx": 15, "ry": 9, "fill": ACCENT, "opacity": 0.35,
                         "_pulse": True}),
        Prim("ellipse", {"cx": CX + 17, "cy": SH_Y + 8, "rx": 15, "ry": 9, "fill": ACCENT, "opacity": 0.35,
                         "_pulse": True}),
        ghost(limb(["upperarm_L", "forearm_L", "hand_L"], 13, NEAR) + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR),
              ARMS, OPEN, 0.14),
        *arms_p,
        arrow(f"M{lo[0] + 2:.0f} {lo[1] - 22:.0f} Q{lo[0] + 16:.0f} {lu[1] - 4:.0f} {lu[0] - 22:.0f} {lu[1] - 14:.0f}",
              show=[(2.6, 3.9)]),
        arrow(f"M{ro[0] - 2:.0f} {ro[1] - 22:.0f} Q{ro[0] - 16:.0f} {ru[1] - 4:.0f} {ru[0] + 22:.0f} {ru[1] - 14:.0f}",
              show=[(2.6, 3.9)]),
        label("Ellbogen berührt die Matte", CX, 112, 2.1, 2.6, 12, GOOD),
        *side_inset(),
        caption_band(),
        caption("Rückenlage, Hanteln über der Brust", 0, 0.5),
        caption("Einatmen – Arme seitlich öffnen", 0.5, 2.1),
        caption("Ellbogen tippt kurz auf", 2.1, 2.6),
        caption("Ausatmen – im Bogen zusammenführen", 2.6, 3.9),
        caption("Oben Brust anspannen", 3.9, 4.6),
        static_text("Ellbogen leicht gebeugt – wie eine Umarmung", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, ARMS, title="Butterfly am Boden")
