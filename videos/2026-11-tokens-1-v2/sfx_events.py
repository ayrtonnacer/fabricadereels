"""Efectos del reel "Qué son los tokens (parte 1)" v2 — LA FÁBRICA: un solo plano continuo; whoosh en el pico de cada viaje de la cámara.
Banco CC0 (banco()) + materiales onetake (air/glass/bubble) + UNA sala compartida (send). Tiempos globales (= assets/fabrica.js)."""
from sfxlib import *


def build(T, S, lib=None):
    bm = propio('boom-cinematico'); ch = propio('chinn'); dig = propio('interface-texto-digital')
    ok = HAY_ONETAKE
    pop_ = (lambda f=500: bubble(f, 0.2)) if ok else pop
    ding_ = (lambda f=659, d=0.9: glass(f, d, 0.7)) if ok else ding
    def w(t, d=0.6, g=0.4, i=3, a=250, b=2600):                 # whoosh = aire + swish real, centrado en el pico del movimiento
        T.put(t - d / 2, air(d, a, b) if ok else whoosh(d), g, send=0.5)
        x = banco('whoosh', f'swish-{i}')
        if x is not None: T.put(t - 0.05, x, g * 0.6, send=0.4)
    def tk(t, g=0.25, i=0):                                       # dato / corte: click de interfaz real
        x = banco('ui', 'click', i); T.put(t, x if x is not None else tick(), g, send=0.15)
    # gancho
    T.put(0.1, bm * 0.9 if bm is not None else boom(), 0.6, send=0.3); T.put(0.15, pop_(520), 0.3, send=0.3)
    if dig is not None: T.put(2.75, dig[:int(SR * 0.9)], 0.35, send=0.1)
    w(3.85, 0.5, 0.25, 5, 300, 1800)
    # A: cuchilla, se separan, números
    T.put(5.0, air(1.0, 220, 3400) if ok else whoosh(0.9), 0.3, send=0.4)
    for k in range(5): tk(5.15 + 0.17 * k, 0.22, k)
    w(6.5, 0.7, 0.4, 2)
    for k in range(6): T.put(8.15 + 0.08 * k, pop_(430 + 40 * k), 0.22, send=0.3)
    # viaje A→B (grúa) y estación B
    w(10.65, 0.8, 0.5, 9, 200, 3000); T.put(11.05, sub(66, 0.6) if ok else thunk(), 0.25, send=0.3)
    T.put(11.05, ding_(784, 0.7), 0.16, send=0.5); tk(12.0)
    w(13.3, 0.6, 0.35, 7)
    T.put(13.85, pop_(420), 0.28, send=0.3); T.put(14.05, pop_(470), 0.28, send=0.3)
    tk(15.9, 0.3, 3); T.put(17.05, ding_(1318.5, 1.3), 0.2, send=0.6); T.put(17.07, ding_(1976, 1.3), 0.12, send=0.6)
    # viaje B→C y estación C
    w(19.0, 0.8, 0.45, 4); T.put(19.4, sub(62, 0.5) if ok else thunk(), 0.2, send=0.3)
    for t, f in [(19.6, 400), (20.15, 480), (20.85, 560)]: T.put(t, pop_(f), 0.3, send=0.3)
    tk(22.25, 0.3, 5)
    # viaje C→D y estación D
    w(24.4, 0.8, 0.45, 6); T.put(24.8, sub(62, 0.5) if ok else thunk(), 0.2, send=0.3)
    for k in range(9): tk(25.35 + 0.2 * k, 0.12, k)
    w(27.55, 0.5, 0.3, 8); T.put(27.7, ding_(1046, 0.9), 0.16, send=0.5)
    # viaje D→E y la foto
    w(30.6, 0.8, 0.45, 10); T.put(31.0, sub(60, 0.5) if ok else thunk(), 0.2, send=0.3)
    tk(33.1, 0.28, 2); w(33.65, 0.5, 0.4, 11)
    w(35.7, 0.55, 0.4, 12)
    for k in range(7): T.put(35.95 + 0.1 * k, pop_(380 + 35 * k), 0.18, send=0.3)
    T.put(36.45, ding_(988, 1.0), 0.16, send=0.5)
    # payoff: la cámara se eleva y ve toda la fábrica; todo gira a números
    w(38.35, 1.1, 0.5, 13, 160, 2200)
    for k in range(10): tk(40.55 + 0.09 * k, 0.18, k + 6)
    T.put(41.3, ding_(1318.5, 1.4), 0.2, send=0.6)
    # cierre
    T.put(41.6, reverse(riser(0.8)), 0.35); T.put(42.45, bm if bm is not None else impact(), 0.55, send=0.3)
    T.put(43.2, ch if ch is not None else sparkle(9), 0.5, send=0.2)
