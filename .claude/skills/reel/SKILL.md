---
name: reel
description: Crear un reel vertical explicativo de @ayrtonnacer (un set 3D con cámara continua en HyperFrames + three.js, voz en off, efectos, música, subtítulos) a partir de un link o tema de programación, matemática, ciberseguridad o Linux.
---
# /reel <link o tema>
Las reglas están en `CLAUDE.md` (ya cargado). El procedimiento completo, con qué leer en cada paso y cuándo está terminado, es **`docs/5-tecnica/FLUJO.md`: abrilo y seguilo en orden.** Resumen:

1. Leer `docs/1-canal/PREFERENCIAS.md`. Guardar el material de Ayrton en `docs/4-referencias/material/` y su pedido en `docs/1-canal/BITACORA.md`.
2. Leer la fuente y **verificar cada dato** contra la fuente primaria.
3. `python engine/reel.py nuevo AAAA-MM-tema` → `guion.md` + `video.json` (leer `docs/3-guion/GUION.md` y `docs/1-canal/PUBLICO.md`) → `python engine/reel.py guion videos/X` sin errores.
4. **✋ Mostrar el guion y esperar el OK de Ayrton.** No animar antes.
5. `python engine/reel.py voz videos/X` hasta que no haya avisos.
6. `plan.md` (leer `docs/2-estilo/CAMARA.md` y `ESTILO.md`) → escribir `assets/set.js` (leer `docs/5-tecnica/THREEJS.md`; molde: `videos/_plantilla/assets/set.js`) → `sfx_events.py` (leer `docs/2-estilo/AUDIO.md`).
7. `python engine/reel.py revisar videos/X` (0 errores) y `python engine/reel.py cuadros videos/X`: **mirar la hoja de cuadros** con la lista del paso 7 del flujo. Repetir hasta que esté bien.
8. `python engine/reel.py render videos/X` → `python engine/reel.py medir videos/X` → corregir o justificar lo que quede fuera.
9. `descripcion.md` → `python engine/reel.py entregar videos/X` → contarle a Ayrton qué hace la cámara (vocabulario de cine) → commit y push a `main`.

Lo que se escribe a mano: `guion.md`, `plan.md`, `video.json`, `assets/set.js`, el tema en `compositions/cierre.html`, `sfx_events.py`, `descripcion.md`. Todo lo demás se genera.
Lo que **no** se cambia sin que Ayrton lo pida: portada y gancho (anatomía), cierre/CTA, firma, paleta, tipografías, voz, música firma, boom y chinn.
No publicar nada en redes.
