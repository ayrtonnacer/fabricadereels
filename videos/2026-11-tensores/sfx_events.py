"""Efectos del reel de tensores. Significados fijos en engine/audio/sfxlib.py y docs/AUDIO.md.
S[id] = segundo de inicio de cada escena. Whoosh en el PICO de velocidad de cada movimiento de cámara (mitad de un 'io')."""
from sfxlib import *


def build(T, S, lib=None):
    bm = propio('boom-cinematico')   # sonido grave de Ayrton al inicio y al final
    # gancho: golpe grave + pop al aparecer la cara; whoosh con el acercamiento
    T.put(0.0, bm * 0.9 if bm is not None else boom(), 0.6); T.put(0.05, pop(1100), 0.3)
    T.put(0.3, whoosh(0.4), 0.4)
    # tipos: la cara se vuelve números; escalar → vector → matriz (pop al aparecer, whoosh en cada viaje de cámara)
    t = S['tipos']
    T.put(t + 1.1, pop(700), 0.25); T.put(t + 1.5, pop(900), 0.25)          # números sobre la cara
    T.put(t + 2.9, pop(1000), 0.4)                                          # escalar
    T.put(t + 6.8, whoosh(0.45), 0.45); T.put(t + 7.2, pop(1150), 0.4)      # viaje al vector (6.2→7.4) y vector
    T.put(t + 10.35, whoosh(0.45), 0.45); T.put(t + 10.8, pop(1250), 0.4)   # viaje a la matriz (9.7→11.0) y matriz
    # tensor: orbita, aparecen las capas, los ejes; zoom out al lote
    t = S['tensor']
    T.put(t + 2.55, whoosh(0.45), 0.4); T.put(t + 2.7, pop(950), 0.35)
    for k, dt in enumerate([3.32, 3.8, 4.19]): T.put(t + dt, tick(), 0.3)
    T.put(t + 6.25, whoosh(0.5), 0.45)                                      # pull-back (5.5→7.0)
    for k in range(4): T.put(t + 6.0 + 0.18 * k, pop(800 + 90 * k), 0.25)
    T.put(t + 8.0, ding(1318.5, 0.5), 0.3)                                  # eje del lote
    # red: entrada y pesos; la entrada cruza la capa (whoosh) y sale transformada
    t = S['red']
    T.put(t + 1.1, pop(900), 0.35); T.put(t + 1.7, pop(1100), 0.35)
    T.put(t + 3.65, whoosh(0.5), 0.5); T.put(t + 3.95, pop(1300), 0.35)
    # detalle: aviso de ambigüedad y error de forma (tono grave = problema)
    t = S['detalle']
    T.put(t + 1.0, pop(1000), 0.3); T.put(t + 2.75, pop(800), 0.3)
    T.put(t + 5.25, pop(1000), 0.3); T.put(t + 5.85, buzz(), 0.35)
    # payoff: ejes de la cara, zoom out al lote y resultado
    t = S['payoff']
    for dt in [0.75, 0.95, 1.15]: T.put(t + dt, tick(), 0.3)
    T.put(t + 2.1, whoosh(0.45), 0.45); T.put(t + 2.44, ding(1760, 0.5), 0.35)
    # cierre: succión → golpe → CTA; chinn (sonido propio de Ayrton) cuando aterriza el CTA
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55)
    ch = propio('chinn'); T.put(t + 0.8, ch if ch is not None else sparkle(9), 0.5)
