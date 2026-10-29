from rig import *
from exercises._morgen_b_props import nose_hint, front_feet_out, label

SLUG = "dead-arms"

# Frontansicht. Arme hängen schlaff und werden aus Schultern/Oberkörper
# geschüttelt: kleine Schulter-/Rumpfimpulse, Oberarm pendelt, Unterarm und
# Hand schlackern verzögert nach (Peitscheneffekt). Füße fix (IK), Knie weich.

FLOOR_Y = 252
CX = 200
SC = 0.88
ANK_L = (CX - 22, FLOOR_Y - 12)
ANK_R = (CX + 22, FLOOR_Y - 12)
BASE = dict(x=CX, y=FLOOR_Y - 116, clav_L=4, clav_R=-4,  # Schultern tief (clav<0 = gesenkt)
            upperarm_L=-13, upperarm_R=13, forearm_L=4, forearm_R=-4)

DT = 0.16                       # halbe Schüttelperiode
N = 20                          # Impulse pro Loop
SEQ = [1, -0.8, 1, -1, 0.7, -1, 0.9, -0.7, 1, -1, 0.8, -0.9, 1, -0.8, 0.9, -1, 1, -0.7, 0.8, -1]


def shake(k: int, s: float) -> dict:
    """Pose für Impuls k mit Richtung s (-1..1). Linke und rechte Seite leicht
    gegenläufig, damit es nach lockerem Schütteln aussieht, nicht nach Marsch."""
    s2 = SEQ[(k + 3) % N]
    p = dict(BASE)
    p["x"] = CX + 2.0 * s
    p["y"] = BASE["y"] + 1.6 * (1 if k % 2 else -0.4)        # weiche Knie federn
    p["chest"] = 3.0 * s
    p["lumbar"] = -1.0 * s
    p["neck"] = -3.0 * s                                     # Kopf bleibt ruhig
    p["clav_L"] = 4 + 2.5 * s                                # Schulter-Impuls, bleibt unten
    p["clav_R"] = -4 + 2.5 * s2
    p["upperarm_L"] = -13 - 13 * s
    p["forearm_L"] = 4 + 24 * s
    p["hand_L"] = 38 * s
    p["upperarm_R"] = 13 + 13 * s2
    p["forearm_R"] = -4 - 24 * s2
    p["hand_R"] = -38 * s2
    return p


def build():
    keys = [(0.0, dict(BASE))]
    for k in range(N):
        keys.append((DT * (k + 1) - DT / 2, shake(k, SEQ[k])))
    keys.append((DT * N, dict(BASE)))
    iks = [
        IK("thigh_L", "shin_L", ANK_L, bend=-1),
        IK("thigh_R", "shin_R", ANK_R, bend=1),
    ]
    tl = Timeline(keys, iks=iks, skeleton=FRONT)
    dur = tl.duration

    legs = (limb(["hip_L", "thigh_L", "shin_L"], 16, NEAR) + limb(["hip_R", "thigh_R", "shin_R"], 16, NEAR)
            + front_feet_out(10))
    fig = front_figure(legs=False, extras_behind=legs)
    # Schüttel-Striche neben den Händen (pulsieren im Takt)
    def wiggle(x, y, sgn):
        return Prim("path", {"d": f"M{x} {y - 9} q{sgn * 5} 4 0 9 q{sgn * -5} 4 0 9", "fill": "none",
                             "stroke": ACCENT, "stroke-width": 2.2, "stroke-linecap": "round"},
                    children=[Prim("animate", {"attributeName": "opacity", "values": "0.15;0.9;0.15",
                                               "dur": f"{2 * DT:.2f}s", "repeatCount": "indefinite"})])
    P0 = FRONT.fk(tl.at(0))
    hlx, hly = pt(P0, "hand_L")
    hrx, hry = pt(P0, "hand_R")
    wig = [wiggle(hlx - 20, hly - 14, -1), wiggle(hlx - 28, hly - 14, -1),
           wiggle(hrx + 20, hry - 14, 1), wiggle(hrx + 28, hry - 14, 1)]

    # Schultern sinken: Pfeile neben dem Hals, Ohr-Abstand
    sh_y = pt(P0, "clav_L")[1]
    down = [arrow(f"M{x} {sh_y - 22} L{x} {sh_y - 8}", width=2.5, show=[(dur / 2, dur)])
            for x in (CX - 30, CX + 30)]

    main = group([*fig,
                  focus("clav_L", rx=11, ry=7, offset=(8, -6), color=GOOD, show=[(dur / 2, dur)]),
                  focus("clav_R", rx=11, ry=7, offset=(-8, -6), color=GOOD, show=[(dur / 2, dur)]),
                  *down, *wig],
                 scale=SC, origin=(CX, FLOOR_Y))
    prims = [
        floor(FLOOR_Y + 1, 60, 340),
        main,
        caption_band(),
        caption("Arme hängen – locker ausschütteln", 0, dur / 2),
        caption("Schultern sinken – weg von den Ohren", dur / 2, dur),
        static_text("Impuls aus Schultern & Oberkörper", 200, 24, 13, MUTED),
        nose_hint(dur=dur),
    ]
    return render(prims, tl, FRONT, title="Dead Arms", fps=25)
