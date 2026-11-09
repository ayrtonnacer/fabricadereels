---
name: reel
description: Crear un reel vertical de motion graphics (HyperFrames + cámara 2.5D, voz en off, efectos, música) a partir de un link o tema de programación, matemática, ciberseguridad o Linux, con el estilo y las reglas de @ayrtonnacer.
---
# /reel <link o tema>
Seguí `CLAUDE.md` y `docs/FLUJO.md`. Resumen:
1. Leer la fuente y verificarla. Leer `docs/ESTILO.md`, `docs/CAMARA.md`, `docs/GUION.md`, `docs/AUDIO.md`, `docs/DECISIONES.md`, `engine/audio/pronunciacion.json`. Para el contrato de HyperFrames, la skill `/hyperframes`.
2. Escribir el guion (tabla escena | pantalla | voz | duración; público técnico) y **pedir aprobación antes de animar**.
3. Con el OK, armar `script-tecnico.md` (planos, cámara, sfx; `docs/CAMARA.md` y `docs/referencias/`).
4. `bash engine/nuevo.sh AAAA-MM-tema`, completar `video.json`, correr `voz.py` hasta que no haya avisos, `tiempos.py`, `subtitulos.py`, armar `compositions/*.html` y `sfx_events.py`.
5. `npx hyperframes check` sin errores y `snapshot` de cuadros clave (0, cada escena, cortes, CTA) y mirarlos; luego `render --workers 4 -o out/mudo.mp4`, `sfx.py`, `mezcla.py`.
6. Entregar `final.mp4` + descripción con créditos. Registrar correcciones en `docs/DECISIONES.md` y palabras nuevas en `pronunciacion.json`.
Repasar `docs/PREFERENCIAS.md` al empezar y antes de entregar. Todo en three.js (`assets/escena3d.js`). Guardar en el repo (siempre, sin que se lo pidan) todo lo que pase Ayrton (`docs/BITACORA.md`, `docs/material/`). Subtítulos siempre (imagen hasta y 1100; subtítulos 1120–1320); sin palabras sueltas; sin puntitos de fondo.
Reglas duras: motion graphics 2D con profundidad por cámara (no three.js como base); `marca.css` con color = significado (verde ok, ámbar aviso, error = bloque rojo con ✕); firma @ayrtonnacer sola, con el acento, al inicio y al final; en el cierre el foco es el CTA (firma chica debajo, sin zoom) y suena el chinn; CTA "dale like / seguime para aprender más de <tema>"; voz sin "pendrive"/"like"; no leer terminal ni carteles; sin scanlines/HUD.
