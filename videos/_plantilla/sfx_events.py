"""Efectos de la plantilla. Significados fijos en engine/audio/sfxlib.py y docs/2-estilo/AUDIO.md.
S[id] = segundo de inicio de cada escena (de video.json). El whoosh va en el PICO de velocidad del movimiento de cámara, no al empezar.
VARIEDAD (2026-11-16): los efectos salen del catálogo medido con elegir(rol): distintos en cada uso y en cada reel (la semilla es el nombre
de la carpeta). Fijos de marca, siempre iguales: boom grave al inicio y al final, chinn cuando aterriza el CTA (media kit)."""
from sfxlib import *


def build(T, S, lib=None):
    ok = HAY_ONETAKE
    def un(rol, sint, **kw):
        x = elegir(rol, **kw); return x if x is not None else sint()
    def w(t, d=0.6, g=0.4):                    # transición: aire sintético + una "curva" real distinta cada vez, centrada en el pico
        T.put(t - d / 2, air(d) if ok else whoosh(d), g, send=0.5)
        x = elegir('curva', max_dur=0.9)
        if x is not None: T.put(t - 0.05, x, g * 0.6, send=0.4)
    aparece = lambda t, g=0.3: T.put(t, un('aparece', lambda: bubble(500, 0.2) if ok else pop(900), max_dur=0.5), g, send=0.3)
    dato = lambda t, g=0.22: T.put(t, un('dato', tick, max_dur=0.35), g, send=0.15)
    resultado = lambda t, g=0.25: T.put(t, un('resultado', lambda: glass(1318, 1.0) if ok else ding(), max_dur=1.6), g, send=0.5)
    aterriza = lambda t, g=0.2: T.put(t, un('golpe', lambda: sub(62, 0.5) if ok else thunk(), max_dur=0.8), g, send=0.3)

    bm = propio('boom-cinematico')            # marca: grave al inicio
    T.put(0.0, bm * 0.9 if bm is not None else boom(), 0.6, send=0.3)
    w(S['explica'] - 0.3)                     # sale del gancho hacia la izquierda (la corriente)
    t = S['explica']
    aparece(t + 0.3); w(t + 3.1); aterriza(t + 3.6); aparece(t + 3.05)
    w(t + 5.7); T.typing(t + 5.45, 17); resultado(t + 5.95)
    # cierre (marca): succión → golpe grave → CTA con chinn
    t = S['cierre']; T.put(t - 0.9, reverse(riser(0.8)), 0.35); T.put(t - 0.05, bm if bm is not None else impact(), 0.55, send=0.3)
    ch = propio('chinn'); T.put(t + 0.55, ch if ch is not None else sparkle(9), 0.5, send=0.2)
