# Medición: de "se siente" a números que se pueden repetir
**Idea** (video de *Crea con LuisPa*, repo MIT `luispablovillasenor-afk/shorts-animados-claude`): no le preguntes a la IA qué opina de un video, **ponela a medir**. *"Una opinión no la puedes recrear, un número sí."* Nuestra herramienta propia (`engine/analisis/medir.py`) toma esa idea y la adapta a motion graphics, con audio, transiciones y ritmo de cámara medidos.

## Para qué sirve (tres usos)
1. **Analizar videos de referencia** que pase Ayrton (transiciones, movimientos de cámara, planos, sonido) y convertirlos en **números** (cortes, transiciones, cámara, ritmo, sonido) que se suman a la biblia de estilo, sin que él tenga que describirlos.
2. **Verificar nuestros reels** antes de entregarlos (¿la cámara se mueve de forma suave?, ¿el ritmo de palabras es el que queremos?, ¿los cortes caen donde pensamos?) con `comparar.py` contra las metas.
3. **Comparar** un reel propio contra la biblia de estilo (`docs/referencias/BIBLIA-DE-ESTILO.md`) o contra un video puntual, y ver qué número se aleja.

## Cómo pasarme un video de referencia
- **Adjuntá el .mp4** en el chat (arrastrar el archivo). Eso es todo: lo leo como archivo, no hace falta ningún "lenguaje de código".
- Mejor un **recorte de 20–60 s** (alcanza y pesa poco). Con audio original si querés medir sonido.
- YouTube/TikTok **no se pueden abrir desde la nube** (bloqueados). En tu compu: `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 "<link>"` o una grabación de pantalla, y lo adjuntás.
- Si querés medir también el ritmo de la voz, pegá la **transcripción** (los subtítulos del video sirven).
- Yo corro `medir.py`, guardo el informe en `docs/referencias/externos/<nombre>/` (o `propios/<reel>/`), regenero las tablas con `python engine/analisis/biblia.py` y te cuento qué aprendí. **Se toma la estructura (ritmo, cámara, sonido), nunca el contenido.**

## Comandos
```
python engine/analisis/medir.py video.mp4 salida/ [--transcripcion texto.txt] [--hojas]
python engine/analisis/comparar.py propio/metricas.json                       # contra las metas (metas.json) y las referencias afines
python engine/analisis/comparar.py referencia/metricas.json propio/metricas.json [--tolerancia 25]   # contra un video puntual
python engine/analisis/biblia.py                                          # regenera las tablas de la biblia de estilo
python engine/analisis/medir.py --autotest      # verifica el método con movimientos sintéticos conocidos
```
Salida en `salida/`: `INFORME.md` (lectura en español, con tabla de cortes/transiciones y de movimientos de cámara), `metricas.json`, `medidas.csv` (por cuadro), `hoja_resumen.jpg` (1 cuadro por segundo) y, con `--hojas`, hojas de 60 cuadros con su número. Un reel de 33 s se mide en ~14 s.

## Qué se mide y cómo leerlo
| Métrica | Qué es | Cómo se mide |
|---|---|---|
| Cortes y plano mediano | cuántos cortes hay y cuánto dura cada plano | la **respuesta de la correlación de fase** se desploma (≈0,9 → <0,2) + salto del histograma de color. En motion graphics el fondo no cambia entre escenas, así que la "diferencia de cuadros" sola **no sirve** (probado). Se distinguen corte seco y transición |
| Cámara en movimiento (%) | en qué % de los cuadros la imagen se desplaza o se agranda | **correlación de fase** entre cuadros consecutivos: convierte cada cuadro a frecuencias (FFT) y el pico de la correlación da el desplazamiento exacto; el zoom sale de lo mismo sobre el espectro en coordenadas log-polares (Fourier–Mellin) |
| Velocidad (px/s a 1080 de ancho) | rapidez de la cámara; **mediana** y p95 | desplazamiento por cuadro × fps |
| Movimiento lento (%) | parte del movimiento < 100 px/s: "deriva casi imperceptible" | ídem |
| Zoom neto (%/s) | + acerca / − aleja | log-polar, calibrado (corrección ×1,10) |
| **Tirón (jerk)** (px/s³) | qué tan bruscamente cambia la aceleración; **menos = más suave** | 3.ª derivada de la posición de la cámara (Savitzky–Golay) dentro de los tramos de movimiento. Es lo que delata un movimiento "mecánico" frente a uno con ease |
| Brillo, contraste, saturación, colores dominantes | el look medido | media de luminancia, su desvío, saturación HSV, moda de colores cuantizados |
| Audio | LUFS, rango dinámico, pico, % de silencio, ataques por segundo, golpes graves, % de voz activa | EBU R128 (ffmpeg) + análisis espectral propio |
| Transiciones | por cada corte: velocidad de cámara en los 0,3 s previos, plano que sigue, distancia al golpe de sonido más cercano; % de cortes con movimiento fuerte antes y % sobre un golpe (±0,1 s) | de la misma detección de cortes y de los ataques de audio |
| Mover–retener–mover | movimientos notorios (pico ≥ 100 px/s) cada 10 s, su pico y duración, retención entre movimientos (≥ 0,5 s), ataque y liberación (tiempo del 10 % al pico y del pico al 10 %) | tramos de movimiento de la cámara; ataque y liberación sobre la velocidad suavizada |
| Palabras por segundo | ritmo de la narración | **solo con transcripción** (palabras ÷ segundos). Sin ella no se estima: el intento de estimarlo por sílabas del audio resultó engañoso (daba 6,0 cuando el real es ~8,6) y se descartó |

## Calibración y límites (cómo sabemos que no miente)
- **Autotest**: imágenes con desplazamientos y zooms conocidos; la traslación sale exacta y el zoom dentro de ±0,25 puntos.
- Validado contra el reel de WiFi, donde conocemos la verdad: 6 cortes reales (3,2 · 7,8 · 13,0 · 17,6 · 25,2 · 29,1 s → detecta 6, con 3,03 s por el inicio del zoom-through), voz activa 79,3 % medida vs 79,5 % real.
- Errores que aparecieron y se corrigieron: detector de cortes por diferencia (1 de 6), voz activa subestimada (63 % → umbral calibrado), zoom que explotaba sin correlación confiable (limitado a ±8 %/cuadro y cuadros sin confianza no cuentan).
- **No mide**: el gusto, el significado, la rotación de cámara (aproximada, se descarta), ni separa cámara de objetos que se mueven (en 3D con piso fijo suele coincidir). Los números describen; **decidir sigue siendo de Ayrton**.

## 30 fps: ¿grabamos a 30? Sí
30 fps es el estándar de contenido explicativo en redes (cine 24; web/redes 30; 60 para acción rápida o gaming). Reels, TikTok y Shorts aceptan hasta 60. Nuestros reels se renderizan a **30 fps** (HyperFrames por defecto) y está medido que alcanza: la cámara va a una velocidad mediana de **13 px/s** y su p95 es **141 px/s ≈ 4,7 px por cuadro**; el parpadeo por saltos recién aparece cuando el movimiento pasa de ~15 px por cuadro. 60 fps duplicaría el tiempo de render sin ganancia visible; solo valdría para movimientos muy rápidos. El analizador mide cada cuadro a la tasa nativa del video (si una referencia está a 60 fps, mide a 60).

## Hallazgos
Van en un solo lugar, con números y comparados con las referencias: `docs/referencias/BIBLIA-DE-ESTILO.md`. (Voz del WiFi v4: 3,11 palabras/s contra una meta de 2,6–2,9; ver la biblia.)

## Regla de uso
Antes de entregar un reel: `medir.py` sobre `final.mp4` con la transcripción, mirar el **tirón**, el **ritmo de palabras** y que los **cortes** caigan donde dice el `plan.md`; correr `comparar.py videos/X/analisis/metricas.json`, guardar el informe en `docs/referencias/propios/<reel>/` y correr `biblia.py`. Cuando Ayrton pase una referencia: medirla primero y recién después proponer.

## earshot: oídos para el audio (Leonxlnx/earshot, MIT)
- Sirve para **describir y comparar sonidos con palabras y números**: `earshot describe a.wav`, `earshot ab A.wav B.wav` (diferencias en palabras + parecido CLAP), `earshot critique film.mp4` (tarjeta contra films profesionales), `earshot timeline`, `earshot sfx/kit` (banco de 252 efectos hechos en código). Usado el 2026-11-11 para afinar la voz Adjutant (`docs/AUDIO.md`).
- **No viene instalado**: en cada sesión nueva hay que instalarlo (≈ 10 min la primera vez): `git clone https://github.com/Leonxlnx/earshot` → `python3 -m venv v && v/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu && v/bin/pip install -e earshot` → `v/bin/earshot doctor --fetch` (baja 1,1 GB de modelos). Requiere salida a internet a: `huggingface.co`, `cdn-lfs.huggingface.co`, `cdn-lfs.hf.co`, `cas-bridge.xethub.hf.co`, `cas-server.xethub.hf.co`, `us.aws.cdn.hf.co`, `download.pytorch.org` (ya están en el entorno "fabricadereels", creado el 2026-11-11).
- Lección: el parecido CLAP (coseno) mide sobre todo el contenido (voz, frase); usarlo para **comparar variantes entre sí**, y confiar en `describe`/`ab` (brillo, cola, piso de ruido, etiquetas AudioSet) para saber QUÉ cambiar.
