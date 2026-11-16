# Plan — Qué son los tokens (parte 1), v2: LA FÁBRICA
Misma voz, datos y tiempos que la v1. Cambia la puesta en escena (pedido de Ayrton: explorar el espacio en 2.5D, no calcar el reel anterior).
Un solo set 3D (`assets/fabrica.js`): una cinta en el piso que serpentea hacia el fondo (eje z) con 5 estaciones — A mensaje y cuchilla (0, 0), B pedazos compartidos (1,6; −3,5), C mayúsculas (−1,6; −7), D idiomas (1,6; −10,5), E foto (−1,6; −14) — y UNA cámara continua (cada composición dibuja el mismo set en el tiempo global, así los límites no se ven). Cubitos sobre la cinta avanzan solo cuando la cámara viaja. Cada estación aparece cuando la cámara llega. Viajes: 9,9–11,3 (grúa por encima de A), 18,3–19,4, 23,7–24,9, 29,7–31,0, 37,6–39,4 (sube al plano general de toda la fábrica: payoff "todo es una lista de números", todas las fichas giran a su número). Whoosh (aire + swish real) en el pico de cada viaje, golpe grave suave al aterrizar.

## Medido (final.mp4)
| | v1 | v2 | meta |
|---|---|---|---|
| Arrastre medio | 0,37 | **0,61** ✓ | ≥ 0,5 |
| Cortes detectados | 2,5/min | **0** (un plano continuo) | — |
| Pico de un movimiento notorio | 640 px/s | **2955 px/s** ✓ | 800–3000 |
| Duración de un movimiento notorio | 0,70 s | **1,35 s** ✓ | 1–4 |
| Cuadros quietos | 77 % | **64 %** ✓ | ≥ 25 % |
| Velocidad p95 | 131 | 2408 (▲ meta 1900: los viajes largos son rápidos) | 400–1900 |
El 0,04 de `arrastre.py` en t = 10,9 s no es un corte: cae en el medio de la grúa (cámara rápida). El único corte real es al CTA.

## v2.2 (2026-11-16): cambios pedidos por Ayrton
- Música desde el inicio (violines), nivelada; ver `docs/2-estilo/AUDIO.md`.
- Final nuevo: después de "todo es una lista de números" y del plano general (grúa), **la pantalla se llena de números** (campo de 5×14 con los IDs reales de los tokens en tan y otros en gris, que aparece desde el centro hacia afuera y llueve cada vez más rápido) → corte al CTA con riser + golpe. `payoff` dura 6 s (antes 4,4) y el CTA empieza a los 44,1 s; el video dura 49,1 s.
