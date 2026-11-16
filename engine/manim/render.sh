#!/usr/bin/env bash
# Renderiza una escena de Manim a 1080×1920 / 30 fps. Uso: bash engine/manim/render.sh archivo.py Escena [--transparent]
set -euo pipefail
cd "$(dirname "$0")/../.."
f=$1; s=$2; shift 2
.venv-manim/bin/manim -qh --disable_caching --media_dir out/manim "$@" "$f" "$s"
