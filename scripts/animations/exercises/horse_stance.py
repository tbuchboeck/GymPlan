from rig import *
from exercises._morgen_b_props import nose_hint, label

SLUG = "horse-stance"

# Seitansicht (Blick nach rechts) im tiefen Reitersitz + kleine statische
# Frontansicht oben links (zeigt den breiten Stand). Das Becken rollt locker
# nach vorne (Steißbein unter) und nach hinten (Po raus). Umsetzung: "rot"
# kippt das Becken, Lenden-/Brustwirbel gleichen gegen, damit der Oberkörper
# aufrecht bleibt. Füße fix (IK), Hände liegen locker auf den Oberschenkeln
# (IK auf einen Punkt am Oberschenkel).

FLOOR_Y = 252
CX = 210
SC = 0.92
ANK_Y = FLOOR_Y - 9
ANK_N = (CX + 26, ANK_Y)
ANK_F = (CX + 31, ANK_Y)

BASE = dict(x=CX - 22, y=ANK_Y - 62, neck=-2, head=0)


def tilt_pose(tilt, shift):
    """tilt > 0: Becken nach hinten gekippt (Po raus, anteriore Kippung);
    tilt < 0: nach vorne gerollt (Steißbein unter). shift = Becken vor/zurück."""
    return dict(BASE, rot=-tilt, x=BASE["x"] + shift, lumbar=tilt * 0.55, thorax=tilt * 0.35,
                chest=tilt * 0.1, tilt=tilt)


NEUT = tilt_pose(0, 0)
FWD = tilt_pose(-17, 5)
BACK = tilt_pose(19, -6)


def on_thigh(leg, k, lift=-11):
    """Punkt auf dem Oberschenkel (Anteil k vom Hüftgelenk), etwas darüber."""
    def f(pose):
        P = SIDE.fk(pose)
        sx, sy, ex, ey, a = P[f"thigh_{leg}"]
        return sx + (ex - sx) * k, sy + (ey - sy) * k + lift
    return f


def build():
    iks = [
        IK("thigh_n", "shin_n", ANK_N, bend=1, end_seg="foot_n", end_abs=0),
        IK("thigh_f", "shin_f", ANK_F, bend=1, end_seg="foot_f", end_abs=0),
        IK("upperarm_n", "forearm_n", on_thigh("n", 0.72), bend=-1, end_seg="hand_n", end_abs=-28),
        IK("upperarm_f", "forearm_f", on_thigh("f", 0.78, -9), bend=-1, end_seg="hand_f", end_abs=-28),
    ]
    keys = [(0, NEUT), (0.9, FWD), (1.3, FWD), (2.5, BACK), (2.9, BACK), (3.8, NEUT)]
    tl = Timeline(keys, iks=iks, skeleton=SIDE)
    dur = tl.duration

    # Becken als eigenes Oval (kippt mit rot) + Kipp-Linie
    def pelvis(pad):
        def f(c):
            x, y = pt(c["P"], "root", end=False)
            a = -c["pose"].get("rot", 0.0)        # SVG-Rotation (im Uhrzeigersinn positiv)
            return {"cx": x + 2, "cy": y - 2, "transform": f"rotate({a:.1f} {x:.1f} {y:.1f})"}
        return Prim("ellipse", {"rx": 15 + pad, "ry": 12 + pad, "fill": SKIN_LINE if pad else TORSO}, f)

    def tilt_line(c):
        x, y = pt(c["P"], "root", end=False)
        a = math.radians(c["pose"].get("rot", 0.0))
        dx, dy = math.cos(a), -math.sin(a)
        return {"x1": x - 30 * dx, "y1": y - 6 - 30 * dy, "x2": x + 30 * dx, "y2": y - 6 + 30 * dy}

    figure = []
    figure += limb(["thigh_f", "shin_f", "foot_f"], 15, FAR)
    figure += limb(["upperarm_f", "forearm_f", "hand_f"], 11, FAR)
    figure += limb(["neck"], 13, TORSO)
    figure += limb(["lumbar", "thorax"], 30, TORSO)
    figure += limb(["thorax", "chest"], 26, TORSO, outline=False)
    figure += [pelvis(1.5), pelvis(0)]
    figure += head_side()
    figure += limb(["thigh_n", "shin_n", "foot_n"], 16, NEAR)
    figure += [Prim("line", {"stroke": ACCENT, "stroke-width": 3, "stroke-linecap": "round", "opacity": 0.9},
                    tilt_line)]
    figure += limb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR)

    # Lot für den aufrechten Oberkörper
    def lot(c):
        x, y = pt(c["P"], "chest")
        return {"x1": x, "y1": y - 52, "x2": x, "y2": y + 60}
    lot_line = Prim("line", {"stroke": GOOD, "stroke-width": 1.5, "stroke-dasharray": "5 5", "opacity": 0.5}, lot)

    P0 = SIDE.fk(tl.at(0))
    rx, ry = pt(P0, "root", end=False)
    roll_fwd = arrow(f"M{rx - 34:.0f} {ry + 22:.0f} Q{rx - 18:.0f} {ry + 40:.0f} {rx + 2:.0f} {ry + 34:.0f}",
                     width=2.8, show=[(0.0, 1.0)])
    roll_back = arrow(f"M{rx + 6:.0f} {ry + 34:.0f} Q{rx - 18:.0f} {ry + 44:.0f} {rx - 38:.0f} {ry + 24:.0f}",
                      width=2.8, show=[(1.3, 2.6)])

    main = group([
        lot_line,
        *figure,
        roll_fwd, roll_back,
    ], scale=SC, origin=(CX, FLOOR_Y))

    # Front-Inset (statisch): breiter Reitersitz
    FP = dict(x=0, y=0, upperarm_L=-12, upperarm_R=12)
    ix, iy, iw, ih = 14, 44, 92, 112
    fpose = dict(FP)
    from rig import FRONT as FR
    ank = 50
    for side, sgn, bend in (("L", -1, -1), ("R", 1, 1)):
        fpose = solve_ik(FR, fpose, IK(f"thigh_{side}", f"shin_{side}", (sgn * ank, 66), bend=bend))
    fpose = solve_ik(FR, fpose, IK("upperarm_L", "forearm_L", (-30, 24), bend=1))
    fpose = solve_ik(FR, fpose, IK("upperarm_R", "forearm_R", (30, 24), bend=-1))
    inset_fig = front_figure(legs=True)
    inset = group([ghost(inset_fig, FR, fpose, 1.0)], scale=0.42, origin=(0, 0),
                  dx=ix + iw / 2, dy=iy + 52)
    inset_box = [
        Prim("rect", {"x": ix, "y": iy, "width": iw, "height": ih, "rx": 8, "fill": "#0b1220", "opacity": 0.6,
                      "stroke": "#334155", "stroke-width": 1}),
        Prim("line", {"x1": ix + 8, "y1": iy + 52 + 0.42 * 82, "x2": ix + iw - 8, "y2": iy + 52 + 0.42 * 82,
                      "stroke": FLOOR, "stroke-width": 2}),
        inset,
        static_text("von vorn: breit", ix + iw / 2, iy + ih - 6, 12, MUTED),
    ]

    prims = [
        floor(FLOOR_Y + 1, 120, 360),
        *inset_box,
        main,
        label("Steißbein unter", 142, 222, 0, 1.3, size=12, anchor="end"),
        label("Po leicht raus", 142, 222, 1.3, 2.9, size=12, anchor="end"),
        caption_band(),
        caption("Becken nach vorne rollen", 0, 1.3),
        caption("Becken nach hinten rollen", 1.3, 2.9),
        caption("Locker weiter – Oberkörper bleibt ruhig", 2.9, dur),
        static_text("Tief & breit – Schultern entspannt", 200, 24, LEAD_SIZE, MUTED),
        nose_hint(dur=dur),
    ]
    return render(prims, tl, SIDE, title="Horse Stance", fps=15)
