---
tipo: concepto (didáctico)
tema: "qué es un tensor y para qué lo usa la inteligencia artificial"
concepto_unico: "Un tensor es una caja de números con las dimensiones que haga falta; así la máquina guarda todo."
duracion_objetivo_s: 55
cierre: cta
loop_principal: "Para una máquina, una foto, una canción y un texto son lo mismo (¿por qué?)."
cierre_loop: "Por eso, para ella, todo es lo mismo: tensores."
verificado: sí
version: 5 (2026-11-12)   # nivel didáctico del texto que pasó Ayrton (docs/material/2026-11-12-que-es-un-tensor.txt)
---
## Criterio
La v4 era correcta pero técnica (lote, capas, pérdida, PyTorch vs TensorFlow): no se entendía si no sabías ya. La v5 explica desde lo cotidiano, con **un solo ejemplo que crece de a una dimensión**: un píxel → una fila → una foto en blanco y negro → una foto en color → un video. Cada paso suma un eje y es un uso real. Después, los otros datos (sonido, texto) y qué hace la máquina con eso.
Recurso didáctico fijo: arriba de la pantalla, un **mapa de dimensiones** `0D · 1D · 2D · 3D · 4D` que se va encendiendo (el paso actual en rojo) y acumula lo aprendido.

| # | escena | voz | pantalla y cámara | s aprox. |
|---|--------|-----|---|---|
| 1 | gancho | Para una máquina, una foto, una canción y un texto son lo mismo. | tres objetos en línea (paisaje suave, onda de sonido, renglón de texto) que se convierten en el mismo bloque de números; acercamiento | 0–4 |
| 2 | escalar | Empecemos por un número: el brillo de un píxel. Es un escalar. | la cámara entra a la foto hasta un solo punto con su número (128) y su tono de gris; mapa: **0D** | 4–9 |
| 3 | vector | Una fila de píxeles es una lista: un vector. | se abre la fila de ese punto; mapa: **1D** | 9–12 |
| 4 | matriz | Una foto en blanco y negro es una cuadrícula, como una planilla: una matriz. | la fila se completa en la foto entera (se ve como foto de lejos y como planilla de cerca); mapa: **2D** | 12–17 |
| 5 | tensor | En color son tres cuadrículas apiladas: un cubo de números. Eso es un tensor. | se separan tres capas (tinte rojo, verde, azul) y forman un cubo; órbita para ver la profundidad; mapa: **3D** | 17–23 |
| 6 | video | Y un video suma el tiempo: cubos uno detrás de otro. | los cubos se alinean en el tiempo, con un cursor de reproducción; mapa: **4D** | 23–27 |
| 7 | definición | Un tensor es eso: números ordenados en todas las dimensiones que necesites. | todo el recorrido en un plano (punto, fila, foto, cubo, video), cada uno con su 0D…4D | 27–32 |
| 8 | otros datos | El sonido es una lista larga de números; un texto, palabras convertidas en números. | la onda se vuelve una fila de números (1D); cada palabra se vuelve una fila de números (2D) | 32–38 |
| 9 | usos | Con cuentas sobre tensores, una máquina distingue caras, entiende tu voz o te contesta. | los bloques entran a un modelo y salen tres resultados: un recuadro sobre la foto, texto de lo que se dijo, una respuesta | 38–44 |
| 10 | payoff | Por eso, para ella, todo es lo mismo: tensores. Y por eso Google le puso TensorFlow a su librería. | vuelven los tres objetos del gancho, ya como bloques iguales; aparece la palabra "TensorFlow" (texto, sin logo) | 44–50 |
| 11 | cierre | Dale me gusta y seguime para aprender más sobre inteligencia artificial. | CTA grande, firma chica debajo, chinn | 50–55 |

143 palabras; lectura medida: 42,6 s de voz, ~48 s con pausas → video de ~55 s (2,6 pal/s).
Voz: sin "IA", "red", "arranca", "rojo" ni "herramienta" (r cortas que suenan mal). Lectura: `docs/material/pronunciacion/tensores-guion-v5-lectura.mp3`.
Visual: nada pixelado como protagonista; la foto es un paisaje suave y la cuadrícula solo aparece al acercarse (es lo que se enseña). Los tintes rojo/verde/azul de las capas son la única excepción a la paleta y tienen significado (los canales).
Datos: brillo de un píxel 0–255 en 8 bits; foto en color = alto × ancho × 3; video = cuadros × alto × ancho × 3; audio = muestras en el tiempo; texto = palabras convertidas en vectores (embeddings); TensorFlow se llama así por los tensores que "fluyen" por el cálculo.
