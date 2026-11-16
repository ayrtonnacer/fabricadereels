# Plan numérico — <título>
Se arma DESPUÉS de que Ayrton aprueba el guion y ANTES de animar. Todo con números de `docs/4-referencias/BIBLIA-DE-ESTILO.md`; al terminar el render, `python engine/analisis/comparar.py videos/X/analisis/metricas.json` dice si se cumplieron.

## Metas del reel (copiar de `docs/4-referencias/metas.json`; ajustar solo con motivo)
| Parámetro | Meta | Por qué se desvía (si lo hace) |
|---|---|---|
| Duración / palabras por segundo | ___ s / 2,6–2,9 | |
| Cortes por minuto · plano mediano | ___ · ___ s | |
| Cámara en movimiento | 60–90 % de los cuadros (alarma; con pausas de verdad quedan ≥ 25 % quietos, ver `docs/2-estilo/CAMARA.md` regla 9) | |
| Continuidad entre escenas (`arrastre.py`) | medio ≥ 0,5; ningún límite en 0,0 salvo cambio de tema/CTA | |
| Variación de planos | el más largo ≥ 4× el más corto · ≥ 25 % cuadros quietos · un tramo quieto ≥ 1 s | |
| Velocidad mediana · pico de un movimiento notorio | ___ px/s · ___ px/s | |
| Ataque / liberación de un movimiento | ___ s / ___ s (parecidos = ease simétrico) | |
| Retención entre movimientos | ___ s | |
| Volumen · pico | −14 LUFS · ≤ −1,5 dBTP | |

## Planos (un renglón por escena; todo en números)
| Esc | Desde–hasta (s) | Voz (texto exacto) | Set (objetos y z) | Cámara: tipo · zoom total % · pico px/s · ataque/liberación s | Entradas (t local, s) | SFX (s; en el pico del movimiento) | Transición: tipo · vel. de cámara antes (px/s) |
|---|---|---|---|---|---|---|---|
| gancho | 0–3 | | | | | | |
| … | | | | | | | |
| cierre | | "Dale me gusta y seguime…" | CTA grande, firma chica debajo | llega al CTA y queda | CTA palabra por palabra, firma +1,1 s | chinn al aterrizar | — |

## Límites entre escenas (uno por cada corte; ver tipos en `docs/4-referencias/material/2026-11-onetake.md`)
| De → a | Qué SOBREVIVE y en qué se transforma | Tipo (objeto · contenedor · empuje de cámara · círculo · grupo · superficie) | Cómo termina el plano (resorte / desenfoque / corte; no repetir dos seguidas) |
|---|---|---|---|
| gancho → … | | | |

## Chequeo (con números, después del render)
- [ ] `python engine/analisis/arrastre.py videos/X/final.mp4 --escenas videos/X/video.json` (continuidad, quietud, variación de planos, mapa de energía)
- [ ] `python engine/analisis/barro.py videos/X/final.mp4` (graves-medios acumulados en la mezcla)
- [ ] `comparar.py` sin parámetros fuera de la meta (o desvío justificado arriba)
- [ ] cuadro 0 muestra la idea (miniatura) · [ ] nada quieto > 3 s · [ ] texto entre 200 y 1330 px de alto · [ ] cuadros revisados con `snapshot`
