# Desglose de referencia — Explicador largo de producto (agentes de IA, 104 s) con subtítulos por palabra

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-ref-5.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analizar_video.py`. Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `referencias/motion-ref-5/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-ref-5.mp4` · 720x1280 · 30 fps · 1:44
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un explicador de casi dos minutos: una mascota de píxeles guía el relato (problema → herramienta → demo → capacidades → precio → escala → llamada), con tarjetas de interfaz reales y subtítulos de dos a seis palabras que cambian de a una.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–9,6 s | Mascota con íconos de herramientas: «every AI agent you use right now…» |
| Problema | 9,6–28 s | «…has a live data problem»; razona con datos de entrenamiento viejos; «there is a tool that feeds your agent with live premium data you can trust» |
| Solución | 28–42 s | La mascota pregunta, aparecen tarjetas «Company Headcount», «Work Email», «A Domain's Backlinks» con precios |
| Demo | 42–78 s | «One setup prompt drops a skill into your agent»; más de 40 proveedores de datos; una sola clave, sin suscripciones; tarjetas «Rank Tracking API», «Jobs API» |
| Beneficios | 78–92 s | Código con error («A failed call costs nothing») y precio oficial $129 vs $0,66 («you only pay for what you actually use») |
| Escala | 92–98 s | Globo y «over 1900 premium data endpoints from all of the…» |
| CTA | 98–104,5 s | «Comment "DATA" and I will send you the direct link» y «Make sure you follow…» |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–16 | Fondo gris claro; una mascota naranja de píxeles aparece sola, luego con íconos de herramientas que se encienden uno por uno; texto que cambia de palabra a palabra abajo; marca de agua del autor | Mascota quieta con elementos que aparecen; subtítulo de dos a seis palabras que cambia de a una | «every AI agent you use right now has a live data problem» |
| P2 | 16–34 | La mascota baja por un hilo; una ventana de terminal oscura muestra a la mascota razonando; luego cartel con personas «most people have never seen what an agent…»; ventana del producto (Glasser.AI) y captura de la web que entra | Corte a una captura de pantalla en tarjeta flotante con sombra suave | «it reasons from training data that is months old and guesses» |
| P3 | 34–79 | Tarjetas de interfaz (detalle con precio) en un carril; la mascota con íconos de prueba; luego una grilla de proveedores; tarjetas «Rank Tracking API», «Jobs API», «LinkedIn Data API» con iconos y botones; mascota con una tarjeta en la mano | Las tarjetas entran apiladas y se reemplazan; cada una se sostiene 1,5–2 s | «ask it to pull the keywords driving the most…», «ask it to get verified emails for an entire list of LinkedIn profiles» |
| P4–P5 | 79–86 | La mascota con una tarjeta; luego un bloque de código oscuro con un aviso rojo | Corte rápido a una vista de código | «A failed call costs nothing» · «An empty result costs nothing» |
| P6 | 86–104,5 | Tarjetas de precio ($129 vs $0,66); globo terráqueo que gira con la grilla de proveedores; «Comment DATA» y el logo con corona | Globo con giro continuo; el cierre queda quieto | «you only pay when you get real data back» · «Comment "DATA"» |

## 4. Ritmo (medido)
- 6 planos · **2.9 cortes/min** · plano medio 17.41 s (mediana 17.15 s; más corto 3.67 s, más largo 44.33 s) → ritmo **contemplativo**.

## 5. Sonido
- Volumen **−11,7 LUFS** (fuerte), rango ≈15 dB, pico dentro del límite. **46 o más golpes medidos**, casi todos «medios» cada ≈1,5–2,5 s: clics de interfaz que marcan cada tarjeta y cada cambio de palabra.
- Locución continua (no hay silencios > 0,4 s): la música y los tics van debajo.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Mascota-guía | Un personaje fijo que acompaña el relato y señala lo que importa; cambia de pose, no de lugar | Un objeto 3D fijo como guía (el paquete de datos, un candado); regla de variedad: uno por reel |
| Subtítulos por palabra | Dos a seis palabras y la clave en negrita; cambian al ritmo de la voz | `docs/DINAMISMO.md` (por ahora sin subtítulos por pedido de Ayrton); si los pide: pastillas por palabra con tiempos reales |
| Tarjetas de producto flotantes | Capturas o maquetas de interfaz con sombra suave que se apilan y se reemplazan | `cartel()` de varias líneas con borde del tema; mejor construir la interfaz en HTML que usar capturas ajenas |
| Contraste de costo | Dos tarjetas de precio lado a lado ($129 vs $0,66) | Chips comparativos en rojo/verde; cifras verificadas |
| Cierre con llamada a la acción | «Comment DATA and I will send you the link» para generar interacción | Nuestra regla 3: «Dale like» y «Seguime para aprender más de <tema>»; no pedir comentarios clave |

## 7. Qué NO copiar
El producto (Glasser.AI, InsiderForce), los precios, la mascota de píxeles, la marca de agua y el CTA de «comentá la palabra para recibir el link» (engagement-bait). El nivel de −11,7 LUFS: nuestro objetivo es −14. Y la duración (104 s): un reel nuestro termina en 60 s; esto es una serie de 2 reels.

## 8. Ideas para nuestros reels
- **Un reel largo se parte en serie** (parte 1/2) como hicimos con el artículo de Cisco, en vez de estirar a 104 s.
- **Tarjetas apiladas con una frase de definición** (como «Rank Tracking API») para presentar protocolos o comandos con su resultado.

## Datos crudos
- `referencias/motion-ref-5/planos.json` y `audio.json` (medidos). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.
