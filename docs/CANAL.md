# El canal: quién, para qué y hacia dónde
Contexto de fondo para cada decisión de guion, estética y voz. Lo contó Ayrton el 2026-11-14.

## Quién y para qué
- **Ayrton (@ayrtonnacer)** hace divulgación de **programación, matemática, ciencia, ciberseguridad y Linux**, sin mostrar la cara.
- Dos objetivos:
  1. **Comunidad y marca personal**: que lo reconozcan y lo sigan. Los reels también son su portfolio para reclutadores.
  2. **Aprender mejor**: cada reel lo obliga a entender un tema a fondo para poder explicarlo. Es **aprendizaje basado en proyectos** ([Wikipedia](https://es.wikipedia.org/wiki/Aprendizaje_basado_en_proyectos); copia en `material/2026-11-14-aprendizaje-basado-en-proyectos-wikipedia.pdf`): se aprende produciendo algo real para un público real, investigando una pregunta, con revisión y una entrega pública. Para el canal: **cada reel es un proyecto de estudio**, la pregunta del hook es la pregunta de investigación y el público es quien evalúa.

## Inspiraciones (canales sin cara que lograron comunidad)
| Canal | Tema | Qué tomar |
|---|---|---|
| [Kurzgesagt](https://www.youtube.com/@kurzgesagt/featured) | Ciencia | Identidad visual inconfundible (paleta, estilo plano, el pájaro), siempre la misma voz y la misma música. Se reconoce en un cuadro. |
| [Fireship](https://www.youtube.com/@Fireship) | Programación (inglés) | El más conocido de programación sin cara: ritmo muy rápido, humor, formato fijo ("X in 100 seconds"), voz propia y reconocible. |
| [3Blue1Brown](https://www.youtube.com/c/3blue1brown) | Matemática | Animación que **muestra** la idea en vez de decirla (Manim), fondo oscuro, colores con significado fijo, intuición antes de la fórmula. |
| [FaztTech](https://www.youtube.com/@FaztTech) | Programación (Argentina) | Argentino y en español: prueba que hay público hispanohablante grande para programación. |

## La tesis: lo que se repite es lo que se reconoce
> "Si tenés 5 videos virales pero distintos entre sí, nunca vas a lograr crear comunidad y que te reconozcan." (Ayrton)

Sin cara, la marca se construye con **elementos que se repiten en cada reel**:
| Elemento | Qué tenemos (fijo) | Estado |
|---|---|---|
| Estética y color | Tema Scale: negro puro, objetos 3D de línea gris, acento Foundry Tan, Host Grotesk + Geist Mono (`ESTILO.md`) | ✓ definido (2026-11-14) |
| Estructura | Portada 0,1 s → hook con título → explicación con un ejemplo que crece → payoff → CTA con firma | ✓ definido |
| Sonido | Boom grave al inicio y al final, chinn en el CTA, whoosh en la cámara (`AUDIO.md`) | ✓ definido |
| Voz | Daniela (Piper), se nota robótica | ⚠ a mejorar: voz clonada de Ayrton (`AUDIO.md` → Voz propia) |
| Música | Cambia según el reel | ⚠ a definir: una firma musical o un estilo fijo |
| Firma | `@ayrtonnacer` en tan al inicio y al final | ✓ |

**Regla para el repo**: el inicio, el cierre, la paleta, la voz y los sonidos fijos **no se cambian entre reels** salvo decisión explícita de Ayrton. Lo que cambia es el medio (tema, objetos, ejemplo).

## Próximas mejoras (en este orden)
Números del reel de tensores medido (`referencias/propios/2026-11-tensores-scale-oscuro/`) contra las metas (`referencias/metas.json`):
1. **Dinamismo de cámara.** Es la mayor diferencia con las referencias:
   | Métrica | Tensores | Meta |
   |---|---|---|
   | % de cuadros con cámara en movimiento | 37,9 | 60–90 |
   | Movimientos notorios cada 10 s | 0,5 | 1,5–5 |
   | Velocidad mediana (px/s) | 5 | 20–70 |
   | Duración mediana del plano (s) | 8,0 | 2,5–6,5 |
   | % de cortes precedidos por un movimiento | 0 | 30–70 |
   | % de cortes sobre un golpe de sonido | 33 | 50–100 |
   Qué hacer: un movimiento notorio cada 3 a 5 s, transiciones que salgan de un movimiento rápido de cámara (en vez de cortes secos), planos de 3 a 6 s y el corte sobre el golpe.
2. **Hook.** Título grande en pantalla desde el cuadro 0 y una pregunta o un dato que choque en menos de 3 s. Medirlo con la retención a los 3 s de Instagram.
3. **Portada.** Hoy es el cuadro de 0,1 s con título + objeto + firma. Mejorarla: un objeto protagonista más grande, menos texto (3 a 5 palabras) y que se lea en miniatura. Comparar con las portadas de los canales de arriba.
4. **Voz propia** (feedback del público, `PUBLICO.md`).

**Banco de prueba estético (2026-11-15)**: `videos/2026-11-banco-estetica/RESULTADOS.md`. Encuadre (ancho del contenido 60 → 72 %, igual que las referencias), luz de contorno, desenfoque (rack focus con la voz) y cámara (en movimiento 28 → 64 %). Pendiente que Ayrton elija qué pasa a la plantilla; brecha que queda: la franja de abajo de los subtítulos vacía.

## Cómo trabajaría un profesional de primer nivel (ideas para profundizar, no para agrandar)
- **Partir de material crudo**: el paper, la documentación oficial o el libro de texto en vez de un artículo que ya lo resume. Y del lado del público, partir de las **métricas crudas** de cada reel (curva de retención, en qué segundo se van) en vez de opiniones.
- **Métodos**: una pregunta de investigación por reel (aprendizaje basado en proyectos); la técnica Feynman (si no se puede explicar simple, todavía no se entendió); revisión técnica de un par antes de publicar; pruebas A/B de portada y hook cuando la plataforma lo permita; medir con `medir.py` y `comparar.py` antes de opinar.
- **Validación externa**: que lo dé por bueno algo que no seamos ni Claude ni Ayrton. Los **números de la plataforma** (retención a los 3 s, % que lo ve completo, compartidos), un **experto del tema** que no encuentre errores y un **principiante** que, después de verlo, pueda explicar la idea con sus palabras.
