from rig import *
from exercises.open_book import Cam, Rig3, add, floor_rect

SLUG = "thread-the-needle"

# Perspektive: schräg von vorn-links und leicht von oben (gleicher 3D-Mini-Rig
# wie open_book). Die Drehachse (Wirbelsäule) zeigt grob zum Betrachter: das
# Durchfädeln unter dem Körper und das Aufdrehen zur Decke liegen beide in der
# Bildebene, gleichzeitig sieht man, dass Hüfte und Knie stehen bleiben.
# x = linke Körperseite, y = oben, z = Richtung Kopf. Rechter Arm fädelt.

CAM = Cam(yaw=-62, pitch=20, scale=1.1, cx=156, cy=230)
UP, LO, HAND = 36, 32, 13


def ik3(s, t, l1, l2, pole):
    """2-Knochen-IK im Raum: Ellbogen in Richtung `pole`."""
    d = [t[i] - s[i] for i in range(3)]
    dist = max(1e-6, min(math.sqrt(sum(v * v for v in d)), l1 + l2 - 1e-3))
    u = [v / max(1e-6, math.sqrt(sum(w * w for w in d))) for v in d]
    a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    pd = sum(pole[i] * u[i] for i in range(3))
    pv = [pole[i] - pd * u[i] for i in range(3)]
    pn = math.sqrt(sum(v * v for v in pv)) or 1.0
    return tuple(s[i] + u[i] * a + pv[i] / pn * h for i in range(3))


def rotz(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a), v[2])


def joints(p):
    th = p.get("th", 0.0)           # + = rechte Schulter sinkt, - = öffnet zur Decke
    sink = p.get("sink", 0.0)       # Oberkörper sinkt (linker Ellbogen beugt)
    J = {}
    # Hüfte über den Knien, Unterschenkel liegen
    for side, x in (("L", 13), ("R", -13)):
        J["hip" + side] = (x, 60, -82)
        J["knee" + side] = (x, 8, -80)
        J["foot" + side] = (x, 7, -128)
    J["pelvis"] = (0, 62, -82)
    sc = (-0.12 * th, 72 - sink, 0)
    J["sc"] = sc
    J["waist"] = (0, 66 - sink * 0.35, -42)
    v = rotz((19, 0, 0), th)        # Vektor zur linken Schulter
    J["shL"], J["shR"] = add(sc, v), add(sc, v, -1)
    J["chest_c"] = add(sc, (0, 0, -20))
    # linke Hand bleibt am Boden
    J["haL0"] = (21, 6, 2)
    J["haL1"] = (22, 6, 14)
    J["wrL"] = J["haL0"]
    J["elL"] = ik3(J["shL"], J["wrL"], UP, LO, (0.55, 0, -0.85))
    # rechter Arm: gestreckt, Winkel psi in der Querebene
    s = J["shR"]
    psi = p.get("psi", -90.0)
    zt = p.get("zt", 0.0)
    if s[1] + (UP + LO) * math.sin(math.radians(psi)) < 6 and math.cos(math.radians(psi)) > 0.02:
        psi = -math.degrees(math.asin(min(1.0, (s[1] - 6) / (UP + LO))))
    r = math.radians(psi)
    d = (math.cos(r), math.sin(r), zt)
    J["elR"] = add(s, d, UP)
    J["umR"] = add(s, d, UP * 0.55)
    J["wrR"] = add(s, d, UP + LO)
    onfloor = max(0.0, min(1.0, (12 - J["wrR"][1]) / 6))   # Hand flach am Boden (nach vorn)
    hand_dir = tuple(d[i] * (1 - onfloor) + (0, 0, 1)[i] * onfloor * (1 - p.get("thr", 0.0))
                     + d[i] * onfloor * p.get("thr", 0.0) for i in range(3))
    n = math.sqrt(sum(x * x for x in hand_dir)) or 1
    J["haR"] = add(J["wrR"], tuple(x / n for x in hand_dir), HAND)
    # Kopf: Hals nach vorn, dreht mit der BWS, Blick folgt
    nb = add(sc, (0, 1, 12))
    J["neck"] = nb
    hd = rotz((0, -0.42, 0.9), th * 0.5)
    J["head"] = add(nb, hd, 24)
    g = p.get("gaze", 0.0)
    J["gaze"] = rotz((0, -1, 0.35), -g)
    return J


START = dict(th=0, sink=0, psi=-90, zt=0, gaze=0, thr=0)
THREAD = dict(th=40, sink=34, psi=-30, zt=-0.1, gaze=-55, thr=1)
OPEN = dict(th=-55, sink=-12, psi=-240, zt=0, gaze=150, thr=0)


def build():
    rig = Rig3(joints, CAM)
    tl = Timeline([(0, START), (0.8, START), (2.8, THREAD), (4.4, THREAD), (5.8, START), (6.2, START),
                   (8.2, OPEN), (9.8, OPEN), (11.4, START), (12.0, START)])
    def hand_path(t0, t1, n=16):
        pts = [CAM(joints(tl.at(t0 + (t1 - t0) * i / n))["haR"]) for i in range(n + 1)]
        return smooth_path(pts[1:-1])

    prims = [
        *floor_rect(CAM, -62, 42, -150, 60),
        *rig.limb(["hipR", "kneeR", "footR"], 15, FAR),
        *rig.limb(["shR", "elR", "wrR", "haR"], 11, FAR),
        *rig.slab(["hipL", "shL", "shR", "hipR"], TORSO, 18),
        *rig.limb(["hipL", "hipR"], 22, TORSO, outline=False),
        *rig.limb(["pelvis", "waist", "chest_c"], 24, TORSO, outline=False),
        *rig.limb(["shL", "shR"], 22, "#8f98fb"),
        Prim("g", {"_show": [(1.6, 5.0)]}, children=rig.limb(["umR", "elR", "wrR", "haR"], 11, FAR)),
        *rig.limb(["sc", "neck", "head"], 12, TORSO),
        *rig.head("head", "gaze"),
        *rig.limb(["hipL", "kneeL", "footL"], 16, NEAR),
        *rig.limb(["shL", "elL", "wrL", "haL1"], 12, NEAR),
        arrow(hand_path(0.8, 2.8), width=2.2, show=[(0.8, 2.8)]),
        arrow(hand_path(6.2, 8.2), width=2.2, show=[(6.2, 8.2)]),
        caption_band(),
        caption("Vierfüßlerstand, Gewicht gleichmäßig", 0, 0.8),
        caption("Rechten Arm unter dem Körper durchfädeln", 0.8, 2.8),
        caption("Schulter und Schläfe sinken – Schulter trägt", 2.8, 4.4),
        caption("Arm zurückholen", 4.4, 6.2),
        caption("Im Bogen zur Decke – Blick folgt", 6.2, 8.2),
        caption("Brust öffnet sich – kurz halten", 8.2, 9.8),
        caption("Zurück in den Vierfüßlerstand", 9.8, 12.0),
        static_text("Hüfte bleibt über den Knien", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Thread the Needle")
