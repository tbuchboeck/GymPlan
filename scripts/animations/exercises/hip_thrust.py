from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "hip-thrust"

# Hip Thrust: Schulterblätter auf der Bankkante (links), Füße am Boden.
# Skalar "lift" 0..1 dreht den Rumpf um den Schulterkontakt nach oben,
# bis Oberkörper und Oberschenkel waagrecht eine Linie bilden.
FLOOR_Y = 240
BENCH_TOP = 196
SH = (120, BENCH_TOP - 6)       # Schulterkontakt auf der Bank
SPINE = 78
DOWN_A = -38                    # Becken hängt nach unten
UP_A = 0                        # waagrecht
ANKLE = (262, FLOOR_Y - 7)


def pre(p):
    a = DOWN_A + (UP_A - DOWN_A) * p.get("lift", 0.0)
    r = math.radians(a)
    p["x"] = SH[0] + SPINE * math.cos(r)
    p["y"] = SH[1] - SPINE * math.sin(r)
    p["rot"] = 90 + a
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    P = SIDE.fk(p)
    ca = P["chest"][4]
    set_abs(SIDE, p, "neck", ca - 14)
    set_abs(SIDE, p, "head", ca - 22)
    return p


IKS = [
    IK("thigh_n", "shin_n", ANKLE, bend=1, end_seg="foot_n", end_abs=0),
    IK("thigh_f", "shin_f", (ANKLE[0] - 3, ANKLE[1]), bend=1, end_seg="foot_f", end_abs=0),
    IK("upperarm_n", "forearm_n", (SH[0] - 18, BENCH_TOP + 2), bend=-1, end_seg="hand_n", end_abs=180),
    IK("upperarm_f", "forearm_f", (SH[0] - 22, BENCH_TOP + 2), bend=-1, end_seg="hand_f", end_abs=180),
]

T_UP0, T_UP1, T_H1, T_DN1, T_END = 0.8, 2.8, 4.8, 7.3, 8.0


def build():
    tl = FnTimeline([(0, dict(lift=0)), (T_UP0, dict(lift=0)), (T_UP1, dict(lift=1)), (T_H1, dict(lift=1)),
                     (T_DN1, dict(lift=0)), (T_END, dict(lift=0))], iks=IKS, skeleton=SIDE, pre=pre)

    def line_pts(c):
        P = c["P"]
        return pt(P, "chest"), pt(P, "thigh_n")

    bench = [
        Prim("rect", {"x": 30, "y": BENCH_TOP, "width": 98, "height": 12, "rx": 4, "fill": PROP}),
        Prim("rect", {"x": 44, "y": BENCH_TOP + 12, "width": 8, "height": FLOOR_Y - BENCH_TOP - 12, "fill": PROP_DARK}),
        Prim("rect", {"x": 104, "y": BENCH_TOP + 12, "width": 8, "height": FLOOR_Y - BENCH_TOP - 12, "fill": PROP_DARK}),
    ]
    scene = group([
        floor(FLOOR_Y, 20, 380),
        *bench,
        *side_figure(),
        dyn_line(line_pts, show=[(T_UP1, T_H1)]),
        focus("root", rx=17, ry=12, offset=(4, 8), end=False, show=[(T_UP0, T_H1)]),
        arrow("M200 222 L200 196", show=[(T_UP0, T_UP1)]),
        arrow("M200 196 L200 220", show=[(T_H1, T_DN1)]),
    ], scale=1.05, origin=(200, FLOOR_Y))
    prims = [
        scene,
        label("eine Linie", 196, 150, T_UP1, T_H1, 12, GOOD),
        *counter(T_UP1, 2, 300, 120, size=18),
        caption_band(),
        caption("Schulterblätter an die Bank, Füße am Boden", 0, T_UP0),
        caption("Ausatmen – Gesäß fest, Becken hoch", T_UP0, T_UP1),
        caption("Oben 2 s halten – Rippen unten", T_UP1, T_H1),
        caption("Langsam absenken", T_H1, T_END),
        static_text("Kraft aus dem Gesäß – kein Hohlkreuz", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Hip Thrust")
