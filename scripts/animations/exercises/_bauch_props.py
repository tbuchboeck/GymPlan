"""Gemeinsame Helfer für die Bodenübungen aus homeWorkoutPlan2 (Bauch, Matte).

Kein eigenes Übungsmodul (Unterstrich) – build.py lädt diese Datei nicht.
Enthält: Mattenhöhe, Bauchlage-Grundpose (Unterarmstütz), Arm-IKs, Kopf
von oben (Draufsicht) und einen Bein-Zeichner mit Verkürzung.
"""
from rig import *

FLOOR_Y = 234           # Oberkante der Matte
MAT_X0, MAT_X1 = 34, 366

# Bauchlage, Kopf rechts, Oberkörper auf die Unterarme gestützt (Sphinx).
# Becken liegt, Beine lang, Zehen gestreckt.
PRONE = dict(x=176, y=FLOOR_Y - 15, rot=-90,
             lumbar=9, thorax=13, chest=10, neck=-12, head=-2,
             thigh_n=3, shin_n=-1, foot_n=-68,
             thigh_f=3, shin_f=-1, foot_f=-68)


def prone_shoulder(pose=PRONE):
    P = SIDE.fk(pose)
    return pt(P, "chest")


def forearm_iks(wrist=None, dx_far=-5):
    """Unterarme flach auf der Matte, Ellbogen unter der Schulter.
    wrist: Handgelenk der nahen Seite (fix)."""
    if wrist is None:
        sx, _ = prone_shoulder()
        wrist = (sx + 33, FLOOR_Y - 6)
    wf = (wrist[0] + dx_far, wrist[1])
    return [
        IK("upperarm_n", "forearm_n", wrist, bend=-1, end_seg="hand_n", end_abs=-4),
        IK("upperarm_f", "forearm_f", wf, bend=-1, end_seg="hand_f", end_abs=-4),
    ]


SCALE = 1.2
ORIGIN = (200, FLOOR_Y + 3)


def mat_layer(x0=60, x1=342):
    """Matte (wird mit der Figur skaliert)."""
    return [mat(FLOOR_Y, x0, x1)]


def stage(children, scale=SCALE):
    """Figur + Matte etwas größer, Mattenoberkante bleibt auf FLOOR_Y."""
    return [floor(FLOOR_Y + 10, 16, 384), group(children, scale=scale, origin=ORIGIN)]


def elbow_pad(x, w=26):
    """Kleine Polsterkante unter den Ellbogen – zeigt den Stützpunkt."""
    return Prim("ellipse", {"cx": x, "cy": FLOOR_Y + 1, "rx": w / 2, "ry": 3, "fill": PROP, "opacity": 0.8})


def hip_line(color=GOOD):
    """Gestrichelte Linie: Becken bleibt auf der Matte."""
    return Prim("line", {"stroke": color, "stroke-width": 1.5, "stroke-dasharray": "4 4", "opacity": 0.7},
                lambda c: (lambda x, y: {"x1": x - 26, "y1": FLOOR_Y + 3, "x2": x + 26, "y2": FLOOR_Y + 3})(
                    *pt(c["P"], "root", end=False)))


class PinTimeline(Timeline):
    """Timeline, die vor den IKs die Schulter (Ende von `joint`) auf einem
    festen Punkt hält: Pose gibt die Beckenhöhe `y` und die Krümmung vor,
    `rot` und `x` werden so gelöst, dass die Schulter exakt auf `pin` liegt.
    (rig.Anchor dreht nur, hält aber den Abstand nicht.)"""

    def __init__(self, keys, pin, joint="chest", iks=None, skeleton=SIDE):
        super().__init__(keys, iks=iks or [], skeleton=skeleton)
        self.pin = pin
        self.joint = joint

    def at(self, t):
        pose = self._interp(t)
        if self.pin is not None:
            pose = pin_pose(self.skeleton, pose, self.pin, self.joint)
        pose = apply_abs(self.skeleton, pose)
        for ik in self.iks:
            pose = solve_anchor(self.skeleton, pose, ik) if isinstance(ik, Anchor) else solve_ik(self.skeleton, pose, ik)
        return pose


def pin_pose(skel, pose, pin, joint="chest"):
    q = dict(pose, x=0.0, y=0.0, rot=0.0)
    P = skel.fk(q)
    vx, vy = P[joint][2], P[joint][3]
    L = math.hypot(vx, vy)
    phi = math.degrees(math.atan2(-vy, vx))
    # gesucht: rot, sodass pin_y - y_root = -L*sin(phi+rot)
    s = max(-1.0, min(1.0, -(pin[1] - pose.get("y", 0.0)) / L))
    base = math.degrees(math.asin(s))
    # zwei Lösungen; nimm die, die näher an der gewünschten rot liegt
    want = pose.get("rot", 0.0)
    cands = [base - phi, 180 - base - phi]
    rot = min(cands, key=lambda r: abs(((r - want + 180) % 360) - 180))
    a = math.radians(phi + rot)
    out = dict(pose)
    out["rot"] = rot
    out["x"] = pin[0] - L * math.cos(a)
    return out


def apply_abs(skel, pose):
    """Schlüssel "<segment>@" = absoluter Weltwinkel dieses Segments (statt
    relativ). Praktisch für Beine, wenn sich das Becken mitdreht."""
    if not any(k.endswith("@") for k in pose):
        return pose
    out = dict(pose)
    for s in skel.segs:
        k = s.name + "@"
        if k in out:
            P = skel.fk(out)
            if s.parent is None:
                pa = out.get("rot", 0.0)
            else:
                pa = P[s.parent][4]
            out[s.name] = out[k] - pa - s.rest
    return out
