# Estilo visual: motion graphics

- Formato 1080×1920, 30 fps. Zona segura: todo lo que se lee entre los 200 y los 1330 px de alto (arriba y abajo tapa la interfaz de las apps; nunca texto bajo la barra de botones de la derecha). Debajo de 1330 px solo textura (piso, fondo).
- **Lenguaje**: motion graphics 2D (tipografía grande, tarjetas, terminal, diagramas que se arman) con **cámara que se mueve en un set con profundidad** (`docs/CAMARA.md`). Sin modelos 3D salvo un plano puntual que lo pida.
- **Identidad**: `assets/marca.css` de cada video (copiada de la plantilla). Tema cyber / HackTheBox: fondo `--bg #0B111C`, tarjetas `--panel`, filetes `--line`, texto `--text`, secundario `--muted`, acento lima `--acc #9FEF00`. Siempre `var(--…)`, nunca colores fijos.
- **Color = significado**: énfasis (palabra clave, firma, progreso) = `--acc` · ✓ correcto = `--ok` verde · ⚠ aviso = `--warn` ámbar · ✕ error = bloque rojo RELLENO (`.chip.err`). Nunca el mismo color para lo bueno y lo malo; verde y ámbar solo en estados.
- **Tipografía**: IBM Plex Sans 500/700 (`--sans`) y IBM Plex Mono (`--mono`), locales en `assets/fonts/`. Espaciado normal o apretado (titulares −0,02 a −0,03 em); **nunca** mayúsculas con espaciado amplio.
- **Titulares**: 1–3 líneas, una idea por escena, la palabra clave con `.acc`. Un titular que aterrizó queda quieto: el movimiento lo pone la cámara o el elemento siguiente.
- **Entradas de texto**: palabra por palabra con desenfoque (blur 10 → 0, ~0,18 s, 60–120 ms entre palabras), sin deslizar. Variar la entrada entre escenas (ver `/hyperframes` → `references/motion.md`).
- **Paso**: "Paso 1 de 7" en Plex Sans + segmentos (`.pasos`), fijo en pantalla (fuera de la cámara).
- **Firma**: `@ayrtonnacer` al inicio y al final, con `--acc`, sola (sin punto, ícono ni adorno). Lo resaltado es lo que se debe recordar.
- **Ritmo**: un cambio visual cada 1,5–3 s (entra algo, viaja la cámara, se dibuja un resalte). Nada quieto más de 3 s.
- **Prohibido**: líneas de escaneo, marcos HUD / esquinas en L, "// TUTORIAL", "[ GRATIS ]", texto de fuente al final, loops de "flotar/respirar", rebote en interfaz, todas las escenas entrando igual.
- **Subtítulos**: no, salvo que Ayrton los pida (si los pide: bloque de captions del registro de HyperFrames, adaptado a la marca).
