#!/usr/bin/env bash
# Baja un reel de Instagram (u otra red) para analizarlo con engine/analisis/medir.py.  Uso:
#   bash engine/bajar_referencia.sh <url> [carpeta_destino]        (por defecto /tmp/referencias)
# Instala yt-dlp (herramienta de terceros, pedida por Ayrton el 2026-11-17) en un entorno aparte FUERA del repo la primera vez de cada sesión.
# Instagram limita las descargas seguidas (error 429): si pasa, esperar 20 s y repetir. El video NO se guarda en el repo: solo el informe (material/).
set -euo pipefail
VENV="${YTDLP_VENV:-$HOME/.cache/yt-dlp-venv}"
[ -x "$VENV/bin/yt-dlp" ] || { python3 -m venv "$VENV" && "$VENV/bin/pip" install -q yt-dlp; }
OUT="${2:-/tmp/referencias}"; mkdir -p "$OUT"
"$VENV/bin/yt-dlp" -q --no-progress -o "$OUT/%(id)s.%(ext)s" "$1" && ls -la "$OUT"
echo "siguiente: python engine/analisis/medir.py $OUT/<id>.mp4 <carpeta_salida> --hojas   (informe + hoja de cuadros)"
