# Plan de cámara — El bucle for
## El set
- **Idea del espacio**: un estudio blanco infinito con un campo de miles de esferas negras; la escala cuenta la historia (cinco → mil → un millón). Un tramo en negro "adentro" del for.
- **Corriente**: hacia el fondo (−z): se atraviesa el anillo y se entra al tubo.
| Estación | Posición (x, y, z) m | Idea | Objetos |
|---|---|---|---|
| A | 0, 0, 0 | la lista de 5 y la tarjeta de código, dentro del campo | 5 esferas con nombre, tarjeta blanca, anillo tan (el for) |
| C | 0,6, 0, −4,2 | adentro del for (fondo negro) | tubo de vidrio con 5 esferas blancas, anillo tan |
| D | 2,7, 0, −1,2 | range() crea números de a uno | una esfera negra grande |

## Plano por plano
| Línea | Inicio | Plano y ángulo | Movimiento | Qué aparece | Sonido |
|---|---|---|---|---|---|
| l01 | 0,4 | general en picado rasante | push-in lento | título + firma, campo de esferas | boom de apertura |
| l02 | 3,8 | medio frontal de la fila | grúa que baja (0,9 s) | el campo se hunde en ola; 5 nombres | viaje + aterriza + ticks |
| l03 | 8,2 | tarjeta de frente | dolly out corto; en "mil", zoom out a general | 5 print a mano → 1000 líneas; el campo vuelve | tipeo, viaje |
| l04 | 12,8 | tarjeta de frente | dolly in | el campo se hunde; el for en tres líneas | viaje |
| l05 | 17,5 | medio a la altura de la fila | grúa corta + travelling lateral | el anillo salta de esfera en esfera: "Hola Ana"… | un pop por saludo |
| l06 | 23,2 | frente al anillo → contrapicado del tubo | lo atraviesa (pasa a negro) | tubo con 5 esferas | viaje + aterriza |
| l07 | 25,6 | contrapicado | quieta; dolly in en "termina" | cae una esfera por "próximo"; vacío; "fin" | ticks, error suave, resultado |
| l08 | 32,7 | picado casi cenital | latigazo + giro lento | range(1_000_000_000), 48 bytes, números de a uno | viaje, ticks |
| l09 | 39,4 | general alto → tarjeta | grúa arriba; baja en "cambia" | onda de luz por el campo; la lista pasa a range(1_000_000) | resultado, viaje, tipeo |
| CTA | 44,8 | CTA centrado | corte | CTA + firma | succión → boom → chinn |

## Medido (después del render)
- Cámara en movimiento la mayor parte del tiempo; retención mediana 0,9 s (meta 1–4 s): el reel es más dinámico a propósito, como las referencias.
- Brillo medio 0,63: fuera de la meta (pensada para fondo negro). Esperable en el tema claro.
- `arrastre.py` marca "diapositiva" en los límites de escena: falsa alarma en fondo blanco (los cuadros a ambos lados son continuos, revisado a mano).
