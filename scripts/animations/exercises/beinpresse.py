from rig import *
from exercises._gymgeraete_props import *

SLUG = "beinpresse"

# Seitansicht, Blick nach rechts. Sitz + Lehne fix, die Fußplatte läuft auf
# einem Schlitten nach rechts; das Kabel läuft über Rollen zum Gewichtsblock.
# Gesäß bleibt auf dem Sitz, Rücken an der Lehne, Hände an den Seitengriffen.

FLOOR_Y = 248
HIP = (132.0, 182.0)
LEAN = 28.0                      # Lehne: Grad aus der Senkrechten nach hinten
ANK_Y = 170.0                    # Fußgelenk-Höhe (Platte etwa auf Hüfthöhe)
THIGH, SHIN = 50.0, 48.0


def _ank_x(knee_deg):
    d = math.sqrt(THIGH ** 2 + SHIN ** 2 - 2 * THIGH * SHIN * math.cos(math.radians(knee_deg)))
    return HIP[0] + math.sqrt(d * d - (ANK_Y - HIP[1]) ** 2)


AX0 = _ank_x(90)                 # Start: rechter Winkel im Knie
AX1 = _ank_x(158)                # Ende: fast gestreckt, Knie bleibt weich
TRAVEL = AX1 - AX0
GRIP = (124.0, 170.0)
PLATE_OFF = 10.0                 # Fußsohle -> Plattenoberfläche


def ankle(p):
    return (AX0 + TRAVEL * p.get("push", 0.0), ANK_Y)


def plate_x(c):
    return ankle(c["pose"])[0] + PLATE_OFF


BASE = dict(x=HIP[0], y=HIP[1], rot=LEAN, neck=-24, head=-8, push=0.0)
OUT = dict(BASE, push=1.0, neck=-26)


def machine_back() -> list[Prim]:
    """Rahmen, Sitz, Lehne, Schienen – hinter der Figur."""
    up = (math.cos(math.radians(90 + LEAN)), -math.sin(math.radians(90 + LEAN)))
    back = (math.cos(math.radians(180 + LEAN)), -math.sin(math.radians(180 + LEAN)))
    b0 = (HIP[0] + back[0] * 19 + up[0] * 6, HIP[1] + back[1] * 19 + up[1] * 6)
    b1 = (b0[0] + up[0] * 84, b0[1] + up[1] * 84)
    prims = [
        # Bodenrahmen
        rect(48, FLOOR_Y - 8, 290, 9, PROP_DARK, 4),
        # Sitzstütze + Lehnenstütze
        line(140, 206, 140, FLOOR_Y - 6, PROP_DARK, 9),
        line(b0[0] + 10, b0[1] + 18, 82, FLOOR_Y - 6, PROP_DARK, 8),
        line(b0[0] + up[0] * 40 + 8, b0[1] + up[1] * 40 + 4, 82, FLOOR_Y - 6, PROP_DARK, 6),
        # Schiene für den Schlitten
        line(196, 214, 300, 214, PROP_DARK, 6),
        line(298, 214, 298, FLOOR_Y - 6, PROP_DARK, 7),
        line(200, 214, 200, FLOOR_Y - 6, PROP_DARK, 6),
        # Lehne (gepolstert)
        line(b0[0], b0[1], b1[0], b1[1], PROP_DARK, 17),
        line(b0[0], b0[1], b1[0], b1[1], PROP, 13),
        # Kopfstütze-Andeutung endet unter dem Kopf
        # Sitzpolster
        rect(96, 194, 82, 13, PROP_DARK, 6),
        rect(98, 195, 78, 9, PROP, 5),
    ]
    return prims


def sled() -> list[Prim]:
    """Fußplatte auf Schlitten, folgt den Füßen."""
    def plate(c):
        x = plate_x(c)
        return ((x + 3, ANK_Y - 42), (x + 3, ANK_Y + 20))

    def carriage(c):
        x = plate_x(c)
        return ((x - 8, 211), (x + 22, 211))

    def strut(c):
        x = plate_x(c)
        return ((x + 6, ANK_Y + 14), (x + 14, 209))

    return [
        dline(carriage, "#56657c", 9),
        dline(strut, PROP_DARK, 6),
        dline(plate, PROP_DARK, 11),
        dline(plate, PROP, 7),
    ]


def grip() -> list[Prim]:
    return [line(GRIP[0], GRIP[1] + 4, 128, 196, PROP_DARK, 5),
            line(GRIP[0] - 6, GRIP[1], GRIP[0] + 6, GRIP[1], "#1f2937", 7)]


def build():
    iks = [
        IK("thigh_n", "shin_n", ankle, bend=1, end_seg="foot_n", end_abs=84),
        IK("thigh_f", "shin_f", lambda p: (ankle(p)[0] - 3, ankle(p)[1] + 2), bend=1, end_seg="foot_f",
           end_abs=84),
        IK("upperarm_n", "forearm_n", GRIP, bend=1),
        IK("upperarm_f", "forearm_f", (GRIP[0] - 4, GRIP[1] + 1), bend=1),
    ]
    T = [0, 0.8, 2.4, 3.0, 5.4, 6.0]
    tl = Timeline([(T[0], BASE), (T[1], BASE), (T[2], OUT), (T[3], OUT), (T[4], BASE), (T[5], BASE)],
                  iks=iks, skeleton=SIDE)

    # Kabel: Schlitten -> Rolle unter den Knien -> Boden -> hinter dem Turm hoch -> Platten
    STACK_X = 334
    lift = lambda c: TRAVEL * c["pose"].get("push", 0.0)
    stack, pulley = weight_stack(STACK_X, 58, FLOOR_Y, lift, n=10, sel=4, w=30)
    cable = dpath(lambda c: [(plate_x(c) - 8, 216), (190, 216), (190, 238), (356, 238), (356, 62),
                             (pulley[0], pulley[1] - 5)], "#cbd5e1", 1.4, opacity=0.8)
    pulleys = [circle(190, 220, 4.5, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.2}),
               circle(190, 234, 4.5, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 1.2})]

    # Kniewinkel-Hinweise an fixen Stellen (aus der Pose berechnet)
    P0 = SIDE.fk(tl.at(0.0))
    kx, ky = pt(P0, "thigh_n")
    P1 = SIDE.fk(tl.at(T[2]))
    kx1, ky1 = pt(P1, "thigh_n")
    a_th = P0["thigh_n"][4]
    a_sh = P0["shin_n"][4]

    def arc(cx, cy, r, a0, a1):
        p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
        return f"M{p0[0]:.1f} {p0[1]:.1f}A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}"

    # Winkel zwischen Oberschenkel (zurück zur Hüfte) und Schienbein
    angle90 = Prim("g", {"_show": [(0, T[1] + 0.3), (T[4] - 0.2, T[5])]}, children=[
        Prim("path", {"d": arc(kx, ky, 15, a_th + 180, a_sh), "fill": "none", "stroke": GOOD,
                      "stroke-width": 2.5, "stroke-linecap": "round"}),
        static_text("90°", kx + 4, ky - 20, 12, GOOD, weight="700"),
    ])
    soft = Prim("g", {"_show": [(T[2] - 0.2, T[3] + 0.2)]}, children=[
        static_text("Knie bleibt weich", kx1 + 6, ky1 - 30, 12, WARN, weight="700"),
    ])

    figure = side_fig(extras_behind=machine_back() + [cable] + pulleys + stack + sled(),
                         extras_front=grip())
    scene = group([
        *figure,
        focus_mid("thigh_n", 0.5, 17, 9, perp=-2, show=[(T[1], T[4])]),
        arrow("M246 104 L276 104", show=[(T[1], T[2])]),
        arrow("M276 104 L246 104", show=[(T[3], T[4])]),
        angle90, soft,
    ], scale=1.12, origin=(190, 150), dy=-6)
    prims = [
        scene,
        caption_band(),
        caption("Rücken an die Lehne, Knie 90°", 0, T[1]),
        caption("Ausatmen – Platte wegdrücken", T[1], T[2]),
        caption("Nicht ganz durchstrecken", T[2], T[3]),
        caption("Langsam zurück bis 90°", T[3], T[5]),
        static_text("Mind. 90° im Knie – oben nicht durchstrecken", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Beinpresse horizontal")
