# Bandeja de entrada de referencias
Poné acá los mp4 que bajes (o adjuntalos en el chat y los dejo yo acá). **Un archivo = un reel.** Nombre sugerido: `canal_titulo-corto.mp4` (ej. `fireship_what-is-a-token.mp4`).
- Tamaño: GitHub no acepta archivos de más de 100 MB; con 540p–720p un reel pesa 3–10 MB. Si pesa mucho: `ffmpeg -i in.mp4 -vf scale=-2:720 -crf 28 out.mp4`.
- Opcional: un `canal_titulo-corto.txt` al lado con el link original y qué te gusta de ese reel (ritmo, cámara, sonido…). Eso se guarda y orienta el análisis.
- Si es de un canal nuevo, anotalo en `docs/1-canal/CANAL.md` (inspiraciones).
**Después**: `python engine/analisis/analizar_lote.py` mide cada mp4 nuevo → `docs/4-referencias/externos/<slug>/` (INFORME + métricas + hoja de cuadros), actualiza la biblia de estilo y mueve el mp4 a `assets/referencias/`. Se commitea todo a `main`.
