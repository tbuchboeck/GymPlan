from rig import *

SLUG = "tuerrahmen-dehnung"

# Seitansicht (Blick nach rechts). Die Person steht in der Türöffnung, die Wand
# mit dem Rahmen erscheint im Profil als senkrechtes Band. Der nahe Unterarm
# liegt senkrecht am Rahmen, der Ellbogen bleibt auf Schulterhöhe fix. Mit dem
# Körper vorlehnen -> die Schulter wandert vor den Ellbogen, der Oberarm zeigt
# nach hinten = Brustdehnung (grün). Der Unterarm bleibt hinter dem Kopf.
# Kleines Inset links oben: 90/90-Armhaltung von vorn.

FLOOR_Y = 250
POST_X = 150                       # Vorderkante des Rahmens
BACK_FOOT = (POST_X - 18, FLOOR_Y - 6)
FRONT_FOOT = (POST_X + 84, FLOOR_Y - 6)

BASE = dict(x=POST_X + 28, y=FLOOR_Y - 96, neck=-4, head=2,
            upperarm_f=8, forearm_f=18)
LEAN = dict(BASE, x=POST_X + 54, y=FLOOR_Y - 91, rot=-9, lumbar=3, chest=2, neck=4, head=4)
LEAN_IN = dict(LEAN, x=POST_X + 57, y=FLOOR_Y - 90)

SH_Y = None                        # wird in build() aus der Startpose bestimmt


def elbow_point():
    P = SIDE.fk(BASE)
    sx, sy = pt(P, "chest")
    return (POST_X - 8, sy + 2)


ELBOW = elbow_point()
FORE = 32
HAND = 13


def near_arm_pts(c):
    s = pt(c["P"], "chest")
    ex, ey = ELBOW
    return [s, (ex, ey), (ex + 1, ey - FORE), (ex + 2, ey - FORE - HAND)]


def near_arm():
    f = lambda c: {"d": smooth_path(near_arm_pts(c)[:2]) + smooth_path(near_arm_pts(c)[1:]).replace("M", "L", 1)}
    return [Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": 15, "stroke-linecap": "round",
                          "stroke-linejoin": "round"}, f),
            Prim("path", {"fill": "none", "stroke": NEAR, "stroke-width": 12, "stroke-linecap": "round",
                          "stroke-linejoin": "round"}, f)]


def figure():
    """Wie side_figure, aber der nahe Arm ist eigens gezeichnet (am Rahmen)."""
    prims = []
    prims += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], 30, TORSO)
    prims += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims += near_arm()          # Unterarm liegt hinter dem Kopf
    prims += head_side()
    return prims


IN_X, IN_Y, IN_W, IN_H = 12, 34, 96, 96


def arm_inset():
    """90/90-Armhaltung von vorn (statisch), mit Rahmen und Schulterlinie."""
    pose = dict(x=0, y=0, upperarm_R=90, forearm_R=90, upperarm_L=4, forearm_L=-4)
    parts = (limb(["neck"], 13, TORSO) + limb(["lumbar", "thorax", "chest"], 44, TORSO)
             + [Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22, "stroke-linecap": "round"},
                     lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"), pt(c["P"], "clav_R")])})]
             + limb(["upperarm_L", "forearm_L", "hand_L"], 13, FAR)
             + limb(["upperarm_R", "forearm_R", "hand_R"], 13, NEAR) + head_front())
    P = FRONT.fk(pose)
    ex, ey = pt(P, "upperarm_R")
    frozen = ghost(parts, FRONT, pose, opacity=1.0)
    post = Prim("rect", {"x": ex + 7, "y": ey - 60, "width": 12, "height": 140, "fill": "#94a3b8"})
    ang = Prim("path", {"d": f"M{ex - 14} {ey}L{ex - 14} {ey - 14}L{ex} {ey - 14}", "fill": "none",
                        "stroke": ACCENT, "stroke-width": 3})
    sh_y = pt(P, "clav_R")[1]
    level = Prim("line", {"x1": pt(P, "clav_L")[0] - 24, "y1": sh_y, "x2": ex + 30, "y2": sh_y, "stroke": GOOD,
                          "stroke-width": 2.5, "stroke-dasharray": "5 5"})
    cx, cy = pt(P, "chest")
    g = group([post, frozen, level, ang], scale=0.62, origin=(cx, cy),
              dx=IN_X + 38 - cx, dy=IN_Y + 66 - cy)
    clip = Prim("g", {"clip-path": "url(#clipArm)"}, children=[
        Prim("rect", {"x": IN_X, "y": IN_Y, "width": IN_W, "height": IN_H, "fill": "#0b1220", "opacity": 0.8}), g])
    return [clip, static_text("von vorn", IN_X + IN_W / 2, IN_Y + IN_H + 14, 12, MUTED)]


def build():
    iks = [
        IK("thigh_n", "shin_n", FRONT_FOOT, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", BACK_FOOT, bend=1, end_seg="foot_f", end_abs=0),
    ]
    tl = Timeline([(0, BASE), (1.4, BASE), (3.4, LEAN), (5.2, LEAN_IN), (7.0, LEAN),
                   (7.6, LEAN), (9.2, BASE), (9.6, BASE)], iks=iks, skeleton=SIDE)
    wall = [
        Prim("rect", {"x": POST_X - 30, "y": 40, "width": 24, "height": FLOOR_Y - 40, "fill": "#3b4a63"}),
        Prim("rect", {"x": POST_X - 8, "y": 40, "width": 6, "height": FLOOR_Y - 40, "fill": "#94a3b8"}),
    ]
    ex, ey = ELBOW
    level = Prim("line", {"x1": ex - 40, "y1": ey, "x2": ex + 120, "y2": ey, "stroke": GOOD,
                          "stroke-width": 1.5, "stroke-dasharray": "5 5", "opacity": 0.7})
    elbow_dot = Prim("circle", {"cx": ex, "cy": ey, "r": 4, "fill": ACCENT})
    chest_focus = focus("chest", rx=15, ry=11, offset=(14, 16), color=GOOD, end=False, show=[(2.4, 7.8)])
    SC, OX = 0.84, 210

    def tr(x, y):
        return OX + (x - OX) * SC, FLOOR_Y + (y - FLOOR_Y) * SC

    scene = group([
        *wall,
        level,
        ghost(limb(["lumbar", "thorax"], 30, TORSO) + head_side(), SIDE, BASE, 0.15),
        *figure(),
        chest_focus,
        elbow_dot,
    ], scale=SC, origin=(OX, FLOOR_Y))
    lx, ly = tr(ex + 124, ey)
    ax, ay = tr(POST_X + 90, 150)
    wx, wy = tr(POST_X - 34, 200)
    prims = [
        floor(FLOOR_Y, 20, 380),
        scene,
        arrow(f"M{ax:.0f} {ay:.0f} L{ax + 28:.0f} {ay:.0f}", show=[(1.4, 3.4)]),
        static_text("Türrahmen", wx, wy, 12, MUTED, anchor="end"),
        static_text("Ellbogen auf", lx, ly - 4, 12, GOOD, anchor="start"),
        static_text("Schulterhöhe", lx, ly + 10, 12, GOOD, anchor="start"),
        *arm_inset(),
        caption_band(),
        caption("Unterarm an den Rahmen, Ellbogen 90°", 0, 1.4),
        caption("Mit dem Körper langsam vorlehnen", 1.4, 3.4),
        caption("Brust zieht – 30 s ruhig atmen", 3.4, 7.6),
        caption("Langsam zurück", 7.6, 9.6),
        static_text("Kribbeln im Arm? Spannung sofort lösen", 200, 22, LEAD_SIZE, MUTED),
    ]
    clip = (f'<clipPath id="clipArm"><rect x="{IN_X}" y="{IN_Y}" width="{IN_W}" height="{IN_H}" rx="8"/>'
            '</clipPath>')
    return render(prims, tl, SIDE, title="Brustdehnung im Türrahmen", fps=12, extra_defs=clip)
