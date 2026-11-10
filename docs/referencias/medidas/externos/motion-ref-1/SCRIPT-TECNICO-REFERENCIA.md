# Script técnico medido de motion-ref-1.mp4

9.33 s · 30.0 fps · 720×1278 · 7 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 1.5 s | inicio | acercamiento; zoom +18 %; vel. máx 3489 px/s; 1.4 s en movimiento de 1.5 | 0.28 | 1; — |
| 2 | 1.5 s | 0.5 s | corte seco | alejamiento; zoom -16 %; vel. máx 622 px/s; 0.4 s en movimiento de 0.5 | 0.44 | 3; — |
| 3 | 2.0 s | 0.4 s | corte seco | alejamiento; zoom -26 %; vel. máx 236 px/s; 0.3 s en movimiento de 0.4 | 0.37 | 2; 2.0 |
| 4 | 2.4 s | 2.3 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -119 %; vel. máx 5753 px/s; 2.1 s en movimiento de 2.3 | 0.12 | 5; 4.3 |
| 5 | 4.7 s | 2.3 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +1 %; vel. máx 2900 px/s; 2.1 s en movimiento de 2.3 | 0.32 | 5; — |
| 6 | 6.9 s | 2.3 s | corte seco | acercamiento/alejamiento; zoom +38 %; vel. máx 2613 px/s; 1.7 s en movimiento de 2.3 | 0.22 | 5; 9.0 |
| 7 | 9.3 s | 0.1 s | transición + corte (movimiento fuerte antes) | quieta | 0.32 | 1; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
