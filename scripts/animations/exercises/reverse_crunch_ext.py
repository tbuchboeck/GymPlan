from rig import *
from exercises._bauch_props import (FLOOR_Y, PRONE, PinTimeline, apply_abs, pin_pose, figure, forearm_iks, legs_sharp,
                                    mat_layer, prone_shoulder, stage)

SLUG = "reverse-crunch-extended"

# Bauchlage, auf die Unterarme gestützt (Ellbogen seitlich unter den Schultern).
# Knie angewinkelt unter den Bauch ziehen – Becken hebt sich, Rücken rundet –
# dann die Beine lang nach hinten strecken und gestreckt ablegen.
SH = prone_shoulder()

# Sprunggelenk (ax, ay) wird per IK gehalten: Füße gleiten knapp über/auf der
# Matte, statt beim Anziehen durch den Boden zu schwingen.
LIE = dict(y=PRONE["y"], rot=-90, lumbar=PRONE["lumbar"], thorax=PRONE["thorax"], chest=PRONE["chest"],
           neck=-12, head=-2, ax=78, ay=223, af=74, ay_f=223,
           **{"foot_n@": 204, "foot_f@": 204})
TUCK = dict(LIE, y=FLOOR_Y - 56, lumbar=-22, thorax=-8, chest=4, neck=-8, head=-4,
            ax=150, ay=225, af=145, ay_f=225, **{"foot_n@": 208, "foot_f@": 208})
RISE = dict(LIE, y=FLOOR_Y - 44, lumbar=-10, thorax=0, chest=6, neck=-12, head=-3,
            ax=96, ay=223, af=92, ay_f=223, **{"foot_n@": 206, "foot_f@": 206})
PLANK = dict(LIE, y=FLOOR_Y - 32, lumbar=0, thorax=0, chest=0, neck=-6, head=-4,
             ax=74, ay=219, af=72, ay_f=219, **{"foot_n@": 232, "foot_f@": 232})


def leg_iks():
    return [IK("thigh_n", "shin_n", lambda p: (p["ax"], p["ay"]), bend=1),
            IK("thigh_f", "shin_f", lambda p: (p["af"], p["ay_f"]), bend=1)]


class KneeClearTimeline(PinTimeline):
    """Hebt die Sprunggelenke (ay) gerade so weit an, dass die Knie beim
    Anziehen/Strecken nicht in die Matte tauchen."""
    KNEE_MIN = FLOOR_Y - 11   # Kniemitte mindestens so hoch (Radius ~8)

    def at(self, t):
        over = {}
        pose = self.at_with(over, t)
        for side, key in (("n", "ay"), ("f", "ay_f")):
            if pt(SIDE.fk(pose), f"thigh_{side}")[1] <= self.KNEE_MIN:
                continue
            base = self._interp(t)[key]
            lo, hi = base - 70, base       # lo: sicher hoch genug, hi: zu tief
            for _ in range(22):
                mid = (lo + hi) / 2
                trial = self.at_with(dict(over, **{key: mid}), t)
                if pt(SIDE.fk(trial), f"thigh_{side}")[1] > self.KNEE_MIN:
                    hi = mid
                else:
                    lo = mid
            over[key] = lo
            pose = self.at_with(over, t)
        return pose

    def at_with(self, override, t):
        pose = self._interp(t)
        pose.update(override)
        pose = pin_pose(self.skeleton, pose, self.pin, self.joint)
        pose = apply_abs(self.skeleton, pose)
        for ik in self.iks:
            pose = solve_ik(self.skeleton, pose, ik)
        return apply_abs(self.skeleton, pose)


def build():
    keys = [(0, LIE), (0.8, LIE), (1.5, RISE), (2.2, TUCK), (2.9, TUCK), (4.0, PLANK), (4.4, PLANK),
            (5.8, LIE), (6.4, LIE)]
    tl = KneeClearTimeline(keys, SH, iks=forearm_iks() + leg_iks())
    s0 = tl.at(0)
    prims = [
        *stage([
            *mat_layer(),
            ghost(legs_sharp(), SIDE, s0, 0.15),
            *figure(),
            focus("lumbar", rx=20, ry=8, offset=(0, 13), show=[(0.8, 4.4)]),
            arrow("M62 200 Q100 186 138 196", show=[(0.8, 2.2)]),
            arrow("M120 194 Q86 184 56 198", show=[(2.9, 4.0)]),
            arrow("M140 176 Q146 190 140 204", show=[(4.4, 5.8)]),
        ]),
        caption_band(),
        caption("Unterarme stützen, Beine lang", 0, 0.8),
        caption("Ausatmen – Knie unter den Bauch ziehen", 0.8, 2.2),
        caption("Rücken rund – Bauch fest", 2.2, 2.9),
        caption("Beine lang nach hinten strecken", 2.9, 4.4),
        caption("Gestreckt langsam ablegen", 4.4, 6.4),
        static_text("Ellbogen unter den Schultern – Kraft aus dem Bauch", 200, 24, 13, MUTED),
    ]
    return render(prims, tl, SIDE, title="Reverse Crunch (gestreckt)")
