# Plan de cámara — Qué son las variables en Python
Tiempos reales en `assets/tiempos.js` (salen de la voz). Poses calculadas para que lo que se lee caiga entre y 200 y 1100.

## El set
- **Idea del espacio**: un recorrido de etiquetas (placas tan con hilo blanco) que apuntan a valores (placas grises) sobre losas de "memoria".
- **Corriente**: hacia la **derecha** y al fondo (el reel anterior iba a la izquierda). Cierre: la cámara sube por encima del set y vuelve al gancho (el loop se cierra en el mismo lugar donde se abrió).

| Estación | Posición (x, y, z) m | Idea | Objetos (el tan es la etiqueta) |
|---|---|---|---|
| A | 0, 0, 0 | gancho / payoff: no es una caja | caja de línea + ✕, etiqueta "edad" colgada del 19 |
| B | 1,4, 0, −2,2 | qué es y cómo se crea | losa "memoria", 19, etiqueta "edad", código `edad = 19` |
| C | 2,5, 0, −2,0 | usar el nombre = usar el valor | `edad` (se da vuelta: 19) `+ 1` `= 20` |
| D | 3,6, 0, −4,6 | el tipo vive en el valor | 19 / "hola" / [1, 2] con int, str, list; la etiqueta salta al texto |
| E | 5,0, 0, −7,0 | dos nombres, un valor | 250 con "precio" y "total"; la copia fantasma se borra |

## Plano por plano
| Línea | Voz (s) | Estación | Plano y ángulo | Llegada | Qué aparece | Sonido |
|---|---|---|---|---|---|---|
| l01 | 0,35 | A | medio, tres cuartos, leve picado | portada; push-in lento | título + firma; ✕ caja en "caja" | boom; zumbido suave |
| l02 | 3,56 | B | medio frontal | travelling 0,85 s | etiqueta en "nombre", hilo en "apunta", 19 en "valor", rótulo "memoria" | viaje + aterriza; aparece |
| l03 | 8,15 | B | contrapicado cercano | dolly in 0,75 s | `edad = 19`: se enciende 19 en "crea", edad en "asocia" | tipeo; tic |
| l04–l05 | 14,1 | C | frontal | travelling lateral 0,8 s | `edad` en "nombre", se da vuelta (19) en "valor"; `+ 1` en "más"; `= 20` en "veinte" | viaje; aparece; resultado suave |
| l06–l07 | 21,6 | D | general en picado | travelling + grúa 0,85 s | 19, "hola", [1, 2] en su palabra con int/str/list; etiqueta en l07 | viaje + aterriza; tics |
| l08 | 29,0 | D | medio, leve picado | dolly in 0,8 s | la etiqueta se despega del 19 y se pega al texto ("pasar" → "texto") | viaje corto |
| l09 | 34,0 | D | contrapicado | 0,7 s | el 19 queda solo | — |
| l10 | 37,2 | E | medio tres cuartos | travelling 0,85 s | precio → 250; total en "dos", hilo en "mismo"; `total = precio` | viaje + aterriza; aparece |
| l11 | 40,4 | E | picado alto | grúa 0,8 s | copia fantasma en "copia" que se borra | zumbido suave; viaje |
| l12 | 44,6 | A | medio tres cuartos | grúa por encima del set y bajada (1,5 s) | la caja se borra en "guarda"; la etiqueta en tan en "nombra" | viaje + aterriza; resultado |
| CTA | 49,2 | — | CTA centrado | corte | CTA palabra por palabra; firma | succión → boom → chinn |

## Dinamismo (corrección de Ayrton 11-17, referencia medida en `docs/4-referencias/material/2026-11-17-ref-ig-dinamismo/`)
- Sin losas de soporte. Las retenciones ya no son quietas: **deriva orbital lenta** (≈ 10° y 8 % de acercamiento, < 100 px/s; el texto sigue legible). Los planos altos derivan alejándose para no recortar bordes.
- Etiquetas y valores **entran volando** desde fuera del cuadro (no solo por escala). Cámara en movimiento: 45 % de los cuadros (antes ≈ 20 %; la referencia: 75 %).
- Sonido: el "waaash" de la succión antes del CTA se cambió por el hit metálico real del banco (marca).

## Medido (`reel.py medir`)
- Fuera de meta: retención mediana 0,80 s (meta 1–4 s; a propósito: la deriva continua parte las retenciones, pedido de Ayrton) y brillo medio 0,01 (negro puro de la estética Scale: justificado).
- Arrastre bajo en 3,3 / 36,9 / 44,4 s: los límites de escena caen en medio de viajes rápidos (plano secuencia, sin corte real). 49,0 s = corte al CTA (permitido).
- Whisper: 95 % de palabras entendidas. "Si edad" se oía "si día" → la frase pasó a "Con edad igual a diecinueve".
