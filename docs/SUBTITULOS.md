# Subtítulos (activados por defecto desde 2026-11-09)
Motivo (Ayrton): mucha gente mira los reels **sin sonido**; el video tiene que entenderse leyendo.

## Cómo se hacen
1. `python engine/audio/voz.py videos/X` — además de la voz guarda `audio/palabras.json`: el **tiempo exacto de cada palabra**. Salen de la duración por fonema que da el propio modelo de Piper (`include_alignments`, paquete `onnx`), así que no hace falta transcribir con Whisper ni hay deriva.
2. `python engine/subtitulos.py videos/X` — arma `compositions/subtitulos.html` (generado: no editar a mano) y el host en `index.html` (`data-track-kind="captions"`, `z-index: 50`).
Correr los dos después de cambiar texto o tiempos de la voz.

## Reglas
- **Zona segura**: franja **y 1120–1320** (1080×1920). Arriba de lo que tapa la interfaz de las apps (≥ 1330 px hacia abajo) y debajo de la imagen. Por eso la cámara sube todo el set 170 px (`DY` en `assets/camara.js`) y **la imagen no pasa de y ≈ 1100**. Nada importante en los 200 px superiores.
- Bloques de 2–5 palabras, 1–2 líneas, máx. ~34 caracteres; cortan en puntuación. Un bloque **no termina en artículo, preposición o conjunción** (esa palabra pasa al siguiente). Nunca una palabra sola en la última línea (`text-wrap: balance` + `&nbsp;` entre las dos últimas palabras; ver `docs/TIPOGRAFIA.md`).
- Plex Sans 700, 70 px, color de texto del tema, sombra para leer sobre cualquier fondo. Espaciado normal o apretado, nunca abierto.
- La **palabra que se dice** se pinta con el acento (`--acc`); el cambio es un corte seco. Los bloques aparecen de golpe.
- No repetir en pantalla lo que ya dice el subtítulo (se sacó la bajada "Por eso a veces no llega" del gancho).
- Números y siglas: el subtítulo muestra el texto original ("2,4"), la voz lo lee por diccionario ("dos coma cuatro").

## Cómo verificar que está sincronizado
`voz.py` ya imprime avisos si el conteo de palabras no coincide. Para "escuchar" el audio sin oído: dibujar la onda de `audio/voz.wav` con una línea en el inicio de cada palabra de `palabras.json` (y la de `sfx.wav` debajo); los inicios deben caer en los ataques de las sílabas, y los efectos en el pico de cada movimiento. Esa imagen se armó para el reel de WiFi (ver `docs/BITACORA.md`).
