# Script técnico medido de motion-ref-4.mp4

31.57 s · 30.0 fps · 720×1278 · 11 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 0.5 s | inicio | alejamiento; zoom -2 %; vel. máx 3242 px/s; 0.4 s en movimiento de 0.5 | 0.09 | 3; — |
| 2 | 0.5 s | 1.6 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +4 %; vel. máx 746 px/s; 1.5 s en movimiento de 1.6 | 0.07 | 8; — |
| 3 | 2.1 s | 2.6 s | corte seco | acercamiento/paneo/deriva; zoom +20 %; vel. máx 604 px/s; 2.1 s en movimiento de 2.6 | 0.02 | 6; — |
| 4 | 4.7 s | 2.3 s | corte seco | acercamiento; zoom +6 %; vel. máx 941 px/s; 2.1 s en movimiento de 2.3 | 0.03 | 5; — |
| 5 | 7.0 s | 5.1 s | corte seco | acercamiento; zoom +27 %; vel. máx 936 px/s; 4.9 s en movimiento de 5.1 | 0.06 | 16; 7.0, 9.6 |
| 6 | 12.1 s | 2.0 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom -0 %; vel. máx 2401 px/s; 1.6 s en movimiento de 2.0 | 0.09 | 6; — |
| 7 | 14.0 s | 2.6 s | transición + corte (movimiento fuerte antes) | acercamiento/paneo/deriva; zoom +7 %; vel. máx 1561 px/s; 1.8 s en movimiento de 2.6 | 0.01 | 7; — |
| 8 | 16.7 s | 4.8 s | corte seco | paneo/deriva; zoom +4 %; vel. máx 1192 px/s; 3.8 s en movimiento de 4.8 | 0.02 | 16; — |
| 9 | 21.5 s | 2.9 s | corte seco | alejamiento/paneo/deriva; zoom -22 %; vel. máx 376 px/s; 2.0 s en movimiento de 2.9 | 0.05 | 13; — |
| 10 | 24.4 s | 4.0 s | corte seco | acercamiento; zoom +95 %; vel. máx 2622 px/s; 3.9 s en movimiento de 4.0 | 0.05 | 11; — |
| 11 | 28.4 s | 3.2 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -88 %; vel. máx 896 px/s; 3.1 s en movimiento de 3.2 | 0.04 | 13; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
