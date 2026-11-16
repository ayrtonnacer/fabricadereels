"""Efectos del reel "Qué son los tokens (parte 1)" — v2 con banco CC0 + materiales onetake + una sala compartida (docs/AUDIO.md).
S[id] = segundo de inicio de cada escena. Whoosh en el PICO de velocidad de cada movimiento de cámara. Menos eventos que beats."""
from sfxlib import *


def build(T, S, lib=None):
    bm = propio('boom-cinematico'); ch = propio('chinn'); dig = propio('interface-texto-digital')
    sw = lambda i=3, g=1.0: banco('whoosh', f'swish-{i}', 0, g)            # whoosh real (banco CC0)
    clk = lambda i=0: banco('ui', 'click', i)                                # click de interfaz real
    ok = HAY_ONETAKE
    pop_ = (lambda f=500: bubble(f, 0.2)) if ok else pop
    ding_ = (lambda f=659, d=0.9: glass(f, d, 0.7)) if ok else ding
    air_ = (lambda d=0.5, a=250, b=2600: air(d, a, b)) if ok else (lambda d=0.5, a=250, b=2600: whoosh(d))
    def w(t, d=0.5, g=0.4, i=3, a=250, b=2600):                              # whoosh = aire sintético + swish real, en la sala
        T.put(t, air_(d, a, b), g, send=0.5)
        x = sw(i);
        if x is not None: T.put(t + 0.02, x, g * 0.7, send=0.4)
    def tk(t, g=0.25, i=0):                                                  # dato/número: click real (o digital propio)
        x = clk(i); T.put(t, x if x is not None else tick(), g, send=0.15)
    g = S['gancho']
    T.put(g, bm * 0.9 if bm is not None else boom(), 0.6, send=0.3); T.put(g + 0.05, pop_(520), 0.3, send=0.3)
    if dig is not None: T.put(g + 2.65, dig[:int(SR * 0.9)], 0.35, send=0.1)   # los números aparecen escritos
    else:
        for k in range(6): tk(g + 2.7 + 0.09 * k)
    w(g + 3.7, 0.45, 0.3, 5, 300, 1800)                                      # baja hacia la placa
    t = S['corte']
    w(t + 0.95, 0.95, 0.35, 9, 220, 3400)                                    # la cuchilla recorre el mensaje
    for k in range(5): tk(t + 1.05 + 0.17 * k, 0.22, k)                      # cada corte
    w(t + 2.45, 0.55, 0.45, 2, 250, 2600)                                    # se separan; la cámara se aleja
    for k in range(6): T.put(t + 4.05 + 0.08 * k, pop_(430 + 40 * k), 0.22, send=0.3)   # número de cada token
    t = S['comparten']
    T.put(t + 0.15, ding_(784, 0.7), 0.16, send=0.5); tk(t + 1.1)
    w(t + 2.6, 0.6, 0.4, 7, 250, 2600)
    T.put(t + 2.95, pop_(420), 0.28, send=0.3); T.put(t + 3.15, pop_(470), 0.28, send=0.3)   # se parten
    tk(t + 5.0, 0.3, 3); T.put(t + 6.2, ding_(1318.5, 1.3), 0.2, send=0.6); T.put(t + 6.22, ding_(1976, 1.3), 0.12, send=0.6)   # mismo número: acorde suave
    t = S['mayus']
    for dt, f in [(0.3, 400), (0.85, 480), (1.55, 560)]: T.put(t + dt, pop_(f), 0.3, send=0.3)
    tk(t + 2.95, 0.3, 5)
    t = S['idioma']
    for k in range(9): tk(t + 0.45 + 0.2 * k, 0.12, k)                       # se llenan las barras
    w(t + 2.7, 0.45, 0.35, 4, 300, 2000); T.put(t + 2.78, ding_(1046, 0.9), 0.16, send=0.5)
    t = S['foto']
    tk(t + 2.0, 0.28, 2); w(t + 2.55, 0.6, 0.4, 6, 250, 2600)                # grilla; entra al cuadradito
    w(t + 4.6, 0.6, 0.4, 10, 250, 3000)                                      # sale; los cuadraditos vuelan
    for k in range(7): T.put(t + 4.9 + 0.1 * k, pop_(380 + 35 * k), 0.18, send=0.3)
    T.put(t + 5.4, ding_(988, 1.0), 0.16, send=0.5)
    t = S['payoff']
    for k in range(6): tk(t + 2.5 + 0.07 * k, 0.22, k + 6)                   # giran las fichas
    T.put(t + 3.2, ding_(1318.5, 1.4), 0.2, send=0.6)
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55, send=0.3)
    T.put(t + 0.7, ch if ch is not None else sparkle(9), 0.5, send=0.2)
