# Bitácora de indicaciones de Ayrton
Todo lo que Ayrton dice y pasa se guarda acá (y el material en `docs/material/`), para aprovecharlo en videos futuros: criterios de diseño, cómo dibujar y graficar, sonido, flujo. **Regla: cada vez que Ayrton da una indicación o pasa un archivo, se agrega acá y se lleva a la doc que corresponda.** Las correcciones puntuales de un video van además a `docs/DECISIONES.md`.

## 2026-11-09 — replanteo del proyecto
- Trabajar con **HyperFrames** (más probado que el motor propio); renderizar 3D tardaba muchísimo y quiere **reels rápidos**. Estilo: **motion graphics**; muchos motion graphics son 2D y el **movimiento de cámara** da la profundidad. Revisar todo el repo y sacar lo que sobra. → `docs/CAMARA.md`, `CLAUDE.md`.
- Referencias de movimientos de cámara: las va a pasar a medida que trabajemos. → `docs/referencias/`.
- Sonido "chinn" (cristal) mejor para el cierre. Repo `code-reel-studio`: tipeo real de teclado y otras lógicas. → `docs/AUDIO.md`.
- En el cierre el **foco es el CTA**, no su usuario (la demo hacía zoom a la firma). → `docs/DECISIONES.md`.
- Flujo: link + breve explicación → guion (según lineamientos y público) → **script técnico** (planos, sfx, perspectiva de cámara) → video. A futuro: **publicar automáticamente** en sus redes. → `docs/FLUJO.md`.
- Público: **técnicos, principiantes y reclutadores**; los reels son portfolio y tienen que demostrar que sabe. → `docs/GUION.md`.
- Pidió un reel que explique **qué es el WiFi y cómo funciona** para cualquier público (fuentes: HowStuffWorks, Wikipedia, Cisco). → `videos/2026-11-wifi`.

## 2026-11-09 (tarde) — correcciones sobre el reel de WiFi
- **Subtítulos**: muchas personas ven los reels en silencio (hay estadísticas); respetar los **espacios seguros**. → `docs/SUBTITULOS.md`.
- **Ondas cortadas**: las ondas de 2,4 y 5 GHz se cortaban en la pared, sin continuidad (los dos tramos reiniciaban la fase). Ahora comparten fase. → `docs/CAMARA.md`. (Captura: `docs/material/2026-11-09-wifi-correcciones/1-ondas-cortadas.png`.)
- **Cable que no llegaba al router**: el cable quedaba flotando sobre el router. (`2-cable-no-llega-al-router.png`.) Regla: lo que se conecta tiene que tocarse.
- **Palabra sola** ("llega") en la bajada del gancho. (`3-palabra-sola-llega.png`.) Pasó el artículo de Adobe sobre viudas y huérfanas. → `docs/TIPOGRAFIA.md`.
- **Escuchar el audio**: sugirió usar earshot o Whisper para "escuchar" y verificar. Desde la nube no se pueden bajar modelos (Hugging Face y OpenAI bloqueados; earshot ya se había intentado y no corrió). Solución: los tiempos por palabra salen del propio Piper (exactos) y se verifican dibujando la onda. → `docs/SUBTITULOS.md`. Si quiere Whisper de verdad: correrlo en su compu.
- **Sonido grave** (`boom-cinematico.mp3`, "cinematic impact boom 05" de Universfield): al **inicio y al final**. → `docs/AUDIO.md`.
- **Fondo**: le gustan las **líneas que dan perspectiva** (el piso de grilla) y el **gradiente**. Los **puntitos verdes** de fondo no le encontraba sentido: **sacados**. → `docs/ESTILO.md`.
- **Eje z / three.js**: siente que no se aprovecha la profundidad (z). Se puede usar three.js **si no demora mucho el render**; si demora, no lo quiere. Medido: ver `docs/CAMARA.md` (≈ +1 s de render por segundo de video para una escena simple). Se hizo un piloto en el payoff.
- **Guardar todo en el repo**: indicaciones, materiales, cómo dibujar/graficar, sonido. → esta bitácora y `docs/material/`.
