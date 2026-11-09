#!/usr/bin/env bash
# Crea un video nuevo desde la plantilla:  bash engine/nuevo.sh AAAA-MM-tema
set -euo pipefail
[ $# -eq 1 ] || { echo "uso: bash engine/nuevo.sh AAAA-MM-tema"; exit 1; }
cd "$(dirname "$0")/.."
dst="videos/$1"; [ -e "$dst" ] && { echo "ya existe $dst"; exit 1; }
mkdir -p "$dst"
tar -C videos/_plantilla --exclude=out --exclude=audio --exclude=.hyperframes --exclude=final.mp4 --exclude=__pycache__ -cf - . | tar -C "$dst" -xf -
printf '{"id":"%s","name":"%s"}\n' "$1" "$1" > "$dst/meta.json"
echo "listo: $dst  (siguiente: completar video.json y guion.md; ver docs/FLUJO.md)"
