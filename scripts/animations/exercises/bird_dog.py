from rig import *
from exercises._ruecken_cardio_props import *

SLUG = "bird-dog"

# Vierfüßlerstand, Seitansicht, Blick nach rechts. Nahe Seite = rechts.
# Seite 1: rechtes (nahes) Bein nach hinten + linker (ferner) Arm nach vorn,
# Seite 2 umgekehrt. Stützende Glieder bleiben per IK am Boden; ein
# Gewicht pro Glied blendet zwischen Stütz-IK und freier Streckung.
FLOOR_Y = 240
HAND_N = (239, FLOOR_Y - 5)
HAND_F = (235, FLOOR_Y - 5)
KNEE_N = (158, FLOOR_Y - 8)
KNEE_F = (154, FLOOR_Y - 8)

BASE = dict(x=158, y=182, rot=-83, lumbar=-1, thorax=1, chest=0, neck=-6, head=-8,
            wan=1, waf=1, wln=1, wlf=1)

IK_AN = IK("upperarm_n", "forearm_n", HAND_N, bend=-1, end_seg="hand_n", end_abs=0)
IK_AF = IK("upperarm_f", "forearm_f", HAND_F, bend=-1, end_seg="hand_f", end_abs=0)
IK_LN = IK("thigh_n", "shin_n", (KNEE_N[0] - 48, FLOOR_Y - 8), bend=1, end_seg="foot_n", end_abs=180)
IK_LF = IK("thigh_f", "shin_f", (KNEE_F[0] - 48, FLOOR_Y - 8), bend=1, end_seg="foot_f", end_abs=180)


def solve(p):
    """Stütz-IK mit Gewicht; gestreckte Glieder in absoluten Winkeln."""
    q = dict(p)
    # Ausgangswinkel der Glieder = Stützpose, dann zum Streckwinkel blenden
    for ik in (IK_AN, IK_LN, IK_AF, IK_LF):
        q = solve_ik(SIDE, q, ik)
    for s in "nf":
        wa, wl = p.get(f"wa{s}", 1.0), p.get(f"wl{s}", 1.0)
        if wa < 1:
            ext = dict(q)
            set_abs(SIDE, ext, f"upperarm_{s}", 9)
            set_abs(SIDE, ext, f"forearm_{s}", 9)
            set_abs(SIDE, ext, f"hand_{s}", 9)
            for k in (f"upperarm_{s}", f"forearm_{s}", f"hand_{s}"):
                q[k] = ext[k] + (q[k] - ext[k]) * wa
        if wl < 1:
            ext = dict(q)
            set_abs(SIDE, ext, f"thigh_{s}", 179)
            set_abs(SIDE, ext, f"shin_{s}", 178)
            set_abs(SIDE, ext, f"foot_{s}", 268)
            for k in (f"thigh_{s}", f"shin_{s}", f"foot_{s}"):
                q[k] = ext[k] + (q[k] - ext[k]) * wl
    return q


S1 = dict(BASE, wln=0, waf=0)   # rechtes Bein + linker Arm
S2 = dict(BASE, wlf=0, wan=0)   # linkes Bein + rechter Arm

# Tempo laut Plan: 2 s raus / 5 s halten / 2 s zurück
A0 = 0.8
A1, A2, A3 = A0 + 2, A0 + 7, A0 + 9
B0 = A3 + 0.6
B1, B2, B3 = B0 + 2, B0 + 7, B0 + 9
END = B3 + 0.6


def level(c):
    """Wasserwaage auf dem Kreuzbein: Mittelpunkt über lumbar."""
    P = c["P"]
    x0, y0 = pt(P, "lumbar", end=False)
    x1, y1 = pt(P, "lumbar")
    return (x0 + x1) / 2, (y0 + y1) / 2 - 19


def build():
    tl = FnTimeline([(0, BASE), (A0, BASE), (A1, S1), (A2, S1), (A3, BASE), (B0, BASE),
                     (B1, S2), (B2, S2), (B3, BASE), (END, BASE)], skeleton=SIDE, post=solve)
    S, OX = 1.12, 196
    lev = [
        Prim("rect", {"width": 34, "height": 9, "rx": 4.5, "fill": PROP, "stroke": PROP_DARK, "stroke-width": 1.5},
             lambda c: {"x": level(c)[0] - 17, "y": level(c)[1] - 9}),
        Prim("rect", {"width": 14, "height": 5, "rx": 2.5, "fill": "#0f172a"},
             lambda c: {"x": level(c)[0] - 7, "y": level(c)[1] - 7}),
        Prim("circle", {"r": 2, "fill": GOOD}, lambda c: {"cx": level(c)[0], "cy": level(c)[1] - 4.5}),
    ]
    hold = [(A1, A2), (B1, B2)]
    scene = group([
        mat(FLOOR_Y, 40, 330),
        *side_figure_r(r=6, round_arms=False),
        *lev,
        focus("lumbar", rx=20, ry=9, offset=(0, -8), show=[(A0, A3), (B0, B3)]),
        dyn_line(lambda c: ((40, pt(c["P"], "chest")[1] - 2), (330, pt(c["P"], "chest")[1] - 2)),
                 color=GOOD, width=1.5, dash="3 6", opacity=0.45, show=hold),
        arrow("M92 194 Q70 178 52 172", show=[(A0, A1), (B0, B1)]),
        arrow("M270 150 Q296 138 318 140", show=[(A0, A1), (B0, B1)]),
    ], scale=S, origin=(OX, FLOOR_Y))
    prims = [
        scene,
        label("rechtes Bein + linker Arm", 200, 66, A0, A3, 12, TEXT),
        label("linkes Bein + rechter Arm", 200, 66, B0, B3, 12, TEXT),
        *counter(A1, 5, 200, 92, size=18), *counter(B1, 5, 200, 92, size=18),
        caption_band(),
        caption("Vierfüßlerstand – Bauch fest", 0, A0),
        caption("Bein nach hinten, Arm nach vorn", A0, A1),
        caption("5 s halten – lang machen", A1, A2),
        caption("Kontrolliert zurück", A2, A3),
        caption("Seite wechseln", A3, B0),
        caption("Andere Seite strecken", B0, B1),
        caption("5 s halten – lang machen", B1, B2),
        caption("Kontrolliert zurück", B2, END),
        *tempo_chip([("2 s raus", [(A0, A1), (B0, B1)], None), ("5 s halten", hold, None),
                     ("2 s zurück", [(A2, A3), (B2, B3)], None)]),
        static_text("Becken bleibt gerade – keine Rotation", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Bird Dog", fps=8)
