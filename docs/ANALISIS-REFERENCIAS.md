# Analizar videos de referencia (un documento por video)

## Cómo se llaman los documentos de rodaje
- **Guion técnico** (en inglés *shooting script* o *shot list*): la tabla plano por plano de un video que VAMOS A HACER (qué se ve, cámara, movimiento, texto, sonido, transición). Plantilla en `docs/SHOOTING-SCRIPT.md`.
- **Storyboard**: el mismo guion pero dibujado cuadro por cuadro.
- **Desglose de planos** (*shot breakdown*): el guion técnico hecho al revés, a partir de un video que YA existe. Eso es lo que genera este flujo con los videos de referencia: `referencias/<nombre>/analisis.md`.
- Vocabulario de edición (dolly, orbit, whip pan, match cut, L-cut…): `docs/GLOSARIO-EDICION.md`.

## Flujo (cuando Ayrton dice "analizá este video")
1. **Cargar el video** (ver `assets/referencias/LEEME.md`: adjuntarlo en el chat o dejarlo en `assets/referencias/`). Pedir qué quiere aprender (cámara, ritmo, sonido, estructura…) y qué tramo importa.
2. **Medir**: `python engine/analizar_video.py <video> --nombre <slug> --fuente <link> --objetivo "<qué aprender>" [--desde S --hasta S]`
   Genera en `referencias/<slug>/`: `analisis.md` (borrador con tablas medidas), `planos.json`, `audio.json`, `meta.json` y las hojas `hoja-planos-N.jpg` (inicio/medio/fin de cada plano) y `hoja-tiempo.jpg` (un cuadro cada tantos segundos) y `hoja-cortes-N.jpg` (cuadros casi consecutivos de −0,2 a +0,2 s alrededor de cada corte: ahí se ve cómo está hecha cada transición, el blur, el destello, la dirección). `referencias/INDICE.md` se actualiza solo. Si ya existe `analisis.md`, el borrador nuevo se guarda como `analisis.auto.md` (no se pisa trabajo hecho).
3. **Mirar las hojas de cuadros** (Read sobre los jpg). Nunca confiar solo en los números: el movimiento se mide en 2D y falla en latigazos, órbitas alrededor de un objeto centrado, grúas combinadas y escenas con poca textura. Corregir en el documento lo que el ojo ve distinto.
4. **Completar `analisis.md`** (para las transiciones usar el vocabulario de `docs/MOVIMIENTO.md`: corriente, vector, portador, curva/zoom/foco/latigazo): frase de la idea, estructura (hook/payoff), qué se ve y qué texto hay en cada plano, qué suena (voz, música, efectos, ambiente), **técnicas para tomar** con su traducción a `engine/camara3d.js`, **qué NO copiar** y **ideas para nuestros reels**.
5. **Guardar**: commit del `.md`/`.json` (los jpg y el video no van a git). Resumir a Ayrton en pocas líneas qué se aprendió y qué proponemos.
6. Si una técnica entra al motor o a las reglas, anotarla en `docs/CAMARA-3D.md` / `docs/DECISIONES.md`.

## Reglas
- De una referencia se toma **la técnica** (tiempos, tipo de movimiento, easing, ritmo de cortes, momento del sonido), no el look: la estética, la voz y la música son las de @ayrtonnacer. No se copian textos, gráficos ni identidad del otro creador.
- Cada análisis termina con al menos una idea que sirva a un reel distinto de los anteriores (regla de variedad en `docs/CAMARA-3D.md`).
- Con varios videos del mismo tipo, comparar en una tabla en `referencias/INDICE.md` o en un `referencias/sintesis-<tema>.md` (patrones que se repiten = receta confiable).

## Qué mide la herramienta
| Dato | Cómo | Confiabilidad |
|---|---|---|
| Cortes y planos | cambio de histograma de color + diferencia de cuadros | buena; las disolvencias suaves pueden pasar desapercibidas |
| Movimiento de cámara por plano y por tramo | flujo óptico (LK) + transformación afín: desplazamiento, zoom, giro | buena en push-in, travelling, zoom through; floja en latigazos, órbitas, grúas |
| Velocidad y perfil (ease) | magnitud por segundo y forma en tercios del plano | orientativa |
| Ritmo | cortes/min y duración media de plano | buena |
| Volumen (LUFS, pico, rango) | ffmpeg ebur128 | buena |
| Golpes/whooshes y silencios | detección de ataques en la envolvente + brillo espectral | candidatos; confirmar escuchando |
