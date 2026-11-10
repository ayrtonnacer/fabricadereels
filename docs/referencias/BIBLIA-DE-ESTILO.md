# Biblia de estilo medida
Qué funciona en un reel de motion graphics, **con números**. Se construye midiendo videos (`engine/analisis/medir.py`) y no se opina sobre ellos: *"una opinión no la puedes recrear, un número sí"* (idea del repo de LuisPa, `docs/MEDICION.md`). Es el equivalente a su "biblia de estilo", pero de nuestro estilo (HackTheBox, 3D, explicativo).

- **Cómo se usa**: antes de planear un reel se leen las metas (`metas.json`, abajo); se escriben en `videos/X/plan.md`; después de renderizar se corre `python engine/analisis/comparar.py videos/X/analisis/metricas.json` y se corrige lo que quede fuera de rango.
- **Datos**: una carpeta por video en `externos/` (referencias) y `propios/` (nuestros reels), cada una con `INFORME.md` (lectura), `metricas.json` (números) y `hoja_resumen.jpg` (un cuadro por segundo).
- **Grupos**: *Todas* = las 11 referencias (10 de Ayrton + el ejemplo de LuisPa). *Afines* = las 3 oscuras y contemplativas más parecidas a lo que queremos: `motion-ref-2` (lente explosionada 3D), `motion-ref-3` (anuncio de tarjetas de vidrio, un solo plano), `motion-ref-4` (miedo y codicia). Otras 7 son otro género (promos, collage, glitch: 34–82 cortes por minuto) y se usan solo como contraste; `motion-ref-5` (explicador de 104 s, brillo 0,89) no entra en ninguno de los dos grupos.
- **Límite**: las metas salen de solo 3 videos afines; son provisorias hasta sumar más. Los números describen; decidir sigue siendo de Ayrton.

## Lo que dicen los números (2026-11-10, WiFi v4 contra las afines)
| # | Hallazgo | Afines | WiFi v4 |
|---|---|---|---|
| 1 | **Nuestros movimientos de cámara son ~3 veces más chicos y lentos, aunque igual de frecuentes.** Pico de un movimiento notorio | 916 px/s (872–2995) | **270 px/s** |
| 2 | Misma frecuencia de movimientos: cada 10 s | 3,0 (1,6–4,4) | 3,6 |
| 3 | Velocidad mediana / p95 de la cámara | 33 (22–69) / 526 px/s | **13 / 116 px/s** |
| 4 | Suavidad (tirón mediano; menos = más suave) | 516 px/s³ | 449 ✓ |
| 5 | Cortes por minuto y plano mediano | 9,0 · 4,3 s | 10,9 · 4,6 s ✓ |
| 6 | **Menos cortes llegan "con cámara": transición con movimiento fuerte antes** | 40 % (0–67) | **17 %** |
| 7 | Cortes sobre un golpe de sonido (±0,1 s) | 50 % (40–100) | 67 % ✓ |
| 8 | Movimiento: ataque / liberación | 0,13 / 0,40 s | 0,20 / 0,20 s (liberación corta: frena rápido) |
| 9 | Palabras por segundo | 2,77 (referencia citada) | **3,11** |
| 10 | Saturación media | 0,52 (0,35–0,54) | **0,72** (neón muy vivo) |
| 11 | Golpes graves | 4 (2–41) | 11 |
| 12 | Volumen / pico real | −14,2 LUFS / −0,9 dBTP | −14,0 / −1,7 ✓ |

**Qué hacer con eso**: (a) subir el pico de los movimientos notorios a 800–3000 px/s manteniendo la duración (~1,2–1,5 s) y el tirón < 650; (b) que al menos 3 de cada 10 cortes lleguen después de un movimiento fuerte (zoom a través de un objeto, barrido); (c) bajar la voz a 2,6–2,9 pal/s; (d) revisar la saturación del neón.

## Cómo se ven los dos géneros (medianas del grupo)
| | Contemplativas (afines, n = 3) | Vertiginosas (n = 7: frames, nokia, ref-1, templates, promo, glitch, alejandro) |
|---|---|---|
| Cortes por minuto | 9,0 | 33,6–82,4 |
| Plano mediano | 4,3 s | 0,58–1,47 s |
| Tirón mediano | 516 px/s³ | 456–10.396 px/s³ |
| Brillo medio | 0,06 | 0,25–0,64 |
| Uso | **meta de nuestros reels explicativos** | contraste, no meta |

## Patrones medidos en las afines (qué las hace funcionar)
- **Mover–retener–mover**: motion-ref-2 retiene 1,87 s entre movimientos (la más alta); el pico de sus reencuadres es 872 px/s durante ~1,2 s. motion-ref-3 mantiene un plano continuo de 6,42 s y se mueve en el 86 % de los cuadros.
- **Plano continuo**: 2 de las 3 afines tienen ≤ 3 cortes en 20–25 s (4,8–9,0 cortes por minuto).
- **Cámara casi siempre en movimiento** (63–86 % de los cuadros) pero **lenta en la mayor parte** (57–81 % del movimiento va por debajo de 100 px/s): la deriva sutil rellena y los movimientos notorios (cada 3 s aprox.) marcan los momentos.
- **Sonido**: 3,3–4,3 ataques por segundo; −14,2 LUFS; casi sin silencio (0,1–0,2 %).

## Recursos a evaluar (de las referencias; todavía sin número propio)
Vista explosionada con etiquetas y tooltip (motion-ref-2); texto cinético por palabra con un tic de sonido (motion-ref-4); un objeto que cruza los cortes como portador (motion-ref-1, -4); colores con un solo significado (motion-ref-4: rojo/verde); cierre quieto con silencio previo (motion-ref-3). Si Ayrton quiere uno, se mide cómo lo hace la referencia y se agrega a la tabla.

## Tablas (se regeneran con `python engine/analisis/biblia.py`; no editar a mano)
<!-- TABLAS:inicio -->
### Cada video, número por número

| Parámetro | `motion-inspiration-frames` | `motion-inspiration-nokia` | `motion-ref-1` | `motion-ref-2` | `motion-ref-3` | `motion-ref-4` | `motion-ref-5` | `motion-templates-after-effects` | `pinterest-791437334567656517` | `pinterest-999095498641347187` | `shorts-animados-alejandro` | `2026-11-wifi-v5` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Duración (s) | 18 | 20 | 9 | 20 | 25 | 32 | 104 | 15 | 50 | 9 | 10 | 33 |
| Cortes por minuto | 47,2 | 53,8 | 38,6 | 9,0 | 4,8 | 19,0 | 13,2 | 36,0 | 33,6 | 82,4 | 48,8 | 9,1 |
| Plano mediano (s) | 1,08 | 0,83 | 1,47 | 4,30 | 6,42 | 2,63 | 4,22 | 0,78 | 1,30 | 0,58 | 0,70 | 4,30 |
| Cortes con movimiento fuerte antes (transición) (%) | 14 | 39 | 50 | 67 | 0 | 40 | 0 | 22 | 21 | 25 | 100 | 20 |
| Cortes a ±0,1 s de un golpe de sonido (%) | 64 | 50 | 50 | 100 | 50 | 40 | 96 | 78 | 79 | 100 | 62 | 60 |
| Cámara en movimiento (% cuadros) | 81 | 42 | 85 | 63 | 86 | 85 | 90 | 64 | 60 | 78 | 66 | 68 |
| Velocidad mediana (px/s) | 37 | 201 | 305 | 22 | 69 | 33 | 30 | 161 | 64 | 122 | 110 | 16 |
| Velocidad p95 (px/s) | 428 | 4564 | 2660 | 471 | 1908 | 526 | 487 | 4994 | 2116 | 629 | 1485 | 117 |
| Movimiento lento (< 100 px/s) (%) | 76 | 36 | 19 | 81 | 57 | 71 | 73 | 46 | 56 | 47 | 48 | 94 |
| Zoom neto (+ acerca) (%/s) | 16,84 | -0,91 | -13,03 | -2,12 | -6,41 | 1,83 | -0,78 | 3,39 | -4,63 | 3,07 | -2,44 | 1,77 |
| Tirón mediano (menos = más suave) (px/s³) | 456 | 2858 | 10396 | 516 | 605 | 460 | 336 | 7075 | 1661 | 4837 | 2437 | 518 |
| Movimientos notorios (pico ≥ 100 px/s) cada 10 s | 7,9 | 10,0 | 7,5 | 3,0 | 1,6 | 4,4 | 3,4 | 8,0 | 7,2 | 13,7 | 9,2 | 3,3 |
| Pico mediano de un movimiento notorio (px/s) | 569 | 1822 | 2613 | 872 | 2995 | 916 | 968 | 2064 | 1492 | 438 | 1535 | 335 |
| Duración de un movimiento notorio (s) | 0,98 | 0,55 | 1,40 | 1,21 | 4,00 | 1,55 | 2,67 | 0,51 | 0,75 | 0,59 | 0,57 | 1,37 |
| Retención entre movimientos (≥ 0,5 s) (s) | 0,56 | 0,60 | 0,00 | 1,87 | 0,63 | 0,76 | 0,56 | 0,62 | 0,87 | 0,00 | 0,68 | 0,53 |
| Ataque de un movimiento (10 % → pico) (s) | 0,04 | 0,07 | 0,30 | 0,03 | 0,29 | 0,13 | 0,14 | 0,17 | 0,10 | 0,40 | 0,13 | 0,14 |
| Liberación (pico → 10 %) (s) | 0,52 | 0,12 | 0,22 | 0,40 | 0,44 | 0,13 | 0,47 | 0,10 | 0,23 | 0,23 | 0,17 | 0,13 |
| Brillo medio (0–1) | 0,53 | 0,25 | 0,25 | 0,10 | 0,06 | 0,04 | 0,89 | 0,64 | 0,47 | 0,37 | 0,40 | 0,09 |
| Saturación media (0–1) | 0,08 | 0,23 | 0,58 | 0,52 | 0,35 | 0,54 | 0,02 | 0,17 | 0,54 | 0,27 | 0,59 | 0,73 |
| Volumen integrado (LUFS) | -14,5 | -14,7 | -14,3 | -16,0 | -14,2 | -14,2 | -11,7 | -13,4 | -14,5 | -9,6 | -14,6 | -14,0 |
| Pico real (dBTP) | -0,1 | -3,3 | -1,2 | -3,7 | -0,1 | -0,9 | 2,2 | 2,7 | -0,6 | 1,7 | -1,5 | -1,8 |
| Silencio (%) | 0,8 | 0,7 | 1,6 | 0,2 | 0,1 | 0,1 | 0,0 | 20,9 | 3,7 | 0,0 | 0,0 | 0,3 |
| Voz activa (%) | 99 | 96 | 98 | 100 | 100 | 97 | 96 | 63 | 87 | 100 | 88 | 81 |
| Ataques de sonido por segundo | 3,5 | 2,2 | 2,3 | 4,2 | 4,3 | 3,3 | 5,2 | 3,9 | 4,4 | 6,3 | 2,8 | 3,2 |
| Golpes graves (n) | 2 | 0 | 3 | 41 | 4 | 2 | 5 | 1 | 4 | 0 | 2 | 11 |
| Palabras por segundo (total) (pal/s) | — | — | — | — | — | — | — | — | — | — | — | 3,11 |

### Resumen: 11 referencias · afines = motion-ref-2, motion-ref-3, motion-ref-4 · propio = último reel medido

| Parámetro | Todas: mediana (p25–p75) | Afines: mediana (mín–máx) | Meta nuestra | **2026-11-wifi-v5** | Veredicto |
|---|---|---|---|---|---|
| Duración (s) | 20 (10–32) | 25 (20–32) | — | 33 |  |
| Cortes por minuto | 36,0 (13,2–48,8) | 9,0 (4,8–19,0) | 4,0–20,0 | 9,1 | ✓ |
| Plano mediano (s) | 1,30 (0,78–4,22) | 4,30 (2,63–6,42) | 2,50–6,50 | 4,30 | ✓ |
| Cortes con movimiento fuerte antes (transición) (%) | 25 (14–50) | 40 (0–67) | 30–70 | 20 | ▼ bajo la meta |
| Cortes a ±0,1 s de un golpe de sonido (%) | 64 (50–96) | 50 (40–100) | 50–100 | 60 | ✓ |
| Cámara en movimiento (% cuadros) | 78 (63–85) | 85 (63–86) | 60–90 | 68 | ✓ |
| Velocidad mediana (px/s) | 69 (33–161) | 33 (22–69) | 20–70 | 16 | ▼ bajo la meta |
| Velocidad p95 (px/s) | 1485 (487–2660) | 526 (471–1908) | 400–1900 | 117 | ▼ bajo la meta |
| Movimiento lento (< 100 px/s) (%) | 56 (46–73) | 71 (57–81) | 55–85 | 94 | ▲ sobre la meta |
| Zoom neto (+ acerca) (%/s) | -0,91 (-4,63–3,07) | -2,12 (-6,41–1,83) | — | 1,77 |  |
| Tirón mediano (menos = más suave) (px/s³) | 1661 (460–4837) | 516 (460–605) | 400–650 | 518 | ✓ |
| Movimientos notorios (pico ≥ 100 px/s) cada 10 s | 7,5 (3,4–9,2) | 3,0 (1,6–4,4) | 1,5–5,0 | 3,3 | ✓ |
| Pico mediano de un movimiento notorio (px/s) | 1492 (872–2064) | 916 (872–2995) | 800–3000 | 335 | ▼ bajo la meta |
| Duración de un movimiento notorio (s) | 0,98 (0,57–1,55) | 1,55 (1,21–4,00) | 1,00–4,00 | 1,37 | ✓ |
| Retención entre movimientos (≥ 0,5 s) (s) | 0,62 (0,56–0,76) | 0,76 (0,63–1,87) | 0,50–2,00 | 0,53 | ✓ |
| Ataque de un movimiento (10 % → pico) (s) | 0,13 (0,07–0,29) | 0,13 (0,03–0,29) | 0,03–0,30 | 0,14 | ✓ |
| Liberación (pico → 10 %) (s) | 0,23 (0,13–0,44) | 0,40 (0,13–0,44) | 0,13–0,45 | 0,13 | ✓ |
| Brillo medio (0–1) | 0,37 (0,10–0,53) | 0,06 (0,04–0,10) | 0,04–0,12 | 0,09 | ✓ |
| Saturación media (0–1) | 0,35 (0,17–0,54) | 0,52 (0,35–0,54) | 0,30–0,60 | 0,73 | ▲ sobre la meta |
| Volumen integrado (LUFS) | -14,3 (-14,6–-13,4) | -14,2 (-16,0–-14,2) | -14,5–-13,5 | -14,0 | ✓ |
| Pico real (dBTP) | -0,6 (-1,5–1,7) | -0,9 (-3,7–-0,1) | -3,0–-1,0 | -1,8 | ✓ |
| Silencio (%) | 0,2 (0,0–1,6) | 0,1 (0,1–0,2) | 0,0–1,0 | 0,3 | ✓ |
| Voz activa (%) | 97 (88–100) | 100 (97–100) | — | 81 |  |
| Ataques de sonido por segundo | 3,9 (2,8–4,4) | 4,2 (3,3–4,3) | 3,0–4,5 | 3,2 | ✓ |
| Golpes graves (n) | 2 (1–4) | 4 (2–41) | — | 11 |  |
<!-- TABLAS:fin -->
