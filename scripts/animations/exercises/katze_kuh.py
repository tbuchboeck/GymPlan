from rig import *

SLUG = "katze-kuh"

FLOOR_Y = 246
HAND = (244, FLOOR_Y - 5)
KNEE = (160, FLOOR_Y - 8)

BASE = dict(x=160, y=186, rot=-80, neck=-8, head=-6)
CAT = dict(BASE, y=184, lumbar=24, thorax=-20, chest=-26, neck=-36, head=-14)  # Runden
COW = dict(BASE, y=188, lumbar=-16, thorax=18, chest=18, neck=22, head=8)      # Brustbein sinkt


def build():
    iks = [
        Anchor("chest", (237, 172)),
        IK("upperarm_n", "forearm_n", HAND, bend=-1, end_seg="hand_n", end_abs=0),
        IK("upperarm_f", "forearm_f", (HAND[0] - 4, HAND[1]), bend=-1, end_seg="hand_f", end_abs=0),
        IK("thigh_n", "shin_n", (KNEE[0] - 48, FLOOR_Y - 8), bend=1, end_seg="foot_n", end_abs=180),
        IK("thigh_f", "shin_f", (KNEE[0] - 52, FLOOR_Y - 8), bend=1, end_seg="foot_f", end_abs=180),
    ]
    tl = Timeline([(0, BASE), (0.8, BASE), (2.4, CAT), (3.4, CAT), (5.2, COW), (6.2, COW), (7.4, BASE)],
                  iks=iks, skeleton=SIDE)
    spine_guide = Prim("path", {"fill": "none", "stroke": ACCENT, "stroke-width": 2, "stroke-dasharray": "4 5",
                                "opacity": 0.8},
                       lambda c: {"d": smooth_path([(x, y - 19) for x, y in chain_points(c["P"], ["lumbar", "thorax", "chest"])])})
    prims = [
        mat(FLOOR_Y, 70, 330),
        ghost(limb(["lumbar", "thorax", "chest"], 30, TORSO), SIDE, BASE, 0.15),
        *side_figure(),
        spine_guide,
        focus("thorax", rx=24, ry=9, offset=(0, -10), show=[(0.8, 6.2)]),
        arrow("M200 112 Q214 98 228 112", show=[(0.8, 2.4)]),
        arrow("M214 120 L214 140", show=[(3.4, 5.2)]),
        caption_band(),
        caption("Vierfüßlerstand, Rücken neutral", 0, 0.8),
        caption("Runden: zwischen den Schulterblättern hoch", 0.8, 3.4),
        caption("Strecken: Brustbein sinkt nach vorn-unten", 3.4, 6.2),
        caption("Zurück zur Mitte – mit dem Atem", 6.2, 7.4),
        static_text("Bewegung im mittleren Rücken – LWS bleibt ruhig", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Katze-Kuh (BWS-Fokus)")
