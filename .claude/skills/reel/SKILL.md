---
name: reel
description: Crear un reel vertical de motion graphics (HyperFrames + cámara 2.5D, voz en off, efectos, música) a partir de un link o tema de programación, matemática, ciberseguridad o Linux, con el estilo y las reglas de @ayrtonnacer.
---
# /reel <link o tema>
Seguí `CLAUDE.md` y `docs/FLUJO.md`. Resumen:
1. Leer la fuente y verificarla. Leer `docs/ESTILO.md`, `docs/CAMARA.md`, `docs/GUION.md`, `docs/AUDIO.md`, `docs/DECISIONES.md`, `engine/audio/pronunciacion.json`. Para el contrato de HyperFrames, la skill `/hyperframes`.
2. Escribir el guion (tabla escena | pantalla | cámara | voz | duración) y **pedir aprobación antes de animar**.
3. `bash engine/nuevo.sh AAAA-MM-tema`, completar `video.json`, correr `voz.py` hasta que no haya avisos, `tiempos.py`, armar `compositions/*.html` y `sfx_events.py`.
4. `npx hyperframes check` sin errores y `snapshot` de cuadros clave (0, cada escena, cortes, CTA) y mirarlos; luego `render --workers 4 -o out/mudo.mp4`, `sfx.py`, `mezcla.py`.
5. Entregar `final.mp4` + descripción con créditos. Registrar correcciones en `docs/DECISIONES.md` y palabras nuevas en `pronunciacion.json`.
Reglas duras: motion graphics 2D con profundidad por cámara (no three.js como base); `marca.css` con color = significado (verde ok, ámbar aviso, error = bloque rojo con ✕); firma @ayrtonnacer sola, con el acento, al inicio y al final; CTA "dale like / seguime para aprender más de <tema>"; voz sin "pendrive"/"like"; no leer terminal ni carteles; sin scanlines/HUD.
