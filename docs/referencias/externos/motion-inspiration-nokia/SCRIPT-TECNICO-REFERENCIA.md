# Script técnico medido de motion-inspiration-nokia.mp4

20.07 s · 30.0 fps · 720×1280 · 19 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 0.1 s | inicio | quieta | 0.35 | 0; — |
| 2 | 0.1 s | 0.9 s | corte seco | alejamiento; zoom -23 %; vel. máx 1378 px/s; 0.7 s en movimiento de 0.9 | 0.29 | 2; — |
| 3 | 1.0 s | 0.8 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -7 %; vel. máx 13273 px/s; 0.7 s en movimiento de 0.8 | 0.21 | 3; — |
| 4 | 1.8 s | 0.9 s | corte seco | acercamiento; zoom +8 %; vel. máx 1519 px/s; 0.6 s en movimiento de 0.9 | 0.28 | 4; — |
| 5 | 2.8 s | 0.8 s | corte seco | alejamiento; zoom -40 %; vel. máx 5429 px/s; 0.6 s en movimiento de 0.8 | 0.35 | 3; — |
| 6 | 3.6 s | 1.9 s | corte seco | alejamiento; zoom -21 %; vel. máx 6490 px/s; 1.3 s en movimiento de 1.9 | 0.32 | 6; — |
| 7 | 5.5 s | 1.5 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +31 %; vel. máx 9057 px/s; 1.4 s en movimiento de 1.5 | 0.41 | 6; — |
| 8 | 7.0 s | 1.7 s | corte seco | acercamiento; zoom +19 %; vel. máx 131 px/s; 1.0 s en movimiento de 1.7 | 0.35 | 4; — |
| 9 | 8.7 s | 0.7 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -2 %; vel. máx 1855 px/s; 0.3 s en movimiento de 0.7 | 0.33 | 1; — |
| 10 | 9.4 s | 0.5 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +8 %; vel. máx 3013 px/s; 0.3 s en movimiento de 0.5 | 0.35 | 0; — |
| 11 | 9.9 s | 0.9 s | corte seco | paneo/deriva; zoom +5 %; vel. máx 6238 px/s; 0.8 s en movimiento de 0.9 | 0.42 | 2; — |
| 12 | 10.8 s | 0.4 s | corte seco | quieta | 0.46 | 1; — |
| 13 | 11.3 s | 0.5 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -1 %; vel. máx 524 px/s; 0.3 s en movimiento de 0.5 | 0.26 | 2; — |
| 14 | 11.8 s | 0.8 s | corte seco | alejamiento; zoom -2 %; vel. máx 1482 px/s; 0.7 s en movimiento de 0.8 | 0.23 | 1; — |
| 15 | 12.6 s | 0.6 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +6 %; vel. máx 8912 px/s; 0.4 s en movimiento de 0.6 | 0.31 | 1; — |
| 16 | 13.2 s | 1.3 s | corte seco | alejamiento; zoom -17 %; vel. máx 1927 px/s; 1.2 s en movimiento de 1.3 | 0.33 | 5; — |
| 17 | 14.5 s | 0.7 s | corte seco | acercamiento; zoom +22 %; vel. máx 5792 px/s; 0.4 s en movimiento de 0.7 | 0.20 | 1; — |
| 18 | 15.2 s | 0.6 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +3 %; vel. máx 244 px/s; 0.4 s en movimiento de 0.6 | 0.19 | 2; — |
| 19 | 15.8 s | 4.3 s | corte seco | alejamiento; zoom -12 %; vel. máx 362 px/s; 1.5 s en movimiento de 4.3 | 0.01 | 0; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
