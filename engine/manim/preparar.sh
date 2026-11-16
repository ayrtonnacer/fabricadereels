#!/usr/bin/env bash
# Instala Manim Community (MIT) en un entorno aparte (.venv-manim, ignorado por git). Opcional: solo para reels de matemática.
# Uso: bash engine/manim/preparar.sh      Render: bash engine/manim/render.sh engine/manim/escena_base.py Ejemplo
set -euo pipefail
cd "$(dirname "$0")/../.."
if ! pkg-config --exists pangocairo 2>/dev/null; then apt-get update -q && apt-get install -y -q libcairo2-dev libpango1.0-dev pkg-config python3-dev; fi
[ -d .venv-manim ] || python3 -m venv .venv-manim
.venv-manim/bin/pip install -q manim && .venv-manim/bin/python -c "import manim; print('manim', manim.__version__)"
