from rig import *
from exercises._gymgeraete_props import *

SLUG = "rotary-torso"

# Frontansicht, sitzend, mit 3D-Projektion: Becken und Beine bleiben fest
# (Knie hinter dem Kniepolster), nur der Oberkörper dreht um die Längsachse.
# Brustpolster und Schulterpolster hängen an einem Joch hinter den Schultern
# und drehen exakt mit; die Hände halten die Griffe an den Schulterpolstern.
# Gezeigt wird je eine Wiederholung nach links und nach rechts, weil die Sätze
# abwechseln.

ORIGIN = (200.0, 166.0)
FLOOR_Y = 250
YAW = 38.0


def _arms(J, pose):
    yaw = pose.get("yaw", 0.0)
    for s, side in ((-1, "L"), (1, "R")):
        hand = rot_y((s * 11.0, 54.0, 30.0), yaw)
        pole = rot_y((s * 1.0, -0.9, 0.0), yaw)
        arm_to(J, side, hand, pole)


SK = Proj3D(lambda p: seated_joints(dict(p, spread=7.0), _arms), SEATED_SEGS, ORIGIN, elev=math.radians(30))
proj = SK.proj


def rp(c, p):
    """Punkt der Polster-Baugruppe (dreht mit dem Oberkörper) -> Bild."""
    return proj(rot_y(p, c["pose"].get("yaw", 0.0)))


def ppoly(pts3, fill=PROP, stroke=PROP_DARK, w=2.0) -> Prim:
    pts = [proj(p) for p in pts3]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return Prim("path", {"d": d, "fill": fill, "stroke": stroke, "stroke-width": w, "stroke-linejoin": "round"})


def box(x0, x1, y0, y1, z0, z1, top=PROP, front="#56657c") -> list[Prim]:
    return [
        ppoly([(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)], front),
        ppoly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top),
    ]


def machine_back(lift) -> list[Prim]:
    stack, pulley = weight_stack(352, 60, FLOOR_Y, lift, n=10, sel=4, w=28)
    hub = proj((0, 112, -32))
    return [
        Prim("line", {"x1": 30, "y1": FLOOR_Y, "x2": 380, "y2": FLOOR_Y, "stroke": FLOOR, "stroke-width": 3,
                      "stroke-linecap": "round"}),
        *stack,
        # Säule hinter der Lehne bis zur Drehnabe, Ausleger zum Turm
        line(*proj((0, -84, -34)), *hub, PROP_DARK, 12),
        line(hub[0], hub[1], 340, hub[1], PROP_DARK, 8),
        poly([(pulley[0], pulley[1] - 5), (330, pulley[1] - 5), (330, hub[1] - 2), (hub[0] + 8, hub[1] - 2)],
             "#cbd5e1", 1.4, opacity=0.8),
        ppoly([(-58, -84, -34), (58, -84, -34), (58, -84, 50), (-58, -84, 50)], PROP_DARK, PROP_DARK),
        *box(-40, 40, -6, 116, -36, -22, top="#7c8aa0", front=PROP),
        *box(-44, 44, -24, -11, -26, 32),
        # Fußstütze
        *box(-40, 40, -62, -56, 48, 74, top="#7c8aa0"),
        circle(hub[0], hub[1], 11, PROP_DARK, stroke="#94a3b8", **{"stroke-width": 2}),
        circle(hub[0], hub[1], 4, "#94a3b8"),
    ]


def pads() -> list[Prim]:
    """Joch hinter den Schultern, Schulterpolster vorn an den Schultern und
    Griffbügel vor der Brust – alles dreht mit dem Oberkörper."""
    out = []
    for s in (-1, 1):
        out += [dline(lambda c, s=s: (rp(c, (s * 46.0, 76.0, -20.0)), rp(c, (s * 34.0, 72.0, 14.0))),
                      PROP_DARK, 7)]
    out += [dline(lambda c: (rp(c, (-46.0, 76.0, -20.0)), rp(c, (46.0, 76.0, -20.0))), PROP_DARK, 7)]
    for s in (-1, 1):
        f = lambda c, s=s: (rp(c, (s * 27.0, 84.0, 16.0)), rp(c, (s * 27.0, 66.0, 16.0)))
        out += [dline(f, "#2b3546", 15), dline(f, PROP, 11)]
        g = lambda c, s=s: (rp(c, (s * 30.0, 64.0, 16.0)), rp(c, (s * 18.0, 54.0, 30.0)))
        out += [dline(g, PROP_DARK, 5)]
    out += [dline(lambda c: (rp(c, (-18.0, 54.0, 30.0)), rp(c, (18.0, 54.0, 30.0))), "#1f2937", 7)]
    return out


def knee_pad() -> list[Prim]:
    a, b = proj((-38, -10, 58)), proj((38, -10, 58))
    return [line(*a, *b, "#2b3546", 15), line(*a, *b, PROP, 11),
            line(*proj((-42, -10, 50)), *proj((-46, -58, 50)), PROP_DARK, 5),
            line(*proj((42, -10, 50)), *proj((46, -58, 50)), PROP_DARK, 5)]


def build():
    base = dict(yaw=0.0, turn=0.0)
    left = dict(yaw=YAW, turn=0.75)      # nach links (Person) = Brust dreht nach Bild-rechts
    right = dict(yaw=-YAW, turn=-0.75)
    T = [0, 0.8, 2.2, 2.6, 4.2, 4.6, 6.0, 6.4, 8.0, 8.4]
    tl = Timeline([(T[0], base), (T[1], base), (T[2], left), (T[3], left), (T[4], base), (T[5], base),
                   (T[6], right), (T[7], right), (T[8], base), (T[9], base)], skeleton=SK)
    lift = lambda c: 28 * abs(c["pose"].get("yaw", 0.0)) / YAW

    shoulders_ghost = ghost([Prim("path", {"fill": "none", "stroke": TORSO, "stroke-width": 22,
                                           "stroke-linecap": "round"},
                                  lambda c: {"d": smooth_path([pt(c["P"], "clav_L"), pt(c["P"], "chest"),
                                                               pt(c["P"], "clav_R")])})], SK, base, 0.22)
    fig = seated_front_figure(extras_after_trunk=pads()[:3], extras_after_arms=pads()[3:],
                              legs_front=knee_pad())
    prims = machine_back(lift) + fig + [
        shoulders_ghost,
        focus("waist_L", rx=8, ry=13, offset=(-2, 0), show=[(T[1], T[4]), (T[5], T[8])]),
        focus("waist_R", rx=8, ry=13, offset=(2, 0), show=[(T[1], T[4]), (T[5], T[8])]),
        arrow("M146 50 Q200 32 254 50", show=[(T[1], T[2])]),
        arrow("M254 50 Q200 32 146 50", show=[(T[5], T[6])]),
        Prim("g", {"_show": [(0, T[5])]}, children=[static_text("Satz links", 66, 64, 14, ACCENT, weight="700")]),
        Prim("g", {"_show": [(T[5], T[9])]}, children=[static_text("Satz rechts", 66, 64, 14, ACCENT,
                                                                   weight="700")]),
        caption_band(),
        caption("Brust ans Polster, Arme an die Schulterpolster", 0, T[1], size=14),
        caption("Ausatmen – kontrolliert nach links drehen", T[1], T[3], size=14),
        caption("Langsam zurück zur Mitte", T[3], T[5]),
        caption("Nächster Satz: nach rechts drehen", T[5], T[7]),
        caption("Langsam zurück – Seite je Satz wechseln", T[7], T[9], size=14),
        static_text("Nur der Oberkörper dreht – Becken bleibt fest", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SK, fps=12, title="Rotary Torso")
