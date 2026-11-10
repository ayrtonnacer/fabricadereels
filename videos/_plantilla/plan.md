# Plan numérico — <título>
Se arma DESPUÉS de que Ayrton aprueba el guion y ANTES de animar. Todo con números de `docs/referencias/BIBLIA-DE-ESTILO.md`; al terminar el render, `python engine/analisis/comparar.py videos/X/analisis/metricas.json` dice si se cumplieron.

## Metas del reel (copiar de `docs/referencias/metas.json`; ajustar solo con motivo)
| Parámetro | Meta | Por qué se desvía (si lo hace) |
|---|---|---|
| Duración / palabras por segundo | ___ s / 2,6–2,9 | |
| Cortes por minuto · plano mediano | ___ · ___ s | |
| Cámara en movimiento | 60–90 % de los cuadros | |
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

## Chequeo (con números, después del render)
- [ ] `comparar.py` sin parámetros fuera de la meta (o desvío justificado arriba)
- [ ] cuadro 0 muestra la idea (miniatura) · [ ] nada quieto > 3 s · [ ] texto entre 200 y 1330 px de alto · [ ] cuadros revisados con `snapshot`
