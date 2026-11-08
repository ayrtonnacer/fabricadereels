# Flujo para hacer un reel

1. **Fuente**: leer el link/tema completo (WebFetch/WebSearch). Extraer: objetivo, pasos o ideas clave, comandos o fórmulas, advertencias. Verificar contra la fuente oficial.
2. **Guion** (ver GUION.md): 5–8 pasos; frase por escena; texto de voz natural; qué se muestra en pantalla por escena. Duración objetivo 45–60 s.
3. **✋ Checkpoint**: mostrar el guion al usuario y esperar OK. Pasar luego del texto aprobado a `video.json`.
4. **Crear el video**: `cp -r videos/_plantilla videos/AAAA-MM-tema`; completar `video.json` (escenas con duración, `voz.lineas`, `audio`).
5. **Voz primero**: `python engine/audio/voz.py videos/X`. Ajustar texto/tiempos hasta que no haya avisos. Las duraciones de las escenas se acomodan a la voz (voz ≤ fin de escena − 0,1 s; ≥ 0,15 s entre líneas).
6. **Visual**: editar `index.html` (secciones `.scene`, `data-a`, `data-step`). `preview` en momentos clave (inicio, medio, CTA), mirar cada imagen, corregir desbordes de texto.
7. **Efectos**: `sfx_events.py` con la tabla de significados (AUDIO.md).
7b. **Revisar**: `python engine/revisar.py videos/X --quietud` sin errores; preview en cada costura (docs/MOVIMIENTO.md §7).
8. **Render**: `scenes` → `join` → `mezcla`. Revisar `final.mp4` (−14 LUFS, pico ≤ −1,5 dB).
9. **Entrega**: enviar mp4 + descripción (con créditos de la voz: Piper es_AR-daniela, CC BY-SA 4.0, y de la fuente).
10. **Cierre**: registrar correcciones en DECISIONES.md y palabras nuevas en pronunciacion.json; commit.
