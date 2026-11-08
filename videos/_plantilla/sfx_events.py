"""Efectos de la plantilla. Significados fijos en engine/audio/sfxlib.py (docstring). S[id] = segundo de inicio de cada escena."""
from sfxlib import *


def build(T, S, lib=None):
    T.ambient(0, lvl=0.05)                      # base: que nunca suene vacío
    for k, v in S.items():                      # transición entre escenas
        if k != 'et1' and v > 0: T.put(v - 0.12, whoosh(0.4), 0.55)
    T.put(0.0, boom(), 0.9); T.put(0.05, pop(1100), 0.4); T.put(0.55, glitch(), 0.45)   # gancho
    t = S['s2']; T.typing(t + 0.5, 18); T.enter(t + 1.2); T.put(t + 2.2, pop(1000), 0.35)
    t = S['s3']
    for lt in (0.35, 0.85): T.put(t + lt, pop(1200), 0.5); T.put(t + lt + 0.02, ding(1760, 0.3), 0.25)
    t = S['s4']; T.put(t - 1.0, reverse(riser(0.9)), 0.4); T.put(t - 0.1, impact(), 0.6)   # succión → golpe → CTA
    T.put(t, sparkle(9), 0.5); T.put(t + 0.9, pop(1300), 0.45); T.put(t + 0.9, ding(2093, 0.5), 0.3)
