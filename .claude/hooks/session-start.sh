#!/bin/bash
# Deja una sesión de la nube lista para hacer reels: ffmpeg, paquetes de Python (Piper, OpenCV, Whisper…) y node_modules (HyperFrames).
# Corre en cada inicio/reanudación; si nada cambió, no instala nada (compara hashes).
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}"

command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq ffmpeg; }

# Node: HyperFrames y compañía
hashes=node_modules/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  npm install --no-audit --no-fund
  sha256sum .claude/hooks/session-start.sh package.json package-lock.json > "$hashes" || rm -f "$hashes"
fi

# Python (sistema): Piper, OpenCV, scipy, faster-whisper
pyhashes="$(python3 -I -c 'import sysconfig; print(sysconfig.get_path("purelib"))')/.session-start.sha256"
if ! sha256sum --check --status "$pyhashes" 2>/dev/null; then
  rm -f "$pyhashes"
  python3 -m pip install -q -r requirements.txt
  sha256sum .claude/hooks/session-start.sh requirements.txt > "$pyhashes" || rm -f "$pyhashes"
fi

# Banco de efectos reales (CC0, ~450 archivos; no se sube a git). Si falla la descarga no frena la sesión: se usan los sintéticos.
[ -d assets/sfx/whoosh ] || bash engine/audio/bajar_sfx.sh >/dev/null 2>&1 || echo "aviso: no se pudo bajar el banco de efectos (bash engine/audio/bajar_sfx.sh)"
