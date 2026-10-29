"""Nerve Glide Medianus – Frontansicht, Nahansicht Oberkörper.

Gezeigt am anatomisch rechten Arm (_L = linke Bildschirmseite).
Helfer (Hand, Nerv, verkürzbares Skelett) aus ulnaris_glide.py.
"""
import math

from rig import *
from exercises.ulnaris_glide import (SK, BASE, MapTimeline, lerp, upper_body, captions2, limb,
                                     TOP_HINT, NERVE)

SLUG = "medianus-glide"


def median_map(p):
    """m=0: Ellbogen gebeugt, Hand neben dem Ohr, Handfläche zum Ohr.
    m=1: Ellbogen gestreckt, Handgelenk nach hinten gekippt (Finger zeigen
    nach außen-unten). tilt: +1 = Kopf zur selben Seite (Bildschirm-links)."""
    m, tilt = p.get("m", 0.0), p.get("tilt", 0.0)
    w = m ** 1.6                          # Handgelenk kippt erst gegen Ende
    q = dict(p)
    q.update(
        upperarm_L=-90 + 2 * (1 - m), len_upperarm_L=lerp(0.86, 1, m),
        forearm_L=lerp(-118, 0, m), len_forearm_L=lerp(0.8, 1, m),
        hand_L=lerp(30, 64, w),
        neck=13 * tilt, head=8 * tilt,
        h_pw=lerp(6, 10, m), h_fang=lerp(0, 12, w), h_flen=1, h_plen=1,
        h_th=lerp(-35, -40, m), h_tlen=lerp(0.55, 0.7, m), ring=0,
        glide=0.5 * (2 * m - 1) + 0.5 * tilt,
    )
    return q


START = dict(BASE, m=0, tilt=0)        # gebeugt, Kopf neutral
EXT = dict(BASE, m=1, tilt=1)          # gestreckt, Kopf zur selben Seite
FLEX_OPP = dict(BASE, m=0, tilt=-1)    # gebeugt, Kopf zur Gegenseite


def build():
    T = [0, 1.9, 3.8, 5.7, 7.6]
    tl = MapTimeline([(T[0], START), (T[1], EXT), (T[2], FLEX_OPP), (T[3], EXT), (T[4], START)],
                     median_map, SK)
    to_ext = [(T[0], T[1]), (T[2], T[3])]
    to_flex = [(T[1], T[2]), (T[3], T[4])]
    arrows = [
        arrow("M140 64Q100 62 92 102", width=2, show=to_ext),
        arrow("M98 104Q104 68 138 64", width=2, show=to_flex),
        arrow("M214 64Q202 56 188 61", width=2, show=to_ext),
        arrow("M186 64Q198 56 212 61", width=2, show=to_flex),
    ]
    fig = group([ghost(limb(["upperarm_L", "forearm_L"], 13, NEAR), SK, median_map(START), 0.14)]
                + upper_body("L") + arrows,
                scale=1.5, origin=(200, 120), dx=45, dy=8)
    fig.attrs["clip-path"] = "url(#clipM)"
    label = [
        Prim("line", {"x1": 40, "y1": 196, "x2": 54, "y2": 196, "stroke": NERVE, "stroke-width": 2,
                      "stroke-dasharray": "3 3"}),
        static_text("Nerv gleitet", 60, 200, 10.5, NERVE, anchor="start"),
        static_text("Arm und Kopf", 78, 218, 11, MUTED),
        static_text("bewegen sich gegengleich", 78, 232, 11, MUTED),
    ]
    prims = [fig, *label, caption_band(),
             *captions2([
                 ("Ellbogen strecken, Handgelenk nach hinten", "gleichzeitig Kopf zur selben Seite neigen", T[0], T[1]),
                 ("Ellbogen beugen, Handfläche zum Ohr", "Kopf zur Gegenseite neigen", T[1], T[2]),
                 ("Strecken – Handgelenk kippt nach hinten", "Kopf zur selben Seite · rhythmisch, nie halten", T[2], T[3]),
                 ("Beugen, Kopf zurück zur Mitte", "nur leichter Zug, nie Schmerz", T[3], T[4]),
             ]),
             static_text(TOP_HINT, 200, 24, 13, MUTED)]
    clip = '<clipPath id="clipM"><rect x="0" y="0" width="400" height="258"/></clipPath>'
    return render(prims, tl, SK, fps=12, title="Nerve Glide Medianus", extra_defs=clip)
