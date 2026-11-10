# Desglose de referencia — Promo de marca «Every Brand Starts as a Blank Space» (video largo)

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/pinterest-791437334567656517.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/pinterest-791437334567656517/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/pinterest-791437334567656517.mp4` · 720x1280 · 30 fps · 50 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Un promo de estudio de diseño con estructura problema → solución → resultados → llamada, hecho solo con tipografía, íconos, cursor y un fondo rojo líquido que alterna con escenas blancas.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–3 s | «Every Brand Starts as a…» con cursor que resalta «Starts» |
| Problema | 3–10 s | «Blank Space», mensajes malos («Unclear Message», «Inconsistent visuals», «Low engagement») caen en un tacho de basura |
| Giro | 10–19 s | «Then Clarity Enters»; aparece un ojo y se rodea de íconos (Identity, Movement, Story, Recognition); «Come alive» |
| Prueba | 19–33 s | Logos de clientes y estadísticas (+2500 followers, CTR 3.3x, +10000 impressions, +400 engagement) |
| Beneficios | 33–44 s | «More Reach / More Retention / More Trust», muro de marcas, «WORLDWIDE» |
| CTA | 44–50 s | «If you want to grow in 2026, make your brand MOVE» → logo del estudio |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1–P2 | 0–2,1 | Fondo rojo con manchas oscuras que se deforman; el texto aparece letra por letra; el cursor se posa en «Starts» y un círculo claro crece desde ahí hasta formar la etiqueta blanca | Revelado desde el punto del cursor (iris desde el clic) | «Every Brand Starts as a» |
| P3 | 2,1–3,1 | Fondo blanco: «Blank Space» en gris, entra con escala grande que se asienta | Cambio de color de todo el fondo (rojo → blanco) como corte | «Blank Space» |
| P4 | 3,1–8,0 | Fondo rojo: tarjetas tipo interfaz caen una por una dentro de un tacho negro, la tapa se abre y las traga | Forma del objeto (la tapa) barre la pantalla a blanco: wipe con la forma del tacho | «Unclear Message» «Inconsistent visuals» «Low engagement» |
| P5 | 8,0–9,8 | Blanco: «Then … Enters» con cursor; el recuadro «Clarity» con borde punteado entra desde la derecha | Corte limpio rojo/blanco | «Then Clarity Enters» |
| P6 | 9,8–19,0 | Un ojo se abre sobre fondo rojo; íconos en círculos de vidrio aparecen uno a uno alrededor (huella, flechas, libro, medalla); el ojo parpadea; texto «Come alive» | Escalonado de íconos con rebote leve; el ojo es la figura fija y los íconos orbitan | «Identity» «Movement» «Story» «Recognition» «Come alive» |
| P7–P9 | 19,0–25,0 | Logos de clientes sobre colores planos (azul oscuro, verde azulado, gris claro, negro): cada logo entra con un breve zoom y una captura de su web | Corte seco por logo (≈1,2 s cada uno); fundido por negro hacia lo siguiente | Logos |
| P10 | 25,0–32,2 | Fondo negro y logo dorado que se cierra a la ola blanca inferior; sobre el rojo aparecen círculos de íconos con contadores | Ola blanca líquida que sube desde abajo y empuja el contenido | «+2500 Followers» «CTR up to 3.3x» «+10000 impressions» «+400 Engagement» |
| P11–P13 | 32,2–46,0 | Blanco: frases de beneficio con una palabra en rojo; muro de logos flotando con inclinación; «WORLDWIDE» con un globo dentro de la O | Cortes de color rojo ↔ blanco; palabra clave resaltada | «More Reach» «More Retention» «More Trust» «Brands» «WORLDWIDE» |
| P14 | 46,0–50,0 | Fondo blanco: «Make your brand MOVE» (MOVE gigante en rojo), luego el logo del estudio quieto 4 s | Cierre quieto con el logo | «Make Your Brand MOVE» · logo |

## 4. Ritmo (medido)
- 14 planos · **15.6 cortes/min** · plano medio 3.57 s (mediana 3.2 s; más corto 1.03 s, más largo 9.21 s) → ritmo **pausado**.

## 5. Sonido
- Volumen **−14,5 LUFS**, pico −0,6 dBFS, rango ≈24 dB. Cama de música constante con **75 golpes medidos** (≈cada 0,26–0,35 s) que funcionan como pulso de UI (clics, ticks) más que como efectos.
- **Golpes graves** en los cambios de sección (7,2 s, 12,0 s, 13,4 s, 14,1 s). Sin silencios largos.
- Los cortes rojo ↔ blanco caen sobre el pulso; los contadores y los íconos entran en el pulso, no entre ellos.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Fondo líquido animado | Un degradado rojo con manchas oscuras que se deforman todo el tiempo: es el «aire» de la escena | Fondo de tema con `bg()` de lib.js ya se mueve; falta una variante líquida (shader/canvas) |
| Alternancia de color como transición | El fondo pasa de rojo a blanco y vuelve en cada beat: el cambio de color ES el corte | `salida: "corte"` + dos variantes de fondo por escena (oscuro/claro) con `var(--bg)` |
| Wipe con la forma de un objeto | La tapa del tacho barre la pantalla; un círculo claro crece desde el cursor | Costura nueva «iris/forma» (a implementar; hoy solo hay curva, zoom, foco, latigazo, oscuro) |
| Cursor como personaje | El cursor señala, hace clic y arrastra; es el lenguaje de la interfaz | `dinamismo.cursor` |
| Metáfora visual por problema | Mensajes malos → tacho; claridad → ojo; resultados → contadores en círculos | Elegir UNA metáfora 3D por reel (objeto físico con escala real) |
| Palabra clave en el acento | En cada frase una palabra va en rojo/color distinto | Regla 2 de CLAUDE.md: lo que se debe recordar, en `var(--acc)` |
| Contadores con círculo de ícono | «+2500», «3.3x» suben en una ola que empuja | `data-type`/contador en `custom()`; ola con `clip-path` |

## 7. Qué NO copiar
Estructura de venta (logos de clientes, estadísticas inventadas de marketing, «Download»/URL), la paleta rojo/blanco, el tacho como metáfora (es de ellos para «mensajes malos»), los logos y capturas de terceros.

## 8. Ideas para nuestros reels
- **Error común → solución:** una «tarjeta de error» cae en un tacho y la regla correcta entra como tarjeta verde (para el reel «chmod 777»).
- **Un solo objeto fijo + íconos que orbitan** (como el ojo): una notebook con íconos de conceptos alrededor.
- Alternar fondo oscuro/claro por beat si el reel necesita ritmo sin cámara 3D.

## Datos crudos
- `docs/referencias/analisis/pinterest-791437334567656517/planos.json` y `audio.json` (medidos). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.
