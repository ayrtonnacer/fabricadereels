"""Efectos del reel del bucle for. Mismos tiempos que assets/set.js (los viajes de cámara se calculan igual que allá).
Regla: MENOS sonidos que movimientos; el del viaje en el PICO de velocidad; nada a menos de 40 ms de otro."""
from sfxlib import *


def build(T, S, lib=None):
    P = Paleta(T)
    P.apertura()                                        # MARCA: boom grave en 0 s (no tocar)

    tL0, tA0, tR0, tP0 = S['lista'], S['adentro'], S['rango'], S['payoff']
    P.viaje(tL0 + 0.1, d=0.9, g=0.35)                   # grúa que baja a la fila
    P.aterriza(tL0 + 0.55)
    for k in range(5): P.dato(cuando('l02', 'nombres') + 0.12 * k + 0.05, g=0.14)   # aparecen los cinco nombres
    P.tipeo(cuando('l03', 'escribir'), 20)              # se escriben los cinco saludos a mano
    P.viaje(cuando('l03', 'mil') + 0.2, d=0.9, g=0.4)   # zoom out: el campo de mil vuelve
    P.viaje(cuando('l04', 'for') - 0.1, d=0.6, g=0.3)   # dolly in a las tres líneas
    g0, g1 = cuando('l05', 'primero'), cuando('l05', 'siguiente')
    for t in [g0, g1] + [g1 + 0.42 * k for k in (1, 2, 3)]: P.aparece(t, g=0.2)   # cada saludo
    P.viaje(tA0 + 0.3, d=0.6, g=0.45)                   # atraviesa el anillo: pasa a negro
    P.aterriza(tA0 + 1.3)
    for w in ('próximo', 'una', 'otra', 'vez', 'cuando'): P.dato(cuando('l07', w) + 0.3, g=0.2)   # cae una esfera
    P.error(cuando('l07', 'ninguno') + 0.05, g=0.12)    # pide y no hay nada
    P.resultado(cuando('l07', 'termina'), g=0.18)       # fin
    P.viaje(tR0 + 0.05, d=0.5, g=0.4)                   # latigazo al cenital de range()
    P.dato(cuando('l08', 'casi'))                       # 48 bytes
    for n in range(7): P.dato(cuando('l08', 'crean') + 0.32 * n, g=0.1)   # los números nacen de a uno
    P.viaje(tP0 + 0.5, d=0.9, g=0.35)                   # grúa arriba: el campo entero
    P.resultado(cuando('l09', 'millón'), g=0.2)         # la onda de luz
    P.viaje(cuando('l09', 'cambia') + 0.25, d=0.9, g=0.3)   # baja a la tarjeta
    P.tipeo(cuando('l09', 'lista'), 8)                  # cambia la lista

    P.cierre(S['cierre'])                               # MARCA: succión → boom → chinn (no tocar)
