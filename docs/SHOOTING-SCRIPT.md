# Shooting script (guion de rodaje) — plantilla

Un guion dice QUÉ se cuenta; el shooting script dice CÓMO se ve y suena, segundo a segundo. Copiá la tabla para cada video.

## Cabecera
- Tema / idea única:
- Público y promesa del hook:
- Duración objetivo (≤ palabras = segundos × 2,3):
- Tema visual (`cyber.css` por defecto) y objetos 3D:
- Cierre: CTA multiplataforma o bucle

## Tabla de planos
| Esc | t (s) | Voz (texto exacto) | Plano y cámara | En pantalla | Movimiento / 3D | SFX | Música | Transición salida |
|-----|-------|--------------------|----------------|-------------|-----------------|-----|--------|-------------------|
| s1  | 0–3   |                    |                |             |                 |     |        |                   |

## Cámara en espacio 3D (estilo After Effects)
Pensar la escena como un set continuo: una cámara (`PerspectiveCamera`) que se mueve entre "estaciones" en vez de cortar entre láminas.
- **Estaciones**: posiciones del mundo donde ocurre cada idea.
- **Camino**: dolly, orbit, crane, push-in entre estaciones; easing suave (ease-in-out).
- **Profundidad**: primer plano / plano medio / fondo con paralaje y desenfoque.
- **Implementación**: `engine/camara3d.js` (tomas `fpv`, `orbita`, `cenital`, `mover`, transiciones automáticas, motion blur). Guía y catálogo en `docs/CAMARA-3D.md`: se ELIGE por reel según la idea y se varía respecto del reel anterior (ver "Variedad entre reels"); no hay plan de cámara fijo.
- **Reglas**: una intención por movimiento; el whoosh va en el pico de velocidad; no mover cámara y objeto principal a la vez sin motivo.

## Chequeo
- [ ] Hook visual en el primer segundo · [ ] cada movimiento tiene motivo · [ ] el audio cae en los cues · [ ] frames revisados antes de renderizar
