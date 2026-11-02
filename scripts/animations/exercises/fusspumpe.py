from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "fusspumpe"

# Rückenlage, Beine lang (Kopf links). Nur die Füße bewegen sich:
# Skalar "pump" -1 (gestreckt) .. +1 (angezogen).
FLOOR_Y = 236
C = FLOOR_Y - 16
HIP = (128 + 78, C)
SCALE_SECONDS = 1.0


def pre(p):
    f = p.get("pump", 0.0)
    p["x"], p["y"] = HIP
    p["rot"] = 90
    p["lumbar"] = p["thorax"] = p["chest"] = 0.0
    set_abs(SIDE, p, "neck", 172)
    set_abs(SIDE, p, "head", 176)
    for k in ("n", "f"):
        set_abs(SIDE, p, "thigh_" + k, 2)
        set_abs(SIDE, p, "shin_" + k, -1)
        set_abs(SIDE, p, "foot_" + k, 60 + 40 * f)
    set_abs(SIDE, p, "upperarm_n", 0)
    set_abs(SIDE, p, "forearm_n", 0)
    set_abs(SIDE, p, "hand_n", 0)
    set_abs(SIDE, p, "upperarm_f", 0)
    set_abs(SIDE, p, "forearm_f", 0)
    set_abs(SIDE, p, "hand_f", 0)
    return p


def build():
    keys = []
    t = 0.0
    for _ in range(4):
        keys += [(t, dict(pump=1)), (t + 0.6, dict(pump=1)), (t + 1.2, dict(pump=-1)), (t + 1.8, dict(pump=-1))]
        t += 2.4
    keys.append((t, dict(pump=1)))
    tl = FnTimeline(keys, skeleton=SIDE, pre=pre)
    dur = t
    win_up = [(k * 2.4 - 0.6 if k else 0, k * 2.4 + 0.6) for k in range(5)]
    win_dn = [(k * 2.4 + 0.6, k * 2.4 + 1.8) for k in range(4)]
    scene = group([
        mat(FLOOR_Y, 40, 380),
        *side_figure(),
    ], scale=1.1, origin=(200, FLOOR_Y), dx=-10)
    prims = [
        scene,
        Prim("text", {"x": 330, "y": 150, "font-size": 14, "fill": ACCENT, "font-weight": "700",
                      "text-anchor": "middle", "_show": win_up}, text="anziehen"),
        Prim("text", {"x": 330, "y": 150, "font-size": 14, "fill": GOOD, "font-weight": "700",
                      "text-anchor": "middle", "_show": win_dn}, text="strecken"),
        caption_band(),
        caption("Zehen zur Nase – dann weit wegstrecken", 0, dur / 2),
        caption("20× im ruhigen Takt, Rücken bleibt locker", dur / 2, dur),
        static_text("Nur die Füße bewegen – regt die Durchblutung an", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, fps=12, title="Fußpumpe")
