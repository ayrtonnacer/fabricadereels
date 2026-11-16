"""Efectos del reel "Qué son los tokens (parte 1)". Significados fijos en engine/audio/sfxlib.py y docs/AUDIO.md.
S[id] = segundo de inicio de cada escena. Whoosh en el PICO de velocidad de cada movimiento de cámara."""
from sfxlib import *


def build(T, S, lib=None):
    bm = propio('boom-cinematico')   # grave de Ayrton al inicio y al final
    g = S['gancho']
    T.put(g, bm * 0.9 if bm is not None else boom(), 0.6); T.put(g + 0.05, pop(1100), 0.3)
    for k in range(6): T.put(g + 2.7 + 0.09 * k, tick(), 0.22)          # aparecen los números
    T.put(g + 3.8, whoosh(0.4), 0.35)                                   # baja hacia la placa
    t = S['corte']
    T.put(t + 0.95, whoosh(0.9), 0.3)                                   # la cuchilla recorre el mensaje
    for k in range(5): T.put(t + 1.05 + 0.17 * k, tick(), 0.25)         # cada corte
    T.put(t + 2.45, whoosh(0.5), 0.4)                                   # se separan y la cámara se aleja
    for k in range(6): T.put(t + 4.05 + 0.08 * k, pop(900 + 60 * k), 0.25)   # número de cada token
    t = S['comparten']
    T.put(t + 0.15, pop(1000), 0.3); T.put(t + 1.1, tick(), 0.25)
    T.put(t + 2.6, whoosh(0.5), 0.4)
    T.put(t + 2.95, pop(800), 0.3); T.put(t + 3.15, pop(850), 0.3)       # nitidez y lucidez se parten
    T.put(t + 5.0, tick(), 0.3); T.put(t + 6.2, ding(1318.5, 0.6), 0.35)  # mismo número
    t = S['mayus']
    for dt, f in [(0.3, 950), (0.85, 1050), (1.55, 1150)]: T.put(t + dt, pop(f), 0.3)
    T.put(t + 2.95, tick(), 0.28)
    t = S['idioma']
    for k in range(10): T.put(t + 0.4 + 0.2 * k, tick(), 0.12)          # se llenan las barras
    T.put(t + 2.75, whoosh(0.4), 0.35); T.put(t + 2.75, ding(1568, 0.5), 0.3)
    t = S['foto']
    T.put(t + 2.0, tick(), 0.25); T.put(t + 2.65, whoosh(0.5), 0.45)    # grilla; entra al cuadradito
    T.put(t + 4.7, whoosh(0.5), 0.45)                                   # sale y los cuadraditos vuelan
    for k in range(7): T.put(t + 4.9 + 0.1 * k, pop(850 + 50 * k), 0.2)
    T.put(t + 5.4, ding(1318.5, 0.5), 0.3)
    t = S['payoff']
    for k in range(6): T.put(t + 2.5 + 0.07 * k, tick(), 0.25)          # giran las fichas
    T.put(t + 3.2, ding(1568, 0.6), 0.35)
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55)
    ch = propio('chinn'); T.put(t + 0.7, ch if ch is not None else sparkle(9), 0.5)
