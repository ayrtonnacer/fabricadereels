# Plan de cámara — <título>
Se arma DESPUÉS del OK del guion y de `python engine/reel.py voz` (los segundos salen de ahí), y ANTES de escribir `assets/set.js`.
Reglas y recetas: `docs/2-estilo/CAMARA.md`. Al terminar: `python engine/reel.py medir videos/X` y completar "Medido".

## El set
- **Idea del espacio** (en una frase; distinta del reel anterior): ___
- **Corriente** (hacia dónde van todos los viajes): ___
| Estación | Posición (x, y, z) m | Idea que vive ahí | Objetos (uno solo lleva el tan) |
|---|---|---|---|
| A | 0, 0, 0 | gancho: ___ | ___ |
| B | ___ | ___ | ___ |

## Plano por plano (un renglón por frase de voz)
| Línea | Voz (inicio s) | Estación | Plano y ángulo | Cómo llega la cámara (movimiento · duración) | Qué aparece y con qué palabra | Sonido |
|---|---|---|---|---|---|---|
| l01 | ___ | A | medio, tres cuartos, leve picado | cuadro 0 = portada; push-in lento | título + firma desde el cuadro 0 | boom de apertura |
| l02 | ___ | ___ | ___ | travelling · 0,9 s | ___ | viaje + aterriza |
| … | | | | | | |
| CTA | ___ | — | CTA centrado | corte; aterriza y queda quieta | CTA palabra por palabra; firma a los 1,3 s | succión → boom → chinn |

## Chequeo del plan (antes de animar)
- [ ] Un movimiento por idea nueva; la cámara queda quieta ≥ 1,5 s en cada cosa que se nombra.
- [ ] Al menos tres ángulos distintos (frontal, picado, contrapicado, tres cuartos) y un plano general.
- [ ] Ningún objeto de una estación futura asoma detrás del título ni de un rótulo.
- [ ] Rótulos arriba de los objetos; nada que leer por debajo de y 1100.
- [ ] El recorrido no calca el del reel anterior.

## Medido (después del render)
| | Este reel | Rango |
|---|---|---|
| Ritmo (palabras por segundo) | ___ | 2,4–2,8 |
| Cuadros con cámara en movimiento | ___ % | 25–75 % |
| Movimientos notorios cada 10 s | ___ | 1,5–5 |
| Continuidad (arrastre medio) | ___ | ≥ 0,5 |
| Graves-medios (100–300 Hz) | ___ % | < 35 % |
| Volumen · pico | ___ | −14 LUFS · ≤ −1,5 dBTP |
| Render | ___ s por segundo | ≤ 3 |
Fuera de rango y por qué se acepta: ___
