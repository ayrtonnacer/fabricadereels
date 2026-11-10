# Preferencias de Ayrton (resumen para consultar ANTES de cada video)
Destilado de `docs/BITACORA.md` (cronológico, con el detalle) y `docs/DECISIONES.md`. **Se actualiza en cada tanda de indicaciones** y se repasa al empezar un video y antes de entregarlo; Ayrton no tiene que volver a aclararlo.

## Le gusta
- Estética **cyber / HackTheBox**: azul-negro + lima; IBM Plex. **Piso de líneas en perspectiva** y el **gradiente** de fondo.
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
Link + indicaciones → guion (público: técnicos, principiantes, reclutadores) → **su OK** → script técnico (planos, cámara, sfx) → video → entrega. A futuro: publicar automáticamente en sus redes (no hacerlo sin que lo pida).

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
