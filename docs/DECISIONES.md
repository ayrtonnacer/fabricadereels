# Decisiones y correcciones de Ayrton (no repetir estos errores)
## 2026-11 — Parrot OS USB persistente
- Estética: fondo oscuro tipo cyber/HackTheBox; sin serif, IBM Plex. Se descartó la estética y2k.
- Tipografía del paso: "Pasos 1/7" en mono mayúscula se veía generado por IA → "Paso 1 de 7" en Plex Sans.
- Sacar líneas de escaneo (en el pen y en todo el video), HUD/esquinas, "// TUTORIAL", "[ GRATIS ]" y el texto de la fuente al final. Mantener el glitch de "no olvida nada".
- 3D: escala real (notebook ≈32 cm vs USB ≈5,5 cm); el USB debe ser creíble (punta metálica hueca corta, contactos dorados, argolla); se enchufa a una notebook, no a una caja.
- Voz: no decir "pendrive" (→ memoria); no leer la terminal ni comentar los carteles ("ojo, se borra todo" fuera); no decir "like" (→ "me gusta").
- Marca: firma @ayrtonnacer al inicio y al final, en verde. Error mío: resalté "Linux" en vez del usuario → lo resaltado es lo que debe recordarse.
- CTA: no "guardalo" (no funciona en todas las plataformas) → "Si te gustó el video, dale like" + "Seguime para aprender más de Linux". Quitar "Linux y Dev".
- Audio: efectos más fuertes (gustan los sonidos informáticos/de radio), música con fade in/out ajustada al largo, ducking bajo la voz.
- Proceso: trabajar de forma sistemática con repo propio; el usuario pegará fuentes (programación, matemática, ciberseguridad).

## 2026-11-04 — Cambio de estética y diseño sonoro
- Estética nueva: **Anduril** (anduril.com, yashasmitta.com/anduril): negro puro, blanco, sin color de marca salvo un acento naranja; reemplaza al verde lima/azul oscuro tipo HackTheBox. Se conserva el tema anterior en `engine/themes/cyber.css` y el tag `parrot-cyber-v1`. Todo color va por variables CSS para poder cambiar de tema en un archivo.
- Fuente: Inter Tight (alternativa libre a Helvetica Now Display de Anduril, que es comercial).
- Diseño sonoro: se incorporan al repo las pautas del video de Mirko Vigna (capas, niveles, whoosh/impact/riser/bass drop/braam, silencio, ambiente, no ser literal) en docs/AUDIO.md y nuevos sonidos en sfxlib.py. Banco opcional de efectos reales (Adobe Audition) en assets/sfx/.

## 2026-11-04 (tarde) — Vuelta a HackTheBox
- Ayrton prefirió la estética HackTheBox (verde lima sobre azul oscuro) a la de Anduril. Anduril queda como tema alternativo; el tema activo se elige en `engine/theme.css`. Ante un pedido de "cambiar la estética", probar con 3–4 frames y mostrarlos ANTES de renderizar el video completo.
- La firma `@ayrtonnacer` va sola, sin el punto al lado.
- El sonido de tipeo sintético sonaba artificial: usar tipeo real (muestras de `assets/sfx/propios/`, de su repo code-reel-studio).
- Sonidos: repo de referencia Leonxlnx/earshot (motor de efectos por síntesis; MIT). Se intentó ejecutar su código y el entorno lo bloqueó, así que solo se tomaron sus principios de diseño (docs/AUDIO.md). Si Ayrton quiere usar earshot de verdad: instalarlo en su compu (`pip install` desde el repo) y generar los sonidos allá a `assets/sfx/<tipo>/`.
- Sonido "chinn" (assets/sfx/propios/chinn.mp3, de Ayrton) para las bolitas que aparecen alrededor del USB al inicio del CTA; reemplaza al sparkle sintético. `sfxlib.propio("chinn")`.

## 2026-11-05 — Tema red team y radio
- Para videos de CTF de HackTheBox: estética más roja (referencia Behance "Ghosts of Russia"), pero sin quedar en dúo-tono y con semántica clara: en la versión Anduril el naranja se usaba para todo (bien y error) y no se entendía. Ahora verde=ok, ámbar=aviso, error=bloque rojo relleno con ✕. Tema `themes/redteam.css`; cada video fija su tema en el <link> del index.html.
- Efecto de radio militar para la voz (voz.efecto = "radio").
- Video Parrot re-hecho con tema redteam + voz en radio (fuerza 0.5, squelch de 0.14 s: dejar ≥0.15 s entre líneas y margen de 0.1 s al fin de escena; Piper varía la duración ±0.1 s por corrida, volver a correr voz.py si avisa).
- Existe `videos/2026-11-parrot-usb-htb/` (misma voz de radio y efectos, tema cyber/HackTheBox) solo para comparar contra la versión red team; Ayrton elige con cuál quedarse.
- 2026-11-07: Ayrton pasó 9 shorts de @aprendeiadecero como referencia de **dinamismo y subtítulos** (no de estética). Lo que marcó: ahí las letras tienen demasiado espacio entre sí y en eso lo nuestro está mejor; hay que mantener el espaciado apretado. Lo que hay que tomar está en docs/DINAMISMO.md.
- 2026-11-07 (noche): Ayrton pidió rehacer el tutorial de Parrot aplicando lo aprendido, SIN subtítulos y con voz Piper normal (sin radio), para comparar si sale un tutorial mejor. Carpeta `videos/2026-11-parrot-usb-v3/` (tema redteam). Cambios respecto a la v1: 2D plano en vez de 3D (USB y notebook vectoriales), número gigante de paso, palabras gigantes con blur y sellos, cursor que hace clic, resaltes que se dibujan, zoom lento, avisos en pantalla con la fuente (el error de tipeo «dus-tplus» de la página). Sin subtítulos por pedido (la regla 8 de CLAUDE.md los pide por defecto).
- Motor nuevo: `engine/dinamismo.js` (golpe, atenuar, resalte, kenburns, cursor, pop, slide, dibujar). Los tiempos de clics y palabras gigantes viven en `video.json` → `ev`, y los leen tanto el visual como `sfx_events.py`.
- Error a no repetir: no usar `id="gl"` ni la clase `.ln` en el HTML de un video: el tema usa `#gl` para el canvas 3D (position:absolute a pantalla completa) y `.ln{visibility:hidden}` para las líneas de terminal.
- 2026-11-07 (madrugada): Ayrton vio la v3 y la rechazó: "mucho peor", prefiere el Parrot anterior con estética HackTheBox. Lecciones: (1) NO reemplazar el 3D del USB y la notebook por dibujos planos, el 3D creíble era lo mejor del video; (2) NO cambiar tema, estructura y animaciones a la vez: tocar una cosa por vez y mostrar frames antes; (3) el dinamismo de los shorts de referencia se aplica como capa sobre el video que ya gusta (zoom lento, resaltes, cursor), no como rediseño. La v3 queda en `videos/2026-11-parrot-usb-v3/` solo como experimento; la base buena es la variante HackTheBox (`videos/2026-11-parrot-usb-htb/` / tag `parrot-cyber-v1`).
- 2026-11-07 (02:30): **Decisión final del Parrot**: se queda el ORIGINAL (estética HackTheBox/cyber, voz Daniela sin radio, 3D, sonido chinn y tipeo real; era `parrot-usb-persistente-v5.mp4`). Restaurado en `videos/2026-11-parrot-usb/` (fuente del commit ddac286, con `<link>` a cyber.css) y tag `parrot-final`. Se borraron las variantes red team, htb (y su duplicado hackthebox) y v3 (siguen en el historial de git). Para videos futuros: tema por defecto cyber, **3D sí** (le gustan), efecto de radio y red team solo si los pide; dinamismo como capa opcional, sin subtítulos por ahora.



## 2026-11-07 — Investigación de guiones y videos en bucle
- Ayrton pasó una investigación sobre estructura de guiones (guardada en docs/INVESTIGACION-GUIONES.md) y tutoriales de bucle perfecto: aplicar estructura Hook→Payoff→CTA/bucle y un solo loop principal.
- Bucle: la última frase desemboca en el hook, el último cuadro vuelve al primero (corte oculto en un movimiento), música en silencio en el empalme, sin "dale me gusta" ni firma al final.
- Medido: Piper Daniela da ≈ 2,3 palabras/s en el video completo (no 2,5).
- yt-dlp instalado, pero el proxy de la sesión bloquea YouTube: las referencias se pasan como transcripción o archivos adjuntos.

## 2026-11-09 — Replanteo: HyperFrames + motion graphics con cámara 2.5D
- Pedido de Ayrton: el render 3D tardaba mucho (~18 min un reel en CPU) y quiere sacar reels rápidos; usar HyperFrames (heygen-com/hyperframes), más probado que el motor propio; el estilo que le interesa es **motion graphics 2D donde la profundidad la da el movimiento de cámara** (pasó referencias de movimientos de cámara).
- Hecho: cada video es un proyecto HyperFrames (`index.html` + `compositions/` + `assets/`); cámara 2.5D propia en `assets/camara.js` (capas HTML a distinta z + perspectiva, GSAP) documentada en `docs/CAMARA.md`. Render de la plantilla (15 s): 36 s en CPU con `--workers 4` (≈ 9× más rápido).
- Esto reemplaza la regla anterior "3D sí (three.js)": ya no es la base. 3D real solo para un plano puntual si Ayrton lo pide.
- Se mantiene: tema cyber/HackTheBox (ahora en `assets/marca.css`), color = significado, IBM Plex, firma, CTA, voz Daniela, audio propio (`voz.py`/`sfx.py`/`mezcla.py`, −14 LUFS). HyperFrames renderiza mudo.
- Se borró (queda en git, commit `ae9a888`): motor `render.mjs`/`lib.js`/`dinamismo.js`, temas redteam/anduril, los 3 videos de Parrot, y docs redundantes (PARTES, SHOOTING-SCRIPT, GLOSARIO, DINAMISMO, PRONUNCIACION → fusionados en ESTILO/CAMARA/AUDIO/plantilla de guion).
- Técnico: GSAP y fuentes van locales en `assets/` (el CDN está bloqueado en la nube y el render no debe depender de la red). Capas grandes con máscara (piso, puntos) encarecen mucho el render en CPU: piso ≤ 3000 px. El `check` de HyperFrames toma la viñeta y el fondo como opacos: llevan `data-layout-ignore`.
- 2026-11-09 (tarde), sobre la demo de la plantilla:
  - **CTA en foco**: la demo hacía zoom sobre `@ayrtonnacer` y después mostraba el "Dale like". Mal: el foco es el CTA. Ahora la cámara aterriza sobre el CTA (grande) y queda quieta; la firma aparece después, debajo y más chica, sin zoom.
  - Sonido final: el **chinn** de Ayrton (`assets/sfx/propios/chinn.mp3`), no un "cristal"/sparkle sintético; suena cuando aterriza el CTA.
  - El inicio y el CTA final se mantienen entre reels; lo que cambia es el medio.
  - **Público técnico**: se puede usar vocabulario del área; no explicar lo básico (antes la regla era "nada técnico duro").
  - Flujo: link (+ breve indicación de lo que quiere) → guion → OK → **script técnico** (planos, cámara, sfx; plantilla `videos/_plantilla/script-tecnico.md`) → video. Referencias de cámara en `docs/referencias/` (Ayrton va a pasar más). A futuro: publicar automáticamente en sus redes.
  - code-reel-studio: sus 4 sonidos ya estaban en `assets/sfx/propios/`; se tomó el "recorrido de código" (zoom + paneo línea por línea) como movimiento de cámara. Su música (5 pistas en `public/music/`) no se copió: falta confirmar licencia.
- 2026-11-09 (noche): **Público real**: técnicos + principiantes + reclutadores; los reels son portfolio de Ayrton y tienen que demostrar que sabe (un detalle de profesional por reel). Reemplaza "público técnico" a secas (ver docs/GUION.md).
- Error mío: para el primer reel de WiFi (fuente: HowStuffWorks, "What is WiFi and How Does it Work?") elegí un ángulo lateral (seguridad, filtro MAC) cuando la fuente trataba de **cómo funciona el WiFi**. Ayrton quería eso. Ante una fuente, el guion cubre su tema central primero; los ángulos laterales se ofrecen como otros reels de una serie.
- 2026-11-09 (noche): primer reel hecho con HyperFrames: `videos/2026-11-wifi` (33 s, render 72 s en CPU, −14,2 LUFS). Fuentes: HowStuffWorks + Wikipedia + Cisco. Se descartó el hook "wireless fidelity" porque las fuentes se contradicen. Palabras nuevas en `pronunciacion.json` (sin verificar): WiFi→"guifi", Ethernet→"ísernet", router→"rúter", gigahertz→"gigaérts".
- 2026-11-09 (noche), correcciones de Ayrton al reel de WiFi (detalle en `docs/BITACORA.md`): subtítulos siempre (zona segura); ondas continuas en la pared; el cable llega al router; sin palabras sueltas; sin puntitos verdes de fondo (le gustan las líneas de perspectiva y el gradiente); sonido grave al inicio y al final; más uso del eje z con three.js solo si no hace lento el render (medido: ≈ +1 s de render por segundo de video); guardar indicaciones y materiales en el repo.
- 2026-11-09 (noche, 2): sonido limpio (sin ambiente ni glitch; mezcla sin loudnorm dinámico); sin bits/decorados sin sentido; **todo en three.js** con la librería compartida (`escena3d.js`); "WiFi" → "uaifai" provisorio; el texto del CTA coincide con la voz ("Dale like y seguime para aprender más de <tema>"); `docs/PREFERENCIAS.md` como resumen vivo.
- 2026-11-09 (noche, 3): librería 3D a r187 (Neutral tone mapping, RoomEnvironment, biseles, sombras de contacto, contraluz); render del reel de WiFi sube de 66 s a ~2 min (medido: el entorno IBL es ~30 %) y se acepta por el salto de calidad; notebook sin antena, cables con puertos reales, sin etiqueta "pared"; sonidos nuevos (interface digital, módem, hit metal); "uaifai" aprobado, "ráuter" en prueba; guía en `docs/THREEJS.md`.
- 2026-11-10: herramienta de medición propia (`engine/analisis/`): cámara por correlación de fase (traslación + zoom + tirón), cortes por respuesta de fase (la diferencia de cuadros no sirve en motion graphics), audio y script técnico automático; calibrada con autotest. Hallazgo: el reel de WiFi habla a 3,11 palabras/s (referencia citada: 2,77) → considerar bajar. 30 fps confirmado.
- 2026-11-10: **una sola rama (`main`)**. Contenido rescatado de la rama vieja de motion graphics (referencias, análisis, guion de redes); el motor viejo no se trae (queda en la historia/etiqueta). Patrones a adoptar: vista explosionada con etiquetas, cámara mover–retener–mover, plano continuo, una palabra por tic de sonido, rejilla de beats.
- 2026-11-10 (3): **el análisis de referencias es numérico** (biblia de estilo + `metas.json` + `comparar.py`); se elimina el script técnico/shooting script cualitativo. Los reels se planean en `plan.md` con metas en números y se verifican midiendo.
- 2026-11-10 (4): ondas de radio = anillos, sinusoidal solo en frecuencias; módem en la sección del router; tipeo digital solo en la notebook.

## 2026-11-11 — WiFi v7
- Error a no repetir: mover paquetes con `lerp` entre los extremos de un cable curvo (se salen del cable) → usar `cab.at(s)`. Paquetes en el aire junto a las ondas → sacarlos.
- Defaults nuevos: estética negro + línea + rojo; música Palladio.
- 2026-11-10 (5): prueba de estética **hairline** (placas planas + trazo fino, `--estilo: hairline`) en copia del WiFi, sin tocar el original; está a la espera de su elección. Si gana, pasar el estilo a `assets/escena3d.js` común y a `_plantilla`.
- 2026-11-11: **voz de Daniela a `length_scale` 1,05** y guion al ≤ 2,9 pal/s (96 palabras en 33 s): a 0,92 hablaba ≈ 3,7 pal/s. Para bajar la velocidad no alcanza con la voz: hay que recortar texto o alargar el video. Mezcla: medir música vs voz por línea antes de fijar dB (`musica_nivelar` si la pista tiene mucha dinámica).
- 2026-11-11 (2): error a no repetir: contornos blancos gruesos (4–5 px) y antenas de una sola línea → quedan con cortes y sin riqueza. Usar gris fino continuo y blanco solo para resaltar.

## 2026-11-12 — Reel de tensores (escalar, vector, matriz, tensor)
- Ayrton pidió "armá el guion y el video directamente" (sin checkpoint) a partir de las fuentes, el short de referencia y su explicación a un amigo. Decisión de proceso: cuando lo pide así, se salta el checkpoint (7b); el guion queda igual en `videos/2026-11-tensores/guion.md`.
- Técnico: `Object3D.clone()` serializa `userData` (falla con objetos/funciones) → usar `T.copiar()` de `assets/tensor3d.js`. Encuadre: con `dy` = 170 px y subtítulos en 1120–1320, un objeto de 0,6 m necesita cámara a ≥ 2,6–3,0 m; los rótulos van ARRIBA del objeto (abajo pisan los subtítulos).
- Red: WebFetch no resolvía hosts nuevos aunque el entorno ya estaba abierto; `curl` desde Bash sí. YouTube bloquea la descarga automática (login) y vidIQ sin créditos: los videos de referencia se pasan por Colab (mp4 comprimido a 540p).
- 2026-11-12 (2) — Ayrton rechazó la v1 del reel de tensores: (1) **"usaste literal el video de ejemplo"**: las referencias que pasa son para ver *cómo se explica* de didáctico (ritmo, analogías, qué se muestra), NO para copiar hook, orden ni objetos; inventar ángulo y analogías propias; (2) **la cara de píxeles era "demasiado cuadrada"**: nada pixelado/blocky como protagonista; formas suaves y objetos con más riqueza; (3) **no le gustó la pronunciación** ("machine learning" → "mashín lérnin"; muestras de otras opciones en `docs/material/pronunciacion/cta-variantes.mp3`). Guion v2 con ángulo "ubicar un número con N índices". Prioridad: que quede claro QUÉ ES un tensor.
