from rig import *
from exercises._gymgeraete_props import *

SLUG = "abdominal-crunch-machine"

# Seitansicht, Blick nach rechts. Gesäß fix auf dem Sitz, Unterschenkel hinter
# Rolle B (vorn unten). Rolle A liegt vorn auf den Schultern und hängt an einem
# Hebelarm, der sich um eine Achse neben dem Becken dreht; Hände halten die
# Griffe an Rolle A. Beim Einrollen beugt sich die Wirbelsäule Segment für
# Segment – das Becken bleibt auf dem Sitz.

FLOOR_Y = 248
HIP = (176.0, 186.0)
BASE = dict(x=HIP[0], y=HIP[1], rot=-2, thigh_n=90, shin_n=-92, thigh_f=88, shin_f=-90,
            neck=-4, head=0, crunch=0.0)
CRUNCH = dict(BASE, rot=-6, lumbar=-12, thorax=-20, chest=-22, neck=-16, head=-8, crunch=1.0)
ROLL_B = (236.0, 222.0)


def roll_a(P):
    """Schulterrolle: vorn-oben auf der Brust, folgt dem Brustkorb."""
    x, y = pt(P, "chest")
    a = math.radians(P["chest"][4])
    up = (math.cos(a), -math.sin(a))
    fwd = (math.cos(a - math.pi / 2), -math.sin(a - math.pi / 2))
    return x + fwd[0] * 16 - up[0] * 7, y + fwd[1] * 16 - up[1] * 7


def _pivot():
    a0 = roll_a(SIDE.fk(BASE))
    a1 = roll_a(SIDE.fk(dict(CRUNCH)))
    # Punkt auf der Mittelsenkrechten von a0-a1 auf Höhe des unteren Rückens
    mx, my = (a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2
    dx, dy = a1[0] - a0[0], a1[1] - a0[1]
    ny = HIP[1] - 24
    # (x - mx) * dx + (y - my) * dy = 0
    nx = mx - (ny - my) * dy / dx
    return nx, ny


PIVOT = _pivot()


_A0 = roll_a(SIDE.fk(BASE))
LEVER = math.hypot(_A0[0] - PIVOT[0], _A0[1] - PIVOT[1])


def roll_on_lever(P):
    """Rolle A bleibt exakt auf dem Kreis um die Hebelachse (Hebel hat feste
    Länge); sie gleitet dafür minimal auf der Brust."""
    ax, ay = roll_a(P)
    ang = math.atan2(ay - PIVOT[1], ax - PIVOT[0])
    return PIVOT[0] + LEVER * math.cos(ang), PIVOT[1] + LEVER * math.sin(ang), ang


def roll_pt(c):
    x, y, _ = roll_on_lever(c["P"])
    return x, y


def lever_end(c, ext=22):
    x, y, ang = roll_on_lever(c["P"])
    return x + ext * math.cos(ang), y + ext * math.sin(ang)


def grip_xy(P):
    """Griff an Rolle A (etwas über der Rolle) – dort liegen die Hände."""
    x, y, ang = roll_on_lever(P)
    return x + 6 * math.cos(ang + 1.9), y + 6 * math.sin(ang + 1.9)


def grip_pt(p):
    return grip_xy(SIDE.fk(p))


COL_X = 116


def machine_back(stack) -> list[Prim]:
    return stack + [
        rect(40, FLOOR_Y - 8, 250, 9, PROP_DARK, 4),
        # Säule hinter der Lehne, Ausleger zur Hebelachse (hinter dem Körper)
        line(COL_X, 64, COL_X, FLOOR_Y - 6, PROP_DARK, 10),
        line(COL_X, PIVOT[1], PIVOT[0], PIVOT[1], PROP_DARK, 8),
        circle(PIVOT[0], PIVOT[1], 11, PROP_DARK),
        # Sitzstütze
        line(176, 204, 176, FLOOR_Y - 6, PROP_DARK, 9),
        # Rolle-B-Stütze
        line(ROLL_B[0], ROLL_B[1], 258, FLOOR_Y - 6, PROP_DARK, 7),
        # Lendenpolster
        line(140, 140, 142, 192, PROP_DARK, 14), line(140, 140, 142, 192, PROP, 10),
        # Sitz
        rect(140, 192, 78, 13, PROP_DARK, 6), rect(142, 193, 74, 9, PROP, 5),
        # ferner Hebelarm (hinter dem Körper)
        dline(lambda c: (PIVOT, lever_end(c)), "#3a4659", 7),
    ]


def build():
    iks = [
        IK("upperarm_n", "forearm_n", grip_pt, bend=-1),
        IK("upperarm_f", "forearm_f", lambda p: (grip_pt(p)[0] - 4, grip_pt(p)[1] + 1), bend=-1),
    ]
    T = [0, 0.8, 2.2, 2.8, 4.8, 5.4]
    tl = Timeline([(T[0], BASE), (T[1], BASE), (T[2], CRUNCH), (T[3], CRUNCH), (T[4], BASE),
                         (T[5], BASE)], iks=iks, skeleton=SIDE)

    lift = lambda c: 26 * c["pose"].get("crunch", 0.0)
    stack, pulley = weight_stack(70, 60, FLOOR_Y, lift, n=10, sel=4, w=30)
    cam = (PIVOT[0], PIVOT[1])
    cable = dpath(lambda c: [(pulley[0], pulley[1] - 5), (COL_X, pulley[1] - 5), (COL_X, PIVOT[1] - 10),
                             (cam[0], cam[1] - 10)], "#cbd5e1", 1.4, opacity=0.8)
    top_pulley = circle(COL_X, pulley[1], 5, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.5})

    roll_b = [circle(ROLL_B[0], ROLL_B[1], 9, PROP_DARK), circle(ROLL_B[0], ROLL_B[1], 7, PROP)]
    near_lever = [
        dline(lambda c: (PIVOT, lever_end(c, 8)), PROP_DARK, 9),
        dline(lambda c: (PIVOT, lever_end(c, 8)), PROP, 5),
        circle(PIVOT[0], PIVOT[1], 6, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.5}),
    ]
    roll_a_prims = [
        dcircle(roll_pt, 11, PROP_DARK),
        dcircle(roll_pt, 9, PROP),
        dcircle(roll_pt, 3, PROP_DARK),
    ]

    def label(txt, fn):
        def f(c):
            x, y = fn(c)
            return {"x": x, "y": y}
        return Prim("text", {"font-size": 11, "fill": ACCENT, "font-weight": "700", "text-anchor": "middle"},
                    f, text=txt)

    torso_ghost = ghost(limb(["lumbar", "thorax"], 30, TORSO) + limb(["neck"], 13, TORSO) + head_side(),
                        SIDE, BASE, 0.14)
    figure = side_fig(extras_behind=machine_back([cable, top_pulley] + stack),
                      extras_mid=near_lever,
                      extras_front=roll_b + roll_a_prims)
    prims = [
        torso_ghost,
        *figure,
        label("A", lambda c: (roll_pt(c)[0] + 19, roll_pt(c)[1] - 6)),
        label("B", lambda c: (ROLL_B[0] + 16, ROLL_B[1] + 4)),
        focus_mid("lumbar", 0.9, 9, 17, perp=12, rotate=True, show=[(T[1], T[4])]),
        arrow("M248 96 Q262 116 254 140", show=[(T[1], T[2])]),
        arrow("M254 140 Q262 116 248 96", show=[(T[3], T[4])]),
        caption_band(),
        caption("Rolle A an die Schultern, Beine hinter B", 0, T[1], size=14),
        caption("Ausatmen – Bauch einrollen", T[1], T[2]),
        caption("Kurz halten – Bauch fest", T[2], T[3]),
        caption("Langsam zurück, Spannung halten", T[3], T[5]),
        static_text("Aus dem Bauch rollen – nicht mit den Armen ziehen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Bauchpresse")
