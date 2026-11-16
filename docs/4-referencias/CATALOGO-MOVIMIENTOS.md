# Catálogo de movimientos de cámara (medido en las referencias)
Qué hace la cámara en los videos que le gustan a Ayrton, por tipo de movimiento y con su receta numérica; el tema no importa, importa la técnica. Se regenera con `python engine/analisis/movimientos.py --catalogo`. Vocabulario: `docs/2-estilo/GLOSARIO-EDICION.md`.
191 movimientos en 12 videos.

| Movimiento | n | duración (s) | distancia (% ancho) | pico (px/s) | curva más común |
|---|---|---|---|---|---|
| dolly / zoom in (se acerca) | 44 | 1.20 | 5 | 606 | arranca fuerte y frena largo (ease-out) |
| dolly / zoom out (se aleja) | 44 | 0.89 | 6 | 692 | arranca fuerte y frena largo (ease-out) |
| grúa / tilt hacia abajo | 33 | 1.00 | 13 | 992 | arranca fuerte y frena largo (ease-out) |
| paneo / travelling a la derecha | 23 | 0.78 | 21 | 1659 | arranca lento y termina fuerte (ease-in) |
| grúa / tilt hacia arriba | 21 | 0.60 | 14 | 1333 | arranca fuerte y frena largo (ease-out) |
| paneo / travelling a la izquierda | 15 | 0.93 | 15 | 1072 | arranca fuerte y frena largo (ease-out) |
| latigazo (whip pan) | 6 | 0.27 | 22 | 3258 | arranca fuerte y frena largo (ease-out) |
| diagonal | 5 | 1.73 | 46 | 1085 | arranca lento y termina fuerte (ease-in) |

## Ejemplos para mirar (los 3 más rápidos de cada tipo)
### dolly / zoom in (se acerca)
- `motion-inspiration-nokia` 14.73–15.13 s · 0.4 s · 5792 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-inspiration-nokia/movimientos/` 
- `motion-inspiration-nokia` 9.5–9.87 s · 0.37 s · 3013 px/s · arranca fuerte y frena largo (ease-out) → `externos/motion-inspiration-nokia/movimientos/` 
- `pinterest-791437334567656517` 22.46–23.39 s · 0.93 s · 2952 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
### dolly / zoom out (se aleja)
- `motion-ref-1` 2.47–4.63 s · 2.17 s · 5753 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-ref-1/movimientos/` 
- `motion-inspiration-nokia` 2.83–3.47 s · 0.63 s · 5429 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-inspiration-nokia/movimientos/` 
- `pinterest-791437334567656517` 25.69–26.46 s · 0.77 s · 3320 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
### grúa / tilt hacia abajo
- `pinterest-791437334567656517` 44.74–45.88 s · 1.13 s · 30138 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
- `motion-templates-after-effects` 6.36–8.14 s · 1.79 s · 10878 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-templates-after-effects/movimientos/` 
- `pinterest-791437334567656517` 39.24–41.51 s · 2.27 s · 7334 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
### paneo / travelling a la derecha
- `motion-templates-after-effects` 1.67–4.82 s · 3.15 s · 9871 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-templates-after-effects/movimientos/` 
- `pinterest-791437334567656517` 16.72–18.08 s · 1.37 s · 9355 px/s · arranca lento y termina fuerte (ease-in) → `externos/pinterest-791437334567656517/movimientos/` 
- `motion-inspiration-nokia` 5.57–6.97 s · 1.4 s · 9057 px/s · arranca fuerte y frena largo (ease-out) → `externos/motion-inspiration-nokia/movimientos/` 
### grúa / tilt hacia arriba
- `pinterest-791437334567656517` 32.83–33.47 s · 0.63 s · 15966 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
- `motion-inspiration-nokia` 1.07–1.8 s · 0.73 s · 13273 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-inspiration-nokia/movimientos/` 
- `motion-inspiration-nokia` 12.67–13.13 s · 0.47 s · 8912 px/s · arranca fuerte y frena largo (ease-out) → `externos/motion-inspiration-nokia/movimientos/` 
### paneo / travelling a la izquierda
- `pinterest-791437334567656517` 25.06–25.59 s · 0.53 s · 10783 px/s · simétrico (ease in-out) → `externos/pinterest-791437334567656517/movimientos/` 
- `short-tensores` 39.63–43.0 s · 3.37 s · 6548 px/s · arranca fuerte y frena largo (ease-out) → `externos/short-tensores/movimientos/` 
- `short-tensores` 10.43–18.43 s · 8.0 s · 3496 px/s · simétrico (ease in-out) → `externos/short-tensores/movimientos/` 
### latigazo (whip pan)
- `pinterest-791437334567656517` 8.07–8.34 s · 0.27 s · 4644 px/s · simétrico (ease in-out) → `externos/pinterest-791437334567656517/movimientos/` 
- `pinterest-791437334567656517` 20.39–20.72 s · 0.33 s · 3835 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-791437334567656517/movimientos/` 
- `pinterest-999095498641347187` 7.28–7.55 s · 0.27 s · 3612 px/s · arranca fuerte y frena largo (ease-out) → `externos/pinterest-999095498641347187/movimientos/` 
### diagonal
- `motion-ref-3` 14.62–20.92 s · 6.29 s · 4072 px/s · simétrico (ease in-out) → `externos/motion-ref-3/movimientos/` 
- `motion-templates-after-effects` 5.62–6.29 s · 0.67 s · 2673 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-templates-after-effects/movimientos/` 
- `motion-ref-5` 64.67–70.67 s · 6.0 s · 1085 px/s · arranca lento y termina fuerte (ease-in) → `externos/motion-ref-5/movimientos/` 
