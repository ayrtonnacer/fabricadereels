"""Efectos del reel. Se escriben por SIGNIFICADO con la paleta común (engine/audio/sfxlib.py → Paleta; reglas en docs/2-estilo/AUDIO.md).
S['escena'] = segundo en que empieza esa escena · cuando('l03', 'palabra') = segundo en que la voz dice esa palabra (igual que en assets/set.js).
Regla: MENOS sonidos que movimientos; el del viaje de cámara va en el PICO de velocidad; nada a menos de 40 ms de otro."""
from sfxlib import *


def build(T, S, lib=None):
    P = Paleta(T)
    P.apertura()                                   # MARCA: boom grave en 0 s (no tocar)

    # --- el medio: un renglón por cosa que pasa en assets/set.js, con el MISMO tiempo que allá ---
    tB, tC, tG = S['explica'], cuando('l03'), S['payoff']
    P.viaje(tB)                                    # travelling A → B (el pico cae en el cambio de escena)
    P.aterriza(tB + 0.4)                           # la cámara llega a B (temblor de aterrizaje)
    P.tipeo(cuando('l02', 'concepto'), 24, bits=True)   # se escriben los 0 y 1 en la pantalla
    P.viaje(tC)                                    # travelling B → C
    P.aparece(tC + 0.45)                           # sale la primera onda
    P.viaje(tG + 0.45, d=0.9, g=0.35)              # grúa al plano general
    P.resultado(cuando('l04', 'funcionando'))      # el payoff "da"

    P.cierre(S['cierre'])                          # MARCA: succión → boom → chinn cuando aterriza el CTA (no tocar)
