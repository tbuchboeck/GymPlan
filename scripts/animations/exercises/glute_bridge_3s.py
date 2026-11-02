"""Glute Bridge mit 3 s Halten (für „Morgen im Bett“ und „Rücken akut“)."""
from exercises import glute_bridge

SLUG = "glute-bridge-3s"


def build():
    return glute_bridge.build(hold=3, slug_title="Bridge")
