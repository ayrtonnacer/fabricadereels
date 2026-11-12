---
tipo: concepto
tema: "qué es un tensor y para qué lo usa la inteligencia artificial"
concepto_unico: "Un modelo convierte una foto en un número, tensor por tensor."
duracion_objetivo_s: 50
cierre: cta
loop_principal: "Una foto = más de 150 mil números… ¿qué hace el modelo con ellos?"
cierre_loop: "De ciento cincuenta mil números a uno solo, tensor por tensor."
verificado: sí   # 224×224×3 = 150.528; PyTorch NCHW / TensorFlow NHWC por defecto; fuentes en fuentes/LEEME.md
version: 4 (2026-11-12, revisión con Opus)
---
## Por qué no cerraban la v2/v3
1. **Dos videos pegados**: primero la definición (escalar → tensor) y después una lista de aplicaciones. El "para qué" quedaba como agregado, no como respuesta.
2. **Aplicaciones abstractas** ("reconoce caras, traduce, recomienda"): se dicen pero no se ven funcionar.
3. **12 escenas, ~146 palabras**: más de una idea por reel.

## La idea de la v4: UN viaje
Se sigue **una foto real a través de un modelo**. En ese viaje aparecen los cuatro objetos **donde se usan de verdad**: la foto es un tensor, el lote suma un eje, los pesos son tensores, la salida es un vector y la pérdida es un escalar. La definición y el "para qué" son lo mismo. El escalar se presenta al principio (escalera) y vuelve al final como la pérdida: es el número que el entrenamiento achica.

| # | escena | voz | pantalla y cámara | s aprox. |
|---|--------|-----|---|---|
| 1 | gancho | Para un modelo, esta foto son más de ciento cincuenta mil números. | foto suave (paisaje de montañas en línea y grises, nada pixelado) y un contador que sube a **150.528**; la cámara entra a la foto hasta que se ve hecha de números | 0–3,5 |
| 2 | tensor | Ordenados en tres ejes: alto, ancho y color. Eso es un tensor. | la foto se separa en 3 placas (canales) en profundidad; ejes alto/ancho/canales; órbita | 3,5–8 |
| 3 | escalera | Cero ejes es un escalar; uno, un vector; dos, una matriz. Todos son tensores. | viaje en z: un número → una fila → una planilla → el bloque de la foto; chips 0 · 1 · 2 · 3 ejes | 8–14 |
| 4 | lote | El modelo toma treinta y dos fotos juntas: cuatro ejes. | 32 bloques en fila; forma `(32, 224, 224, 3)`; pull-back | 14–18 |
| 5 | capas | Cada capa las mezcla con sus pesos, que también son tensores. | el lote cruza 3 placas de pesos y en cada una cambia de forma (los chips de forma cambian); la cámara lo sigue en z | 18–23 |
| 6 | salida | Por cada foto sale un vector: una probabilidad por clase. | barras de probabilidad; la de "montaña" en rojo, 0,91 | 23–27 |
| 7 | pérdida | Y cuánto se equivocó queda en un escalar: la pérdida. Entrenar es achicarlo. | todo colapsa en un solo número que baja: 2,30 → 0,12 | 27–32 |
| 8 | la forma | Por eso la forma manda: si no encaja entre capas, el código falla. | dos formas que no encajan; bloque error ✕ | 32–37 |
| 9 | detalle pro | Ojo: PyTorch pone el color primero; TensorFlow, al final. | `(32, 3, 224, 224)` vs `(32, 224, 224, 3)` con el 3 en rojo | 37–41 |
| 10 | payoff | De ciento cincuenta mil números a uno solo, tensor por tensor. | pull-back largo: la foto en un extremo, el número en el otro y la cadena de tensores en el medio (todo el viaje en un plano) | 41–46 |
| 11 | cierre | Dale me gusta y seguime para aprender más sobre inteligencia artificial. | CTA grande, firma chica debajo, chinn | 46–50 |

126 palabras; lectura medida: 37,9 s de voz, ~43 s con pausas, ~50 s con respiros visuales (≈ 2,5 pal/s).
Voz: sin "IA" (se lee "ya"), sin "red" (la r inicial dura 23 ms) y sin "arranca"; PyTorch → "páitorch", TensorFlow → "tensorflou" (sin verificar). Lectura completa: `docs/material/pronunciacion/tensores-guion-v4-lectura.mp3`.
Datos: 224 × 224 × 3 = 150.528 (entrada estándar de ImageNet); la pérdida 2,30 ≈ ln(10) es la de un modelo que adivina al azar entre 10 clases; PyTorch usa (N, C, H, W) y TensorFlow/Keras (N, H, W, C) por defecto.
