from rig import *
from ._hantel_b_props import dumbbell, front_fig, side_fig, label

SLUG = "seitheben-frontheben"

# Zwei Ansichten nebeneinander, nacheinander aktiv:
#   links  Frontansicht – Seitheben (Arme seitlich bis Schulterhöhe)
#   rechts Seitansicht  – Frontheben (gestreckte Arme nach vorn bis Schulterhöhe)
# Die gerade ruhende Figur wird abgeblendet. Render-Skelett ist FRONT; die
# Seitfigur rechnet ihre eigene FK aus den Pose-Schlüsseln mit Präfix "s.".

FLOOR_Y = 250
SC = 0.8
FX, SX = 112, 292                     # Bildschirm-x der beiden Figuren

F_BASE = dict(x=FX, y=FLOOR_Y - 107, hip_L=0, hip_R=0, thigh_L=-4, thigh_R=4, shin_L=2, shin_R=-2)
S_BASE = dict(x=SX, y=FLOOR_Y - 8 - 98, thigh_n=3, shin_n=-3, thigh_f=-3, shin_f=3)


def f_arms(ua, fa, clav=0.0):
    """Frontfigur: ua = Abduktion, fa = Ellbogen (positiv: Hand etwas tiefer)."""
    return dict(F_BASE, upperarm_L=-ua, forearm_L=fa, upperarm_R=ua, forearm_R=-fa, clav_L=-clav, clav_R=clav)


def s_arms(ua, fa=0.0):
    return dict(S_BASE, upperarm_n=ua, forearm_n=fa, upperarm_f=ua - 3, forearm_f=fa)


F_DOWN, F_UP = f_arms(8, 8), f_arms(86, 10)
S_DOWN, S_UP = s_arms(3, 4), s_arms(88, 2)


def key(f, s, act_f):
    d = dict(f)
    d.update({"s." + k: v for k, v in s.items()})
    d["aF"] = 0.35 + 0.65 * act_f
    d["aS"] = 0.35 + 0.65 * (1 - act_f)
    return d


def side_ctx(c):
    pose = {k[2:]: v for k, v in c["pose"].items() if k.startswith("s.")}
    return {"P": SIDE.fk(pose), "pose": pose, "t": c["t"], "u": c["u"]}


def rebind(prims):
    for p in prims:
        if p.dyn is not None:
            old = p.dyn
            p.dyn = lambda c, old=old: old(side_ctx(c))
        rebind(p.children)
    return prims


def build():
    A0, A1, A2, A3, A4 = 0.0, 0.5, 1.6, 2.2, 3.4      # Seitheben
    B0, B1, B2, B3, B4 = 3.9, 4.4, 5.5, 6.1, 7.3      # Frontheben
    END = 7.8
    tl = Timeline([
        (A0, key(F_DOWN, S_DOWN, 1)), (A1, key(F_DOWN, S_DOWN, 1)),
        (A2, key(F_UP, S_DOWN, 1)), (A3, key(F_UP, S_DOWN, 1)),
        (A4, key(F_DOWN, S_DOWN, 1)), (A4 + 0.15, key(F_DOWN, S_DOWN, 1)),
        (B0, key(F_DOWN, S_DOWN, 0)), (B1, key(F_DOWN, S_DOWN, 0)),
        (B2, key(F_DOWN, S_UP, 0)), (B3, key(F_DOWN, S_UP, 0)),
        (B4, key(F_DOWN, S_DOWN, 0)), (B4 + 0.15, key(F_DOWN, S_DOWN, 0)),
        (END, key(F_DOWN, S_DOWN, 1)),
    ], skeleton=FRONT)

    # --- Frontfigur (Seitheben)
    Pf_dn, Pf_up = FRONT.fk(F_DOWN), FRONT.fk(F_UP)
    lh, rh = pt(Pf_dn, "hand_L"), pt(Pf_dn, "hand_R")
    lu, ru = pt(Pf_up, "hand_L"), pt(Pf_up, "hand_R")
    sh_y = pt(Pf_up, "clav_L")[1]
    front = front_fig(db_L=dumbbell("hand_L", "forearm_L", fore=0.75, size=1.15),
                      db_R=dumbbell("hand_R", "forearm_R", fore=0.75, size=1.15))
    f_over = [
        Prim("line", {"x1": lu[0] - 16, "y1": sh_y, "x2": ru[0] + 16, "y2": sh_y, "stroke": GOOD,
                      "stroke-width": 2, "stroke-dasharray": "5 5", "_show": [(A1 + 0.6, A3 + 0.3)]}),
        focus("clav_L", rx=11, ry=10, offset=(-2, 2), show=[(A1, A4)]),
        focus("clav_R", rx=11, ry=10, offset=(2, 2), show=[(A1, A4)]),
        arrow(f"M{lh[0] - 18:.0f} {lh[1] - 8:.0f} Q{lu[0]:.0f} {lh[1] - 10:.0f} {lu[0] + 4:.0f} {lu[1] + 24:.0f}",
              show=[(A1, A2)]),
        arrow(f"M{rh[0] + 18:.0f} {rh[1] - 8:.0f} Q{ru[0]:.0f} {rh[1] - 10:.0f} {ru[0] - 4:.0f} {ru[1] + 24:.0f}",
              show=[(A1, A2)]),
    ]
    g_front = group([*front, *f_over], scale=SC, origin=(FX, FLOOR_Y))
    g_front.dyn = lambda c: {"opacity": c["pose"]["aF"]}

    # --- Seitfigur (Frontheben)
    Ps_dn, Ps_up = SIDE.fk(S_DOWN), SIDE.fk(S_UP)
    hd, hu = pt(Ps_dn, "hand_n"), pt(Ps_up, "hand_n")
    ssh = pt(Ps_up, "chest")
    side = rebind(side_fig(db_far=dumbbell("hand_f", "forearm_f", far=True, fore=0.75, size=1.15),
                           db_near=dumbbell("hand_n", "forearm_n", fore=0.75, size=1.15)))
    s_over = rebind([focus("chest", rx=11, ry=11, offset=(3, 4), show=[(B1, B4)])]) + [
        Prim("line", {"x1": ssh[0] - 20, "y1": ssh[1], "x2": hu[0] + 22, "y2": ssh[1], "stroke": GOOD,
                      "stroke-width": 2, "stroke-dasharray": "5 5", "_show": [(B1 + 0.6, B3 + 0.3)]}),
        arrow(f"M{hd[0] + 18:.0f} {hd[1] - 4:.0f} Q{hu[0] + 10:.0f} {hd[1] - 6:.0f} {hu[0] + 6:.0f} {hu[1] + 22:.0f}",
              show=[(B1, B2)]),
    ]
    g_side = group([*side, *s_over], scale=SC, origin=(SX, FLOOR_Y))
    g_side.dyn = lambda c: {"opacity": c["pose"]["aS"]}

    prims = [
        floor(FLOOR_Y + 1, 24, 376),
        Prim("line", {"x1": 200, "y1": 52, "x2": 200, "y2": 244, "stroke": FLOOR, "stroke-width": 1.5,
                      "stroke-dasharray": "2 6"}),
        g_front, g_side,
        label("1 · Seitheben", FX, 52, A0, B0 - 0.2, 13, ACCENT, weight="700"),
        label("1 · Seitheben", FX, 52, B0 - 0.2, END, 13, MUTED),
        label("2 · Frontheben", SX, 52, A0, B0 - 0.2, 13, MUTED),
        label("2 · Frontheben", SX, 52, B0 - 0.2, END, 13, ACCENT, weight="700"),
        caption_band(),
        caption("Seitheben: Ausatmen – seitlich hoch", A0, A2),
        caption("Schulterhöhe – Schultern tief", A2, A3),
        caption("Einatmen – langsam senken", A3, B0 - 0.2),
        caption("Frontheben: Ausatmen – nach vorn hoch", B0 - 0.2, B2),
        caption("Schulterhöhe – Arme gestreckt", B2, B3),
        caption("Einatmen – langsam senken", B3, END),
        static_text("Nur bis Schulterhöhe – ohne Schwung", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, FRONT, fps=12, title="Seitheben und Frontheben")
