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

## 2026-11-08 — Cámara 3D estilo After Effects
- Ayrton pidió recorridos en 3D con cambios de plano (cenital, órbita, dron en primera persona como en el artefacto del dron) y transiciones de reel viral, hechos con Claude en vez de After Effects. Se creó `engine/camara3d.js` (Rig de tomas con tiempo global, transiciones automáticas entre tomas, motion blur real por sub-cuadros, temblor, speed ramp, carteles 3D) y la demo `videos/_demo-camara3d/`. Guía: `docs/CAMARA-3D.md`.
- Los videos de referencia de YouTube no se pudieron mirar desde la sesión (proxy bloquea YouTube); se usó el conocimiento de la técnica de AE. Falta que Ayrton vea la demo y diga qué movimientos le gustan.

