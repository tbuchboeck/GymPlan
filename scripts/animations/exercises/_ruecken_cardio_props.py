"""Hilfen für glute_bridge, dead_bug, bird_dog, side_plank_knee, hula_hoop, tanzen."""
from rig import *


class FnTimeline(Timeline):
    """Timeline mit Vor-/Nach-Funktion pro Frame: pre(pose) läuft nach dem
    Interpolieren und vor den IKs (z. B. Becken aus Skalar 'lift' berechnen),
    post(pose) nach den IKs."""

    def __init__(self, keys, iks=(), skeleton=None, pre=None, post=None):
        super().__init__(keys, list(iks), skeleton)
        self.pre = pre
        self.post = post

    def at(self, t):
        pose = self._interp(t)
        pose["_t"] = t
        if self.pre:
            pose = self.pre(pose)
        for ik in self.iks:
            if isinstance(ik, Anchor):
                pose = solve_anchor(self.skeleton, pose, ik)
            else:
                pose = solve_ik(self.skeleton, pose, ik)
        if self.post:
            pose = self.post(pose)
        return pose


def set_abs(skel, pose, seg, ang):
    """Setzt den absoluten Winkel eines Segments (Eltern bleiben)."""
    P = skel.fk(pose)
    pose[seg] = pose.get(seg, 0.0) + ang - P[seg][4]
    return pose


def counter(t0, n, x, y, step=1.0, size=16, color=ACCENT):
    """Zählt 1..n im Sekundentakt ab t0 (Halte-Phase)."""
    out = []
    for i in range(n):
        out.append(Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": "700",
                                 "text-anchor": "middle",
                                 "_show": [(t0 + i * step, t0 + (i + 1) * step)]}, text=f"{i + 1}"))
    return out


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="middle", weight="500"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": weight,
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def dyn_line(fn, color=GOOD, width=2, dash="5 5", opacity=0.8, show=None):
    """Gestrichelte Linie zwischen zwei dynamischen Punkten fn(c)->(p,q)."""
    def f(c):
        (x1, y1), (x2, y2) = fn(c)
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    p = Prim("line", {"stroke": color, "stroke-width": width, "stroke-dasharray": dash,
                      "opacity": opacity, "stroke-linecap": "round"}, f)
    if show is not None:
        p.attrs["_show"] = show
    return p


def tempo_chip(parts, x=200, y=44, size=11):
    """Kleine Tempo-Zeile; parts = [(text, t0, t1)], aktiver Teil leuchtet."""
    out = []
    total = sum(len(p[0]) for p in parts) + 3 * (len(parts) - 1)
    cw = size * 0.56
    cx = x - total * cw / 2
    for text, t0, t1 in parts:
        w = len(text) * cw
        mx = cx + w / 2
        out.append(Prim("text", {"x": mx, "y": y, "font-size": size, "fill": MUTED, "text-anchor": "middle"},
                        text=text))
        win = t0 if isinstance(t0, list) else [(t0, t1)]
        out.append(Prim("text", {"x": mx, "y": y, "font-size": size, "fill": ACCENT, "font-weight": "700",
                                 "text-anchor": "middle", "_show": win}, text=text))
        cx += w + 3 * cw
    return out


def rounded_path(points, r=7.0):
    """Polylinie mit kleinen Rundungen an den Gelenken (klarere Knie/Ellbogen
    als smooth_path, das Winkel stark verschleift)."""
    if len(points) < 3:
        return smooth_path(points)
    d = f"M{points[0][0]:.1f} {points[0][1]:.1f}"
    for i in range(1, len(points) - 1):
        (px, py), (cx, cy), (nx, ny) = points[i - 1], points[i], points[i + 1]
        l1 = math.hypot(cx - px, cy - py) or 1
        l2 = math.hypot(nx - cx, ny - cy) or 1
        rr = min(r, l1 / 2, l2 / 2)
        ax, ay = cx - (cx - px) / l1 * rr, cy - (cy - py) / l1 * rr
        bx, by = cx + (nx - cx) / l2 * rr, cy + (ny - cy) / l2 * rr
        d += f"L{ax:.1f} {ay:.1f}Q{cx:.1f} {cy:.1f} {bx:.1f} {by:.1f}"
    d += f"L{points[-1][0]:.1f} {points[-1][1]:.1f}"
    return d


def rlimb(names, width, color, outline=True, r=7.0):
    """Wie rig.limb, aber mit rounded_path (deutlichere Gelenkwinkel)."""
    out = []
    f = lambda c, n=names: {"d": rounded_path(chain_points(c["P"], n), r)}
    if outline:
        out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}, f))
    return out


def side_figure_r(torso_w=30, extras_behind=(), extras_front=(), r=7.0, far_color=FAR):
    """side_figure mit deutlicheren Gelenkwinkeln an Armen/Beinen."""
    prims = list(extras_behind)
    prims += rlimb(["thigh_f", "shin_f", "foot_f"], 15, far_color, r=r)
    prims += rlimb(["upperarm_f", "forearm_f", "hand_f"], 11, far_color, r=r)
    prims += limb(["neck"], 13, TORSO)
    prims += limb(["lumbar", "thorax"], torso_w, TORSO)
    prims += limb(["thorax", "chest"], torso_w - 4, TORSO, outline=False)
    prims += head_side()
    prims += rlimb(["thigh_n", "shin_n", "foot_n"], 16, NEAR, r=r)
    prims += rlimb(["upperarm_n", "forearm_n", "hand_n"], 12, NEAR, r=r)
    prims += list(extras_front)
    return prims
