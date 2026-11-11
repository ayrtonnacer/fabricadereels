# Estilo visual: motion graphics

- Formato 1080×1920, 30 fps. Zona segura: todo lo que se lee entre los 200 y los 1330 px de alto (arriba y abajo tapa la interfaz de las apps; nunca texto bajo la barra de botones de la derecha). Debajo de 1330 px solo textura (piso, fondo). Con subtítulos, la imagen termina en y ≈ 1100.
- **Lenguaje**: motion graphics 2D (tipografía grande, tarjetas, terminal, diagramas que se arman) con **cámara que se mueve en un set con profundidad** (`docs/CAMARA.md`). Sin modelos 3D salvo un plano puntual que lo pida.
- **Estándar de calidad del look (Ayrton, 2026-11-11): objetos en GRIS, blanco solo para resaltar.** Aristas de los objetos en `--edge` (gris #A1A1AA, 2,2 px) sobre placas casi negras `--plate`; **blanco `--hi`** únicamente para cables, señal en el aire y tipografía, así el blanco resalta y el conjunto gana riqueza. Las antenas son cilindros finos **con cuerpo** (aristas continuas), no un palo de una línea. **Las líneas no se cortan**: trazo fino (2,2 px; a 4–5 px las aristas vecinas se tapan entre sí) y sin aristas interrumpidas por otras caras. Revisar cada objeto de cerca en el `snapshot`.
- **Identidad (default desde 2026-11-11, tema "línea")**: `assets/marca.css` de cada video (copiada de la plantilla). Fondo negro `--bg #06070C`, **objetos 3D dibujados solo con contorno blanco** (`--trazo`) sobre relleno negro, piso de líneas grises, acento **rojo `--acc #FF2E3F`**, secundario blanco (`--sky`: cables, internet, 5 GHz). Colores medidos del reel de WiFi que Ayrton eligió. Siempre `var(--…)`, nunca colores fijos. Tema anterior (azul-negro + lima, sólido): `engine/themes/cyber.css` + `--estilo: solido`.
- **Paleta (un color = un significado; si hace falta otro, se agrega acá y en `marca.css`)**:
  | Variable | Valor | Significado |
  |---|---|---|
  | `--acc` | #FD2B3C rojo | énfasis: palabra clave, firma, señal/ondas, paquetes, progreso |
  | `--trazo` / `--text` | #F5F6F8 blanco | contorno de objetos, texto, cables, 5 GHz |
  | `--muted` | #8D909B | rótulos secundarios, bordes de cuartos |
  | `--ok` | #2EE08C verde | ✓ correcto (chips de estado) |
  | `--warn` | #FFB020 ámbar | ⚠ aviso |
  | `--err` | #FF6A1F naranja-rojo | ✕ error: bloque RELLENO con ✕ (distinto del acento rojo por color y por forma) |
  | `--sky` | #F5F6F8 | secundario neutro (reservado: si algún día se necesita un 2.º acento, se cambia acá) |
  Fondos: `--bg`, `--bg-hondo`, `--bg-glow`, `--panel`, `--line`, `--piso`.
- **Color = significado**: énfasis (palabra clave, firma, progreso) = `--acc` (rojo) · ✓ correcto = `--ok` verde · ⚠ aviso = `--warn` ámbar · ✕ error = bloque naranja-rojo RELLENO con ✕ (`.chip.err`). Nunca el mismo color para lo bueno y lo malo; verde y ámbar solo en estados.
- **Tipografía**: IBM Plex Sans 500/700 (`--sans`) y IBM Plex Mono (`--mono`), locales en `assets/fonts/`. Espaciado normal o apretado (titulares −0,02 a −0,03 em); **nunca** mayúsculas con espaciado amplio.
- **Titulares**: 1–3 líneas, una idea por escena, la palabra clave con `.acc`. Un titular que aterrizó queda quieto: el movimiento lo pone la cámara o el elemento siguiente.
- **Entradas de texto**: palabra por palabra con desenfoque (blur 10 → 0, ~0,18 s, 60–120 ms entre palabras), sin deslizar. Variar la entrada entre escenas (ver `/hyperframes` → `references/motion.md`).
- **Paso**: "Paso 1 de 7" en Plex Sans + segmentos (`.pasos`), fijo en pantalla (fuera de la cámara).
- **Firma**: `@ayrtonnacer` al inicio y al final, con `--acc`, sola (sin punto, ícono ni adorno). Lo resaltado es lo que se debe recordar.
- **Ritmo**: un cambio visual cada 1,5–3 s (entra algo, viaja la cámara, se dibuja un resalte). Nada quieto más de 3 s.
- **Prohibido**: líneas de escaneo, marcos HUD / esquinas en L, "// TUTORIAL", "[ GRATIS ]", texto de fuente al final, loops de "flotar/respirar", rebote en interfaz, todas las escenas entrando igual.
- **Subtítulos**: SÍ, siempre (Ayrton, 2026-11-09: se ve mucho en silencio). Ver `docs/SUBTITULOS.md`. Zona segura: imagen entre y 200 y 1100; subtítulos en y 1120–1320; debajo de 1320 solo el piso.
- **Fondo**: negro + **piso de líneas en perspectiva** grises (le gustan a Ayrton). **Sin puntitos verdes** (no tenían sentido; sacados). **Nada decorativo sin significado** (tampoco unos y ceros desenfocados de fondo: Ayrton marcó un "1" sin sentido). La profundidad sale del 3D real y de la cámara (`docs/CAMARA.md`).
- **Texto**: nada de palabras sueltas en la última línea (`docs/TIPOGRAFIA.md`).
