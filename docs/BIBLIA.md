# Mapa de la documentación
Para **hacer un reel** alcanza con `../CLAUDE.md` (reglas) + `5-tecnica/FLUJO.md` (paso a paso, que dice qué leer en cada etapa). Esto es el mapa completo.

| Documento | Qué tiene | Tipo |
|---|---|---|
| **`1-canal/PREFERENCIAS.md`** | gustos y errores de Ayrton, por tema, solo lo vigente | **leer siempre** |
| `1-canal/PUBLICO.md` | para quién es y qué dijo la gente de cada reel | leer al escribir el guion |
| `1-canal/CANAL.md` | quién es Ayrton, inspiraciones, qué se repite, próximas mejoras | consulta |
| `1-canal/BITACORA.md` | todo lo que dijo, en orden | historial (se agrega al final) |
| `1-canal/DECISIONES.md` | cada corrección, por video | historial (tiene decisiones viejas ya reemplazadas) |
| **`2-estilo/ESTILO.md`** | paleta, tipografía y tamaños, portada, gancho, cierre, objetos | **leer al animar** |
| **`2-estilo/CAMARA.md`** | modelo set + estaciones, las 9 reglas, recetas de planos y movimientos | **leer al animar** |
| **`2-estilo/AUDIO.md`** | capas, sonidos de marca, cómo se escribe `sfx_events.py`, pronunciación | **leer al hacer el sonido** |
| `2-estilo/SUBTITULOS.md` · `TIPOGRAFIA.md` | cómo se generan los subtítulos; palabras sueltas | consulta |
| `2-estilo/GLOSARIO-EDICION.md` | vocabulario de cine con ejemplos por segundo | para hablar con Ayrton |
| `2-estilo/BRIEF-MEDIA-KIT.md` · `media-kit/` | el sistema de diseño de la marca (abrir `media-kit/Media Kit.dc.html`) | consulta |
| **`3-guion/GUION.md`** | estructura, ritmo, reglas de la voz, checklist | **leer al escribir el guion** |
| `3-guion/INVESTIGACION-GUIONES.md` | investigación larga con fuentes | consulta |
| `4-referencias/metas.json` | rangos de alarma para nuestros reels | lo usa `reel.py medir` |
| `4-referencias/BIBLIA-DE-ESTILO.md` · `CATALOGO-MOVIMIENTOS.md` | lo medido en videos de referencia | consulta |
| `4-referencias/externos/` · `propios/` · `material/` | mediciones de referencias, de nuestros reels, y todo lo que pasó Ayrton | datos |
| **`5-tecnica/FLUJO.md`** | el paso a paso de un reel, con errores típicos | **seguir siempre** |
| **`5-tecnica/THREEJS.md`** | funciones de la librería 3D y el patrón del set | **leer al animar** |
| `5-tecnica/MEDICION.md` | qué mide cada herramienta y cómo leerlo | consulta |
| `5-tecnica/PUBLICACION.md` | estado de los videos, panel y publicación programada (propuesta) | consulta |
| `5-tecnica/FISICA.md` · `MANIM.md` | física horneada (Rapier) y animación matemática: opcionales | solo si el reel lo pide |
| `REFACTOR-2026-11-17.md` | qué se ordenó el 17/11/2026 y por qué | para Ayrton |

Otros: `../videos/LEEME.md` (estado de cada video) · `../engine/audio/pronunciacion.json` · `../engine/themes/LEEME.md` (temas viejos) · `../assets/sfx/LEEME.md` (banco de efectos).

**Cómo se mantiene esto ordenado**
- Una regla vive en **un solo documento**; los demás la enlazan.
- Cuando Ayrton cambia de opinión: se **reemplaza** el renglón en `PREFERENCIAS.md` (y en el documento del tema) y se anota una línea en `BITACORA.md`. No se apilan "agregados" al final.
- Lo que deja de usarse se borra (queda en el historial de git).
