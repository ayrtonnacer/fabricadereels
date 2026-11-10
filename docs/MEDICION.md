# Medición: de "se siente" a números que se pueden repetir
**Idea** (video de *Crea con LuisPa*, repo MIT `luispablovillasenor-afk/shorts-animados-claude`): no le preguntes a la IA qué opina de un video, **ponela a medir**. *"Una opinión no la puedes recrear, un número sí."* Nuestra herramienta propia (`engine/analisis/medir.py`) toma esa idea y la adapta a motion graphics, con audio y script técnico automático.

## Para qué sirve (tres usos)
1. **Analizar videos de referencia** que pase Ayrton (transiciones, movimientos de cámara, planos, sonido) y convertirlos en parámetros y en un **script técnico medido**, sin que él tenga que describirlos.
2. **Verificar nuestros reels** antes de entregarlos (¿la cámara se mueve de forma suave?, ¿el ritmo de palabras es el que queremos?, ¿los cortes caen donde pensamos?).
3. **Comparar** un reel propio contra una referencia y ver qué número se aleja (`comparar.py`).

## Cómo pasarme un video de referencia
- **Adjuntá el .mp4** en el chat (arrastrar el archivo). Eso es todo: lo leo como archivo, no hace falta ningún "lenguaje de código".
- Mejor un **recorte de 20–60 s** (alcanza y pesa poco). Con audio original si querés medir sonido.
- YouTube/TikTok **no se pueden abrir desde la nube** (bloqueados). En tu compu: `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 "<link>"` o una grabación de pantalla, y lo adjuntás.
- Si querés medir también el ritmo de la voz, pegá la **transcripción** (los subtítulos del video sirven).
- Yo corro `medir.py`, guardo el informe y el script técnico en `docs/referencias/externos/<nombre>/ (o `propios/<reel>/`)`, agrego los números a `docs/referencias/PARAMETROS.md` y te cuento qué aprendí. **Se toma la estructura (ritmo, cámara, sonido), nunca el contenido.**

## Comandos
```
python engine/analisis/medir.py video.mp4 salida/ [--transcripcion texto.txt] [--hojas]
python engine/analisis/comparar.py referencia/metricas.json propio/metricas.json [--tolerancia 25]
python engine/analisis/medir.py --autotest      # verifica el método con movimientos sintéticos conocidos
```
Salida en `salida/`: `INFORME.md` (lectura en español), `SCRIPT-TECNICO-REFERENCIA.md` (un renglón por plano), `metricas.json`, `medidas.csv` (por cuadro), `hoja_resumen.jpg` (1 cuadro por segundo) y, con `--hojas`, hojas de 60 cuadros con su número. Un reel de 33 s se mide en ~14 s.

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
| Palabras por segundo | ritmo de la narración | **solo con transcripción** (palabras ÷ segundos). Sin ella no se estima: el intento de estimarlo por sílabas del audio resultó engañoso (daba 6,0 cuando el real es ~8,6) y se descartó |

## Calibración y límites (cómo sabemos que no miente)
- **Autotest**: imágenes con desplazamientos y zooms conocidos; la traslación sale exacta y el zoom dentro de ±0,25 puntos.
- Validado contra el reel de WiFi, donde conocemos la verdad: 6 cortes reales (3,2 · 7,8 · 13,0 · 17,6 · 25,2 · 29,1 s → detecta 6, con 3,03 s por el inicio del zoom-through), voz activa 79,3 % medida vs 79,5 % real.
- Errores que aparecieron y se corrigieron: detector de cortes por diferencia (1 de 6), voz activa subestimada (63 % → umbral calibrado), zoom que explotaba sin correlación confiable (limitado a ±8 %/cuadro y cuadros sin confianza no cuentan).
- **No mide**: el gusto, el significado, la rotación de cámara (aproximada, se descarta), ni separa cámara de objetos que se mueven (en 3D con piso fijo suele coincidir). Los números describen; **decidir sigue siendo de Ayrton**.

## 30 fps: ¿grabamos a 30? Sí
30 fps es el estándar de contenido explicativo en redes (cine 24; web/redes 30; 60 para acción rápida o gaming). Reels, TikTok y Shorts aceptan hasta 60. Nuestros reels se renderizan a **30 fps** (HyperFrames por defecto) y está medido que alcanza: la cámara va a una velocidad mediana de **13 px/s** y su p95 es **141 px/s ≈ 4,7 px por cuadro**; el parpadeo por saltos recién aparece cuando el movimiento pasa de ~15 px por cuadro. 60 fps duplicaría el tiempo de render sin ganancia visible; solo valdría para movimientos muy rápidos. El analizador mide cada cuadro a la tasa nativa del video (si una referencia está a 60 fps, mide a 60).

## Primeros hallazgos (reel de WiFi v4 vs ejemplo externo del repo)
- Cámara en movimiento en **67 %** de los cuadros (el ejemplo externo: 66 %; el video que vio Ayrton hablaba de 65 %): coincidencia con la "cámara que nunca se queda quieta".
- Nuestra cámara es **mucho más lenta** que la del ejemplo (mediana 13 vs 110 px/s; 93 % de movimiento lento vs 49 %) y **mucho más suave** (jerk mediano ~450 vs ~2.400 px/s³): es el estilo de dolly lento y orbitas con ease que queremos.
- Ritmo: 6 cortes (plano mediano 4,6 s) contra 8 cortes en 9,8 s del ejemplo (plano mediano 0,7 s): somos mucho más calmos. Es una decisión de estilo, no un error.
- **Voz: 3,11 palabras por segundo** en total (3,9 mientras se habla). La referencia que cita el video de LuisPa (canal de referencia *Zack D. Films*) es **2,77**: vamos ~12 % más rápido, y por encima de la regla de planificación de `docs/GUION.md` (2,3). Para público que está aprendiendo conviene bajar a ~2,8: `voz.length_scale` ≈ 1,0 o ~10 % menos palabras.
- Audio: −14,0 LUFS, 0,3 % de silencio (casi no hay aire entre frases); la referencia externa tiene 0 %.

## Regla de uso
Antes de entregar un reel: `medir.py` sobre `final.mp4` con la transcripción, mirar el **tirón**, el **ritmo de palabras** y que los **cortes** caigan donde dice el script técnico; guardar el informe en `videos/X/analisis/` y sumar la fila a `docs/referencias/PARAMETROS.md`. Cuando Ayrton pase una referencia: medirla primero y recién después proponer.
