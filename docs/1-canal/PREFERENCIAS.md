# Preferencias de Ayrton (resumen para consultar ANTES de cada video)
Destilado de `docs/1-canal/BITACORA.md` (cronológico, con el detalle) y `docs/1-canal/DECISIONES.md`. **Se actualiza en cada tanda de indicaciones** y se repasa al empezar un video y antes de entregarlo; Ayrton no tiene que volver a aclararlo.

## Le gusta
- **Cámara de película al servicio del concepto** (2026-11-15): planos continuos (un objeto se transforma en el siguiente en vez de cortar), pocos movimientos clave y dinámicos, **pausas** sobre cada objeto nombrado, y planos generales que muestren las ideas juntas (ej.: escalar, vector y matriz vistos de lejos). Entradas con carácter y diseño de sonido en cada movimiento.
- Estética (**por defecto desde 2026-11-14**): **tema Scale** — negro puro, objetos 3D de línea gris, un solo acento Foundry Tan, Host Grotesk + Geist Mono, subtítulos con barra negra (reel de tensores, publicado y con buena respuesta). Línea roja (WiFi) y lima/azul quedan como temas alternativos en `engine/themes/`. **Piso de líneas en perspectiva** y el **gradiente** de fondo.
- **Profundidad real**: objetos 3D con perspectiva (le gustó cuando aparecieron los teléfonos en 3D); cámara que se mueve y revela. Prefiere **todo en three.js** (objetos, ondas, cables) mientras el render no se vuelva lento.
- Motion graphics con **movimiento de cámara** como protagonista de la profundidad.
- **Voz Daniela limpia** (sin efecto de radio) y sonido **limpio**: sin ruido de fondo; efectos puntuales con significado; **chinn** al aparecer el CTA; **sonido grave** (`boom-cinematico`) al inicio y al final; tipeo real de teclado.
- **Subtítulos** siempre (mucha gente mira en silencio), en zona segura.
- Cierre con **foco en el CTA**; la firma chica debajo.
- Que cada reel **demuestre que sabe** (portfolio para reclutadores): un detalle de profesional.
- Reels **rápidos de producir**.

## No le gusta / errores a no repetir
- **Cámara que se mueve todo el tiempo o zoom de más** (banco v4, 2026-11-15): confunde. La cámara se mueve **solo en los momentos clave** y **se queda quieta** cuando se nombra un objeto; **pausas** para que se lea. Nada de desenfocar lo que se explica.
- Elementos de fondo **sin sentido** (puntitos verdes, un "1" suelto flotando): todo lo decorativo tiene que significar algo.
- **Palabras sueltas** en la última línea (viudas/huérfanas).
- Ondas **cortadas** (sin continuidad); cables que **no tocan** el objeto.
- Texto del CTA que **no coincide con la voz**: debe decir "Dale like y seguime para aprender más de <tema>".
- Zoom a su usuario en el cierre; "guardalo"; efecto de radio / sonido sucio; estética roja o Anduril.
- Render lento (el motor viejo con 3D pesado): three.js solo simple (medido ≈ +1 s de render por segundo de video).
- Pronunciación mal: "WiFi" escrito "guifi" sonaba "gifi" → usar "uaifai" (pendiente que Ayrton elija de oído entre 3 variantes en `docs/4-referencias/material/pronunciacion/`).

## Flujo acordado
Link + indicaciones → guion (público: técnicos, principiantes, reclutadores) → **su OK** → plan numérico (metas de la biblia de estilo) → video → entrega. A futuro: publicar automáticamente en sus redes (no hacerlo sin que lo pida).

## Agregado 2026-11-09 (noche, 3)
- **Realismo con sentido**: las notebooks no llevan antena a la vista; los **cables tocan los objetos** (puertos, centro del globo); las ondas de radio no necesitan encajar justo.
- **Cero etiquetas obvias**: no rotular lo que se ve ("pared"); el espectador no es tonto.
- **Bits chicos y dentro de la pantalla**; sonido digital de interfaz para tipear 0 y 1 (el teclado solo para código); módem como guiño de "conexión"; hit metálico mejor que un whoosh suave en el cierre.
- **"WiFi" = "uaifai"** (aprobado). "router" = "ráuter" (a confirmar).
- CTA: "de <tema>" para temas de una palabra; "sobre <tema>" para frases largas.
- Pasa **investigación propia** (guías, artículos) para que la use y la deje documentada: `docs/5-tecnica/THREEJS.md`.

## Agregado 2026-11-10
- **Medir en vez de opinar**: prefiere parámetros técnicos replicables a percepciones subjetivas; quiere analizar videos de referencia (transiciones, cámara, planos, sonido) para tener parámetros de inspiración. Se le pasa el .mp4 a Claude y se mide (`docs/5-tecnica/MEDICION.md`).
- Renderizamos a **30 fps** (estándar; alcanza para nuestro movimiento).

## Agregado 2026-11-10 (2)
- **Una sola rama (`main`)**: no quiere ramas ni PR; todo directo a `main`. Explicarle GitHub en simple y evitar jerga.
- Referencias suyas que le gustan (10 videos en `assets/referencias/`): las **contemplativas/oscuras** con cámara que mueve–retiene–mueve y planos continuos; patrón favorito para reels técnicos: **vista explosionada 3D con etiquetas y tooltip** (`docs/4-referencias/BIBLIA-DE-ESTILO.md`).

## Agregado 2026-11-10 (3)
- **Todo análisis con números** (como el repo de LuisPa): nada de "se siente", nada de script técnico cualitativo. Un solo lugar (`docs/4-referencias/`), una sola herramienta (`medir.py`), comparar siempre contra las metas. **Borrar lo que no se usa.**
- **Ondas de radio = anillos/círculos** que se expanden; la onda sinusoidal solo para explicar frecuencias (2,4/5 GHz). Tipeo digital solo al escribir los 0/1 en la computadora; en el router, sonido de módem/router.
- **Gastar pocos tokens**: ir directo, pocas iteraciones, sin releer docs ni regenerar de más; que alcance con pasar el material.
- **Física (2026-11-11)**: solo si explica algo; se hornea con Rapier (`docs/5-tecnica/FISICA.md`), nunca simulación en vivo; sin `Math.random()`; los choques sincronizan los efectos. No usar React/R3F.
- **Paquetes (2026-11-11)**: cuadraditos SOLO sobre cables y siguiendo su curva (`cab.at`); en el aire, solo ondas. Lo que viaja sigue la forma real del medio.
- **Música por defecto** (desde 2026-11-16): *Can You Hear The Music* (`assets/musica/can-you-hear-the-music.mp3`); antes Palladio.

## Agregado 2026-11-11
- **Guardar cada pronunciación correcta apenas Ayrton la confirma o corrige**: va a `engine/audio/pronunciacion.json` (`estado: "ok"` + nota con la fecha y la fuente) y se anota en `docs/1-canal/BITACORA.md`. Al terminar un video, las palabras que no corrigió quedan `ok` (las aprobó de oído). Confirmadas: uaifai, ráuter, ísernet, gigaérts, "dos coma cuatro".
- **Estándar de calidad (2026-11-11)**: objetos GRISES de trazo fino y continuo; blanco solo para cables, señal y tipografía; antenas con cuerpo; revisar cada objeto de cerca. Voz: probar el efecto Adjutant (StarCraft) para el público nerd (`voz.efecto: adjutant`).
- **Voz sin efectos (2026-11-11)**: por defecto SIEMPRE Daniela limpia (`voz.efecto: "ninguno"`). El efecto Adjutant se probó y no le gustó; no proponerlo de nuevo salvo que lo pida.

## Agregado 2026-11-12
- **Las referencias que pasa son para aprender CÓMO se explica, no para copiarlas**: no repetir su hook, su orden ni sus objetos; proponer ángulo y analogías propias.
- **Nada pixelado/"cuadrado" como protagonista** (la cara de 8×8 del reel de tensores no le gustó): formas suaves, objetos con más riqueza.
- **Cuidar la pronunciación**: ante una palabra en inglés, ofrecer variantes de audio antes de usarla; "machine learning" como "mashín lérnin" no le gustó.
- En un reel conceptual lo primero es que **quede claro la definición** (qué ES la cosa), antes que lucirse con la animación.
- **Portada (2026-11-13)**: todos los reels arrancan con un cuadro fijo de **0,1 s** que sirve de portada al publicar (se elige como fotograma de portada): título grande del hook + el objeto clave + firma. Después, el hook con su **título** en pantalla (como en el reel de WiFi: "Tu WiFi es una radio").
- **Tipografía en pantalla**: le hacen ruido los textos muy juntos o con mucho espacio vacío; revisar aire y alineación de rótulos, chips y subtítulos en cada `snapshot`.
- **Guardar los reels terminados**: copia liviana del final en `docs/4-referencias/propios/<reel>/` junto con su medición, para tener referencia de lo que le gusta.
- **Paleta Scale (2026-11-13)**: probando colores de Scale AI. **No le gusta el verde (Evergreen) como fondo**; los colores de Scale se usan como **acento sobre base neutra** (negro/blanco/grises), no como superficie. Acento elegido para la prueba: Foundry Tan `#A8927C`.
- **Subtítulos sobre imágenes (2026-11-13)**: si el fondo tiene mucho detalle (números, fotos), usar la **barra negra detrás del subtítulo** (`video.json → subtitulos.fondo`). Pidió probar la tipografía de Scale (Host Grotesk + Geist Mono).
- **Público y feedback (2026-11-14)**: el reel de tensores tuvo mejor respuesta de lo esperado. Lo que gustó: **explica para el que no sabe de IT** (la mayoría). Lo que falla: **la voz se nota robótica**; le sugirieron **clonar su voz** para la marca personal. Todo en `docs/1-canal/PUBLICO.md`; anotar ahí el feedback de cada reel publicado.
- **Marca reconocible (2026-11-14)**: canal sin cara como Kurzgesagt, Fireship, 3Blue1Brown, FaztTech; lo que hace que lo reconozcan es **lo que se repite** (estética, color, voz, música, inicio y cierre). No variar esos elementos entre reels. Detalle en `docs/1-canal/CANAL.md`.
- **A mejorar (2026-11-14)**: portada, hook y **dinamismo de cámara** (medido: 0,5 movimientos notorios cada 10 s contra 1,5–5 de las referencias; ver `docs/1-canal/CANAL.md` → Próximas mejoras).
- **Repo para compartir (2026-11-14)**: todo lo importante tiene que estar en `main` en GitHub, para que otra persona pueda editar los videos como él quiere.

## Agregado 2026-11-15 (onetake)
- **Cámara continua de verdad**: en cada límite entre escenas algo sobrevive y se transforma en lo siguiente; se mide con `engine/analisis/arrastre.py` (medio ≥ 0,5). Ayrton pasó el repo onetake y pidió **no instalar nada** por seguridad: estudiar leyendo y tomar ideas/umbrales (licencia no comercial: nada de copiar código).
- Pausas verdaderamente quietas (≥ 25 % de cuadros) y cámara que anticipa al objeto; no más movimiento. Detalle: `docs/2-estilo/CAMARA.md` (reglas 7–9) y `docs/4-referencias/material/2026-11-onetake.md`.


## Agregado 2026-11-16 (tokens)
- **Cada reel con su propia puesta en escena**: se mantienen inicio (firma) y cierre (CTA), pero el medio NO copia el reel anterior (orden de planos, objetos de frente, título arriba). Explorar el espacio: estaciones en profundidad, recorridos de cámara por el set, vistas explosionadas.
- **Sonido más rico**: usar los sonidos propios que encajan con el tema (ej. `interface-texto-digital` para datos/tokens, `zoom-click` en acercamientos) además de los sintéticos; falta un banco de efectos reales (pendiente de su OK sobre la fuente).
- Datos técnicos concretos y verificados en reels conceptuales (no quedarse en la definición).

## Agregado 2026-11-16 (v2 de tokens)
- **Todos los reels en 2.5D con cámara fluida** (le gustó la v2 "fábrica"): un solo set 3D que la cámara recorre en plano secuencia; jugar con entradas, dolly in / out, grúa y **ángulos distintos (picado, contrapicado, lateral)**; transiciones de plano a plano **más rápidas** (viajes de ~0,8 s) y retenciones quietas cuando se nombra algo.
- **Nada que estorbe al texto**: la línea de montaje (cinta con cubitos) se sacó porque pasaba por detrás de las fichas. Decorado solo si explica algo y nunca detrás de lo que se lee.
- **Explicarle lo que hago con vocabulario de cine** (plano, ángulo, movimiento, transición): `docs/2-estilo/GLOSARIO-EDICION.md`, con ejemplos por segundo.
- **Música firma**: *Can You Hear The Music*, en todos los reels; elegir el tramo para que el crescendo termine en el CTA.
- **Media kit (2026-11-16)** en `docs/media-kit/` (abrir `Media Kit.dc.html`): manda en portada, hook, tamaños, reglas de uso y transiciones. Revisar cada reel contra él antes de entregar.
- **Portada y hook con la anatomía del media kit en todos los reels** (plantilla). **Efectos variados** (no repetir el mismo whoosh/golpe): `elegir(rol)`; fijos de marca solo boom y chinn.
