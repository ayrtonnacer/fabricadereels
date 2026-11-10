"""Efectos del reel de WiFi. Significados fijos (docs/AUDIO.md). S[id] = inicio de cada escena. Whoosh en el PICO del movimiento de cámara."""
from sfxlib import *


def tramo(nombre, a, b, fade_in=0.02, fade_out=0.08, gain=1.0):
    """Recorte [a, b] s de un sonido propio (assets/sfx/propios/<nombre>) con fundidos; None si falta."""
    x = propio(nombre)
    if x is None: return None
    y = x[int(a * SR):int(b * SR)].copy(); fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi: y[:fi] *= np.linspace(0, 1, fi)
    if fo: y[-fo:] *= np.linspace(1, 0, fo)
    return y * gain


def build(T, S, lib=None):
    # gancho: golpe de apertura; zoom through (cam 2,6→3,2 s, pico al final)
    bm = propio('boom-cinematico')   # sonido grave de Ayrton (al inicio y al final); si falta, el sintético
    T.put(0.0, bm * 0.9 if bm is not None else boom(), 0.6); T.put(0.05, pop(1100), 0.3)
    T.put(S['envia'] - 0.3, whoosh(0.45), 0.6)
    # envía: aparece el notebook, se tipean los bits, antena, la onda se dibuja, salen las ondas
    t = S['envia']
    T.put(t + 0.3, pop(1000), 0.35); dg = tramo('interface-texto-digital', 0.0, 0.95); T.put(t + 0.4, dg if dg is not None else tick(), 0.55)
    T.put(t + 1.2, pop(1300), 0.35); T.put(t + 1.45, whoosh(0.5), 0.35)
    for k in range(4): T.put(t + 1.5 + 0.5 * k, pop(900 - 50 * k), 0.22)
    # router: la onda llega, decodifica (tipeo), cable (thunk), paquetes, y de vuelta
    t = S['router']
    T.put(t - 0.12, whoosh(0.4), 0.45); T.put(t + 0.3, pop(1000), 0.3)
    T.put(t + 0.7, whoosh(0.4), 0.3)
    # toda la sección del router lleva el sonido de módem (ya NO el tipeo digital, que queda solo para los bits de la notebook)
    md = tramo('modem-conexion', 2.5, 6.6, 0.15, 0.45); T.put(t + 0.9, md if md is not None else whoosh(0.4), 0.45)
    T.put(t + 2.3, thunk(), 0.5)
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
    hm = propio('hit-metal'); t = S['cierre']; T.put(t - 0.55, hm if hm is not None else reverse(riser(0.8)), 0.55); T.put(t - 0.05, bm if bm is not None else impact(), 0.55)
    ch = propio('chinn'); T.put(t + 0.55, ch if ch is not None else sparkle(9), 0.5)
