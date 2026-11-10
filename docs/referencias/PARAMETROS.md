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
| Velocidad mediana | 20–70 px/s; p95 < 250 px/s | referencias contemplativas de Ayrton: 22–69; hoy estamos en 13 (algo lenta) |
| Tirón mediano | < 650 px/s³ | referencias contemplativas: 460–605; WiFi 449 |
| Plano mediano | 3–6 s | un cambio visual cada 1,5–3 s dentro del plano |
| Palabras/s | 2,6–2,9 (total) | hoy 3,11: algo rápido para principiantes |
| Volumen | −14 LUFS, pico ≤ −1,5 dBTP | ya cumple |
| Brillo medio | 0,07–0,12 | fondo oscuro HTB |

## Referencias de Ayrton (10 videos del 9/11, medidos con `medir.py`; lectura cualitativa en `referencias/SINTESIS.md`)
| Video | Dur. | Cortes (por min) | Plano mediano | Cámara en mov. | Vel. mediana | Mov. lento | Jerk mediano | Brillo | LUFS |
|---|---|---|---|---|---|---|---|---|---|
| Instagram strategy (frases, oscuro/claro) | 18 s | 14 (47.2) | 1.08 s | 80.9 % | 37 px/s | 76.1 % | 456 | 0.534 | -14.5 |
| Nokia collage (cortes al beat) | 20 s | 18 (53.8) | 0.83 s | 42.4 % | 201 px/s | 35.7 % | 2858 | 0.251 | -14.7 |
| Sting ilustrado | 9 s | 6 (38.6) | 1.47 s | 85.4 % | 305 px/s | 19.2 % | 10396 | 0.247 | -14.3 |
| **Lente explosionada 3D** (1 plano, mover–retener–mover) | 20 s | 3 (9.0) | 4.3 s | 63.2 % | 22 px/s | 81.1 % | 516 | 0.103 | -16.0 |
| **Anuncio con tarjetas de vidrio** (1 plano continuo) | 25 s | 2 (4.8) | 6.42 s | 86.4 % | 69 px/s | 57.1 % | 605 | 0.058 | -14.2 |
| **Miedo y codicia** (rojo/verde, tic por palabra) | 32 s | 10 (19.0) | 2.63 s | 85.3 % | 33 px/s | 70.7 % | 460 | 0.044 | -14.2 |
| Explicador largo (104 s, agentes de IA) | 104 s | 23 (13.2) | 4.22 s | 89.5 % | 30 px/s | 72.7 % | 336 | 0.889 | -11.7 |
| Motion Templates After Effects | 15 s | 9 (36.0) | 0.78 s | 64.2 % | 161 px/s | 46.4 % | 7075 | 0.644 | -13.4 |
| Promo de marca (50 s) | 50 s | 28 (33.6) | 1.3 s | 59.5 % | 64 px/s | 56.5 % | 1661 | 0.465 | -14.5 |
| Glitch cyber | 9 s | 12 (82.4) | 0.58 s | 77.5 % | 122 px/s | 46.6 % | 4837 | 0.368 | -9.6 |

### Qué dicen los números
- Las referencias **contemplativas y oscuras** (Lente, Anuncio de vidrio, Miedo y codicia, brillo 0,04–0,10) son las más parecidas a nuestro estilo HackTheBox: plano mediano 2,6–6,4 s, cámara en movimiento 63–86 % de los cuadros, **velocidad mediana 22–69 px/s**, **tirón 460–605 px/s³**. Nuestro reel de WiFi: 4,6 s, 67 %, 13 px/s, 449. Conclusión: el *suavizado* ya está en el rango; nuestra cámara es algo **más lenta** que la de esas referencias.
- Las referencias **vertiginosas** (cortes cada 0,6–1,5 s, 36–82 cortes por minuto, tirón 2.800–10.400) son otro género (promos, glitch, collage): no son la meta para reels explicativos.
- Dos de las diez no tienen cortes (un plano continuo): Lente y Anuncio de vidrio. Volumen: casi todas en −14 LUFS, igual que nosotros.
