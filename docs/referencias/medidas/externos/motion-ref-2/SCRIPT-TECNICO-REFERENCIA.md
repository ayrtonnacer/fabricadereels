# Script técnico medido de motion-ref-2.mp4

20.03 s · 30.0 fps · 1280×720 · 4 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 10.0 s | inicio | alejamiento/paneo/deriva; zoom -107 %; vel. máx 1999 px/s; 7.3 s en movimiento de 10.0 | 0.11 | 42; 0.0, 0.3, 0.5, 1.3, 2.0, 2.3, 2.5, 3.1, 4.5, 5.3, 5.5, 6.0, 7.3, 7.3, 8.5, 8.8, 9.3 |
| 2 | 10.0 s | 4.1 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +21 %; vel. máx 161 px/s; 0.7 s en movimiento de 4.1 | 0.09 | 17; 10.0, 10.3, 10.8, 11.3, 11.8, 12.0, 12.3, 13.3, 13.8, 14.0 |
| 3 | 14.1 s | 4.5 s | transición + corte (movimiento fuerte antes) | acercamiento/alejamiento; zoom +53 %; vel. máx 559 px/s; 3.5 s en movimiento de 4.5 | 0.09 | 20; 14.8, 14.9, 15.3, 15.5, 15.8, 16.3, 16.5, 16.8, 17.3, 17.8, 18.0 |
| 4 | 18.6 s | 1.5 s | corte seco | acercamiento; zoom +42 %; vel. máx 1604 px/s; 1.4 s en movimiento de 1.5 | 0.17 | 5; 18.8, 19.3, 19.8 |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
