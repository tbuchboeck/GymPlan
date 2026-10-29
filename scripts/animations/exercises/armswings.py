from rig import *
from exercises._morgen_props import (FnTimeline, Front3D, nose_badge, nose_note, top_inset, TAU)

SLUG = "armswings"

# Frontansicht. Arme schwingen knapp unter Schulterhöhe vor dem Körper
# überkreuz (abwechselnd liegt der linke/rechte Arm oben) und öffnen weit
# nach hinten – die Hände verschwinden dabei hinter der Körperebene
# (Arme werden in der Projektion kürzer, dunkler). Knie federn locker mit.
# Draufsicht-Inset zeigt, wie weit die Arme nach hinten gehen.

FLOOR_Y = 250
CX = 180
SC = 0.8
SWING = 1.6                 # ein Kreuzen + Öffnen
DUR = 2 * SWING
ANK_Y = FLOOR_Y - 15
PEL_Y = ANK_Y - 95


def pose_at(t):
    ph = TAU * t / SWING
    c = math.cos(ph)                    # +1 offen (t=0), -1 gekreuzt
    fl = 42 - 82 * c                    # -40 hinten ... 124 gekreuzt
    ab = 74 - 6 * (1 - c) / 2           # beim Kreuzen etwas tiefer
    pose = dict(x=CX, y=PEL_Y + 2.5 * (1 - abs(c)), ank_y=ANK_Y, ankL_x=CX - 18, ankR_x=CX + 18,
                toe_out=10, toe_len=16, shrug=-1.5 * (1 - c) / 2)
    for key in ("L", "R"):
        pose["ab%s1" % key] = ab
        pose["fl%s1" % key] = fl
        pose["ab%s2" % key] = ab + 4
        pose["fl%s2" % key] = fl + 10 * (-c)        # Ellbogen weich, Unterarm schwingt nach
    pose["topL"] = 1.0 if t < SWING else 0.0      # wer oben kreuzt, wechselt
    return pose


FIG = Front3D()


def hands_top(pose):
    g = FIG.geo(pose)
    cx = g["chest"][0]
    return [(g["armL"][-1][0] - cx, g["armL"][-1][2]), (g["armR"][-1][0] - cx, g["armR"][-1][2])]


def build():
    tl = FnTimeline(pose_at, DUR, skeleton=FRONT)
    q = SWING / 2
    fig = group([
        Prim("ellipse", {"cx": CX, "cy": FLOOR_Y, "rx": 46, "ry": 5, "fill": "#000", "opacity": 0.25}),
        *FIG.prims(cross_rank=True),
        focus("chest", rx=22, ry=9, offset=(0, 14), color=GOOD, show=[(q * 0.6, q * 1.4), (SWING + q * 0.6, SWING + q * 1.4)]),
    ], scale=SC, origin=(CX, FLOOR_Y))
    sy = FLOOR_Y - (FLOOR_Y - (PEL_Y - 76)) * SC     # Schulterhöhe im Bild
    prims = [
        floor(FLOOR_Y, 30, 300),
        fig,
        # Öffnen: Pfeile nach außen, Kreuzen: nach innen (nur je eine Seite, sparsam)
        arrow(f"M{CX - 40} {sy + 36:.0f} Q{CX - 62} {sy + 28:.0f} {CX - 74} {sy + 12:.0f}",
              show=[(q + 0.1, SWING - 0.15), (SWING + q + 0.1, DUR - 0.15)]),
        arrow(f"M{CX + 40} {sy + 36:.0f} Q{CX + 62} {sy + 28:.0f} {CX + 74} {sy + 12:.0f}",
              show=[(q + 0.1, SWING - 0.15), (SWING + q + 0.1, DUR - 0.15)]),
        *top_inset(345, 140, 36, lambda p: (0.0, 0.0), arms=hands_top, sh_frac=0.28, hip_frac=0.22),
        static_text("hinten", 345, 99, 9, MUTED),
        *nose_badge([(0, q, "out"), (q, SWING, "in"), (SWING, SWING + q, "out"), (SWING + q, DUR, "in")]),
        nose_note(),
        static_text("Zieht/kribbelt der rechte Arm?", 14, 48, 10, WARN, anchor="start"),
        static_text("→ kleiner schwingen", 14, 61, 10, WARN, anchor="start"),
        caption_band(),
        caption("Vorne locker kreuzen – ausatmen", 0, q),
        caption("Weit nach hinten öffnen – einatmen", q, SWING),
        caption("Kreuzen – andere Hand oben", SWING, SWING + q),
        caption("Brust öffnen – einatmen", SWING + q, DUR),
        static_text("Schwung aus dem Oberkörper – nicht reißen", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, title="Armswings", fps=15)
