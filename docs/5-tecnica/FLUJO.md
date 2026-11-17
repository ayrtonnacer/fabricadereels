# Flujo para hacer un reel (paso a paso)
Cada paso tiene: **qué leer**, **qué hacer**, y **listo cuando** (la condición para pasar al siguiente). Comandos desde la raíz del repo. `X` = carpeta del video (`videos/AAAA-MM-tema`).
No saltear pasos ni adelantarse: animar antes del OK del guion es el error más caro.

## 0. Preparar
- **Leer**: `docs/1-canal/PREFERENCIAS.md` (entero; es corto).
- **Hacer**: guardar todo lo que Ayrton pasó (PDF, capturas, audio, texto) en `docs/4-referencias/material/` y anotar su pedido en `docs/1-canal/BITACORA.md` (una línea con fecha).
- **Listo cuando**: el material está en el repo.

## 1. Fuente
- **Hacer**: leer la fuente completa (WebFetch; si falla, `curl` desde Bash). Sacar: la idea central, el mecanismo (el porqué), 2–4 datos concretos, y qué se presta a mostrarse en 3D.
- **Verificar cada dato contra la fuente primaria o midiéndolo** (documentación oficial, paper, o la herramienta real: p. ej. los tokens se contaron con tiktoken). Los artículos de divulgación, aunque sean de empresas grandes, traen ejemplos inventados.
- El guion cubre el **tema central** de la fuente; los ángulos laterales se ofrecen como otros reels.
- **Listo cuando**: hay una lista de datos verificados con su origen.

## 2. Guion
- **Leer**: `docs/3-guion/GUION.md`, `docs/1-canal/PUBLICO.md`.
- **Hacer**: `python engine/reel.py nuevo AAAA-MM-tema`. Completar `guion.md` y, en `video.json`: `titulo`, `tema`, `fuente`, `scenes` (dejar `portada` 0.1 primero y `cierre` último; el medio, una escena por idea) y `voz.lineas` (con `t` estimado: ≈ 3 palabras por segundo mientras habla + 0,4 s de pausa entre frases). Cambiar el tema en `compositions/cierre.html`.
- Para un tema nuevo, ofrecer 2–3 ángulos distintos antes de escribir.
- `python engine/reel.py guion X` → corregir todo ✕.
- **Listo cuando**: `reel.py guion` no da errores y el guion pasa el checklist de `GUION.md`.

## 3. ✋ Checkpoint con Ayrton
- **Mostrar** (en el chat, corto): la idea en una frase; la tabla **escena | lo que se ve | voz | duración**; por escena, el plano y el movimiento de cámara en vocabulario de cine (`docs/2-estilo/GLOSARIO-EDICION.md`); el título de portada; los datos con su fuente; palabras con pronunciación dudosa (ofrecer variantes de audio).
- **Esperar su OK.** Si corrige: aplicar, anotar en `BITACORA.md`, volver a mostrar solo lo que cambió.
- Excepción: si pidió "hacelo directo", seguir sin esperar.

## 4. Voz y tiempos
- **Hacer**: `python engine/reel.py voz X`. Si `voz.py` marca ⚠ (una línea se pasa de su escena o pisa a otra): ajustar `t` de la línea o `d` de la escena en `video.json` y volver a correr. La escena dura lo que pide la voz (la voz termina ≥ 0,1 s antes del fin de la escena; ≥ 0,15 s entre líneas).
- Esto genera `index.html`, `assets/tiempos.js`, un plano por escena y los subtítulos. **A partir de acá ningún tiempo se escribe a mano.**
- **Listo cuando**: voz sin avisos y el ritmo está en 2,4–2,8 palabras por segundo.

## 5. Plan de cámara
- **Leer**: `docs/2-estilo/CAMARA.md`, `docs/2-estilo/ESTILO.md`.
- **Hacer**: completar `plan.md`: las estaciones del set (qué idea vive en cada una y dónde), y por cada frase de voz: plano, ángulo, movimiento de llegada, qué aparece y con qué palabra, sonido. Regla de oro: **un movimiento por idea nueva; quieta mientras se nombra**.
- El recorrido de este reel **no copia el del reel anterior** (mirar `plan.md` del último video en `videos/LEEME.md`).
- **Listo cuando**: cada frase tiene su plano y cada viaje de cámara su motivo.

## 6. El set (`assets/set.js`)
- **Leer**: `docs/5-tecnica/THREEJS.md` (funciones de `E`), y `videos/_plantilla/assets/set.js` como molde (`videos/2026-11-tokens-1-v2/assets/fabrica.js` es un ejemplo completo de 49 s).
- **Hacer**, en este orden: (1) estaciones; (2) objetos y rótulos; (3) lista `CAM` de poses; (4) `dibujar(T)`. Tiempos siempre con `cuando('l03', 'palabra')` / `ESC.<escena>.t0`.
- Encuadrar sin renderizar: `python engine/reel.py encuadre "px,py,pz" "lx,ly,lz" "x,y,z" …` dice en qué píxel cae cada punto. Lo que se lee: x 60–1020, y 200–1100.
- Objetos nuevos: relleno `E.std()` + `E.contornear()`; colores `P.edge`, `P.hi`, `P.acc`. Si un objeto sirve para otros reels, va a un archivo aparte (`assets/<tema>3d.js`).

## 7. Revisar y mirar cuadros (repetir hasta que quede bien)
- `python engine/reel.py revisar X` → 0 errores (✕). Los avisos (⚠) se leen y se corrigen o se justifican.
- `python engine/reel.py cuadros X` → abrir `X/out/cuadros/contact-sheet.jpg` y **mirar cada cuadro** preguntando:
  1. Cuadro 0: ¿se entiende la idea en miniatura? Firma + título de 3–5 palabras + objeto, nada detrás del título.
  2. ¿Lo que nombra la voz está entero, quieto y legible, entre y 200 y 1100? ¿Algo pisa los subtítulos (y 1120–1320)?
  3. ¿Hay rótulos encimados, pegados entre sí o con una palabra sola en la última línea?
  4. ¿Cables que no tocan, líneas cortadas, objetos atravesados, algo que asoma detrás de un texto?
  5. ¿Se usa un solo acento tan por plano y significa "mirá acá"?
  6. Cierre: CTA grande y centrado, firma chica debajo, texto igual a la voz.
- Un cuadro dudoso se vuelve a sacar solo: `python engine/reel.py cuadros X 12.4,13.1`. Cambiar **una cosa por vez**.
- **Listo cuando**: revisar da 0 errores y los 6 puntos están bien en todos los cuadros.

## 8. Sonido (`sfx_events.py`)
- **Leer**: `docs/2-estilo/AUDIO.md`.
- **Hacer**: un renglón por cosa que pasa en `set.js`, con el mismo tiempo. `P.apertura()` y `P.cierre(...)` no se tocan. `P.viaje(t)` en el **pico** de cada viaje de cámara (la mitad del viaje). Menos sonidos que movimientos.

## 9. Render, medir, corregir
- `python engine/reel.py render X` → `final.mp4`. Si pasa de 3 s por segundo de video: simplificar el set.
- `python engine/reel.py medir X` → mirar "Fuera de la meta", el arrastre (continuidad) y el barro (graves). Lo que queda fuera se corrige o se justifica en `plan.md`. `--escuchar` (Whisper) antes de entregar: palabras que se entienden mal → `pronunciacion.json`.
- Mirar 3–4 cuadros del `final.mp4` en los viajes de cámara (no deben verse saltos).

## 10. Entregar
- Escribir `descripcion.md` (gancho + 2–3 líneas + fuentes + créditos: "Voz: Piper es_AR-daniela, CC BY-SA 4.0" + hashtags).
- `python engine/reel.py entregar X` y completar su lista. Repasar `PREFERENCIAS.md` contra el video.
- Contarle a Ayrton, en vocabulario de cine y con segundos, qué hace la cámara y qué quedó fuera de las metas. Mandarle el `final.mp4` y la portada.
- `video.json → "estado": "listo"`, fila en `videos/LEEME.md`, commit y push a `main`.

## 11. Después de sus correcciones
- Cada corrección: `BITACORA.md` (una línea) → si es una regla nueva, `PREFERENCIAS.md` en su sección (reemplazar, no apilar) → al cerrar el video, resumen en `DECISIONES.md`. Palabras corregidas → `pronunciacion.json` con `estado: "ok"`.
- Cambios chicos: tocar solo lo afectado, `reel.py cuadros X <tiempos>` y volver a renderizar.
- Cuando publique: `"estado": "publicado"` y el feedback en `docs/1-canal/PUBLICO.md`.

## Errores típicos y cómo se arreglan
| Síntoma | Causa | Arreglo |
|---|---|---|
| `check` se queda esperando o una escena sale negra | error de JavaScript en `set.js` (el timeline no se registró) | mirar la consola en `npx hyperframes snapshot`; revisar nombres de funciones de `E` |
| Un objeto no aparece cuando la voz lo nombra | tiempo escrito a mano o `cuando()` con una palabra que no está en la línea | `reel.py revisar` lo marca; usar la palabra exacta del texto |
| Cambió la voz y la imagen quedó corrida | no se corrió `reel.py voz` | correrlo; todo se reacomoda |
| El sonido es el viejo | `sfx_events.py` falló | `reel.py audio X` y leer el error |
| Un rótulo queda en el lugar del cuadro anterior | se movió la cámara después de ubicarlo | `R.dibujar(T)` va al final de `dibujar`, después de `E.ruta` |
| Render lento (> 3 s por segundo) | set pesado | menos mallas y segmentos; sin sombras ni postproceso (`THREEJS.md`) |
| Texto fuera de cuadro o sobre los subtítulos | cámara muy cerca | `reel.py encuadre` y alejar la cámara o bajar el punto al que mira (sube el objeto) |
