"""Efectos de la plantilla. Significados fijos en engine/audio/sfxlib.py (docstring) y docs/AUDIO.md.
S[id] = segundo de inicio de cada escena (de video.json). Los tiempos de la cámara están en compositions/*.html:
el whoosh va en el PICO de velocidad del movimiento, no al empezar."""
from sfxlib import *


def build(T, S, lib=None):
    T.ambient(0, lvl=0.05)                                   # base: que nunca suene vacío
    # gancho: golpe de apertura con el aterrizaje de la cámara; zoom through al final
    T.put(0.0, boom(), 0.8); T.put(0.05, pop(1100), 0.35)
    T.put(S['explica'] - 0.35, whoosh(0.45), 0.6)              # pico del zoom through (cam.ir 2.85 → 3.45)
    # explica: un pop por estación cuando aparece; whoosh en cada viaje de cámara
    t = S['explica']
    T.put(t + 0.3, pop(1000), 0.35)
    T.put(t + 3.1, whoosh(0.4), 0.45)                          # viaje a la estación 2 (2.6 → 3.6, pico ~3.1)
    T.put(t + 3.05, pop(1150), 0.35)
    T.put(t + 5.7, whoosh(0.4), 0.45)                          # viaje a la terminal (5.2 → 6.2)
    T.typing(t + 5.45, 17)
    T.put(t + 5.95, ding(1760, 0.4), 0.3)                      # ✓ resultado correcto
    # cierre: succión → golpe → firma
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t, impact(), 0.55)
    T.put(t + 0.9, sparkle(9), 0.4)
