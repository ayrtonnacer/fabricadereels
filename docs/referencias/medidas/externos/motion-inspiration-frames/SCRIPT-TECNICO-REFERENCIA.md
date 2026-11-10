# Script técnico medido de motion-inspiration-frames.mp4

17.8 s · 25.0 fps · 720×1280 · 15 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 1.5 s | inicio | acercamiento; zoom +43 %; vel. máx 1695 px/s; 1.4 s en movimiento de 1.5 | 0.85 | 6; 0.2 |
| 2 | 1.5 s | 1.7 s | corte seco | acercamiento; zoom +70 %; vel. máx 368 px/s; 1.6 s en movimiento de 1.7 | 0.24 | 9; — |
| 3 | 3.2 s | 0.9 s | corte seco | paneo/deriva; zoom -0 %; vel. máx 612 px/s; 0.6 s en movimiento de 0.9 | 0.02 | 4; — |
| 4 | 4.1 s | 0.8 s | corte seco | acercamiento; zoom +1 %; vel. máx 849 px/s; 0.6 s en movimiento de 0.8 | 0.03 | 1; — |
| 5 | 4.9 s | 1.1 s | corte seco | acercamiento; zoom +33 %; vel. máx 614 px/s; 0.9 s en movimiento de 1.1 | 0.90 | 7; 5.0 |
| 6 | 6.0 s | 1.5 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +26 %; vel. máx 595 px/s; 1.3 s en movimiento de 1.5 | 0.07 | 5; — |
| 7 | 7.5 s | 2.1 s | corte seco | acercamiento; zoom +30 %; vel. máx 412 px/s; 1.6 s en movimiento de 2.1 | 0.85 | 5; — |
| 8 | 9.6 s | 0.8 s | corte seco | acercamiento; zoom +3 %; vel. máx 210 px/s; 0.5 s en movimiento de 0.8 | 0.95 | 2; — |
| 9 | 10.3 s | 1.0 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -4 %; vel. máx 61 px/s; 0.6 s en movimiento de 1.0 | 0.91 | 4; — |
| 10 | 11.3 s | 1.4 s | corte seco | paneo/deriva; zoom -0 %; vel. máx 237 px/s; 1.0 s en movimiento de 1.4 | 0.95 | 5; — |
| 11 | 12.7 s | 1.5 s | corte seco | acercamiento; zoom +34 %; vel. máx 209 px/s; 1.2 s en movimiento de 1.5 | 0.16 | 4; — |
| 12 | 14.2 s | 1.3 s | corte seco | acercamiento; zoom +3 %; vel. máx 543 px/s; 1.0 s en movimiento de 1.3 | 0.72 | 4; — |
| 13 | 15.5 s | 0.8 s | corte seco | acercamiento; zoom +9 %; vel. máx 492 px/s; 0.6 s en movimiento de 0.8 | 0.89 | 1; — |
| 14 | 16.3 s | 0.8 s | corte seco | alejamiento; zoom -3 %; vel. máx 643 px/s; 0.6 s en movimiento de 0.8 | 0.09 | 3; — |
| 15 | 17.1 s | 0.7 s | corte seco | alejamiento; zoom -1 %; vel. máx 620 px/s; 0.6 s en movimiento de 0.7 | 0.01 | 2; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
