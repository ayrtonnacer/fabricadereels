# code-reel-studio (repo de Ayrton, github.com/ayrtonnacer/code-reel-studio)
App que convierte un fragmento de código en un reel 9:16 (Remotion). Lo que sirve como movimiento de cámara:

| Plano | Qué se ve | Cámara | Sonido |
|---|---|---|---|
| Acto 1 | el código se tipea en una tarjeta con resaltado de sintaxis (velocidad fija de caracteres por segundo, cursor que parpadea) | quieta, encuadre completo | `intro-whoosh` al empezar, `mouse-click` al arrancar, tipeo real |
| Pausa | código completo | quieta ~0,3 s | — |
| Zoom in | — | zoom (×1,6–2) hacia la primera línea, ease-out | `zoom-click` |
| Recorrido | cada línea importante, con su explicación (sacada de los comentarios del código) | paneo línea por línea con una pausa en cada una (snap) | — |
| Zoom out | código completo otra vez | vuelve a ×1, ease-in-out | `zoom-click` |

**Qué tomamos**: el "recorrido de código" como movimiento (ver `docs/CAMARA.md`): en nuestro set, el bloque de código es una estación; el zoom es `z` de la cámara y el paneo es `y` (alto de línea × número de línea), con `power3.inOut` y pausa de lectura en cada línea. Los 4 sonidos ya están en `assets/sfx/propios/` (`propio('zoom-click')`, `propio('mouse-click')`, `propio('intro-whoosh')`; el tipeo real lo usa `T.typing`).
