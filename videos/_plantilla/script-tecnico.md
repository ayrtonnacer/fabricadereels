# Script técnico — <título>
Se arma DESPUÉS de que Ayrton aprueba el guion y ANTES de animar. Dice cómo se ve y suena cada plano, segundo a segundo.
Vocabulario de cámara: `docs/CAMARA.md`. Referencias de movimientos: `docs/referencias/`.

## Cabecera
- Idea única (≤ 12 palabras):
- Duración (voz medida con voz.py):
- Cierre: CTA (foco en el llamado; firma chica debajo; chinn al aterrizar) | bucle
- Música (tramo / clima):
- Referencia de cámara usada (archivo en docs/referencias/):

## Planos
| Esc | t (s) | Voz (texto exacto) | Set (qué hay en el mundo y a qué z) | Cámara (pose inicial → movimiento, ease, duración) | Entradas en pantalla (t local) | SFX (en el pico del movimiento) | Transición de salida |
|-----|-------|--------------------|-------------------------------------|---------------------------------------------------|-------------------------------|---------------------------------|---------------------|
| gancho | 0–3 | | | aterrizaje `z:-520,rx:20 → z:0` expo.out 1.6 s | | boom 0.0 | zoom through 0.6 s power3.in |
| … | | | | | | | |
| cierre | | "Dale me gusta y seguime…" | CTA grande, firma chica debajo, piso | aterriza en el CTA y queda quieta | CTA palabra por palabra, firma +1.1 s | riser invertido → impact → chinn | — |

## Chequeo
- [ ] Cuadro 0 muestra la idea (miniatura) · [ ] cada movimiento tiene una intención · [ ] whoosh en el pico de velocidad
- [ ] nada quieto > 3 s · [ ] texto entre 200 y 1330 px de alto · [ ] CTA en foco, no la firma · [ ] cuadros revisados con `snapshot`
