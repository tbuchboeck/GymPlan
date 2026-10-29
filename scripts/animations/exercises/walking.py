from rig import *
from exercises._tb_gym_props import *

SLUG = "walking"

# Entspanntes Gehen, Seitansicht (Blick nach rechts). Echter Gangzyklus:
# Standbein rollt über Ferse -> ganzer Fuß -> Ballen ab und gleitet mit dem
# Boden nach hinten (Figur bleibt in der Bildmitte, der Boden zieht durch),
# Schwungbein pendelt mit gebeugtem Knie nach vorn. Becken hebt/senkt sich
# leicht, Arme schwingen gegengleich. Pose wird pro Frame analytisch aus der
# Gangphase berechnet.

FLOOR_Y = 246
ANK_Y = FLOOR_Y - 8.0          # Fußgelenkhöhe bei flachem Fuß
CX = 196.0                     # Becken (x fix)
CYCLE = 1.3                    # Sekunden pro Doppelschritt
N_CYC = 4
HALF = 27.0                    # halbe Schrittlänge (Fußgelenk relativ zum Becken)
STANCE = 0.6                   # Anteil Standphase
FOOT = 20.0
LEGLEN = 50 + 48 - 2.5         # Stand-Bein fast gestreckt
SCALE = 0.84
SPEED = 2 * HALF / (STANCE * CYCLE)   # px/s des Bodens


def _foot(phi):
    """Fußgelenk (dx relativ zum Becken, y) und Fußwinkel für Gangphase phi."""
    if phi < STANCE:
        s = phi / STANCE
        toe_x = HALF + FOOT - 2 * HALF * s     # Fuß gleitet gleichmäßig nach hinten
        if s < 0.12:                            # Fersenaufsatz: Zehen noch oben
            a = 14 * (1 - smooth(s / 0.12))
        elif s > 0.72:                          # Ferse hebt ab, Abrollen über Ballen
            a = -34 * smooth((s - 0.72) / 0.28)
        else:
            a = 0.0
        if a >= 0:   # um die Ferse drehen
            ax, ay = toe_x - FOOT, ANK_Y
        else:        # um die Zehen drehen
            ra = math.radians(a)
            ax, ay = toe_x - FOOT * math.cos(ra), ANK_Y + FOOT * math.sin(ra)
        return ax, ay, a
    s = (phi - STANCE) / (1 - STANCE)
    # Start = Ende der Standphase, Ziel = Fersenaufsatz vorn
    ra0 = math.radians(-34)
    x0 = HALF + FOOT - 2 * HALF - FOOT * math.cos(ra0)
    y0 = ANK_Y + FOOT * math.sin(ra0)
    x1, y1 = HALF, ANK_Y
    u = smooth(s)
    x = x0 + (x1 - x0) * u
    y = y0 + (y1 - y0) * u - 15 * math.sin(math.pi * min(1, s * 1.15)) ** 1.2
    a = -34 + 48 * smooth(min(1, s * 1.3))
    return x, y, a


class WalkTimeline(Timeline):
    def __init__(self):
        super().__init__([(0, {}), (CYCLE * N_CYC, {})], skeleton=SIDE)

    def at(self, t):
        ph = (t / CYCLE) % 1.0
        feet = {"n": _foot(ph), "f": _foot((ph + 0.5) % 1.0)}
        # Beckenhöhe: Standbein(e) fast gestreckt
        ys = []
        for k, (dx, ay, a) in feet.items():
            ys.append(ay - math.sqrt(max(1.0, LEGLEN ** 2 - dx ** 2)))
        y = max(ys)
        # x der Pose ist Becken, Füße relativ dazu
        pose = {"x": CX, "y": y, "rot": -3, "neck": 4, "head": -1}
        # Rumpf: leichte Gegenrotation (Brust kippt kaum), Atem
        for k in ("n", "f"):
            dx, ay, a = feet[k]
            pose = solve_ik(SIDE, pose, IK("thigh_" + k, "shin_" + k, (CX + dx, ay), bend=1,
                                            end_seg="foot_" + k, end_abs=a))
        # Arme gegengleich zum gleichseitigen Bein
        for k, other in (("n", "f"), ("f", "n")):
            leg = feet[k][0] / HALF                     # +1 = Bein vorn
            swing = -leg
            pose["upperarm_" + k] = 24 * swing + 2
            pose["forearm_" + k] = 18 + 10 * max(0.0, swing)
            pose["hand_" + k] = 4
        pose["t"] = t
        return pose


def build():
    tl = WalkTimeline()
    dur = tl.duration

    def ground(c):
        return {"stroke-dashoffset": c["t"] * SPEED * SCALE}   # gesamt 302.4 = 8 Muster à 37.8

    # Bodenmarkierungen ziehen mit der Geschwindigkeit des Standfußes nach hinten
    dashes = Prim("line", {"x1": 20, "y1": FLOOR_Y + 5, "x2": 380, "y2": FLOOR_Y + 5, "stroke": "#475569",
                           "stroke-width": 2.5, "stroke-dasharray": "12 25.8", "stroke-linecap": "round"}, ground)
    # Dashoffset positiv verschiebt das Muster nach links -> Boden läuft nach hinten
    shadow = Prim("ellipse", {"cx": CX + 4, "cy": FLOOR_Y + 1, "rx": 42, "ry": 4, "fill": "#0b1220",
                              "opacity": 0.5})

    def arms(far):
        k = "f" if far else "n"
        return limb([f"upperarm_{k}", f"forearm_{k}", f"hand_{k}"], 11 if far else 12, FAR if far else NEAR)

    prims_fig = []
    prims_fig += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    prims_fig += arms(True)
    prims_fig += limb(["neck"], 13, TORSO)
    prims_fig += limb(["lumbar", "thorax"], 30, TORSO)
    prims_fig += limb(["thorax", "chest"], 26, TORSO, outline=False)
    prims_fig += head_side()
    prims_fig += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    prims_fig += arms(False)

    relax = focus("lumbar", rx=8, ry=12, offset=(-10, 0), color=GOOD, end=False, show=[(3 * CYCLE, 4 * CYCLE)])
    T = CYCLE
    scene = group([shadow, *prims_fig, relax], scale=SCALE, origin=(CX, FLOOR_Y))
    prims = [
        floor(FLOOR_Y, 20, 380),
        dashes,
        scene,
        caption_band(),
        static_text("Locker gehen – Schultern entspannt, ruhig atmen", 200, 22, LEAD_SIZE, MUTED),
        caption("Ferse setzt auf, Fuß rollt ab", 0, T),
        caption("Arme schwingen locker gegengleich", T, 2 * T),
        caption("Aufrecht, Blick nach vorn", 2 * T, 3 * T),
        caption("Ruhig atmen – Rücken entspannt", 3 * T, 4 * T),
    ]
    return render(prims, tl, SIDE, fps=15, title="Entspanntes Gehen")
