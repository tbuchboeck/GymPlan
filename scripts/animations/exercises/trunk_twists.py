from rig import *
from exercises._morgen_props import (FnTimeline, Front3D, nose_badge, nose_note, top_inset, TAU)

SLUG = "trunk-twists"

# Frontansicht. Oberkörper dreht locker links/rechts (Schulterlinie verkürzt
# sich, Brustbein-Linie wandert), Becken/Beine bleiben ruhig, die Arme
# schwingen mit etwas Verzögerung locker um den Körper. Draufsicht-Inset
# zeigt Schulter- gegen Hüftlinie.

FLOOR_Y = 250
CX = 186
SC = 0.8
DUR = 3.2
ANK_Y = FLOOR_Y - 8
PEL_Y = ANK_Y - 94          # Knie weich
YAW = 52                    # max. Schulterdrehung


# (ab1, fl1, ab2, fl2): Arm schwingt aus / wickelt vorn um den Bauch / hinten um den Rücken
ARM_MID = (44, 10, 50, 16)
ARM_FRONT = (30, 92, 72, 165)
ARM_BACK = (32, -70, 66, -150)


def pose_at(t):
    ph = TAU * t / DUR
    s_t = math.sin(ph)                 # Rumpf
    s_a = math.sin(ph - 0.55)          # Arme hängen etwas nach
    sy = YAW * s_t
    pose = dict(x=CX, y=PEL_Y + 1.2 * abs(math.cos(ph)), hy=4 * s_t, sy=sy,
                ankL_x=CX - 17, ankR_x=CX + 17, ank_y=ANK_Y, toe_out=10,
                turn=0.75 * math.sin(math.radians(sy)) / math.sin(math.radians(YAW)) * 0.8)
    for key, sgn in (("L", 1), ("R", -1)):
        s = sgn * s_a
        tgt = ARM_FRONT if s > 0 else ARM_BACK
        w = abs(s) ** 1.3
        for i, k in enumerate(("ab%s1", "fl%s1", "ab%s2", "fl%s2")):
            pose[k % key] = ARM_MID[i] + (tgt[i] - ARM_MID[i]) * w
    pose["breath"] = math.sin(ph)
    return pose


FIG = Front3D()


def build():
    tl = FnTimeline(pose_at, DUR, skeleton=FRONT)
    h = DUR / 2
    fig = group([
        Prim("ellipse", {"cx": CX, "cy": FLOOR_Y, "rx": 46, "ry": 5, "fill": "#000", "opacity": 0.25}),
        *FIG.prims(),
        focus("thorax", rx=18, ry=11, offset=(0, -6), show=[(0, DUR)]),
    ], scale=SC, origin=(CX, FLOOR_Y))
    # Pfeile über den Schultern (Bildschirmkoordinaten nach Skalierung)
    ay = FLOOR_Y - (FLOOR_Y - (PEL_Y - 92)) * SC
    prims = [
        floor(FLOOR_Y, 40, 300),
        fig,
        arrow(f"M{CX - 30} {ay:.0f} Q{CX} {ay - 12:.0f} {CX + 30} {ay:.0f}", show=[(0.15, h * 0.55)]),
        arrow(f"M{CX + 30} {ay:.0f} Q{CX} {ay - 12:.0f} {CX - 30} {ay:.0f}", show=[(h + 0.15, h + h * 0.55)]),
        *top_inset(345, 140, 27, lambda p: (p.get("hy", 0.0), p.get("sy", 0.0))),
        Prim("line", {"x1": 312, "y1": 186, "x2": 324, "y2": 186, "stroke": TORSO, "stroke-width": 5,
                      "stroke-linecap": "round"}),
        static_text("Schultern", 329, 190, 10, MUTED, anchor="start"),
        Prim("line", {"x1": 312, "y1": 201, "x2": 324, "y2": 201, "stroke": NEAR, "stroke-width": 5,
                      "stroke-linecap": "round"}),
        static_text("Becken ruhig", 329, 205, 10, GOOD, anchor="start"),
        *nose_badge([(0, h, "in"), (h, DUR, "out")]),
        nose_note(),
        caption_band(),
        caption("Nach links drehen – Arme schwingen mit", 0, h),
        caption("Nach rechts – locker, aus der BWS", h, DUR),
        static_text("Drehung aus dem mittleren Rücken – Becken bleibt ruhig", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Trunk Twists", fps=15)
