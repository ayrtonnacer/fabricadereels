# Script técnico medido de final.mp4

33.1 s · 30.0 fps · 1080×1920 · 7 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 3.0 s | inicio | acercamiento; zoom +38 %; vel. máx 335 px/s; 2.9 s en movimiento de 3.0 | 0.10 | 9; 0.2, 2.8 |
| 2 | 3.0 s | 4.8 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -22 %; vel. máx 1668 px/s; 4.2 s en movimiento de 4.8 | 0.09 | 16; 3.4 |
| 3 | 7.8 s | 5.2 s | corte seco | acercamiento/alejamiento/paneo/deriva; zoom -4 %; vel. máx 307 px/s; 4.8 s en movimiento de 5.2 | 0.09 | 15; 11.8 |
| 4 | 13.0 s | 4.6 s | corte seco | acercamiento/paneo/deriva; zoom +10 %; vel. máx 106 px/s; 3.4 s en movimiento de 4.6 | 0.08 | 17; — |
| 5 | 17.6 s | 7.6 s | corte seco | acercamiento/alejamiento/paneo/deriva; zoom +0 %; vel. máx 788 px/s; 3.9 s en movimiento de 7.6 | 0.07 | 29; 20.4, 20.5 |
| 6 | 25.2 s | 3.9 s | corte seco | acercamiento/alejamiento; zoom +0 %; vel. máx 469 px/s; 3.1 s en movimiento de 3.9 | 0.10 | 12; 25.4, 25.5 |
| 7 | 29.1 s | 4.0 s | corte seco | paneo/deriva; zoom +0 %; vel. máx 10 px/s; 0.4 s en movimiento de 4.0 | 0.09 | 11; 29.2, 29.3, 29.4 |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
