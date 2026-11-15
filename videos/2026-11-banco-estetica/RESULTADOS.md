# Banco de prueba estético: resultados (2026-11-15)

**Qué es.** Tres planos del reel de tensores (gancho, bloque 3D, cierre; 20 s) para probar **de a una** cuatro mejoras de nivel profesional y medir cada una. Nada se pasó todavía a la plantilla: primero decide Ayrton.

**Cómo se usa.** En `index.html`, `window.NIVEL` va de 0 a 4 y cada nivel suma una mejora:
0 original · 1 encuadre · 2 luz de contorno · 3 desenfoque de profundidad y de movimiento · 4 cámara en las metas.
Videos (no se suben a git; se regeneran): `out/v0.mp4` … `out/v4.mp4` y `out/antes-despues.mp4` (v0 | v4 lado a lado).
Hoja cuadro a cuadro contra `motion-ref-2`: `analisis/hoja-comparativa.jpg` (`python videos/2026-11-banco-estetica/hoja.py`).
Medidas: `analisis/medidas-vN/` (`medir.py`) y encuadre con `engine/analisis/encuadre.py`.

## Qué hace cada nivel
| Nivel | Qué cambia | Dónde |
|---|---|---|
| 1 · Encuadre | Gancho: los 3 objetos en diagonal hacia el fondo (la foto adelante, grande, cruza el borde) en vez de una fila chica. Bloque 3D: de 3/4 y de cerca, cruza el borde izquierdo. Portada: el bloque ocupa ~80 % del ancho. Cierre: el bloque (el tema) vuelve detrás del CTA, en penumbra. | `compositions/*.html` (`N >= 1`) |
| 2 · Luz de contorno | En estilo línea no hay sombreado: la luz se dibuja **en las aristas** (lado de la luz → blanco; lado opuesto → gris oscuro) + un halo neutro detrás del protagonista. El acento tan queda solo para el significado. | `assets/escena3d.js` (`E.LUZ`, `E.luzColores`, `E.halo`) |
| 3 · Desenfoque | **Profundidad**: pase de posproceso con la profundidad de cada píxel (círculo de confusión ∝ \|z − foco\| / z, como una lente). Foco = donde mira la cámara; en el gancho **el foco salta al objeto que nombra la voz** (foto → canción → texto); en el cierre el foco está en el CTA y el bloque queda borroso atrás. **Movimiento**: obturador de 180°; si la cámara mueve la imagen más de ~4 px en un cuadro, se promedian hasta 5 sub-tomas (determinístico). | `assets/escena3d.js` (`E.POST`, `dibujar`) |
| 4 · Cámara | Deriva lenta constante con traslación real (cámara y punto de mira juntos; la órbita sola casi no mueve la imagen), paneos cortos hacia lo que nombra la voz, viaje notorio a 3/4, y **cada corte sale de un empujón rápido** en la dirección en que entra la escena siguiente. El cierre aterriza y queda quieto (regla del manual). | `compositions/*.html` (`N >= 4`) |

## Números (medidos con `medir.py`; ✓ = dentro de la meta de `metas.json`)
| Parámetro | Meta | v0 | v1 | v2 | v3 | v4 | motion-ref-2 |
|---|---|---|---|---|---|---|---|
| Cortes con movimiento antes (%) | 30–70 | 0 | 0 | 0 | 0 | 25 | 67 |
| Cámara en movimiento (% cuadros) | 60–90 | 28 | 28 | 28 | 31 | **64 ✓** | 63 |
| Velocidad mediana (px/s) | 20–70 | 4 | 5 | 6 | 6 | 12 | 22 |
| Movimientos notorios cada 10 s | 1,5–5 | 1,0 | **2,5 ✓** | **2,0 ✓** | **2,0 ✓** | **3,5 ✓** | 3,0 |
| Pico de un movimiento notorio (px/s) | 800–3000 | 7070 | 615 | **866 ✓** | **1054 ✓** | 502 | 872 |
| Duración de un movimiento notorio (s) | 1–4 | 0,35 | 0,27 | 0,75 | 0,82 | **1,0 ✓** | 1,21 |
| Tirón mediano (px/s³) | 400–650 | **479 ✓** | **561 ✓** | 710 | **471 ✓** | **412 ✓** | 516 |
| Retención entre movimientos (s) | 0,5–2 | **0,9 ✓** | **1,9 ✓** | 2,1 | **1,65 ✓** | **0,6 ✓** | 1,87 |
| Liberación (s) | 0,13–0,45 | 0,07 | **0,39 ✓** | **0,23 ✓** | **0,30 ✓** | **0,18 ✓** | 0,40 |

**Encuadre** (`encuadre.py`, cuadro completo; las referencias no tienen título ni subtítulos):
| | v0 | v1 | v2 | v3 | v4 | ref-2 | ref-3 | ref-4 |
|---|---|---|---|---|---|---|---|---|
| Ancho del contenido (%) | 60 | 72 | 72 | 73 | 72 | 73 | 72 | 72 |
| Alto del contenido (%) | 41 | 46 | 45 | 50 | 50 | 54 | 67 | 45 |

**Costo de render** (CPU, 4 workers; regla del manual: ≈ 3 s por segundo de video):
| v0 | v1 | v2 | v3 | v4 |
|---|---|---|---|---|
| 3,0 s/s | 3,9 s/s | 5,0 s/s | 10,0 s/s | 12,0 s/s |

## Lectura
- **Encuadre (v1)**: el ancho del contenido pasó de 60 % a 72 %, igual que las tres referencias afines. Es la mejora más barata y la más visible. El alto sigue por debajo (50 % contra 54–67 %): la franja de abajo de los subtítulos (y > 1320) queda vacía por diseño (título arriba, subtítulos en 1120–1320). **Es la brecha que queda** y es una decisión de Ayrton, no técnica.
- **Luz (v2)**: sutil, se ve en primer plano (bordes de arriba más claros, halo que separa el bloque del negro). No cambia ningún número de cámara; ningún medidor de los nuestros la capta.
- **Desenfoque (v3)**: el rack focus del gancho guía la mirada con la voz, y el cierre por fin tiene el CTA nítido sobre un fondo con el tema. La "nitidez relativa" sube de 3 a 6–8, en el rango de las referencias (2–12). Cuesta el doble de render.
- **Cámara (v4)**: "cámara en movimiento" entra en la meta (28 → 64 %, igual a ref-2) y aparecen cortes con movimiento antes (0 → 25 %). Siguen bajos la velocidad mediana (12 contra 20–70) y el pico de los movimientos notorios (502 contra 800–3000): la deriva es más tímida que la de las referencias. Siguiente ajuste: duplicar la deriva lateral y que el viaje a 3/4 tenga más paneo y menos órbita.
- **Saturación** queda fuera de la meta (0,07 contra 0,3–0,6) **a propósito**: la estética Scale es gris con un solo acento. La meta sale de referencias de colores vivos; habría que recalcularla para el tema Scale.

## Fallas encontradas en el camino (y cómo se arreglaron)
1. Con posproceso el fondo se volvía gris: las mezclas del halo y del piso se hacían en espacio lineal. Arreglo: la textura intermedia guarda colores en sRGB, como sin posproceso.
2. El desenfoque de movimiento dejaba copias visibles de los números (sub-tomas a > 10 px). Arreglo: si el movimiento es más largo, se acorta el obturador para que las sub-tomas queden a ≤ 4 px.
3. El desenfoque de profundidad duplicaba los números (16 muestras en un radio fijo). Arreglo: el radio de muestreo se adapta al desenfoque de cada píxel (24 muestras).
4. Costo: la primera versión tardaba 33 s por segundo de video. El antialiasing por hardware de la textura intermedia era la mitad del costo y no se notaba en las líneas (ya son suaves): se sacó. Quedó en 10–12 s/s.
5. Las primeras mediciones de costo no valían: otro render corría en paralelo. Se repitieron con la máquina libre.

## Qué falta decidir (Ayrton)
1. ¿Pasan a la plantilla? Propuesta: **encuadre y cámara sí** (cuestan poco y cumplen las metas); **luz sí** (barata y sutil); **desenfoque solo donde tenga significado** (rack focus del gancho y fondo del cierre), por el costo de render (12 s/s ≈ 11 min para un reel de 55 s, contra ~3 min hoy).
2. ¿Se usa la franja de abajo de los subtítulos? Para llenar el cuadro vertical como las referencias, el objeto podría seguir por detrás de la barra de subtítulos o los subtítulos podrían bajar. Hoy la regla dice imagen hasta y ≈ 1100.
3. ¿Recalculamos la meta de saturación para la estética Scale?

## Validación externa (pendiente)
- Prueba a ciegas: mostrar cuadros de v0, v4 y de referencias a 5–10 personas sin decir cuál es cuál.
- Retención a los 3 s del próximo reel publicado, contra la del reel de tensores.
