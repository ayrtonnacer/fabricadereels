# Flujo para hacer un reel

El flujo en cuatro pasos (acordado con Ayrton, 2026-11-09), con sus puertas de aprobación:

1. **Fuente → idea.** Ayrton pasa el link del contenido educativo. Leerlo entero, verificar comandos, fórmulas y advertencias contra la fuente oficial, y bajarlo a UNA idea de ≤ 12 palabras.
2. **Guion** con las mejores prácticas de storytelling (docs/GUION.md: hook ≤ 3 s, un loop abierto y cerrado en el payoff, 2,3 palabras/s). ✋ **Puerta 1: Ayrton aprueba el guion** (texto de voz + una línea por escena).
3. **Estructura técnica (shooting script)** basada en la biblioteca de referencias (`referencias/SINTESIS.md` y los desgloses): tabla de planos con cámara, transición de salida, texto en pantalla, sfx y música. ✋ **Puerta 2: Ayrton aprueba la tabla y 3–4 cuadros clave** (se sacan con `./reel preview`, antes de renderizar).
4. **Armar el video** y mostrarlo (`./reel render`), con el desglose técnico guardado junto al video.

Lo que se agregó al flujo original de cuatro pasos, y por qué:
- **Voz antes del guion técnico.** Los cortes tienen que caer en las frases, y eso se sabe recién cuando está la voz (`./reel voz`). Por eso el paso 3 se hace con los tiempos reales de la voz.
- **Música y BPM elegidos antes del paso 3.** En las referencias los cortes caen a ±0,1 s de un golpe del ritmo; hay que saber el beat para ubicarlos (ver SINTESIS.md). En un reel hablado, el ritmo lo lleva la voz y el sonido es escaso.
- **Elegir 1–3 referencias por reel** de la biblioteca, según la idea (tabla de CAMARA-3D.md), y **no repetir** hook, analogía, mundo 3D, plan de cámara ni transiciones del reel anterior.
- **Dos puertas, no una:** la segunda evita renderizar minutos de video que Ayrton no quiere (lección de la v3 del Parrot).
- **Revisión antes de mostrar:** `./reel revisar --quietud` sin errores y los cuadros mirados como un extraño (docs/MOVIMIENTO.md §7).
- **Cada referencia nueva** que pase Ayrton se analiza (`./reel analizar`), se guarda su desglose y se suma a SINTESIS.md: la biblioteca crece con el uso.

## Pasos detallados
1. **Fuente**: leer el link/tema completo (WebFetch/WebSearch). Extraer: objetivo, pasos o ideas clave, comandos o fórmulas, advertencias. Verificar contra la fuente oficial.
2. **Guion** (ver GUION.md): 5–8 pasos; frase por escena; texto de voz natural; qué se muestra en pantalla por escena. Duración objetivo 45–60 s.
3. **✋ Checkpoint 1**: mostrar el guion al usuario y esperar OK. Pasar luego del texto aprobado a `video.json`.
4. **Crear el video**: `./reel nuevo <tema>` (copia la plantilla a videos/AAAA-MM-tema); completar `video.json` (escenas con duración, `voz.lineas`, `audio`).
5. **Voz primero**: `./reel voz videos/X`. Ajustar texto/tiempos hasta que no haya avisos. Las duraciones de las escenas se acomodan a la voz (voz ≤ fin de escena − 0,1 s; ≥ 0,15 s entre líneas).
6. **Estructura técnica**: completar `docs/SHOOTING-SCRIPT.md` para este reel (guardarla como `videos/X/shooting.md`), con las referencias elegidas, las transiciones (`salida` en `video.json`), la cámara (`rig.toma`) y los sfx con sus tiempos. ✋ **Checkpoint 2**: tabla + 3–4 cuadros (`./reel preview`).
7. **Visual**: editar `index.html` (secciones `.scene`, `data-a`, `data-step`). `preview` en momentos clave (inicio, cada costura, pico de cada movimiento, CTA), mirar cada imagen, corregir desbordes de texto.
8. **Efectos**: `sfx_events.py` con la tabla de significados (AUDIO.md) y los golpes en los mismos instantes que los cortes.
9. **Revisar**: `./reel revisar videos/X --quietud` sin errores; preview en cada costura (docs/MOVIMIENTO.md §7).
10. **Render**: `./reel render videos/X` (scenes → join → mezcla). Revisar `final.mp4` (−14 LUFS, pico ≤ −1,5 dB).
11. **Entrega**: enviar mp4 + descripción (con créditos de la voz: Piper es_AR-daniela, CC BY-SA 4.0, y de la fuente) + el desglose técnico (`shooting.md`).
12. **Cierre**: registrar correcciones en DECISIONES.md y palabras nuevas en pronunciacion.json; commit.
