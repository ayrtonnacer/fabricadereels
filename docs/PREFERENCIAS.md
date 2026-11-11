# Preferencias de Ayrton (resumen para consultar ANTES de cada video)
Destilado de `docs/BITACORA.md` (cronológico, con el detalle) y `docs/DECISIONES.md`. **Se actualiza en cada tanda de indicaciones** y se repasa al empezar un video y antes de entregarlo; Ayrton no tiene que volver a aclararlo.

## Le gusta
- Estética (2026-11-11): **negro + objetos en línea (contorno blanco) + acento rojo**, referencia = el reel de WiFi que pasó Ayrton; IBM Plex. Lima/azul queda como tema alternativo. **Piso de líneas en perspectiva** y el **gradiente** de fondo.
- **Profundidad real**: objetos 3D con perspectiva (le gustó cuando aparecieron los teléfonos en 3D); cámara que se mueve y revela. Prefiere **todo en three.js** (objetos, ondas, cables) mientras el render no se vuelva lento.
- Motion graphics con **movimiento de cámara** como protagonista de la profundidad.
- **Voz Daniela limpia** (sin efecto de radio) y sonido **limpio**: sin ruido de fondo; efectos puntuales con significado; **chinn** al aparecer el CTA; **sonido grave** (`boom-cinematico`) al inicio y al final; tipeo real de teclado.
- **Subtítulos** siempre (mucha gente mira en silencio), en zona segura.
- Cierre con **foco en el CTA**; la firma chica debajo.
- Que cada reel **demuestre que sabe** (portfolio para reclutadores): un detalle de profesional.
- Reels **rápidos de producir**.

## No le gusta / errores a no repetir
- Elementos de fondo **sin sentido** (puntitos verdes, un "1" suelto flotando): todo lo decorativo tiene que significar algo.
- **Palabras sueltas** en la última línea (viudas/huérfanas).
- Ondas **cortadas** (sin continuidad); cables que **no tocan** el objeto.
- Texto del CTA que **no coincide con la voz**: debe decir "Dale like y seguime para aprender más de <tema>".
- Zoom a su usuario en el cierre; "guardalo"; efecto de radio / sonido sucio; estética roja o Anduril.
- Render lento (el motor viejo con 3D pesado): three.js solo simple (medido ≈ +1 s de render por segundo de video).
- Pronunciación mal: "WiFi" escrito "guifi" sonaba "gifi" → usar "uaifai" (pendiente que Ayrton elija de oído entre 3 variantes en `docs/material/pronunciacion/`).

## Flujo acordado
Link + indicaciones → guion (público: técnicos, principiantes, reclutadores) → **su OK** → plan numérico (metas de la biblia de estilo) → video → entrega. A futuro: publicar automáticamente en sus redes (no hacerlo sin que lo pida).

## Agregado 2026-11-09 (noche, 3)
- **Realismo con sentido**: las notebooks no llevan antena a la vista; los **cables tocan los objetos** (puertos, centro del globo); las ondas de radio no necesitan encajar justo.
- **Cero etiquetas obvias**: no rotular lo que se ve ("pared"); el espectador no es tonto.
- **Bits chicos y dentro de la pantalla**; sonido digital de interfaz para tipear 0 y 1 (el teclado solo para código); módem como guiño de "conexión"; hit metálico mejor que un whoosh suave en el cierre.
- **"WiFi" = "uaifai"** (aprobado). "router" = "ráuter" (a confirmar).
- CTA: "de <tema>" para temas de una palabra; "sobre <tema>" para frases largas.
- Pasa **investigación propia** (guías, artículos) para que la use y la deje documentada: `docs/THREEJS.md`.

## Agregado 2026-11-10
- **Medir en vez de opinar**: prefiere parámetros técnicos replicables a percepciones subjetivas; quiere analizar videos de referencia (transiciones, cámara, planos, sonido) para tener parámetros de inspiración. Se le pasa el .mp4 a Claude y se mide (`docs/MEDICION.md`).
- Renderizamos a **30 fps** (estándar; alcanza para nuestro movimiento).

## Agregado 2026-11-10 (2)
- **Una sola rama (`main`)**: no quiere ramas ni PR; todo directo a `main`. Explicarle GitHub en simple y evitar jerga.
- Referencias suyas que le gustan (10 videos en `assets/referencias/`): las **contemplativas/oscuras** con cámara que mueve–retiene–mueve y planos continuos; patrón favorito para reels técnicos: **vista explosionada 3D con etiquetas y tooltip** (`docs/referencias/BIBLIA-DE-ESTILO.md`).

## Agregado 2026-11-10 (3)
- **Todo análisis con números** (como el repo de LuisPa): nada de "se siente", nada de script técnico cualitativo. Un solo lugar (`docs/referencias/`), una sola herramienta (`medir.py`), comparar siempre contra las metas. **Borrar lo que no se usa.**
- **Ondas de radio = anillos/círculos** que se expanden; la onda sinusoidal solo para explicar frecuencias (2,4/5 GHz). Tipeo digital solo al escribir los 0/1 en la computadora; en el router, sonido de módem/router.
- **Gastar pocos tokens**: ir directo, pocas iteraciones, sin releer docs ni regenerar de más; que alcance con pasar el material.
- **Física (2026-11-11)**: solo si explica algo; se hornea con Rapier (`docs/FISICA.md`), nunca simulación en vivo; sin `Math.random()`; los choques sincronizan los efectos. No usar React/R3F.
- **Paquetes (2026-11-11)**: cuadraditos SOLO sobre cables y siguiendo su curva (`cab.at`); en el aire, solo ondas. Lo que viaja sigue la forma real del medio.
- **Música por defecto**: Palladio (`assets/musica/palladio.mp3`, desde 0,6 s), en todos los reels.
