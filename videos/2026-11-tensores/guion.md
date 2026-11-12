---
tipo: concepto
tema: "escalar, vector, matriz y tensor en machine learning"
concepto_unico: "Todo dato en ML es un arreglo de números; su forma (shape) decide si el modelo funciona."
duracion_objetivo_s: 45
cierre: cta
loop_principal: "¿Cuántas dimensiones tiene un lote de fotos?"
cierre_loop: "Cuatro: lote, canales, alto y ancho."
verificado: sí   # GfG, Wikipedia y Towards Data Science; ver fuentes/LEEME.md
---
Fuentes pasadas por Ayrton (leídas GfG y Wikipedia; Medium, TDS, Kaggle y Reddit no accesibles): GeeksforGeeks, Wikipedia "Tensor", Reddit r/physicsmemes, Kaggle (paulrohan2020), Medium (malickiart), Towards Data Science.

| # | escena | voz | s |
|---|--------|-----|---|
| 1 | gancho | ¿Qué forma tiene tu cara para una IA? | 0–3,0 |
| 2 | tipos | Una IA no ve: solo multiplica números. | 3,3 |
| 3 | tipos | Un número solo es un escalar: la pérdida del modelo. | 5,9 |
| 4 | tipos | Una lista es un vector: las características de un dato. | 9,4 |
| 5 | tipos | Una tabla es una matriz: los pesos de una capa. | 12,9 |
| 6 | tensor | Con más ejes, un tensor. Tu foto en color tiene tres: alto, ancho y canales. | 16,5 |
| 7 | tensor | Apilá treinta y dos fotos y el modelo recibe cuatro ejes: un lote. | 21,8 |
| 8 | red | En la red, la entrada y los pesos son tensores. Cada capa los transforma. | 26,3 |
| 9 | detalle | Ojo: acá, rango es la cantidad de ejes. En álgebra lineal es otra cosa. | 31,5 |
| 10 | detalle | Y si las formas no encajan, el modelo ni arranca. | 36,3 |
| 11 | payoff | Tu cara: tres ejes. Un lote de caras: cuatro. | 39,9 |
| 12 | cierre | Dale me gusta y seguime para aprender más de machine learning. | 44,4 |

Versión final (2026-11-12): hook personal (idea del short de referencia y de cómo se lo explicó Ayrton a un amigo), "para qué sirve" = la entrada y los pesos de una red son tensores, detalle de profesional = "rango" en ML vs álgebra lineal, y error de forma (canales primero vs canales al final). Loop: la cara del hook vuelve en el payoff con sus ejes. 131 palabras, 48,6 s. Cámara y efectos: `plan.md`.
