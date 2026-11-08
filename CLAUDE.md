# Fábrica de reels — manual de operación

Repo de @ayrtonnacer para producir reels verticales (1080×1920, ~45–60 s) explicativos de programación, matemática, ciberseguridad y Linux.
Flujo: **el usuario pega una fuente (link o tema) → Claude escribe el guion → el usuario lo aprueba → se anima en HTML/three.js → voz Piper (Daniela es_AR) + efectos + música → mp4.**

Cuando el usuario diga "hacé un reel de <fuente>" (o `/reel`), seguí `docs/FLUJO.md` paso a paso. Leé antes `docs/ESTILO.md`, `docs/DINAMISMO.md` (ritmo, animaciones y subtítulos), `docs/GUION.md` (estructura Hook→Payoff→CTA/bucle, 2,3 palabras/s; investigación completa en `docs/INVESTIGACION-GUIONES.md`; plantilla `videos/_plantilla/guion.md`), `docs/AUDIO.md` y `engine/audio/pronunciacion.json`. Cámara 3D (recorridos de dron, órbita, cenital, latigazo, zoom through): `docs/CAMARA-3D.md` + `engine/camara3d.js`, demo `videos/_demo-camara3d/`. Movimiento y transiciones (ley del vector, costuras, señales de video generado): `docs/MOVIMIENTO.md` + `engine/costuras.js`. Videos de referencia: `docs/ANALISIS-REFERENCIAS.md` (`python engine/analizar_video.py` → un documento por video en `referencias/`). Marco mental: `docs/PARTES.md` (el video como un auto), plantilla `docs/SHOOTING-SCRIPT.md` y `docs/GLOSARIO-EDICION.md`. Mirá `docs/DECISIONES.md`: ahí está cada corrección que el usuario hizo; no repitas esos errores.

## Estructura (es un framework propio: `docs/FRAMEWORK.md`)
- `engine/` — el motor: `lib.js` (tiempo, escenas, `data-a`, `__render(t)`), `costuras.js` (transiciones), `camara3d.js` (cámara 3D), `dinamismo.js` (capa opcional), `themes/` (`cyber.css` = HackTheBox, el POR DEFECTO, + `estados.css` para chips ok/aviso/error; `redteam.css` opcional, no gustó en Parrot), `render.mjs` + `servidor.mjs` (render con Chromium/FFmpeg), `visor.html` (reproductor), `revisar.py` (chequeos), `analizar_video.py` (referencias), `audio/` (`voz.py`, `sfx.py`, `sfxlib.py`, `mezcla.py`, `pronunciacion.json`), `cli.mjs` (= `./reel`).
- `videos/<AAAA-MM-tema>/` — un video: `video.json` (única fuente de verdad; esquema en docs/FRAMEWORK.md), `index.html` (visual), `sfx_events.py` (efectos); `out/`, `audio/`, `frames/`, `final.mp4` no van a git.
- `videos/_plantilla/` — punto de partida (`./reel nuevo <tema>`). `videos/2026-11-parrot-usb/` — video DEFINITIVO y de referencia (tag `parrot-final`). `videos/_demo-camara3d/` — demo de cámara.
- `assets/voces/` (modelo Piper), `assets/musica/`, `assets/referencias/` — NO van a git; ver sus `LEEME.md`.

## Comandos (desde la raíz; `./reel ayuda`)
```
./reel nuevo <tema> [--titulo "…"]     # copia la plantilla a videos/AAAA-MM-<tema>
./reel revisar <video> [--quietud]     # chequeos antes de renderizar: esquema, determinismo, firma, voz, colores, costuras, tramos quietos
./reel preview <video> 1 12 30         # cuadros sueltos → <video>/frames/ (mirarlos SIEMPRE antes de renderizar)
./reel ver <video>                     # visor en el navegador (puerto 8080): reproducir, escenas, cuadro a cuadro
./reel render <video> [s1 s2…]         # revisar → voz → efectos → escenas → unir → mezcla → final.mp4
./reel voz | efectos | mezcla <video>  # un paso suelto del audio
./reel analizar ref.mp4 --nombre x     # video de referencia → referencias/x/analisis.md
```
Render sin GPU: ~175 ms/cuadro en HTML, ~320 ms en 3D (más con desenfoque de movimiento); `GPU=1` si hay GPU. Renderizar solo las escenas cambiadas.

## Reglas que nunca se rompen (detalle en docs/)
1. Estética: por defecto `themes/cyber.css` (HackTheBox: azul-negro + lima; lo que Ayrton eligió para Parrot). `themes/redteam.css` (negro con brasas rojas) solo si Ayrton lo pide. **Color = significado**: énfasis = acento del tema, verde+✓ ok, ámbar+⚠ aviso, error = bloque rojo relleno+✕. IBM Plex Sans/Mono, cajas con borde fino y esquinas suaves. Sin scanlines, sin HUD/esquinas, sin etiquetas en mayúsculas espaciadas, sin texto de fuente al final. Paso = "Paso 1 de 7" en sans. Usar siempre variables CSS (`var(--acc)`), nunca colores fijos. Firma `@ayrtonnacer` SIN punto ni adornos al lado.
2. Firma `@ayrtonnacer` al inicio y al final, **resaltada con el acento del tema** (lo que se debe recordar lleva el resalte; nunca resaltar el tema en su lugar).
3. CTA multiplataforma: "Dale like" (texto) / "dale me gusta" (voz) + "Seguime para aprender más de <tema>". Nunca "guardalo".
4. Voz: palabras simples, no leer la terminal ni los carteles; nada técnico duro; "memoria", no "pendrive"; "me gusta", no "like". Pronunciación por diccionario, no a ojo.
5. **3D: le gusta a Ayrton** (USB y notebook del Parrot). Cuando haya objetos físicos, usar three.js con escala real (notebook ≈32 cm, USB ≈5,5 cm) y materiales creíbles; no reemplazarlo por dibujos planos.
6. Audio (ver docs/AUDIO.md; opción de voz con efecto de radio `voz.efecto="radio"; basado en diseño sonoro profesional): 4 capas (voz, música, efectos, ambiente), voz −14 LUFS, efectos audibles pero nunca al nivel de la voz (ducking), música con fade in/out ajustada a la duración, silencio como recurso, whoosh en el pico del movimiento.
7. **Guion**: una idea por reel, loop principal abierto en el hook y cerrado en el payoff antes del cierre, hook ≤ 3 s sin muletillas de IA, ≤ duración × 2,3 palabras. Parrot-bucle: cierre sin CTA que empalma con el hook.
7b. **Checkpoint**: mostrar el guion (texto de voz + una línea por escena) y esperar aprobación ANTES de animar/renderizar.
8. **Dinamismo** (docs/DINAMISMO.md): es una CAPA opcional sobre un video que ya gusta (zoom lento, resaltes que se dibujan, cursor, palabra gigante con blur), no un rediseño. Subtítulos solo si Ayrton los pide. Cambiar UNA cosa por vez y mostrar frames antes de renderizar. Letras con espaciado normal o apretado.
9. Terminar cada video agregando a `docs/DECISIONES.md` lo que el usuario corrigió y a `pronunciacion.json` cada palabra nueva.
