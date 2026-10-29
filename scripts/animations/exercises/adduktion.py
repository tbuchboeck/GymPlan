from rig import *
from exercises._gymgeraete_hip import build_hip

SLUG = "adduktion"

# Frontansicht, sitzend. Polster innen an den Knien; die Hebelarme drehen um
# Achsen unter dem Sitz, Fußstützen laufen mit. Oberschenkel sind per
# 3D-Projektion verkürzt (sie zeigen zum Betrachter). Gesäß bleibt auf dem
# Sitz, Hände an den Seitengriffen.


def build():
    return build_hip(True, "Adduktionsmaschine")
