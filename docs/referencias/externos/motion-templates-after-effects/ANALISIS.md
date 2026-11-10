# Desglose de referencia — Motion Templates (After Effects) — «Put your ideas in motion»

> Referencia de motion graphics que pasó Ayrton (2026-11-09), guardada en `assets/referencias/motion-templates-after-effects.mp4`. Cortes, ritmo y volumen: **medidos** por `engine/analisis/previo/analizar_video.py` (histórico; hoy `engine/analisis/medir.py`). Planos, movimientos y transiciones: **leídos mirando los cuadros** (en motion graphics 2D las etiquetas automáticas de movimiento no sirven: se mueven los elementos, no una cámara). Vocabulario: `docs/GLOSARIO-EDICION.md` y `docs/MOVIMIENTO.md`. Hojas de cuadros locales en `docs/referencias/analisis/motion-templates-after-effects/` (no van a git; se regeneran con `./reel analizar`).

## Ficha
- **Archivo:** `assets/referencias/motion-templates-after-effects.mp4` · 720x1280 · 60 fps · 15 s
- **Fuente:** Pinterest (archivo adjuntado por Ayrton; sin link directo)
- **Qué queremos aprender:** estructura técnica: planos, transiciones, movimientos de cámara, ritmo y sonido, para usarlos en próximos reels.

## 1. En una frase
Promo de una tienda de plantillas de motion: un texto simple se convierte en un mundo de tarjetas de fotos que vuelan en 3D, con cortes casi cada 0,25 s sobre el ritmo, y cierra con una tarjeta quieta de descarga.

## 2. Estructura narrativa
| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Hook | 0–2,2 s | Texto «Put your ideas in motion» y un cursor; silencio de 0,45 s antes del clic |
| Desarrollo | 2,2–12 s | El clic despega las tarjetas; montaje vertiginoso de tarjetas, abanico, collage, pila de capas, carpetas |
| Payoff | 10,4–12 s | Push-in del collage hacia el cierre |
| CTA | 12–15 s | Tarjeta blanca: «Download Motion Templates» + ícono de descarga + URL, 3 s quietos |

## 3. Guion técnico (planos y transiciones)
| # | Tiempo | Qué se ve | Movimiento / transición de salida | Texto |
|---|---|---|---|---|
| P1 | 0–3,8 | Texto negro sobre blanco que crece palabra por palabra; una foto aparece dentro de la línea; a los 2,3 s entra un cursor y hace clic en una tarjeta gris: la foto se despega como tarjeta 3D con perspectiva y otras tarjetas flotan a distintas profundidades alrededor del texto | Pull-out suave y paralaje (cada tarjeta a otra profundidad) → corte en el pico | «Put your ideas in motion» |
| P2–P4 | 3,8–4,9 | Tres cortes de 0,23 s: tarjetas (póster THE SMITHS, perro, lentes de sol) cruzan el cuadro de lado a lado y se agrandan hasta llenarlo | Latigazo de tarjetas; cada corte cae sobre un golpe de sonido | — |
| P5 | 4,9–5,6 | La tarjeta del perro crece hasta ser el fondo; íconos de apps (Fotos, Música, emoji) aparecen sobre vidrio a la izquierda | Zoom a través de un objeto: la tarjeta se vuelve el mundo | — |
| P6 | 5,6–6,3 | Fondo negro, abanico de tarjetas de colores que gira en 3D | Corte seco sobre golpe | — |
| P7–P8 | 6,3–7,1 | Collage en grilla de imágenes; a los 6,5 s las teselas salen deslizándose y una tesela azul con forma de blob crece hasta llenar todo | Forma que se convierte en la siguiente escena (match por forma) | «BIG» |
| P9–P10 | 7,1–8,2 | Pila vertical de tarjetas (THE NET SOCIETY, VEED, PIN…): la cámara baja recorriéndola; cada tarjeta roza el borde y deja ver la siguiente | Tilt down a través de capas apiladas en profundidad | — |
| P11 | 8,2–9,0 | Ventana blanca con carpetas azules («Folder Name»); una tarjeta cae dentro de una carpeta; cursor | Metáfora de interfaz de computadora | «Folder Name» |
| P12–P14 | 9,0–10,4 | Collage de fotos que se acercan y alejan en mosaico, cada imagen escalonada | Zoom colectivo con escalonado | «LK ZOOM» |
| P15 | 10,4–12,0 | Push-in del collage con fundido por negro | Push-in → fundido | — |
| P16 | 12–15 | Fondo blanco: «Download Motion Templates» en gris que pasa a negro, ícono de descarga que se llena de azul, «velvele.store» en azul | Texto que se revela de gris a color; 3 s de quietud para leer el CTA | «Download Motion Templates» · «velvele.store» |

## 4. Ritmo (medido)
- 16 planos · **59.9 cortes/min** · plano medio 0.94 s (mediana 0.57 s; más corto 0.23 s, más largo 3.8 s) → ritmo **vertiginoso**.

## 5. Sonido
- Volumen integrado **−13,4 LUFS**, rango dinámico muy grande (≈81 dB: hay silencios casi totales).
- **Silencio de 1,71 a 2,16 s** justo antes del clic del cursor; el primer golpe fuerte cae en 2,16 s. Es la «coma dramática» de `docs/MOVIMIENTO.md`.
- **Golpes cada ≈0,32 s** de 3,1 a 9,9 s (17 golpes medidos); los cortes de 3,80, 4,04, 4,27, 4,87 y 5,61 s caen a ±0,1 s de un golpe: montaje sobre el ritmo. Mezcla de golpes medios (impactos) y brillantes (chasquidos / whooshes). Después de 10 s el audio se abre y queda un cierre limpio.

## 6. Técnicas para tomar
| Técnica | Cómo se hace | Cómo la hacemos en Claqueta |
|---|---|---|
| Cursor que dispara la acción | Silencio → clic → la foto se despega como tarjeta (causa y efecto en el mismo cuadro) | `dinamismo.cursor` + toma `mover` de camara3d; golpe y silencio en `sfx_events.py` |
| Tarjetas 3D a distintas profundidades | Planos con foto a diferentes z, la cámara se desplaza y el paralaje da la sensación 3D | `cartel()` con textura de imagen y `rig.toma` con travelling (ya está en `_demo-camara3d`) |
| Cortes cada 0,25 s sobre el ritmo | Montaje en ráfaga justo en el momento álgido, no en todo el video | `costuras` `latigazo` + golpes de `sfx_events.py` en cada corte; ver patrón de ritmo en `../../SINTESIS.md` |
| Objeto → mundo | Una tarjeta crece hasta llenar el cuadro y pasa a ser la escena siguiente | Toma `mover` con ease `entrada` + `destello`/corte (la receta «zoom through») |
| Pila de capas con tilt down | Tarjetas apiladas en z y una cámara que baja rozándolas | Nuevo set 3D: planos apilados + `rig.toma` `mover` hacia abajo (a armar) |
| Cierre quieto y legible | 3 s sin movimiento, texto que se revela gris → color, firma/URL en el color de acento | Firma `@ayrtonnacer` en `var(--acc)`; `data-a` para el revelado |

## 7. Qué NO copiar
Las fotos y portadas de terceros (THE SMITHS, perro, lentes, VEED, PIN…), la marca velvele.store, la paleta blanco/negro/azul y la tipografía de ellos. Nuestras tarjetas llevan contenido propio (código, comandos, diagramas) con IBM Plex y los colores de `cyber.css`.

## 8. Ideas para nuestros reels
- **Cifrado César / hash:** letras o bloques como tarjetas 3D en pila; la cámara baja por la pila para mostrar cada paso.
- **Permisos de Linux:** metáfora de carpetas (como P11): una tarjeta «permiso» cae en cada carpeta.
- **Cierre con silencio previo:** una pausa de 0,4 s antes del payoff, como el silencio antes del clic.

## Datos crudos
- `INFORME.md` y `metricas.json` de esta carpeta (medidos con `medir.py`). Resumen de patrones de todas las referencias: `referencias/SINTESIS.md`.
