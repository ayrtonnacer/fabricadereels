"""Efectos del reel "Qué es un tensor". Significados fijos en engine/audio/sfxlib.py y docs/AUDIO.md.
S[id] = segundo de inicio de cada escena. Whoosh en el PICO de velocidad de cada movimiento de cámara (mitad de un 'io')."""
from sfxlib import *


def build(T, S, lib=None):
    bm = propio('boom-cinematico')   # grave de Ayrton al inicio y al final
    # gancho: golpe + pop; los tres objetos se vuelven el mismo bloque (pops) y la cámara orbita (whoosh)
    T.put(0.0, bm * 0.9 if bm is not None else boom(), 0.6); T.put(0.05, pop(1100), 0.3)
    for k in range(3): T.put(3.0 + 0.1 * k, pop(850 + 120 * k), 0.3)
    T.put(3.4, whoosh(0.45), 0.4)
    # píxel: entrada a la foto (whoosh), aparece la cuadrícula (tick), sale el píxel (pop), vuelta atrás y sale la fila (ticks)
    t = S['pixel']
    T.put(t + 1.6, whoosh(0.5), 0.45); T.put(t + 1.4, tick(), 0.25); T.put(t + 1.7, pop(1000), 0.4)
    T.put(t + 4.75, whoosh(0.45), 0.4)
    for k in range(5): T.put(t + 4.5 + 0.2 * k, tick(), 0.22)
    # foto: alejarse (whoosh), cuadrícula (tick), color y capas (pops), órbita (whoosh), cubo y "tensor" (ding)
    t = S['foto']
    T.put(t + 0.7, whoosh(0.45), 0.4); T.put(t + 2.1, tick(), 0.25)
    T.put(t + 5.4, pop(900), 0.3); T.put(t + 6.05, whoosh(0.5), 0.45)
    for k in range(3): T.put(t + 6.0 + 0.3 * k, pop(950 + 100 * k), 0.3)
    T.put(t + 7.45, pop(1300), 0.35); T.put(t + 8.75, ding(1318.5, 0.6), 0.35)
    # video: el cursor recorre el tiempo (ticks), alejarse a ver todo (whoosh), aparecen 0D..4D (pops), "todas" (ding)
    t = S['video']
    for k in range(4): T.put(t + 0.6 + 0.7 * k, tick(), 0.22)
    T.put(t + 3.95, whoosh(0.5), 0.45)
    for k in range(5): T.put(t + 4.2 + 0.3 * k, pop(800 + 90 * k), 0.28)
    T.put(t + 6.1, ding(1568, 0.5), 0.3)
    # datos: la onda y su fila de números; las palabras y sus filas
    t = S['datos']
    T.put(t + 1.2, pop(900), 0.28)
    for k in range(3): T.put(t + 2.6 + 0.15 * k, tick(), 0.22)
    T.put(t + 3.6, pop(1100), 0.28)
    # usos: modelo, y los tres resultados (pop + ding en la respuesta)
    t = S['usos']
    for dt in [0.3, 2.3, 3.0, 3.7, 4.1, 4.5]: T.put(t + dt, pop(950), 0.28)
    T.put(t + 2.85, tick(), 0.3); T.put(t + 4.95, ding(1760, 0.5), 0.3)
    # payoff: vuelven los objetos y se vuelven bloques (pops + whoosh), "tensores" (ding), acercamiento y TensorFlow
    t = S['payoff']
    for k in range(3): T.put(t + 1.3 + 0.12 * k, pop(850 + 120 * k), 0.3)
    T.put(t + 1.75, whoosh(0.45), 0.4); T.put(t + 2.35, ding(1318.5, 0.6), 0.35)
    T.put(t + 4.3, whoosh(0.5), 0.4); T.put(t + 4.25, pop(1200), 0.3)
    # cierre: succión → golpe → CTA; chinn (sonido de Ayrton) cuando aterriza el CTA
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55)
    ch = propio('chinn'); T.put(t + 0.7, ch if ch is not None else sparkle(9), 0.5)
