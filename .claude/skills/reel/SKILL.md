---
name: reel
description: Crear un reel vertical animado (voz en off, efectos, música) a partir de un link o tema de programación, matemática, ciberseguridad o Linux, con el estilo y las reglas de @ayrtonnacer.
---
# /reel <link o tema>
Seguí `CLAUDE.md` y `docs/FLUJO.md`. Resumen:
1. Leer la fuente y verificarla. Leer `docs/ESTILO.md`, `docs/GUION.md`, `docs/MOVIMIENTO.md`, `docs/CAMARA-3D.md`, `docs/AUDIO.md`, `docs/DECISIONES.md` y `engine/audio/pronunciacion.json`. Mirar el reel anterior para NO repetir hook, analogía, mundo 3D, plan de cámara ni transiciones.
2. Escribir el guion (tabla escena | pantalla | voz | duración | cámara/transición) y **pedir aprobación antes de animar**.
3. `./reel nuevo <tema>`, completar `video.json`, `./reel voz` hasta que no haya avisos, armar `index.html` y `sfx_events.py`.
4. `./reel revisar <video> --quietud` sin errores; `./reel preview` en los cuadros clave (inicio, cada costura, pico de cada movimiento, CTA) y mirarlos.
5. `./reel render <video>`. Entregar `final.mp4` + descripción con créditos (voz Piper es_AR-daniela, CC BY-SA 4.0, y la fuente).
6. Registrar correcciones en `docs/DECISIONES.md` y palabras nuevas en `pronunciacion.json`.
Reglas duras (CLAUDE.md): tema `cyber.css` por defecto (redteam solo si Ayrton lo pide), color = significado; firma @ayrtonnacer sola, en el acento, al inicio y al final; CTA "Dale like" / "dale me gusta" + "Seguime para aprender más de <tema>"; voz sin "pendrive"/"like"/"guardalo"; no leer terminal ni carteles; sin scanlines/HUD/mayúsculas espaciadas; 3D con escala real; solo voz, música y estética son fijas, todo lo demás varía entre reels.
