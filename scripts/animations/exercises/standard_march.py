from rig import *
from exercises._morgen_b_props import nose_hint, label

SLUG = "standard-march"

# Seitansicht (Blick nach rechts – nahe Seite = rechte Körperseite).
# Am Stand marschieren: Knie hoch, die gegengleiche Hand tippt aufs Knie.
# Nahes (rechtes) Knie <- ferne (linke) Hand, fernes (linkes) Knie <- nahe Hand.
# Die tippende Hand wird per IK auf das Knie geführt und weich eingeblendet
# (Pose-Skalare tap_n / tap_f = 0..1). Rumpf aufrecht, Kinn leicht zurück.

FLOOR_Y = 252
CX = 196
SC = 0.88
STAND = dict(x=CX, y=FLOOR_Y - 107, neck=5, head=-6,
             upperarm_n=-4, forearm_n=10, upperarm_f=-2, forearm_f=10, tap_n=0, tap_f=0)
# Nahes (rechtes) Knie hoch, ferne (linke) Hand tippt; nahe Hand pendelt leicht zurück
UP_N = dict(STAND, thigh_n=88, shin_n=-96, foot_n=-14, upperarm_n=-18, forearm_n=22, tap_f=1,
            y=FLOOR_Y - 106, lumbar=-1)
UP_F = dict(STAND, thigh_f=88, shin_f=-96, foot_f=-14, upperarm_f=-18, forearm_f=22, tap_n=1,
            y=FLOOR_Y - 106, lumbar=-1)


def blend(p, ik, w):
    if w <= 0.001:
        return p
    q = solve_ik(SIDE, p, ik)
    out = dict(p)
    for k in (ik.upper, ik.lower, ik.end_seg):
        if k:
            d = (q[k] - p.get(k, 0.0) + 180.0) % 360.0 - 180.0   # kürzester Weg
            out[k] = p.get(k, 0.0) + d * w
    return out


class MarchTimeline(Timeline):
    def at(self, t):
        p = self._interp(t)
        P = SIDE.fk(p)
        for arm, leg, w in (("f", "n", p["tap_f"]), ("n", "f", p["tap_n"])):
            kx, ky = pt(P, f"thigh_{leg}")
            # Handgelenk knapp hinter dem Knie auf der Oberseite, Finger zeigen nach vorn
            ik = IK(f"upperarm_{arm}", f"forearm_{arm}", (kx - 14, ky - 13), bend=-1,
                    end_seg=f"hand_{arm}", end_abs=-12)
            p = blend(p, ik, smooth(min(1.0, w)))
        return p


def build():
    keys = [(0, STAND), (0.55, UP_N), (0.75, UP_N), (1.2, STAND), (1.75, UP_F), (1.95, UP_F), (2.4, STAND)]
    tl = MarchTimeline(keys, skeleton=SIDE)
    dur = tl.duration

    # Körperlot: Ohr – Schulter – Hüfte – Knöchel
    P0 = SIDE.fk(STAND)
    lot_x = pt(P0, "root", end=False)[0]
    lot = Prim("line", {"x1": lot_x, "y1": pt(P0, "head")[1] - 24, "x2": lot_x, "y2": FLOOR_Y - 4,
                        "stroke": GOOD, "stroke-width": 1.5, "stroke-dasharray": "5 6", "opacity": 0.45})

    def tap_flash(arm, leg, show):
        def f(c):
            x, y = pt(c["P"], f"thigh_{leg}")
            return {"cx": x - 6, "cy": y - 14}
        return Prim("g", {"_show": show}, children=[
            Prim("circle", {"r": 15, "fill": ACCENT, "opacity": 0.16}, f),
            Prim("circle", {"r": 15, "fill": "none", "stroke": ACCENT, "stroke-width": 3}, f)])

    def chin_cue():
        def f(c):
            x, y = pt(c["P"], "head")
            return {"d": f"M{x + 34:.1f} {y + 6:.1f}L{x + 22:.1f} {y + 6:.1f}"}
        return Prim("path", {"fill": "none", "stroke": ACCENT, "stroke-width": 2.5, "stroke-linecap": "round",
                             "marker-end": "url(#arrowhead)", "opacity": 0.8}, f)

    knee_arrow = lambda show: arrow(f"M{CX + 74} 206 Q{CX + 82} 186 {CX + 76} 162", width=2.5, show=show)
    main = group([
        *side_figure(extras_front=[
            # Tippt die ferne Hand aufs nahe Knie, liegt der Arm vor dem Körper
            *[Prim(q.tag, dict(q.attrs), (lambda c, d=q.dyn: {**d(c), "opacity": 1 if c["pose"]["tap_f"] > 0.35 else 0}))
              for q in limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)],
        ]),
        tap_flash("f", "n", [(0.45, 0.95)]),
        tap_flash("n", "f", [(1.65, 2.15)]),
        knee_arrow([(0.05, 0.55), (1.25, 1.75)]),
        chin_cue(),
    ], scale=SC, origin=(CX, FLOOR_Y))

    prims = [
        floor(FLOOR_Y + 1, 70, 330),
        main,
        caption_band(),
        caption("Rechtes Knie hoch – linke Hand tippt", 0, 1.2),
        caption("Linkes Knie hoch – rechte Hand tippt", 1.2, dur),
        static_text("Aufrecht bleiben – Kinn leicht zurück", 200, 24, LEAD_SIZE, MUTED),
        label("Kinn zurück", 236, 68, 0, dur, size=12, anchor="start"),
        nose_hint(dur=dur),
    ]
    return render(prims, tl, SIDE, title="Standard March", fps=15)
