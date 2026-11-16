#!/usr/bin/env bash
# Baja el banco de efectos reales (TODOS CC0 / dominio público, verificado en la página de cada pack el 2026-11-16) a assets/sfx/<tipo>/.
# assets/sfx/* no se sube a git: este script lo reconstruye en cualquier entorno.  Uso: bash engine/audio/bajar_sfx.sh
# Fuente: OpenGameArt.org (Kenney, StarNinjas, artisticdude, pyranostudios, rubberduck, Joth). CC0 = sin atribución obligatoria; igual se lista en assets/sfx/CREDITOS.md.
set -euo pipefail
cd "$(dirname "$0")/../.."; D=assets/sfx; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
get() { # tipo  url-del-archivo  [nombre-pack]
  local tipo=$1 url=$2 pack=$3 f="$T/$(basename "${2%%\?*}")"; mkdir -p "$D/$tipo/$pack"
  curl -fsSL -m 120 "$url" -o "$f"
  case "$f" in *.zip) unzip -qo "$f" -d "$D/$tipo/$pack" ;; *) cp "$f" "$D/$tipo/$pack/" ;; esac; echo "ok $tipo/$pack"; }
O=https://opengameart.org/sites/default/files
get whoosh $O/swishes.zip swishes
get whoosh $O/whoosh2_0.wav air-whoosh
get ui     $O/UI_SFX_Set.zip ui-sfx-set
get ui     $O/kenney_interfaceSounds.zip kenney-interface
get click  $O/10_clicks_and_switches.zip clicks-switches
get hit    $O/sfx_breaking_and_falling.zip breaking-falling
get bell   $O/ding_-_starninjas.zip dings
get scifi  $O/sci-fi_sounds.zip kenney-scifi
get scifi  "$O/7%20Space%20Sounds_1.mp3" space-sounds
echo "listo: $(find $D -type f \( -name '*.wav' -o -name '*.ogg' -o -name '*.mp3' \) | wc -l) archivos"
