from rig import *
from exercises._cardio_props import PostTimeline, figure, label, lerp, leg

SLUG = "bauch-beine-po"

# Vierfüßlerstand, Seitansicht (Blick nach rechts), wie katze_kuh: Hände und
# fernes Knie per IK am Boden, Anchor hält die Schultern über den Händen.
# Das nahe (rechte) Bein streckt sich nach hinten oben (Donkey Kick) und
# kommt kontrolliert zurück; Becken und Rücken bleiben waagrecht.

FLOOR_Y = 246
HAND = (244, FLOOR_Y - 5)
HIP = (160, 186)
ANK_REST = (HIP[0] - 48, FLOOR_Y - 8)

BASE = dict(x=HIP[0], y=HIP[1], rot=-80, neck=-6, head=-4, k=0)
KICK = dict(BASE, k=1, neck=-4)


def post(p):
    p = solve_anchor(SIDE, p, Anchor("chest", (237, 172)))
    p = solve_ik(SIDE, p, IK("upperarm_n", "forearm_n", HAND, bend=-1, end_seg="hand_n", end_abs=0))
    p = solve_ik(SIDE, p, IK("upperarm_f", "forearm_f", (HAND[0] - 4, HAND[1]), bend=-1,
                             end_seg="hand_f", end_abs=0))
    p = leg(p, "f", (ANK_REST[0] - 4, ANK_REST[1]), 180, bend=1)
    # nahes Bein: erst Hüfte strecken (Knie bleibt gebeugt, Sohle zur Decke),
    # dann das Knie strecken – als Blend der absoluten Winkel
    k = p.get("k", 0.0)
    p = leg(p, "n", ANK_REST, 180, bend=1)
    if k > 1e-4:
        P = SIDE.fk(p)
        root_abs = p.get("rot", 0) + 90
        th0, sh0 = P["thigh_n"][4], P["shin_n"][4]
        knee0 = sh0 - th0
        th0 = (th0 - 190 + 180) % 360 - 180 + 190      # nahe 190 normalisieren
        th = lerp(th0, 192, k)
        k2 = k
        bendmore = -12 * math.sin(math.pi * k)          # Ferse leicht Richtung Decke, ohne Knoten
        knee = lerp(knee0, -6, k2 * k2 * (3 - 2 * k2)) + bendmore
        p["thigh_n"] = th - root_abs - 180
        p["shin_n"] = knee
        foot_abs = lerp(180, 268, k)
        p["foot_n"] = foot_abs - (th + knee) - 90
    return p


def build():
    keys = [(0, BASE), (0.6, BASE), (1.6, KICK), (2.3, KICK), (3.4, BASE), (4.4, BASE)]
    tl = PostTimeline(keys, post)
    P0 = SIDE.fk(post(BASE))
    (x1, y1), (x2, y2) = pt(P0, "lumbar", end=False), pt(P0, "chest")
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = math.sin(a) * 19, -math.cos(a) * 19      # Normale nach oben (Rückenseite)
    back_line = Prim("line", {"x1": x1 + nx - 8, "y1": y1 + ny, "x2": x2 + nx, "y2": y2 + ny, "stroke": GOOD,
                              "stroke-width": 2, "stroke-dasharray": "5 5", "opacity": 0.75})
    kick_ghost = ghost(figure(), SIDE, post(KICK), 0.12)
    prims = [
        mat(FLOOR_Y, 40, 330),
        kick_ghost,
        *figure(),
        back_line,
        focus("root", rx=14, ry=12, offset=(-6, -8), show=[(0.6, 3.4)]),
        arrow("M100 230 Q52 232 42 188", show=[(0.6, 1.6)]),
        arrow("M42 188 Q52 232 100 230", show=[(2.3, 3.4)]),
        label("Rücken gerade", 186, 132, 0.6, 3.4, 12, GOOD),
        caption_band(),
        caption("Vierfüßler – Hände unter den Schultern", 0, 0.6),
        caption("Ausatmen – Bein nach hinten oben", 0.6, 1.6),
        caption("Kurz halten – Po anspannen", 1.6, 2.3),
        caption("Langsam zurück in den Vierfüßler", 2.3, 3.4),
        caption("15× – dann Seite wechseln", 3.4, 4.4),
        static_text("Becken bleibt waagrecht – kein Hohlkreuz", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bauch Beine Po (Donkey Kicks)")
