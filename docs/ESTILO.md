# Estilo visual: motion graphics

- Formato 1080×1920, 30 fps. Zona segura: todo lo que se lee entre los 200 y los 1330 px de alto (arriba y abajo tapa la interfaz de las apps; nunca texto bajo la barra de botones de la derecha). Debajo de 1330 px solo textura (piso, fondo). Con subtítulos, la imagen termina en y ≈ 1100.
- **Lenguaje**: motion graphics 2D (tipografía grande, tarjetas, terminal, diagramas que se arman) con **cámara que se mueve en un set con profundidad** (`docs/CAMARA.md`). Sin modelos 3D salvo un plano puntual que lo pida.
- **Estándar de calidad del look (Ayrton, 2026-11-11): objetos en GRIS, blanco solo para resaltar.** Aristas de los objetos en `--edge` (gris #A1A1AA, 2,2 px) sobre placas casi negras `--plate`; **blanco `--hi`** únicamente para cables, señal en el aire y tipografía, así el blanco resalta y el conjunto gana riqueza. Las antenas son cilindros finos **con cuerpo** (aristas continuas), no un palo de una línea. **Las líneas no se cortan**: trazo fino (2,2 px; a 4–5 px las aristas vecinas se tapan entre sí) y sin aristas interrumpidas por otras caras. Revisar cada objeto de cerca en el `snapshot`.
- **Identidad (default desde 2026-11-14, tema "Scale")**: `assets/marca.css` de cada video (copiada de la plantilla), inspirada en la guía de marca de Scale AI (brand.scale.com) y elegida por Ayrton en el reel de tensores (`videos/2026-11-tensores-scale-oscuro/`). **Base neutra**: fondo negro puro `#000000`, objetos 3D de **línea gris** `--edge #929292` sobre placas negras, piso de líneas grises; texto blanco y gris medio `#C7C7C7`. **Un solo acento: Foundry Tan `--acc #A8927C`** (palabra clave, firma, señal). Los colores de Scale van **como acento, nunca de fondo** (el verde Evergreen de fondo fue descartado). Subtítulos con **barra negra** detrás (`video.json → subtitulos.fondo`). Siempre `var(--…)`, nunca colores fijos. Temas anteriores (línea roja, cyber) en `engine/themes/` (ver su `LEEME.md`).
- **Paleta (un color = un significado; si hace falta otro, se agrega acá y en `marca.css`)**:
  | Variable | Valor | Significado |
  |---|---|---|
  | `--acc` | #A8927C Foundry Tan | énfasis: palabra clave, firma, señal, progreso (único acento) |
  | `--text` / `--hi` | #FFFFFF blanco | texto, cables, lo que debe resaltar |
  | `--edge` | #929292 gris | aristas de los objetos 3D |
  | `--muted` | #C7C7C7 gris medio | rótulos secundarios |
  | `--ok` | #2EE08C verde | ✓ correcto (chips de estado) |
  | `--warn` | #A8927C tan | ⚠ aviso (con ⚠ para distinguirlo del énfasis) |
  | `--err` | #DC2626 rojo | ✕ error: bloque RELLENO con ✕ (el rojo de la guía de Scale) |
  | capas extra | Cloud Slate #839CB2, Archive Purple #79648C | solo si hacen falta varias categorías (p. ej. canales de una foto) |
  Fondos: `--bg`, `--bg-hondo`, `--bg-glow`, `--panel`, `--line`, `--piso`.
- **Color = significado**: énfasis (palabra clave, firma, progreso) = `--acc` (tan) · ✓ correcto = `--ok` verde · ⚠ aviso = `--warn` + ⚠ · ✕ error = bloque rojo RELLENO con ✕ (`.chip.err`). Nunca el mismo color para lo bueno y lo malo; verde y ámbar solo en estados.
- **Tipografía** (de Scale; Aeonik es paga): **Host Grotesk** (`--sans`, texto) y **Geist Mono** (`--mono`, números y detalle), locales en `assets/fonts/`. Las texturas con letras del 3D usan Geist Mono (`escena3d.js`). Espaciado normal o apretado (titulares −0,02 a −0,03 em); **nunca** mayúsculas con espaciado amplio.
- **Titulares**: 1–3 líneas, una idea por escena, la palabra clave con `.acc`. Un titular que aterrizó queda quieto: el movimiento lo pone la cámara o el elemento siguiente.
- **Entradas de texto**: palabra por palabra con desenfoque (blur 10 → 0, ~0,18 s, 60–120 ms entre palabras), sin deslizar. Variar la entrada entre escenas (ver `/hyperframes` → `references/motion.md`).
- **Paso**: "Paso 1 de 7" en sans (`--sans`) + segmentos (`.pasos`), fijo en pantalla (fuera de la cámara).
- **Firma**: `@ayrtonnacer` al inicio y al final, con `--acc`, sola (sin punto, ícono ni adorno). Lo resaltado es lo que se debe recordar.
- **Ritmo**: un cambio visual cada 1,5–3 s (entra algo, viaja la cámara, se dibuja un resalte). Nada quieto más de 3 s.
- **Prohibido**: líneas de escaneo, marcos HUD / esquinas en L, "// TUTORIAL", "[ GRATIS ]", texto de fuente al final, loops de "flotar/respirar", rebote en interfaz, todas las escenas entrando igual.
- **Subtítulos**: SÍ, siempre (Ayrton, 2026-11-09: se ve mucho en silencio). Ver `docs/SUBTITULOS.md`. Zona segura: imagen entre y 200 y 1100; subtítulos en y 1120–1320; debajo de 1320 solo el piso.
- **Fondo**: negro + **piso de líneas en perspectiva** grises (le gustan a Ayrton). **Sin puntitos verdes** (no tenían sentido; sacados). **Nada decorativo sin significado** (tampoco unos y ceros desenfocados de fondo: Ayrton marcó un "1" sin sentido). La profundidad sale del 3D real y de la cámara (`docs/CAMARA.md`).
- **Texto**: nada de palabras sueltas en la última línea (`docs/TIPOGRAFIA.md`).
