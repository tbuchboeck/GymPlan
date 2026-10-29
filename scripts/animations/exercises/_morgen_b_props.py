"""Helfer für die @morgen-Übungen dead_arms, golferswings, standard_march,
ballet_squat, horse_stance. Unterstrich: build.py lädt diese Datei nicht."""
from rig import *


def anim(attr, values, dur, keytimes=None, **extra):
    """Eigenständige SMIL-Animation (unabhängig von der Haupt-Timeline)."""
    a = {"attributeName": attr, "values": values, "dur": f"{dur}s", "repeatCount": "indefinite"}
    if keytimes:
        a["keyTimes"] = keytimes
    a.update(extra)
    return Prim("animate", a)


def nose_hint(x=330, y=36, dur=4.0):
    """Dezentes Pill-Badge: Nasenprofil, Luftpunkte strömen im ruhigen
    Atemrhythmus (eigener 4-s-Takt) zur Nase und wieder hinaus, Text „Nase“."""
    w, h = 62, 20
    out = [Prim("rect", {"x": x, "y": y, "width": w, "height": h, "rx": 10, "fill": "#0b1220",
                         "opacity": 0.7, "stroke": "#334155", "stroke-width": 1})]
    nx, ny = x + 20, y + 4          # Stirnpunkt; Profil blickt nach links
    out.append(Prim("path", {"d": f"M{nx} {ny}L{nx - 6} {ny + 9}L{nx - 1} {ny + 11}",
                             "fill": "none", "stroke": HEAD, "stroke-width": 1.8,
                             "stroke-linecap": "round", "stroke-linejoin": "round"}))
    for i in range(3):
        x0, x1 = x + 5, nx - 6
        yy = ny + 10.5
        b = f"{i * 0.22:.2f}s"
        out.append(Prim("circle", {"cx": x0, "cy": yy, "r": 1.3, "fill": GOOD, "opacity": 0}, children=[
            anim("cx", f"{x0};{x1};{x1};{x0};{x0}", dur, "0;0.4;0.5;0.9;1", begin=b),
            anim("opacity", "0;0.9;0;0.6;0", dur, "0;0.38;0.5;0.8;1", begin=b),
        ]))
    out.append(Prim("text", {"x": x + 42, "y": y + 14, "font-size": 11, "fill": GOOD, "font-weight": "600",
                             "text-anchor": "middle"}, text="Nase"))
    return Prim("g", {"opacity": 0.95}, children=out)


def label(text, x, y, t0, t1, size=12, color=ACCENT, anchor="middle"):
    return Prim("text", {"x": x, "y": y, "font-size": size, "fill": color, "font-weight": "500",
                         "text-anchor": anchor, "_show": [(t0, t1)]}, text=text)


def front_feet_out(out_deg=0.0, color=NEAR, lift=None):
    """Füße in Frontansicht als flache Ovale unter dem Knöchel. out_deg dreht
    sie nach außen (breiter, seitlich versetzt). lift(side, c) -> 0..1 stellt
    den Fuß auf die Zehen (Oval wird schmaler/höher)."""
    k = math.sin(math.radians(out_deg))

    def foot(side, pad):
        sgn = -1 if side == "L" else 1

        def f(c):
            x, y = pt(c["P"], f"shin_{side}")
            l = lift(side, c) if lift else 0.0
            return {"cx": x + sgn * 7 * k, "cy": y + 6 + 2 * l,
                    "rx": round(7 + 7 * k - 2 * l + pad, 1), "ry": round(4.5 + 1.5 * l + pad, 1)}
        return f
    out = []
    for s in ("L", "R"):
        out.append(Prim("ellipse", {"fill": SKIN_LINE}, foot(s, 1.5)))
        out.append(Prim("ellipse", {"fill": color}, foot(s, 0)))
    return out
