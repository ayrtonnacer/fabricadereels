#!/usr/bin/env bash
# Deja una sesión NUEVA lista para trabajar (cada sesión arranca en un contenedor limpio, sin dependencias instaladas). Es idempotente: correrlo de más no rompe nada.
#   bash engine/preparar.sh
set -uo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || echo "FALTA ffmpeg (apt-get install -y ffmpeg)"
command -v node >/dev/null || echo "FALTA node ≥ 22"
python3 -c "import piper, cv2, scipy, numpy, faster_whisper" 2>/dev/null || pip install -q -r requirements.txt 2>&1 | grep -v "WARNING: Running pip as the 'root'" | tail -2
[ -d node_modules/hyperframes ] || npm install --no-audit --no-fund 2>&1 | tail -1
python3 -c "import piper, cv2, scipy, numpy, faster_whisper" 2>/dev/null && echo "python: ok" || echo "python: FALTAN paquetes (pip install -r requirements.txt)"
[ -x node_modules/.bin/hyperframes ] && echo "hyperframes: ok" || echo "hyperframes: FALTA (npm install)"
[ -d assets/sfx/whoosh ] || bash engine/audio/bajar_sfx.sh 2>&1 | tail -1 || echo "banco de efectos: no se pudo bajar (se usan los sintéticos)"
