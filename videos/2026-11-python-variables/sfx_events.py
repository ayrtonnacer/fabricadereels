"""Efectos del reel de variables. Mismos tiempos que assets/set.js (los viajes v1…v9 se calculan igual que allá).
Regla: MENOS sonidos que movimientos; el del viaje en el PICO de velocidad; nada a menos de 40 ms de otro."""
from sfxlib import *


def build(T, S, lib=None):
    P = Paleta(T)
    P.apertura()                                        # MARCA: boom grave en 0 s (no tocar)

    v1, v2, v3 = cuando('l02') - 0.85, cuando('l03') - 0.6, cuando('l04') - 0.5
    v4, v5, v7 = cuando('l06') - 0.55, cuando('l08') - 0.5, cuando('l10') - 0.5
    v8, v9 = cuando('l11') - 0.4, cuando('l12') - 0.5

    P.error(cuando('l01', 'caja'), g=0.18)             # ✕ sobre la caja: no es eso
    P.viaje(v1 + 0.42)                                  # A → B
    P.aterriza(v1 + 0.85)
    P.aparece(cuando('l02', 'valor'))                   # el 19 aparece en la memoria
    P.viaje(v2 + 0.35, d=0.5, g=0.3)                    # dolly in al código
    P.tipeo(cuando('l03', 'asignar'), 9)                # se escribe edad = 19
    P.dato(cuando('l03', 'asocia'))                     # el nombre se asocia
    P.viaje(v3 + 0.4)                                   # B → C (la cuenta)
    P.aparece(cuando('l04', 'valor'))                   # la etiqueta se da vuelta: 19
    P.resultado(cuando('l05', 'veinte'), g=0.18)        # = 20
    P.viaje(v4 + 0.42)                                  # C → D (los tipos)
    P.aterriza(v4 + 0.85)
    P.dato(cuando('l06', 'número')); P.dato(cuando('l06', 'texto')); P.dato(cuando('l06', 'lista'))
    P.viaje(cuando('l08', 'pasar') + 0.5, d=0.5, g=0.3)   # la etiqueta salta al texto
    P.viaje(v7 + 0.42)                                  # D → E
    P.aterriza(v7 + 0.85)
    P.aparece(cuando('l10', 'dos'))                     # la segunda etiqueta
    P.error(cuando('l11', 'copia') + 0.6, g=0.12)       # la copia fantasma se borra
    P.viaje(v8 + 0.4, d=0.9, g=0.35)                    # grúa a los dos hilos
    P.viaje(v9 + 0.7, d=0.9, g=0.4)                     # grúa por encima del set y vuelta al gancho
    P.aterriza(v9 + 1.5)
    P.resultado(cuando('l12', 'nombra'))                # payoff

    P.cierre(S['cierre'])                               # MARCA: succión → boom → chinn (no tocar)
