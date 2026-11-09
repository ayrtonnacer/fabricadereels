"""Efectos del reel de redes: sonido escaso (un impacto por idea) sobre una cama de ambiente; los golpes caen en los cortes y en lo que se enciende.
S[id] = segundo de inicio de cada escena. Con voz, los efectos bajan solos (ducking en mezcla.py)."""
from sfxlib import *


def build(T, S, lib=None):
    T.ambient(0, lvl=0.05)                                              # sala técnica: que nunca suene vacío
    s1, s2, s3, s4, s5, s6, s7 = (S[k] for k in ('s1', 's2', 's3', 's4', 's5', 's6', 's7'))
    # hook: firma + los tres equipos se encienden de a uno
    T.put(s1 + 0.0, boom(), 0.7); T.put(s1 + 0.05, pop(1100), 0.35)
    for t in (0.4, 1.2, 2.0): T.put(s1 + t, ding(1568, 0.35), 0.25)
    T.put(s1 + 3.55, whoosh(0.5), 0.8)                                   # latigazo hacia el mapa
    # contexto: mapa y enlaces
    T.put(s2 + 0.1, powerup(), 0.3); T.put(s2 + 2.5, sparkle(5), 0.3)
    T.put(s2 + 4.5, reverse(riser(0.8)), 0.4)                            # succión hacia el switch
    # switch: puertos y cables que se encienden
    T.put(s3 + 0.9, hit(), 0.5)
    for t in (3.5, 4.9, 6.3): T.put(s3 + t, pop(1200), 0.45); T.put(s3 + t + 0.02, ding(1760, 0.3), 0.25)
    for t in (7.0, 7.1): T.put(s3 + t, tick(), 0.3)
    T.put(s3 + 7.0, impact(), 0.45)                                      # se cierra el marco de la red local
    T.put(s3 + 12.2, reverse(riser(0.9)), 0.4)                           # hacia el router
    # router: dos redes, rutas, mejor ruta
    T.put(s4 + 0.9, hit(), 0.5)
    for t in (2.2, 3.2): T.put(s4 + t, pop(1000), 0.4)
    T.put(s4 + 5.5, chime(), 0.35)                                       # analiza
    for t in (6.4, 6.75, 7.1): T.put(s4 + t, tick(), 0.3)
    T.put(s4 + 8.6, impact(), 0.55); T.put(s4 + 8.65, ding(2093, 0.5), 0.3)   # elige la mejor ruta
    T.put(s4 + 9.4, whoosh(0.6), 0.5)                                    # el paquete sale hacia internet
    T.put(s4 + 11.8, sparkle(7), 0.4)
    # punto de acceso: ancho de banda → ondas
    T.put(s5 + 0.9, hit(), 0.5); T.put(s5 + 2.0, powerup(), 0.4)
    for i in range(3): T.put(s5 + 2.6 + i * 1.5, sweep(500, 1400, 0.7, 0.3), 0.3)
    for t in (3.8, 5.2, 6.7): T.put(s5 + t, pop(1500), 0.35)             # los dispositivos se conectan
    # payoff: grúa a cenital, un verbo por equipo
    T.put(s6 + 0.1, riser(0.9), 0.4)
    for i in range(3): T.put(s6 + 0.9 + i * 0.8, impact() if i == 2 else hit(), 0.5 if i == 2 else 0.4)
    # CTA
    T.put(s7 + 0.1, whoosh(0.4), 0.4); T.put(s7 + 0.9, pop(1300), 0.45); T.put(s7 + 0.9, ding(2093, 0.5), 0.3)
