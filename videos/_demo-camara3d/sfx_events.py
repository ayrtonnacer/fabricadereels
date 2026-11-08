"""Efectos de la demo de cámara 3D: el sonido sigue a la cámara (whoosh en el pico de cada movimiento rápido)."""
from sfxlib import *


def build(T, S, lib=None):
    T.ambient(0, lvl=0.06)                                   # zumbido de sala de servidores
    T.put(0.0, boom(), 0.7); T.put(0.1, pop(1100), 0.35)      # gancho + firma
    T.put(3.95, whoosh(0.5), 0.8)                            # latigazo 3.9→4.45 (pico ≈4.17)
    T.put(4.4, hit(), 0.45)
    T.put(8.2, riser(1.6), 0.35)                             # grúa subiendo hacia el cenital
    for i in range(10): T.put(8.5 + i * 0.16, tick(), 0.3)   # la red se dibuja en el piso
    T.put(12.2, riser(1.15), 0.5)                            # picada que acelera
    T.put(13.32, impact(), 0.75); T.put(13.4, whoosh(0.4, up=False), 0.5)   # atraviesa el nodo
    T.put(16.0, pop(1300), 0.4); T.put(16.0, ding(2093, 0.5), 0.25)          # firma al final
