---
tipo: concepto
tema: "qué es un tensor y para qué sirve en inteligencia artificial"
concepto_unico: "Un tensor son números ubicados con N índices, y la IA los usa para todo."
duracion_objetivo_s: 58
cierre: cta
loop_principal: "¿Cuántos datos necesitás para ubicar un número?"
cierre_loop: "Esa cantidad de índices es lo que define al tensor."
verificado: sí   # GfG, Wikipedia, Towards Data Science (ver fuentes/LEEME.md)
version: 3 (2026-11-12)   # v2 + "para qué sirve" (datos reales, aplicaciones, por qué se necesita); CTA sobre inteligencia artificial
---
Ángulo: **ubicar un número** (analogía propia). Dos mitades: (1) qué ES un tensor (escenas 1–5) y (2) PARA QUÉ sirve y por qué hay que dominarlo en IA (escenas 6–9).

| # | escena | pantalla | voz | s aprox. |
|---|--------|----------|-----|---|
| 1 | gancho | un número resaltado (rojo) en una grilla que se pierde en profundidad | ¿Cuántos datos necesitás para ubicar un número? | 0–3 |
| 2 | escalar | un número solo; "0 índices" | Si hay uno solo, ninguno: es un escalar. | 3–7 |
| 3 | vector | fila; el resaltado pide `[3]` | En una fila, uno: es un vector. | 7–11 |
| 4 | matriz | planilla; el resaltado pide `[2, 4]` | En una planilla, dos: es una matriz. | 11–15 |
| 5 | tensor | la planilla se repite en profundidad; el resaltado pide `[1, 2, 4]` | Con tres o más, es un tensor. Y todos lo son: cambia la cantidad de índices. | 15–22 |
| 6 | datos reales | foto (suave, en grises) `(alto, ancho, 3)`, video (pila de cuadros) suma el tiempo, texto (filas de palabras con su vector) | Los datos reales ya vienen así: una foto tiene fila, columna y color; un video suma el tiempo; un texto, palabras. | 22–30 |
| 7 | qué se puede hacer | el tensor entra a una red y sale: foto → barras de probabilidad (reconoce), texto → texto (traduce), matriz usuarios × productos con una celda que se enciende (recomienda) | Con eso, una red reconoce caras, traduce idiomas o recomienda qué ver. | 30–36 |
| 8 | por qué hay que saberlo | una pila enorme de tensores y un barrido de luz que los calcula todos a la vez (GPU) | Entrenar un modelo es operar tensores, y las GPU los calculan por miles a la vez. | 36–43 |
| 9 | la forma | dos formas que no encajan: bloque error ✕ | Por eso hay que dominar la forma: si no coincide entre capas, el modelo ni arranca. | 43–49 |
| 10 | detalle pro | rótulos "física" y "IA" | Ojo: en física, un tensor tiene reglas extra. En inteligencia artificial, es la tabla de números. | 49–55 |
| 11 | payoff | el número del gancho con sus N índices al lado, N en rojo | Esa cantidad de índices es lo que define al tensor. | 55–59 |
| 12 | cierre | CTA grande, firma chica debajo, chinn | Dale me gusta y seguime para aprender más sobre inteligencia artificial. | 59–64 |

~146 palabras → ~60 s (~2,4 pal/s). Si querés más corto: sacar la escena 10 (detalle de física) y queda ~54 s.
Respuesta al "para qué": (a) todo dato real —imagen, video, texto, audio— se convierte en tensor; (b) con eso se reconoce, traduce y recomienda; (c) entrenar es operar tensores y las GPU/TPU están hechas para eso en paralelo; (d) por eso la forma de los tensores es lo que más rompe un modelo.
Fuentes del "para qué": GfG (CNN para imágenes, transformers para NLP, GPUs), Towards Data Science (recomendadores con matriz usuarios × productos y un eje de contexto; imágenes RGB y video), Wikipedia (ML: tensor = arreglo multidimensional; física: leyes de transformación).
