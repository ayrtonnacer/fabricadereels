---
tipo: concepto
tema: "qué es un tensor (y por qué importa en machine learning)"
concepto_unico: "Un tensor son números ordenados que ubicás con N índices; ese N es lo que lo define."
duracion_objetivo_s: 48
cierre: cta
loop_principal: "¿Cuántos datos necesitás para ubicar un número?"
cierre_loop: "Esa cantidad de índices es lo que define al tensor."
verificado: sí   # GfG, Wikipedia, Towards Data Science (ver fuentes/LEEME.md)
version: 2 (2026-11-12)   # rehecho: la v1 copió la estructura del short de referencia; las referencias se usan para ver CÓMO se explica, no para repetir su guion
---
Ángulo: **ubicar un número**. Cada concepto responde a "¿cuántos datos hacen falta para decir dónde está?" (analogía propia, sin caras ni cubos de referencia). El tensor aparece como el nombre general, no como "algo más grande que una matriz".

| # | escena | pantalla | voz | s aprox. |
|---|--------|----------|-----|---|
| 1 | gancho | un número resaltado (rojo) dentro de una grilla enorme que se pierde en profundidad; "¿cuántos datos?" | ¿Cuántos datos necesitás para ubicar un número? | 0–3 |
| 2 | escalar | un número solo, sin nada alrededor; chip "0 índices" | Si hay uno solo, ninguno. Eso es un escalar. | 3–8 |
| 3 | vector | fila de números; el resaltado pide un solo índice `[3]` | En una fila, uno: la posición. Es un vector. | 8–13 |
| 4 | matriz | planilla; el resaltado pide fila y columna `[2, 4]` | En una planilla, dos: fila y columna. Una matriz. | 13–18 |
| 5 | tensor | la planilla se repite en profundidad (hojas); el resaltado pide hoja, fila, columna `[1, 2, 4]` | Con tres o más, aparece el tensor. Y todos son tensores: cambia la cantidad de índices. | 18–26 |
| 6 | foto | una foto suave (paisaje en grises, nada pixelado) que al acercarse se descompone en números y canales; índices `[fila, columna, canal]` | Una foto en color pide tres: fila, columna y canal. | 26–31 |
| 7 | para qué | lote de fotos como pila; chip con la forma; la GPU procesa todo junto (barrido de luz sobre toda la pila) | Un lote de fotos, cuatro. Y la GPU los procesa todos juntos. | 31–36 |
| 8 | detalle | dos formas que no encajan (bloque error ✕); rótulo "física" vs "ML" | Por eso importa la forma: si no coincide, el modelo ni arranca. Ojo: en física, un tensor tiene reglas extra. Acá, es el arreglo. | 36–44 |
| 9 | payoff | el número del gancho, ahora con sus N índices al lado, el N en rojo | Esa cantidad de índices es lo que define al tensor. | 44–48 |
| 10 | cierre | CTA grande, firma chica debajo, chinn | Dale me gusta y seguime para aprender más de machine learning. | 48–53 |

Palabras de voz ≈ 125 → ~53 s a ~2,4 pal/s (en el límite: si pasa, se corta la escena 8 o se baja a 5 escenas). Loop: se abre en el hook (¿cuántos datos?) y se cierra en el payoff antes del CTA.
Cámara (resumen, a detallar en `plan.md` con el OK): un solo viaje continuo en el eje z por los objetos (número → fila → planilla → hojas), una retención por concepto, whoosh en el pico de cada viaje; la foto se acerca hasta descomponerse en números; el payoff vuelve a la pose del gancho.
Detalle de profesional (escena 8): en física, un tensor además debe transformarse con reglas definidas al cambiar de coordenadas (Wikipedia); en ML es un arreglo multidimensional.
