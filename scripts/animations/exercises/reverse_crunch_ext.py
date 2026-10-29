from rig import *
from exercises._bauch_props import (FLOOR_Y, PRONE, PinTimeline, figure, forearm_iks, legs_sharp,
                                    mat_layer, prone_shoulder, stage)

SLUG = "reverse-crunch-extended"

# Bauchlage, auf die Unterarme gestützt (Ellbogen seitlich unter den Schultern).
# Knie angewinkelt unter den Bauch ziehen – Becken hebt sich, Rücken rundet –
# dann die Beine lang nach hinten strecken und gestreckt ablegen.
SH = prone_shoulder()

# Beine über Weltwinkel (thigh@/shin@). Die Beckenhöhe wird pro Frame so weit
# angehoben, dass Knie und Sprunggelenke nie in die Matte tauchen – beim
# Durchschwingen unter den Bauch hebt sich das Becken also kurz höher.
LIE = dict(y=PRONE["y"], rot=-90, lumbar=PRONE["lumbar"], thorax=PRONE["thorax"], chest=PRONE["chest"],
           neck=-12, head=-2,
           **{"thigh_n@": 183, "shin_n@": 182, "foot_n@": 204,
              "thigh_f@": 183, "shin_f@": 182, "foot_f@": 204})
TUCK = dict(LIE, y=FLOOR_Y - 56, lumbar=-22, thorax=-8, chest=4, neck=14, head=2,
            **{"thigh_n@": 302, "shin_n@": 186, "foot_n@": 210,
               "thigh_f@": 298, "shin_f@": 184, "foot_f@": 210})
PLANK = dict(LIE, y=FLOOR_Y - 32, lumbar=0, thorax=0, chest=0, neck=-6, head=-4,
             **{"thigh_n@": 190, "shin_n@": 190, "foot_n@": 232,
                "thigh_f@": 190, "shin_f@": 190, "foot_f@": 232})

KNEE_MIN = FLOOR_Y - 11   # Kniemitte (Radius ~8) bleibt über der Matte
ANKLE_MIN = FLOOR_Y - 8


class ClearTimeline(PinTimeline):
    def _interp(self, t):
        p = super()._interp(t)
        y = p["y"]
        for side in ("n", "f"):
            a = math.radians(p[f"thigh_{side}@"])
            b = math.radians(p[f"shin_{side}@"])
            y = min(y, KNEE_MIN + 50 * math.sin(a), ANKLE_MIN + 50 * math.sin(a) + 48 * math.sin(b))
        if y < p["y"]:
            # Rücken beim Hochkommen etwas mitrunden
            k = min(1.0, (p["y"] - y) / 12)
            p["lumbar"] = p.get("lumbar", 0) - 6 * k
        p["y"] = y
        return p


def build():
    keys = [(0, LIE), (0.8, LIE), (2.2, TUCK), (2.9, TUCK), (4.0, PLANK), (4.4, PLANK),
            (5.8, LIE), (6.4, LIE)]
    tl = ClearTimeline(keys, SH, iks=forearm_iks())
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
        static_text("Ellbogen unter den Schultern – Kraft aus dem Bauch", 200, 24, LEAD_SIZE, MUTED),
    ]
    return render(prims, tl, SIDE, title="Reverse Crunch (gestreckt)")
