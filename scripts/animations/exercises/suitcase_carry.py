from rig import *
from exercises import walking as W

SLUG = "suitcase-carry"

# Einseitiges Tragen: Gehen wie in walking.py, die nahe Hand trägt eine
# schwere Kurzhantel und hängt ruhig (kein Armschwung), Rumpf bleibt aufrecht.


class CarryTimeline(W.WalkTimeline):
    def at(self, t):
        pose = super().at(t)
        pose["upperarm_n"] = 2
        pose["forearm_n"] = 0
        pose["hand_n"] = 0
        pose["rot"] = -1
        return pose


def dumbbell(c):
    x, y = pt(c["P"], "hand_n")
    return {"x": x - 16, "y": y - 2}


def build():
    tl = CarryTimeline()
    dur = tl.duration
    T = W.CYCLE

    dashes = Prim("line", {"x1": 20, "y1": W.FLOOR_Y + 5, "x2": 380, "y2": W.FLOOR_Y + 5, "stroke": "#475569",
                           "stroke-width": 2.5, "stroke-dasharray": "12 25.8", "stroke-linecap": "round"},
                  lambda c: {"stroke-dashoffset": c["t"] * W.SPEED * W.SCALE})
    bell = [
        Prim("rect", {"width": 32, "height": 7, "rx": 3, "fill": PROP}, dumbbell),
        Prim("rect", {"width": 9, "height": 18, "rx": 3, "fill": PROP_DARK},
             lambda c: {"x": pt(c["P"], "hand_n")[0] - 18, "y": pt(c["P"], "hand_n")[1] - 7.5}),
        Prim("rect", {"width": 9, "height": 18, "rx": 3, "fill": PROP_DARK},
             lambda c: {"x": pt(c["P"], "hand_n")[0] + 9, "y": pt(c["P"], "hand_n")[1] - 7.5}),
    ]
    fig = []
    fig += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    fig += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    fig += limb(["neck"], 13, TORSO)
    fig += limb(["lumbar", "thorax"], 30, TORSO)
    fig += limb(["thorax", "chest"], 26, TORSO, outline=False)
    fig += head_side()
    fig += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    fig += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)
    fig += bell
    core = focus("lumbar", rx=9, ry=14, offset=(-4, 0), end=False, show=[(T, 3 * T)])
    scene = group([*fig, core], scale=W.SCALE, origin=(W.CX, W.FLOOR_Y))
    prims = [
        floor(W.FLOOR_Y, 20, 380),
        dashes,
        scene,
        static_text("Schultern waagrecht", 318, 92, 12, GOOD, weight="600"),
        static_text("nicht zur Last neigen", 318, 106, 12, GOOD, weight="600"),
        caption_band(),
        static_text("Schwere Hantel oder Tasche einseitig tragen", 200, 22, LEAD_SIZE, MUTED),
        caption("Last in einer Hand, aufrecht gehen", 0, T),
        caption("Rumpf fest – seitlich nicht einknicken", T, 3 * T),
        caption("30 s gehen, dann Seite wechseln", 3 * T, 4 * T),
    ]
    return render(prims, tl, SIDE, fps=15, title="Suitcase Carry")
