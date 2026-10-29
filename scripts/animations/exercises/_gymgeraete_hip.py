"""Gemeinsamer Aufbau für Adduktions- und Abduktionsmaschine (Frontansicht,
sitzend, 3D-Projektion aus _gymgeraete_props). build.py lädt diese Datei
nicht als Übung (Unterstrich)."""

from rig import *
from exercises._gymgeraete_props import *

ORIGIN = (200.0, 162.0)
FLOOR_Y = 250
GRIP_Y = 8.0
GRIP_X = 38.0
GRIP_Z = -4.0


def _arms(J, pose):
    for s, side in ((-1, "L"), (1, "R")):
        arm_to(J, side, (s * GRIP_X, GRIP_Y, GRIP_Z), (s * 1.0, 0.0, -0.3))


SK = Proj3D(lambda p: seated_joints(p, _arms), SEATED_SEGS, ORIGIN, elev=math.radians(34))
proj = SK.proj


def J(c):
    return c["P"]["_J"]


def ppoly(pts3, fill=PROP, stroke=PROP_DARK, w=2.0) -> Prim:
    pts = [proj(p) for p in pts3]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return Prim("path", {"d": d, "fill": fill, "stroke": stroke, "stroke-width": w, "stroke-linejoin": "round"})


def box(x0, x1, y0, y1, z0, z1, top=PROP, front="#56657c") -> list[Prim]:
    """Quader: Vorderseite + Oberseite (Kamera leicht von oben)."""
    return [
        ppoly([(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)], front),
        ppoly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top),
    ]


def pad_pt(c, s, inner):
    k = J(c)["knee_" + ("L" if s < 0 else "R")]
    off = -s * 13 if inner else s * 13
    return (k[0] + off, k[1], k[2] - 8)


def leg_lever(s, inner) -> tuple[list[Prim], list[Prim]]:
    """(hinten: Hebelarm + Fußstütze, vorne: Polster)."""
    side = "L" if s < 0 else "R"
    LEV_Y = -18.0

    def lever(c):
        p = pad_pt(c, s, inner)
        return (proj((s * 6.0, LEV_Y, 10.0)), proj((p[0], LEV_Y, p[2])))

    def post(c):
        p = pad_pt(c, s, inner)
        a = J(c)["ank_" + side]
        return (proj((p[0], LEV_Y, p[2])), proj((p[0], a[1] - 9, a[2] + 2)))

    def peg(c):
        p = pad_pt(c, s, inner)
        a = J(c)["ank_" + side]
        x_in, x_out = (p[0], a[0] + s * 9) if inner else (p[0], a[0] - s * 9)
        return (proj((x_in, a[1] - 9, a[2] + 4)), proj((x_out, a[1] - 9, a[2] + 4)))

    def pad(c):
        p = pad_pt(c, s, inner)
        return (proj((p[0], p[1] + 10, p[2])), proj((p[0], p[1] - 14, p[2])))

    back = [dline(lever, PROP_DARK, 8), dline(post, PROP_DARK, 6), dline(peg, PROP_DARK, 7),
            dline(peg, "#7c8aa0", 4)]
    front = [dline(pad, "#2b3546", 17), dline(pad, PROP, 13)]
    return back, front


def machine(lift, inner):
    stack, pulley = weight_stack(352, 56, FLOOR_Y, lift, n=10, sel=4, w=28)
    bx0, by0 = proj((-34, -12, -26))
    cable = poly([(pulley[0], pulley[1] - 5), (300, pulley[1] - 5), (300, 226), proj((0, -22, -10))],
                 "#cbd5e1", 1.4, opacity=0.8)
    back = stack + [
        Prim("line", {"x1": 30, "y1": FLOOR_Y, "x2": 380, "y2": FLOOR_Y, "stroke": FLOOR, "stroke-width": 3,
                      "stroke-linecap": "round"}),
        cable,
        # Grundrahmen + Säule
        line(*proj((0, -24, -14)), *proj((0, -78, -14)), PROP_DARK, 14),
        ppoly([(-60, -78, -30), (60, -78, -30), (60, -78, 40), (-60, -78, 40)], PROP_DARK, PROP_DARK),
        # Lehne
        *box(-40, 40, -6, 124, -34, -20, top="#7c8aa0", front=PROP),
        # Sitz
        *box(-46, 46, -24, -11, -26, 34),
        # Griffe seitlich
        line(*proj((-GRIP_X - 4, -12, GRIP_Z)), *proj((-GRIP_X, GRIP_Y, GRIP_Z)), PROP_DARK, 5),
        line(*proj((GRIP_X + 4, -12, GRIP_Z)), *proj((GRIP_X, GRIP_Y, GRIP_Z)), PROP_DARK, 5),
        line(*proj((-GRIP_X - 6, GRIP_Y, GRIP_Z)), *proj((-GRIP_X + 6, GRIP_Y, GRIP_Z)), "#1f2937", 7),
        line(*proj((GRIP_X - 6, GRIP_Y, GRIP_Z)), *proj((GRIP_X + 6, GRIP_Y, GRIP_Z)), "#1f2937", 7),
    ]
    lb, lf = leg_lever(-1, inner)
    rb, rf = leg_lever(1, inner)
    return back + lb + rb, lf + rf


def build_hip(inner: bool, title: str):
    """inner=True: Adduktion (Polster innen, Beine zusammen drücken),
    inner=False: Abduktion (Polster außen, Beine auseinander)."""
    if inner:
        S0, S1 = 36.0, 11.0
    else:
        S0, S1 = 9.0, 36.0
    base = dict(spread=S0, turn=0.0)
    work = dict(spread=S1, turn=0.0)
    T = [0, 0.8, 2.2, 2.8, 4.8, 5.4]
    tl = Timeline([(T[0], base), (T[1], base), (T[2], work), (T[3], work), (T[4], base), (T[5], base)],
                  skeleton=SK)
    lift = lambda c: 30 * (c["pose"]["spread"] - S0) / (S1 - S0)
    back, pads = machine(lift, inner)

    # Fokus: Adduktoren (Oberschenkel innen) bzw. Abduktoren (Hüfte außen)
    def foc(s):
        side = "L" if s < 0 else "R"

        def f(c):
            j = J(c)
            if inner:
                h, k = j["hip_" + side], j["knee_" + side]
                p = v_add(v_mul(v_add(h, k), 0.5), (-s * 7, 4, 0))
            else:
                h = j["hip_" + side]
                p = v_add(h, (s * 13, 6, 0))
            x, y = proj(p)
            return {"cx": x, "cy": y}
        rx, ry = (9, 12) if inner else (9, 13)
        return Prim("ellipse", {"rx": rx, "ry": ry, "fill": ACCENT, "opacity": 0.35, "_pulse": True,
                                "_show": [(T[1], T[4])]}, f)

    P0, P1 = SK.fk(base), SK.fk(work)
    kl0, kr0 = pt(P0, "thigh_L"), pt(P0, "thigh_R")
    kl1, kr1 = pt(P1, "thigh_L"), pt(P1, "thigh_R")
    ay = kl0[1] - 2
    if inner:   # Pfeile außen an den Knien, nach innen
        arrows = [arrow(f"M{kl0[0] - 44:.0f} {ay:.0f} L{kl0[0] - 22:.0f} {ay:.0f}", show=[(T[1], T[2])]),
                  arrow(f"M{kr0[0] + 44:.0f} {ay:.0f} L{kr0[0] + 22:.0f} {ay:.0f}", show=[(T[1], T[2])])]
    else:       # Pfeile außen, nach außen
        arrows = [arrow(f"M{kl1[0] - 16:.0f} {ay:.0f} L{kl1[0] - 40:.0f} {ay:.0f}", show=[(T[1], T[2])]),
                  arrow(f"M{kr1[0] + 16:.0f} {ay:.0f} L{kr1[0] + 40:.0f} {ay:.0f}", show=[(T[1], T[2])])]

    fig = seated_front_figure(legs_front=pads)
    legs_ghost = []
    for s in ("L", "R"):
        legs_ghost += limb(["thigh_" + s], 18, NEAR) + limb_j(["shin_" + s, "foot_" + s], 15, NEAR)
    prims = back + [ghost(legs_ghost, SK, base, 0.14)] + fig + [foc(-1), foc(1)] + arrows
    if inner:
        caps = [caption("Polster innen an den Knien, Beine offen", 0, T[1], size=14),
                caption("Ausatmen – Beine zusammendrücken", T[1], T[2]),
                caption("Kurz halten", T[2], T[3]),
                caption("Langsam öffnen – Gewicht nicht absetzen", T[3], T[5], size=14)]
        lead = "Rücken an der Lehne – langsam zurück, nicht fallen lassen"
    else:
        caps = [caption("Polster außen an den Knien, Beine zu", 0, T[1]),
                caption("Ausatmen – Beine nach außen drücken", T[1], T[2]),
                caption("Kurz halten", T[2], T[3]),
                caption("Langsam zurück – Gewicht nicht absetzen", T[3], T[5], size=14)]
        lead = "Becken bleibt ruhig – Kraft aus der Hüfte"
    prims += [caption_band(), *caps, static_text(lead, 200, 24, LEAD_SIZE, MUTED)]
    return render(prims, tl, SK, fps=15, title=title)
