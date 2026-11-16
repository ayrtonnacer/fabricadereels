# Banco de efectos reales (no se sube a git: se reconstruye)
`bash engine/audio/bajar_sfx.sh` baja ~450 efectos **CC0** (dominio público, verificado pack por pack en OpenGameArt) a `assets/sfx/<tipo>/<pack>/`:
`whoosh/` (swishes, air-whoosh) · `ui/` (Kenney interface sounds + 51 UI SFX: click, tick, pluck, switch, rollover…) · `click/` · `hit/` (impactos, metal, vidrio, caídas) · `bell/` (dings) · `scifi/` (Kenney: motores, láseres, ruido de computadora, impactos).
Uso en `sfx_events.py`: `banco('whoosh', 'swish-3')`, `banco('ui', 'click', i)`, `banco('hit', 'metal_hit')`, `banco('scifi', 'computerNoise')` (busca en subcarpetas; el filtro es parte del nombre; `i` elige entre los que coinciden; None si falta → usar el sintético). Los propios de Ayrton siguen en `propios/` (sí se suben).
Créditos y licencias: `docs/2-estilo/AUDIO.md` → "Banco de efectos".
