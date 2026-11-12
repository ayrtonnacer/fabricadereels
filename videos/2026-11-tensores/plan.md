# Plan numérico — Escalar, vector, matriz y tensor (ML)
Duración 48,6 s · 131 palabras = 2,7 pal/s · 7 escenas · render mudo 1 min 29 s (1,8 s/s).
## Metas vs medido (`comparar.py`, final.mp4)
| Parámetro | Meta | Medido |
|---|---|---|
| Cortes/min · plano mediano | 4–20 · 2,5–6,5 s | 8,6 · 4,7 s ✓ |
| Volumen · pico | −14 LUFS · ≤ −1,5 dBTP | −14,1 · −1,6 ✓ |
| Cámara en movimiento | 60–90 % | 44 % (bajo: retenciones largas para leer; objetos 3D quietos mientras la voz explica) |
| Velocidad mediana · pico notorio | 20–70 · 800–3000 px/s | 6 · 240 (bajo: viajes suaves de 1,2–1,5 s; la cámara orbita y viaja pero sin latigazos) |
| Ataques de sonido/s | 3,0–4,5 | 2,6 (pocos efectos: son con significado) |
## Escenas (inicio → fin, s; cámara y efectos)
| Esc | s | Voz | Set | Cámara | SFX |
|---|---|---|---|---|---|
| gancho | 0–3,0 | ¿Qué forma tiene tu cara…? | cara 8×8 (placa) | acercamiento z 4,2 → 3,3, expo | boom 0, pop, whoosh 0,3 |
| tipos | 3,0–16,2 | IA multiplica números; escalar, vector, matriz | cara→números→escalar (z 0) · vector (z −2,2) · matriz (z −4,4) | viaja en z entre objetos, io 1,2–1,3 s | pop por objeto; whoosh en 6,8 y 10,35 (+3,0) |
| tensor | 16,2–26,0 | foto = 3 ejes; lote = 4.º eje | pila de 3 placas, ejes alto/ancho/canales; 5 pilas = lote | orbita (z 2,6→3,0), pull-back a z 5,4 | whoosh 2,55 y 6,25; ticks por eje; ding en el eje lote |
| red | 26,0–31,2 | entrada y pesos son tensores | entrada (pila) · pesos (grilla roja) · salida | de costado, sigue la entrada en z | pops, whoosh 3,65 |
| detalle | 31,2–39,6 | rango = ejes; formas no encajan | pila + chips `rango = ejes`, aviso ámbar, error naranja ✕ | dolly lento | pops, buzz en el error |
| payoff | 39,6–43,6 | tres ejes; lote cuatro | igual que tensor, comprimido | orbita + pull-back | ticks, whoosh 2,1, ding 2,44 |
| cierre | 43,6–48,6 | CTA | CTA grande, firma +3,7 s debajo | aterriza y queda | riser, boom, chinn 0,8 |
