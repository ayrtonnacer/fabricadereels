# Plan numérico — Qué es un tensor (v5.2, didáctico)
55,9 s (portada 0,1 s + 55,8) · ~150 palabras (2,7 pal/s) · 8 escenas + mapa 0D–4D fijo arriba (de "pixel" a "datos") · render mudo 2 min 19 s (2,5 s/s).
## Metas vs medido (`comparar.py`, final.mp4)
| Parámetro | Meta | Medido |
|---|---|---|
| Cortes/min · plano mediano | 4–20 · 2,5–6,5 s | 6,5 · 6,1 s ✓ |
| Volumen · pico | −14 LUFS · ≤ −1,5 dBTP | −14,0 · −1,9 ✓ |
| Ataques de sonido/s | 3,0–4,5 | 3,0 (justo) |
| Cámara en movimiento · velocidad mediana | 60–90 % · 20–70 px/s | 43 % · 4 px/s (bajo: cámara lenta a propósito para que se lea; ver si a Ayrton le falta ritmo) |
## Escenas (inicio, s)
portada 0 · gancho 0,1 · pixel 4,7 · foto 12,3 · video 22,7 · datos 31,1 · usos 36,8 · payoff 42,9 · cierre 50,9. Cámara y efectos por escena en `compositions/*.html` y `sfx_events.py` (whoosh en el pico de cada `io`).
