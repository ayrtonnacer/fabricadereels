# Script técnico medido de video-alejandro-caricatura.mp4

9.83 s · 30.0 fps · 540×960 · 9 planos. Generado por `engine/analisis/medir.py`: cada renglón es una MEDICIÓN, no una opinión.

| # | Desde | Dura | Entra por | Cámara en el plano | Brillo | Sonido (ataques; graves en s) |
|---|---|---|---|---|---|---|
| 1 | 0.0 s | 0.9 s | inicio | acercamiento; zoom +39 %; vel. máx 2114 px/s; 0.8 s en movimiento de 0.9 | 0.40 | 2; — |
| 2 | 0.9 s | 0.7 s | transición + corte (movimiento fuerte antes) | acercamiento; zoom +37 %; vel. máx 1417 px/s; 0.6 s en movimiento de 0.7 | 0.44 | 2; — |
| 3 | 1.6 s | 2.5 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -48 %; vel. máx 1535 px/s; 2.2 s en movimiento de 2.5 | 0.35 | 7; 2.8 |
| 4 | 4.1 s | 2.3 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -50 %; vel. máx 1821 px/s; 1.4 s en movimiento de 2.3 | 0.44 | 7; 5.4 |
| 5 | 6.4 s | 0.7 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +1 %; vel. máx 1230 px/s; 0.4 s en movimiento de 0.7 | 0.43 | 2; — |
| 6 | 7.0 s | 0.5 s | transición + corte (movimiento fuerte antes) | quieta | 0.43 | 2; — |
| 7 | 7.6 s | 0.5 s | transición + corte (movimiento fuerte antes) | quieta | 0.43 | 2; — |
| 8 | 8.0 s | 0.7 s | transición + corte (movimiento fuerte antes) | paneo/deriva; zoom +2 %; vel. máx 1868 px/s; 0.5 s en movimiento de 0.7 | 0.41 | 2; — |
| 9 | 8.7 s | 1.1 s | transición + corte (movimiento fuerte antes) | alejamiento; zoom -14 %; vel. máx 3066 px/s; 1.0 s en movimiento de 1.1 | 0.40 | 1; — |

## Cómo usarlo
- Para inspirarse: copiar la **estructura** (duración de planos, tipo y velocidad de cámara, cuándo caen los golpes), no el contenido.
- Para replicar un movimiento: la columna "Cámara" da tipo, zoom total y velocidad máxima; en `escena3d.js` se traduce con `E.ruta` (px/s ≈ metros/s × ~540 a 4 m de distancia).
