"""Gemeinsame Helfer für die Morgen-Reset-Übungen (morgen_huepfen, bodywaves,
armswings, trunk_twists, hip_twist_hops).

* FnTimeline: Pose analytisch aus t (für weiche, schwingende Loops), danach
  wie gewohnt IK/Anchor.
* nose_badge: dezentes Nasen-Atem-Symbol oben rechts („Nase ein/aus“).
* Front3D: Frontfigur mit einfacher 3D-Projektion für Drehungen (Schulter-
  und Hüftlinie verkürzen sich, Arme können vor/hinter den Rumpf).
* top_inset: kleine Draufsicht (Schulter-/Hüftlinie, optional Arme).
"""
from __future__ import annotations

import math

from rig import *  # noqa: F401,F403
from rig import Timeline, Prim, FRONT, pt, smooth_path, head_front

TAU = 2 * math.pi


class FnTimeline(Timeline):
    """Timeline, deren Pose eine Funktion fn(t) liefert (Loop-Dauer dur)."""

    def __init__(self, fn, dur, iks=None, skeleton=None, post=None):
        super().__init__([(0.0, {}), (dur, {})], iks=iks or [], skeleton=skeleton)
        self.fn = fn
        self.post = post

    def _interp(self, t):
        return dict(self.fn(t))

    def at(self, t):
        pose = super().at(t)
        if self.post:
            pose = self.post(pose)
        return pose


def ease_cos(u):
    """0..1 -> 0..1..0 weich (Kosinus)."""
    return 0.5 - 0.5 * math.cos(TAU * u)


# --------------------------------------------------------------------------
# Nasen-Atem-Symbol
# --------------------------------------------------------------------------

def nose_badge(windows, x=308, y=36, label_in="Nase ein", label_out="Nase aus"):
    """windows: [(t0, t1, "in"|"out"), ...]. Kleines Badge: Nasen-Profil,
    Luftstrom-Striche (laufen zur Nase hin bzw. weg) und Text."""
    w, h = 84, 22
    out = [Prim("rect", {"x": x, "y": y, "width": w, "height": h, "rx": 11, "fill": "#0b1220",
                         "opacity": 0.7, "stroke": "#334155", "stroke-width": 1})]
    nx, ny = x + 22, y + 4
    # Nasenprofil (blickt nach links): Stirn -> Nasenspitze -> Nasenloch
    out.append(Prim("path", {"d": f"M{nx} {ny}L{nx - 6} {ny + 10}L{nx - 1} {ny + 12}",
                             "fill": "none", "stroke": HEAD, "stroke-width": 1.8,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}))
    for t0, t1, kind in windows:
        sign = 1 if kind == "in" else -1
        # Luftstrom: zwei kurze Striche links der Nase, Dashes wandern
        for k, dy in enumerate((ny + 9, ny + 13)):
            p = Prim("line", {"x1": x + 5, "y1": dy, "x2": nx - 7, "y2": dy, "stroke": GOOD if kind == "in" else MUTED,
                              "stroke-width": 1.6, "stroke-linecap": "round", "stroke-dasharray": "2 3",
                              "_show": [(t0, t1)]},
                     lambda c, s=sign: {"stroke-dashoffset": round(-s * (c["t"] * 14) % 5, 1)})
            out.append(p)
        out.append(Prim("text", {"x": x + 56, "y": y + 15, "font-size": 11, "fill": GOOD if kind == "in" else TEXT,
                                 "text-anchor": "middle", "font-weight": "600", "_show": [(t0, t1)]},
                        text=label_in if kind == "in" else label_out))
    return out


def nose_note(x=350, y=72, text="100 % Nase"):
    return Prim("text", {"x": x, "y": y, "font-size": 10, "fill": MUTED, "text-anchor": "middle"}, text=text)


# --------------------------------------------------------------------------
# Draufsicht-Inset
# --------------------------------------------------------------------------

def top_inset(cx, cy, r, get, label="von oben", arms=None):
    """get(pose) -> (hip_yaw_deg, shoulder_yaw_deg). Gesicht zum Betrachter =
    nach unten im Inset. arms(pose) optional -> [(lat, fwd) Hand L, Hand R]
    in Körperkoordinaten (relativ zur Schultermitte, Rumpfdrehung eingerechnet)."""
    out = [Prim("circle", {"cx": cx, "cy": cy, "r": r, "fill": "#0b1220", "opacity": 0.55,
                           "stroke": "#334155", "stroke-width": 1}),
           Prim("text", {"x": cx, "y": cy - r - 5, "font-size": 10, "fill": MUTED, "text-anchor": "middle"},
                text=label),
           # Betrachter-Richtung
           Prim("path", {"d": f"M{cx - 4} {cy + r - 2}L{cx} {cy + r + 3}L{cx + 4} {cy + r - 2}",
                         "fill": "none", "stroke": "#334155", "stroke-width": 1.2})]

    def bar(half, which, color, width):
        def f(c):
            yaw = math.radians(get(c["pose"])[which])
            dx, dy = half * math.cos(yaw), -half * math.sin(yaw)
            return {"x1": cx - dx, "y1": cy - dy, "x2": cx + dx, "y2": cy + dy}
        return Prim("line", {"stroke": color, "stroke-width": width, "stroke-linecap": "round"}, f)

    def nose_tick(which, color, rr):
        def f(c):
            yaw = math.radians(get(c["pose"])[which])
            fx, fy = math.sin(yaw), math.cos(yaw)
            return {"cx": cx + fx * rr, "cy": cy + fy * rr}
        return Prim("circle", {"r": 2.6, "fill": color}, f)

    out.append(bar(r * 0.5, 0, NEAR, 5))
    if arms is not None:
        def arm_line(i):
            def f(c):
                pose = c["pose"]
                yaw = math.radians(get(pose)[1])
                sh = (-1 if i == 0 else 1) * r * 0.62
                sx, sy = cx + sh * math.cos(yaw), cy - sh * math.sin(yaw)
                lat, fwd = arms(pose)[i]
                k = r * 0.62 / 24.0
                return {"x1": sx, "y1": sy, "x2": cx + lat * k, "y2": cy + fwd * k}
            return Prim("line", {"stroke": HEAD, "stroke-width": 3, "stroke-linecap": "round", "opacity": 0.9}, f)
        out += [arm_line(0), arm_line(1)]
    out.append(bar(r * 0.62, 1, TORSO, 6))
    out.append(Prim("circle", {"cx": cx, "cy": cy, "r": 5, "fill": HEAD, "stroke": SKIN_LINE, "stroke-width": 1}))
    out.append(nose_tick(1, ACCENT, 8))
    return out


# --------------------------------------------------------------------------
# Frontfigur mit 3D-Projektion
# --------------------------------------------------------------------------

def rot_y(lat, fwd, yaw_deg):
    """Drehung um die Hochachse. yaw > 0: Front dreht zur rechten Bildseite.
    Liefert (screen_dx, z) mit z > 0 = zum Betrachter."""
    a = math.radians(yaw_deg)
    return lat * math.cos(a) + fwd * math.sin(a), -lat * math.sin(a) + fwd * math.cos(a)


def arm_dir(side, ab, fl):
    """Richtung (lat, up, fwd) eines Armsegments. side=-1 links (Bild), +1 rechts.
    ab: Abduktion aus der Hängeposition (0 hängt, 90 waagrecht seitlich),
    fl: Schwenk um die Hochachse nach vorn (90 = gerade nach vorn, >90 kreuzt
    vor dem Körper, <0 nach hinten)."""
    a, f = math.radians(ab), math.radians(fl)
    return side * math.sin(a) * math.cos(f), -math.cos(a), math.sin(a) * math.sin(f)


def ik3(H, A, l1, l2, fwd):
    """Knie zwischen Hüfte H und Knöchel A (3D, y nach unten), Knick in fwd."""
    d = [A[i] - H[i] for i in range(3)]
    dist = max(1e-6, math.sqrt(sum(v * v for v in d)))
    dist_c = min(dist, l1 + l2 - 1e-3)
    u = [v / dist for v in d]
    along = (l1 * l1 - l2 * l2 + dist_c * dist_c) / (2 * dist_c)
    hh = math.sqrt(max(0.0, l1 * l1 - along * along))
    dot = sum(fwd[i] * u[i] for i in range(3))
    fp = [fwd[i] - dot * u[i] for i in range(3)]
    n = math.sqrt(sum(v * v for v in fp)) or 1.0
    fp = [v / n for v in fp]
    return tuple(H[i] + u[i] * along + fp[i] * hh for i in range(3))


class Front3D:
    """Frontfigur, die Rumpfdrehung zeigen kann.

    Pose-Skalare:
      x, y        Becken (Bildschirm)
      hy          Becken-/Beindrehung (Grad, >0 Front zur rechten Bildseite)
      sy          Schulterdrehung (absolut, Grad)
      turn        Kopf (wie head_front, -1..1); wird sonst aus sy abgeleitet
      ankL_x, ankR_x, ank_y   Knöchelpositionen (Bildschirm)
      Arme: abL1, flL1 (Oberarm), abL2, flL2 (Unterarm+Hand), ebenso R.
            Winkel relativ zum Rumpf (Schulterdrehung wird addiert).
      shrug       Schultern heben (px, >0 hoch)
    """

    UA, FA, HA = 36.0, 32.0, 13.0
    TH, SH = 50.0, 48.0

    def __init__(self, scale=1.0):
        self.scale = scale

    # --- Geometrie --------------------------------------------------------
    def geo(self, pose):
        P = FRONT.fk(pose)
        x, y = pose.get("x", 200.0), pose.get("y", 150.0)
        hy, sy = pose.get("hy", 0.0), pose.get("sy", 0.0)
        g = {"P": P}
        chest = pt(P, "chest")
        g["chest"] = chest
        g["neck"] = pt(P, "neck")
        g["pelvis"] = (x, y)
        g["mid"] = pt(P, "thorax")
        sh_y = chest[1] + 2 - pose.get("shrug", 0.0)
        for side, key in ((-1, "L"), (1, "R")):
            dx, z = rot_y(side * 24.0, 0.0, sy)
            S = (chest[0] + dx, sh_y, z)
            g["sh" + key] = S
            pts = [S]
            cur = S
            for seg, (ab, fl), ln in (
                    ("u", (pose.get("ab%s1" % key, 0.0), pose.get("fl%s1" % key, 0.0)), self.UA),
                    ("f", (pose.get("ab%s2" % key, 0.0), pose.get("fl%s2" % key, 0.0)), self.FA + self.HA)):
                lat, up, fwd = arm_dir(side, ab, fl)
                sdx, sz = rot_y(lat, fwd, sy)
                cur = (cur[0] + sdx * ln, cur[1] - up * ln, cur[2] + sz * ln)
                pts.append(cur)
            g["arm" + key] = pts
            # Hüfte / Bein
            hdx, hz = rot_y(side * 15.0, 0.0, hy)
            Hp = (x + hdx, y + 2, hz)
            ax = pose.get("ank%s_x" % key, x + side * 15.0)
            ay = pose.get("ank_y", y + 96.0)
            A = (ax, ay, pose.get("ank%s_z" % key, hz))
            fdx, fz = rot_y(0.0, 1.0, hy + side * pose.get("toe_out", 8.0))
            K = ik3(Hp, A, self.TH, self.SH, (fdx, 0.0, fz))
            g["leg" + key] = [Hp, K, A]
            toe_len = 13.0
            g["foot" + key] = [(A[0], A[1] + 3, A[2]),
                               (A[0] + fdx * toe_len + side * 2, A[1] + 6 + 3 * (1 - abs(fz)), A[2] + fz * toe_len)]
            g["hip" + key] = Hp
        return g

    # --- Zeichnen ---------------------------------------------------------
    @staticmethod
    def _stroke(fn, width, color, outline=True, extra=None):
        out = []
        def d(c):
            r = {"d": smooth_path([(p[0], p[1]) for p in fn(c)])}
            if extra:
                r.update(extra(c))
            return r
        if outline:
            def d2(c):
                r = {"d": smooth_path([(p[0], p[1]) for p in fn(c)])}
                if extra:
                    r.update(extra(c))
                return r
            out.append(Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-width": width + 3,
                                     "stroke-linecap": "round", "stroke-linejoin": "round"}, d2))
        out.append(Prim("path", {"fill": "none", "stroke": color, "stroke-width": width,
                                 "stroke-linecap": "round", "stroke-linejoin": "round"}, d))
        return out

    def _arm_layer(self, key, front, color, rank=None):
        """Arm, sichtbar nur wenn er vor (front=True) bzw. hinter dem Rumpf ist.
        rank: None oder (topkey, wanted) – Pose-Skalar entscheidet, welcher Arm
        beim Kreuzen oben liegt."""
        def vis(c):
            pts = self.geo(c["pose"])["arm" + key]
            z = (pts[1][2] + 2 * pts[2][2]) / 3
            on = (z > 0) == front
            if on and rank is not None:
                on = (c["pose"].get(rank[0], 0.0) > 0.5) == rank[1]
            return {"opacity": 1 if on else 0}
        return self._stroke(lambda c: self.geo(c["pose"])["arm" + key], 13, color, extra=vis)

    def prims(self, arm_color_L=NEAR, arm_color_R=NEAR, cross_rank=False, marks=True):
        out = []
        # Arme hinter dem Rumpf
        out += self._arm_layer("L", False, FAR)
        out += self._arm_layer("R", False, FAR)
        # Beine (Fuß dahinter, dann Bein)
        for key in ("L", "R"):
            out += self._stroke(lambda c, k=key: self.geo(c["pose"])["foot" + k], 11, NEAR)
            out += self._stroke(lambda c, k=key: self.geo(c["pose"])["leg" + k], 16, NEAR)
        # Becken
        def pelvis(c):
            g = self.geo(c["pose"])
            return [g["hipL"], g["pelvis"], g["hipR"]]
        out += self._stroke(pelvis, 22, TORSO)
        # Hals, Rumpf
        out += self._stroke(lambda c: [self.geo(c["pose"])["chest"], self.geo(c["pose"])["neck"]], 13, TORSO)

        def trunk(c):
            g = self.geo(c["pose"])
            px, py = g["pelvis"]
            return [(px, py - 6), g["mid"], (g["chest"][0], g["chest"][1] + 6)]

        def trunk_w(c):
            sy = math.radians(c["pose"].get("sy", 0.0))
            return {"stroke-width": round(40 - 6 * abs(math.sin(sy)), 1)}

        def trunk_w_o(c):
            sy = math.radians(c["pose"].get("sy", 0.0))
            return {"stroke-width": round(43 - 6 * abs(math.sin(sy)), 1)}

        def shoulders(c):
            g = self.geo(c["pose"])
            return [g["shL"], (g["chest"][0], g["shL"][1]), g["shR"]]

        sh = self._stroke(shoulders, 22, TORSO)
        tr_o = Prim("path", {"fill": "none", "stroke": SKIN_LINE, "stroke-linecap": "round"},
                    lambda c: {"d": smooth_path([(p[0], p[1]) for p in trunk(c)]), **trunk_w_o(c)})
        tr = Prim("path", {"fill": "none", "stroke": TORSO, "stroke-linecap": "round"},
                  lambda c: {"d": smooth_path([(p[0], p[1]) for p in trunk(c)]), **trunk_w(c)})
        out += [sh[0], tr_o, sh[1], tr]
        if marks:
            # Brustbein-Linie wandert mit der Schulterdrehung -> zeigt Drehrichtung
            def sternum(c):
                g = self.geo(c["pose"])
                s = math.sin(math.radians(c["pose"].get("sy", 0.0)))
                cx = g["chest"][0] + 16 * s
                return {"d": f"M{cx:.1f} {g['chest'][1] + 6:.1f}L{g['mid'][0] + 14 * s:.1f} {g['mid'][1] + 4:.1f}"}
            out.append(Prim("path", {"fill": "none", "stroke": "#6366f1", "stroke-width": 3,
                                     "stroke-linecap": "round"}, sternum))
            # Gürtellinie + Nabel: zeigt Beckendrehung
            def belt(c):
                g = self.geo(c["pose"])
                (lx, ly, _), (rx, ry, _) = g["hipL"], g["hipR"]
                return {"d": f"M{lx:.1f} {ly - 9:.1f}L{rx:.1f} {ry - 9:.1f}"}
            out.append(Prim("path", {"fill": "none", "stroke": "#4f46e5", "stroke-width": 3,
                                     "stroke-linecap": "round"}, belt))

            def navel(c):
                g = self.geo(c["pose"])
                s = math.sin(math.radians(c["pose"].get("hy", 0.0)))
                return {"cx": g["pelvis"][0] + 14 * s, "cy": g["pelvis"][1] - 17}
            out.append(Prim("circle", {"r": 2.2, "fill": SKIN_LINE}, navel))
        out += head_front()
        # Arme vor dem Rumpf
        if cross_rank:
            out += self._arm_layer("L", True, arm_color_L, rank=("topL", False))
            out += self._arm_layer("R", True, arm_color_R, rank=("topL", True))
            out += self._arm_layer("L", True, arm_color_L, rank=("topL", True))
            out += self._arm_layer("R", True, arm_color_R, rank=("topL", False))
        else:
            out += self._arm_layer("L", True, arm_color_L)
            out += self._arm_layer("R", True, arm_color_R)
        return out


def shadow(get_x, get_scale, y, rx=34, ry=5):
    """Bodenschatten (schrumpft beim Abheben)."""
    return Prim("ellipse", {"cy": y, "ry": ry, "fill": "#000", "opacity": 0.28},
                lambda c: {"cx": get_x(c), "rx": round(rx * get_scale(c), 1)})
