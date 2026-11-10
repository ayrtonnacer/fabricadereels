# Analizar videos de referencia (un documento por video)
Flujo vigente (2026-11-10). La medición la hace `engine/analisis/medir.py` (ver `docs/MEDICION.md`); la lectura cualitativa la hace Claude mirando los cuadros.

## Cómo se llaman los documentos de rodaje
- **Guion técnico** (*shooting script*): tabla plano por plano de un video que VAMOS A HACER. Plantilla: `videos/_plantilla/script-tecnico.md`.
- **Storyboard**: el mismo guion dibujado cuadro por cuadro.
- **Desglose de planos** (*shot breakdown*): el guion técnico hecho al revés, a partir de un video que YA existe. Es lo que genera este flujo: `SCRIPT-TECNICO-REFERENCIA.md` (medido) + `analisis.md` (lectura).
- Vocabulario (dolly, orbit, whip pan, match cut, L-cut…): `docs/GLOSARIO-EDICION.md`. Reglas de movimiento y transiciones: `docs/MOVIMIENTO.md`.

## Flujo (cuando Ayrton dice "analizá este video")
1. **Recibir el video**: adjunto en el chat (o en `assets/referencias/`). Preguntar qué quiere aprender y, si hay voz, pedir la transcripción.
2. **Medir**: `python engine/analisis/medir.py <video> docs/referencias/externos/<slug> [--transcripcion t.txt] [--hojas]` → `INFORME.md`, `SCRIPT-TECNICO-REFERENCIA.md`, `metricas.json`, `hoja_resumen.jpg`.
3. **Mirar los cuadros** (Read sobre `hoja_resumen.jpg` y, con `--hojas`, las hojas de 60 cuadros). **Nunca confiar solo en los números**: en motion graphics 2D se mueven los elementos, no una cámara, y la medición de cámara solo describe el desplazamiento global.
4. **Completar el desglose cualitativo** en `docs/referencias/externos/<slug>/ANALISIS.md` (frase de la idea; estructura hook→payoff; qué se ve y qué texto; técnicas; transiciones con el vocabulario de `docs/MOVIMIENTO.md`; **cómo hacerlo en nuestro stack**: three.js + `escena3d.js`).
5. **Sumar** una fila a `docs/referencias/PARAMETROS.md` y, si aparece un patrón nuevo, a `docs/referencias/SINTESIS.md`.
6. **Anotar** en `docs/BITACORA.md`. Se toma la **estructura**, nunca el contenido (ni el look de otra marca).

Los 10 análisis hechos hasta ahora están en `docs/referencias/externos/` (índice: `INDICE.md`; síntesis: `SINTESIS.md`; leer la síntesis antes de armar un script técnico).
