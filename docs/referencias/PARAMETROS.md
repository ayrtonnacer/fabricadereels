# Parámetros medidos (tabla viva)
Cada fila sale de `engine/analisis/medir.py` (ver `docs/MEDICION.md`). Las referencias de Ayrton se suman a medida que las pasa; las **metas** son provisorias (salen de nuestros reels aprobados) y se ajustan con cada referencia nueva.

| Video | Dur. | Cortes (por min) | Plano mediano | Cámara en mov. | Vel. mediana | Mov. lento | Zoom neto | Jerk mediano | Brillo | LUFS | Pal/s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **WiFi v4 (propio, HTB 3D)** | 33,1 s | 6 (10,9) | 4,6 s | 67 % | 13 px/s | 93 % | +1,1 %/s | 449 px/s³ | 0,09 | −14,0 | 3,11 |
| Ejemplo externo: Alejandro Magno (repo shorts-animados, caricatura 3D) | 9,8 s | 8 (48,8) | 0,7 s | 66 % | 110 px/s | 49 % | −2,4 %/s | 2.437 px/s³ | 0,40 | −14,6 | n/d |
| Referencia citada (canal Zack D. Films, según el video de LuisPa) | — | — | — | ~65 % | "muy lenta" (un solo eje, acerca y aleja) | — | — | — | — | — | 2,77 |

## Metas provisorias para nuestro estilo (HackTheBox, 3D, explicativo)
| Parámetro | Meta | Nota |
|---|---|---|
| Cámara en movimiento | 60–70 % | nunca queda quieta salvo el CTA |
| Velocidad mediana | 10–40 px/s; p95 < 250 px/s | dolly lento; los viajes rápidos son pocos |
| Tirón mediano | < 800 px/s³ | movimientos con ease, sin sacudidas |
| Plano mediano | 3–6 s | un cambio visual cada 1,5–3 s dentro del plano |
| Palabras/s | 2,6–2,9 (total) | hoy 3,11: algo rápido para principiantes |
| Volumen | −14 LUFS, pico ≤ −1,5 dBTP | ya cumple |
| Brillo medio | 0,07–0,12 | fondo oscuro HTB |
