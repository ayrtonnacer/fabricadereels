# Flujo para hacer un reel

Comandos desde la raíz del repo, salvo donde dice "en la carpeta del video".

0. **Guardar el material**: todo lo que Ayrton pase (PDF, imágenes, sonidos, texto) se copia al repo (`docs/material/`, `assets/sfx/propios/`, `videos/X/fuentes/`) y sus indicaciones se anotan en `docs/BITACORA.md`.
1. **Fuente**: leer el link/tema completo (WebFetch/WebSearch). Extraer objetivo, ideas clave, comandos o fórmulas, advertencias. Verificar contra la fuente oficial.
2. **Guion** (`docs/GUION.md`, plantilla `videos/_plantilla/guion.md`): una idea, Hook → Payoff → CTA/bucle, ≤ duración × 2,3 palabras. Por escena: voz y texto en pantalla (la cámara va en el plan numérico, paso 3b).
3. **✋ Checkpoint**: mostrar el guion (texto de voz + una línea por escena) y esperar OK.
3b. **Plan numérico** (`plan.md` del video, plantilla `videos/_plantilla/plan.md`): metas tomadas de `docs/referencias/BIBLIA-DE-ESTILO.md` y `metas.json` (cortes por minuto, plano mediano, velocidad y ataque/liberación de cámara, retenciones, palabras/s, LUFS) y, por escena, cámara, transición y sonido **en números** (`docs/CAMARA.md`). Se lo muestro a Ayrton junto con los primeros cuadros.
4. **Crear el video**: `bash engine/nuevo.sh AAAA-MM-tema` (copia la plantilla). Completar `video.json`: escenas (`id` = nombre de la composición, `d` = segundos) y `voz.lineas`.
5. **Voz primero**: `python engine/audio/voz.py videos/X`. Ajustar texto y tiempos hasta que no haya avisos; las escenas duran lo que pide la voz (voz ≤ fin de escena − 0,1 s; ≥ 0,15 s entre líneas). Luego `python engine/tiempos.py videos/X` copia las duraciones a `index.html` y `python engine/subtitulos.py videos/X` arma los subtítulos con los tiempos exactos por palabra (`docs/SUBTITULOS.md`).
6. **Visual**: la imagen no pasa de y ≈ 1100 (subtítulos en 1120–1320). una composición por escena en `compositions/` (copiar las de la plantilla). Cada parte aparece cuando la voz la nombra (tiempos locales de la escena = tiempo de la línea − inicio de la escena).
7. **Revisar** (en la carpeta del video): `npx hyperframes check` (sin errores) y `npx hyperframes snapshot --at 0,1.5,…` → **mirar las imágenes** antes de renderizar. Ojo con: cuadro 0 (es la miniatura), textos chicos, cortes entre escenas.
8. **Efectos**: `sfx_events.py` con los significados fijos (`docs/AUDIO.md`); whoosh en el pico de cada movimiento de cámara. `python engine/audio/sfx.py videos/X`.
9. **Render** (en la carpeta del video): `npx hyperframes render --workers 4 -o out/mudo.mp4` (~2,5 s por segundo de video en CPU).
9b. **Medir** (`docs/MEDICION.md`): `python engine/analisis/medir.py videos/X/out/mudo.mp4 videos/X/analisis` (con `--transcripcion` sobre `final.mp4` para palabras/s); `python engine/analisis/comparar.py videos/X/analisis/metricas.json` contra la biblia de estilo y el `plan.md`. Si Ayrton pasó una referencia: medirla (`externos/<slug>/`), correr `python engine/analisis/biblia.py` para actualizar las tablas y recién después proponer.
10. **Mezcla**: `python engine/audio/mezcla.py videos/X` → `final.mp4` (−14 LUFS, pico ≤ −1,5 dB).
11. **Entrega**: mp4 + descripción con créditos (voz: Piper es_AR-daniela, CC BY-SA 4.0; y la fuente).
12. **Cierre**: registrar correcciones en `docs/DECISIONES.md` y palabras nuevas en `engine/audio/pronunciacion.json`; commit.

**A futuro**: publicar automáticamente en las redes de Ayrton (pendiente; no publicar nada sin que lo pida).

Cambios chicos: tocar solo la escena afectada, `snapshot --composition <id>` y volver a renderizar.
