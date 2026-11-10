# Script técnico medido de motion-ref-3.mp4

24.75 s · 24.0 fps · 720×1280 · 3 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 14.5 s | inicio | acercamiento/alejamiento; zoom -94 %; vel. máx 4833 px/s; 13.7 s en movimiento de 14.5 | 0.06 | 71; 1.3, 5.3, 6.9 |
| 2 | 14.5 s | 6.4 s | corte seco | alejamiento; zoom -51 %; vel. máx 4072 px/s; 6.3 s en movimiento de 6.4 | 0.07 | 27; 17.6 |
| 3 | 21.0 s | 3.8 s | corte seco | acercamiento/paneo/deriva; zoom +8 %; vel. máx 1148 px/s; 1.8 s en movimiento de 3.8 | 0.04 | 9; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
