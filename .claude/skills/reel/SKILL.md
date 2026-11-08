---
name: reel
description: Crear un reel vertical animado (voz en off, efectos, música) a partir de un link o tema de programación, matemática, ciberseguridad o Linux, con el estilo y las reglas de @ayrtonnacer.
---
# /reel <link o tema>
Seguí `CLAUDE.md` y `docs/FLUJO.md`. Resumen:
1. Leer la fuente y verificarla. Leer `docs/ESTILO.md`, `docs/GUION.md`, `docs/AUDIO.md`, `docs/DECISIONES.md`, `engine/audio/pronunciacion.json`.
2. Escribir el guion (tabla escena | pantalla | voz | duración) y **pedir aprobación antes de animar**.
3. `cp -r videos/_plantilla videos/AAAA-MM-tema`, completar `video.json`, correr `voz.py` hasta que no haya avisos, armar `index.html` y `sfx_events.py`.
4. `preview` de frames clave y mirarlos; luego `scenes`, `join`, `mezcla`.
5. Entregar `final.mp4` + descripción con créditos. Registrar correcciones en `docs/DECISIONES.md` y palabras nuevas en `pronunciacion.json`.
Reglas duras: tema por tipo de video (CTF/red team = redteam.css con color=significado: verde ok, ámbar aviso, error=bloque rojo con ✕; tutorial clásico = cyber.css); firma @ayrtonnacer sola (sin punto) resaltada en verde al inicio y fin; CTA "dale like / seguime para aprender más de <tema>"; voz sin "pendrive"/"like"; no leer terminal ni carteles; sin scanlines/HUD.
