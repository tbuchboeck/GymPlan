"""Nerve Glide Ulnaris – nur rechter Arm, Frontansicht (Nahansicht Oberkörper).

Frontansicht: _L = linke Bildschirmseite = anatomisch RECHTER Arm.
Enthält auch die Helfer (Hand, Nerv, Skelett mit Verkürzung), die
medianus_glide.py mitbenutzt.
"""
import math

from rig import *

SLUG = "ulnaris-glide"

HAND_SKIN = HEAD
NERVE = "#fde68a"


# --------------------------------------------------------------------------
# Skelett mit perspektivischer Verkürzung: Pose-Skalar "len_<seg>" (Faktor)
# --------------------------------------------------------------------------


class FSkel(Skeleton):
    def fk(self, pose):
        out = {}
        rx, ry = pose.get("x", 200.0), pose.get("y", 200.0)
        for s in self.segs:
            if s.parent is None:
                sx, sy, pa = rx, ry, pose.get("rot", 0.0)
            else:
                p = out[s.parent]
                sx, sy, pa = p[2], p[3], p[4]
            a = pa + s.rest + pose.get(s.name, 0.0)
            ln = s.length * pose.get("len_" + s.name, 1.0)
            out[s.name] = (sx, sy, sx + ln * math.cos(math.radians(a)), sy - ln * math.sin(math.radians(a)), a)
        return out


SK = FSkel(FRONT.segs)

def twin(dyn, outer_w, inner_w, inner_color, outer_color=SKIN_LINE):
    """Animierte Pfadform als Umriss + Füllung (zwei Pfade)."""
    st = {"fill": "none", "stroke-linecap": "round", "stroke-linejoin": "round"}
    return [Prim("path", dict(st, stroke=outer_color, **{"stroke-width": outer_w}), dyn),
            Prim("path", dict(st, stroke=inner_color, **{"stroke-width": inner_w}), dyn)]


def limb2(names, width, color):
    return twin(lambda c, n=names: {"d": smooth_path(chain_points(c["P"], n))}, width + 3, width, color)


# --------------------------------------------------------------------------
# Hand: Handfläche + Finger + Daumen, orientiert am Segment hand_*
# Pose-Skalare (Präfix pre): pw Breite, fang Fingerwinkel relativ zur Hand,
# flen Fingerlänge (Verkürzung), th Daumenwinkel, tlen Daumenlänge
# --------------------------------------------------------------------------


def _hand_frame(c, seg, pre):
    wx, wy, ex, ey, a = c["P"][seg]
    g = c["pose"]
    ar = math.radians(a)
    u = (math.cos(ar), -math.sin(ar))
    n = (-math.sin(ar), -math.cos(ar))  # +90°
    return wx, wy, ex, ey, a, u, n, g


def hand_prims(seg, pre, scale=1.2):
    def frame(c):
        wx, wy, ex, ey, a, u, n, g = _hand_frame(c, seg, pre)
        pw = g.get(pre + "pw", 10) * scale
        L = 12 * scale * g.get(pre + "plen", 1)
        kx, ky = wx + u[0] * L, wy + u[1] * L
        return wx, wy, kx, ky, a, u, n, g, pw

    def palm(c):
        wx, wy, kx, ky, a, u, n, g, pw = frame(c)
        h0, h1 = pw * 0.36, pw * 0.5
        p = lambda x, y: f"{x:.1f} {y:.1f}"
        return {"d": (f"M{p(wx + n[0] * h0, wy + n[1] * h0)}L{p(kx + n[0] * h1, ky + n[1] * h1)}"
                      f"Q{p(kx + u[0] * 3, ky + u[1] * 3)} {p(kx - n[0] * h1, ky - n[1] * h1)}"
                      f"L{p(wx - n[0] * h0, wy - n[1] * h0)}Z")}

    def fingers(c):
        wx, wy, kx, ky, a, u, n, g, pw = frame(c)
        fang, flen = g.get(pre + "fang", 0), g.get(pre + "flen", 1)
        d = ""
        for off, ln, spr in [(-0.36, 7, -6), (-0.12, 8.6, -2), (0.12, 9, 2), (0.36, 8, 6)]:
            bx, by = kx + n[0] * pw * off, ky + n[1] * pw * off
            fa = math.radians(a + fang + spr * (0.4 + 0.6 * flen))
            ll = ln * flen * scale
            d += f"M{bx:.1f} {by:.1f}l{ll * math.cos(fa):.1f} {-ll * math.sin(fa):.1f}"
        th, tl = g.get(pre + "th", 60), g.get(pre + "tlen", 1)
        side = 1 if th >= 0 else -1
        tx = wx + u[0] * 4 * scale + n[0] * pw * 0.4 * side
        ty = wy + u[1] * 4 * scale + n[1] * pw * 0.4 * side
        ta = math.radians(a + th)
        tL = 8 * tl * scale
        d += f"M{tx:.1f} {ty:.1f}l{tL * math.cos(ta):.1f} {-tL * math.sin(ta):.1f}"
        return {"d": d}

    return (twin(fingers, 5.2, 3.2, HAND_SKIN)
            + [Prim("path", {"fill": HAND_SKIN, "stroke": SKIN_LINE, "stroke-width": 1.6,
                             "stroke-linejoin": "round"}, palm)])


def nerve_path(side="L"):
    """Nervenverlauf HWS -> Schulter -> Arm -> Hand. Strichmuster gleitet
    mit Pose-Skalar "glide" (positiv = Richtung Hand)."""
    def f(c):
        P = c["P"]
        nx, ny, nex, ney, _ = P["neck"]
        sgn = -1 if side == "L" else 1
        p0 = (nx + 0.35 * (nex - nx) + sgn * 5, ny + 0.35 * (ney - ny))
        cx, cy = pt(P, f"clav_{side}")
        pts = [p0, ((p0[0] + cx) / 2, (p0[1] + cy) / 2 + 2), (cx, cy + 2),
               pt(P, f"upperarm_{side}"), pt(P, f"forearm_{side}")]
        hx, hy, hex_, hey, _ = P[f"hand_{side}"]
        pts.append((hx + 0.6 * (hex_ - hx), hy + 0.6 * (hey - hy)))
        return {"d": smooth_path(pts), "stroke-dashoffset": -c["pose"].get("glide", 0) * 10}
    return Prim("path", {"fill": "none", "stroke": NERVE, "stroke-width": 1.6, "stroke-dasharray": "3 3",
                         "stroke-linecap": "round", "opacity": 0.95}, f)


# Statischer Rumpf in Frontansicht (Root bei 200/200, Schultern bei y=122)
TORSO_D = ("M191 112Q180 115 173 118Q165 122 166 132L176 142Q177 165 183 182Q181 196 179 212"
           "L221 212Q219 196 217 182Q223 165 224 142L234 132Q235 122 227 118Q220 115 209 112Z")


def torso_prims():
    return [Prim("path", {"d": TORSO_D, "fill": TORSO, "stroke": SKIN_LINE, "stroke-width": 3,
                          "stroke-linejoin": "round"}),
            Prim("path", {"d": "M193 114Q200 121 207 114", "fill": "none", "stroke": SKIN_LINE,
                          "stroke-width": 1.5, "opacity": 0.7}),
            Prim("path", {"d": "M200 150L200 200", "stroke": SKIN_LINE, "stroke-width": 1, "opacity": 0.25})]


def upper_body(active="L", hand_extra_front=()):
    """Rumpf, ruhender Arm, Hals, Kopf, aktiver Arm mit Hand, Nerv."""
    rest = "R" if active == "L" else "L"
    prims = torso_prims()
    prims += limb2([f"upperarm_{rest}", f"forearm_{rest}", f"hand_{rest}"], 13, NEAR)
    prims += limb2(["neck"], 13, TORSO)
    prims += head_front()
    prims += limb2([f"upperarm_{active}", f"forearm_{active}"], 13, NEAR)
    prims += [nerve_path(active)]
    prims += hand_prims(f"hand_{active}", "h_")
    prims += list(hand_extra_front)
    return prims


def captions2(items):
    out = []
    for main, sub, t0, t1 in items:
        out.append(caption(main, t0, t1, y=279, size=14))
        if sub:
            out.append(caption(sub, t0, t1, y=295, size=11, color=MUTED, weight="400"))
    return out


TOP_HINT = (f'Gleiten, keine Dehnung – <tspan fill="{WARN}">kein Kribbeln</tspan>')

# --------------------------------------------------------------------------
# Posen
# --------------------------------------------------------------------------

BASE = dict(x=200, y=200, upperarm_R=4, forearm_R=6, hand_R=0, glide=0,
            h_pw=10, h_fang=0, h_flen=1, h_th=-70, h_tlen=1, ring=0, len_upperarm_L=1, len_forearm_L=1)

# Start: rechter Arm seitlich gestreckt auf Schulterhöhe, Handfläche vorn
# (Daumen oben), Kopf neutral.
STRAIGHT = dict(BASE, upperarm_L=-90, forearm_L=0, hand_L=4)
STRAIGHT_OPP = dict(STRAIGHT, neck=-11, head=-7, turn=0.0, glide=-1)    # Kopf nach links
# Maske: Ellbogen gebeugt, Hand am Auge, Finger zeigen nach hinten,
# Kopf nach rechts (zur Bildschirm-Linken).
MASK = dict(BASE, upperarm_L=-88, len_upperarm_L=0.92, len_forearm_L=1.1, forearm_L=-146, hand_L=-8,
            neck=13, head=8, glide=1,
            h_pw=9, h_fang=78, h_flen=0.85, h_th=-150, h_tlen=0.2, ring=1)


def build():
    T = [0, 1.9, 3.8, 5.7, 7.6]
    tl = Timeline([(T[0], STRAIGHT), (T[1], MASK), (T[2], STRAIGHT_OPP), (T[3], MASK), (T[4], STRAIGHT)],
                  skeleton=SK)

    # Daumen-Zeigefinger-Ring ums Auge ("Maske")
    def ring(c):
        wx, wy, _, _, a = c["P"]["hand_L"]
        x = wx + 18 * math.cos(math.radians(a))
        y = wy - 18 * math.sin(math.radians(a))
        return {"cx": x, "cy": y, "opacity": max(0.0, min(1.0, (c["pose"].get("ring", 0) - 0.55) / 0.45))}
    ring_p = [Prim("circle", {"r": 5.2, "fill": "none", "stroke": SKIN_LINE, "stroke-width": 4.4}, ring),
              Prim("circle", {"r": 5.2, "fill": "none", "stroke": HAND_SKIN, "stroke-width": 2.6}, ring)]

    to_mask = [(T[0], T[1]), (T[2], T[3])]
    to_straight = [(T[1], T[2]), (T[3], T[4])]
    arrows = [
        # Hand-Weg
        arrow("M100 108Q112 76 150 74", width=2, show=to_mask),
        arrow("M150 104Q120 106 104 116", width=2, show=to_straight),
        # Kopf-Neigung
        arrow("M214 64Q202 56 188 61", width=2, show=to_mask),
        arrow("M186 64Q198 56 212 61", width=2, show=to_straight),
    ]
    fig = group([ghost(limb(["upperarm_L", "forearm_L"], 13, NEAR), SK, STRAIGHT, 0.14)]
                + upper_body("L", ring_p) + arrows,
                scale=1.5, origin=(200, 120), dx=45, dy=8)
    fig.attrs["clip-path"] = "url(#clipU)"

    label = [
        Prim("rect", {"x": 22, "y": 176, "width": 112, "height": 24, "rx": 12, "fill": "#0b1220",
                      "stroke": ACCENT, "stroke-width": 1.2, "opacity": 0.9}),
        static_text("nur rechter Arm", 78, 192, 12.5, ACCENT, weight="700"),
        static_text("Arm und Kopf", 78, 218, 11, MUTED),
        static_text("bewegen sich gegengleich", 78, 232, 11, MUTED),
    ]
    prims = [fig, *label, caption_band(),
             *captions2([
                 ("Ellbogen beugen, Hand zum Ohr", "Finger zeigen nach hinten · Kopf nach rechts", T[0], T[1]),
                 ("Arm strecken", "gleichzeitig Kopf nach links neigen", T[1], T[2]),
                 ("Wieder beugen – Maske ums Auge", "Kopf nach rechts · rhythmisch, nie halten", T[2], T[3]),
                 ("Arm strecken, Kopf zurück", "langsam hin und her · 5–10×", T[3], T[4]),
             ]),
             static_text(TOP_HINT, 200, 24, 13, MUTED)]
    clip = '<clipPath id="clipU"><rect x="0" y="0" width="400" height="258"/></clipPath>'
    return render(prims, tl, SK, fps=12, title="Nerve Glide Ulnaris (rechts)", extra_defs=clip)
