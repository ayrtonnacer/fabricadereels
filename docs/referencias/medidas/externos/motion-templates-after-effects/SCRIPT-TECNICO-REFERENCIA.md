# Script técnico medido de motion-templates-after-effects.mp4

15.02 s · 59.94 fps · 720×1280 · 10 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 4.8 s | inicio | alejamiento; zoom -18 %; vel. máx 9871 px/s; 3.1 s en movimiento de 4.8 | 0.90 | 12; — |
| 2 | 4.8 s | 0.8 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +12 %; vel. máx 597 px/s; 0.6 s en movimiento de 0.8 | 0.50 | 6; — |
| 3 | 5.6 s | 0.7 s | corte seco | alejamiento; zoom -21 %; vel. máx 2673 px/s; 0.6 s en movimiento de 0.7 | 0.16 | 6; — |
| 4 | 6.3 s | 1.9 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -12 %; vel. máx 10878 px/s; 1.8 s en movimiento de 1.9 | 0.20 | 14; — |
| 5 | 8.2 s | 0.8 s | corte seco | alejamiento; zoom -14 %; vel. máx 2240 px/s; 0.6 s en movimiento de 0.8 | 0.91 | 6; — |
| 6 | 9.0 s | 0.5 s | corte seco | alejamiento; zoom -2 %; vel. máx 2663 px/s; 0.3 s en movimiento de 0.5 | 0.17 | 5; 9.2 |
| 7 | 9.4 s | 0.5 s | corte seco | acercamiento; zoom +2 %; vel. máx 93 px/s; 0.4 s en movimiento de 0.5 | 0.23 | 4; — |
| 8 | 9.9 s | 0.4 s | corte seco | acercamiento; zoom +21 %; vel. máx 876 px/s; 0.2 s en movimiento de 0.4 | 0.78 | 4; — |
| 9 | 10.4 s | 1.6 s | corte seco | acercamiento; zoom +60 %; vel. máx 2649 px/s; 1.5 s en movimiento de 1.6 | 0.20 | 0; — |
| 10 | 12.0 s | 3.0 s | corte seco | acercamiento; zoom +5 %; vel. máx 1088 px/s; 0.6 s en movimiento de 3.0 | 0.95 | 1; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
