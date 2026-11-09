"""Efectos del reel de WiFi. Significados fijos (docs/AUDIO.md). S[id] = inicio de cada escena. Whoosh en el PICO del movimiento de cámara."""
from sfxlib import *


def build(T, S, lib=None):
    # gancho: golpe de apertura; zoom through (cam 2,6→3,2 s, pico al final)
    bm = propio('boom-cinematico')   # sonido grave de Ayrton (al inicio y al final); si falta, el sintético
    T.put(0.0, bm * 0.9 if bm is not None else boom(), 0.6); T.put(0.05, pop(1100), 0.3)
    T.put(S['envia'] - 0.3, whoosh(0.45), 0.6)
    # envía: aparece el notebook, se tipean los bits, antena, la onda se dibuja, salen las ondas
    t = S['envia']
    T.put(t + 0.3, pop(1000), 0.35); T.typing(t + 0.45, 8)
    T.put(t + 1.2, pop(1300), 0.35); T.put(t + 1.7, whoosh(0.5), 0.35)
    for k in range(3): T.put(t + 2.7 + 0.5 * k, pop(900 - 60 * k), 0.22)
    # router: la onda llega, decodifica (tipeo), cable (thunk), paquetes, y de vuelta
    t = S['router']
    T.put(t - 0.12, whoosh(0.4), 0.45); T.put(t + 0.3, pop(1000), 0.3)
    T.put(t + 0.7, whoosh(0.4), 0.3); T.typing(t + 1.3, 8)
    T.put(t + 2.3, thunk(), 0.5); T.put(t + 2.6, whoosh(0.4), 0.4)
    for k in range(3): T.put(t + 2.8 + 0.16 * k, tick(), 0.3)
    T.put(t + 4.2, whoosh(0.4), 0.45)
    # ethernet: el cable pasa a ondas (detalle de profesional)
    t = S['ethernet']
    T.put(t - 0.12, whoosh(0.4), 0.45); T.put(t + 0.4, pop(1000), 0.3); T.put(t + 0.7, thunk(), 0.4)
    T.put(t + 2.35, whoosh(0.4), 0.4); T.put(t + 3.3, ding(1760, 0.4), 0.3)
    # bandas
    t = S['bandas']
    T.put(t - 0.12, whoosh(0.4), 0.45); T.put(t + 0.4, pop(1100), 0.3); T.put(t + 1.5, pop(900), 0.3)
    T.put(t + 4.6, thunk(), 0.5); T.put(t + 5.1, whoosh(0.4), 0.35); T.put(t + 5.35, alert(), 0.3)
    # payoff: se aleja y revela el departamento; dos ✓
    t = S['payoff']
    T.put(t + 0.6, whoosh(0.5), 0.5); T.put(t + 1.55, ding(1568, 0.4), 0.3); T.put(t + 2.15, ding(2093, 0.5), 0.3)
    # cierre: succión → golpe → CTA; chinn de Ayrton cuando aterriza el CTA
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55)
    ch = propio('chinn'); T.put(t + 0.55, ch if ch is not None else sparkle(9), 0.5)
