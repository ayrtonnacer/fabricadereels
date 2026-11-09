"""Efectos del reel de redes: sonido escaso (un impacto por idea) sobre una cama de ambiente; los golpes caen donde la voz nombra cada cosa.
S[id] = segundo de inicio de cada escena (tiempos relativos a la escena, anclados a las pausas de la voz de Daniela)."""
from sfxlib import *


def build(T, S, lib=None):
    T.ambient(0, lvl=0.05)
    s1, s2, s3, s4, s5, s6, s7 = (S[k] for k in ('s1', 's2', 's3', 's4', 's5', 's6', 's7'))
    # hook: firma + los tres equipos se encienden de a uno, al nombrarlos
    T.put(s1 + 0.0, boom(), 0.7); T.put(s1 + 0.05, pop(1100), 0.35)
    for t in (0.4, 1.2, 2.0): T.put(s1 + t, ding(1568, 0.35), 0.25)
    T.put(s1 + 3.05, whoosh(0.5), 0.8)                                   # latigazo hacia el mapa
    # contexto: enlaces entre los puestos e internet
    T.put(s2 + 0.1, powerup(), 0.3)
    for t in (0.6, 1.1, 1.6): T.put(s2 + t, tick(), 0.35)
    T.put(s3 - 1.0, reverse(riser(0.6)), 0.35)
    # switch
    T.put(s3 + 0.6, hit(), 0.5)
    for t in (4.0, 5.2, 5.8): T.put(s3 + t, pop(1200), 0.45); T.put(s3 + t + 0.02, ding(1760, 0.3), 0.25)
    T.put(s3 + 6.8, impact(), 0.45)                                      # se cierra «edificio · campus»
    T.put(s4 - 1.0, reverse(riser(0.8)), 0.35)
    # router
    T.put(s4 + 0.8, hit(), 0.5)
    for t in (1.5, 2.2): T.put(s4 + t, pop(1000), 0.4)
    T.put(s4 + 5.9, chime(), 0.35)                                       # despachador analiza
    for t in (7.4, 7.7, 8.0): T.put(s4 + t, tick(), 0.3)
    T.put(s4 + 8.7, impact(), 0.55); T.put(s4 + 8.75, ding(2093, 0.5), 0.3)   # elige la mejor ruta
    T.put(s4 + 9.3, whoosh(0.6), 0.5)
    T.put(s4 + 11.2, sparkle(7), 0.4)
    # punto de acceso
    T.put(s5 + 0.9, hit(), 0.5); T.put(s5 + 1.0, powerup(), 0.35)
    T.put(s5 + 4.0, sweep(300, 900, 0.9, 0.3), 0.3)                      # ancho de banda por el cable
    for i in range(3): T.put(s5 + 5.8 + i * 1.0, sweep(500, 1400, 0.7, 0.3), 0.3)
    for t in (6.4, 7.2, 8.0): T.put(s5 + t, pop(1500), 0.35)             # dispositivos que se conectan
    # payoff: grúa a cenital y un verbo por equipo
    T.put(s6 + 0.1, riser(0.9), 0.4)
    for i in range(3): T.put(s6 + 1.5 + i * 1.25, impact() if i == 2 else hit(), 0.5 if i == 2 else 0.4)
    # CTA
    T.put(s7 + 0.1, whoosh(0.4), 0.4); T.put(s7 + 0.9, pop(1300), 0.45); T.put(s7 + 0.9, ding(2093, 0.5), 0.3)
