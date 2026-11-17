# Temas de color
El tema por defecto vive en `videos/_plantilla/assets/marca.css` (y cada video tiene su copia). Hoy es **Scale** (desde 2026-11-14): negro puro, objetos 3D de línea gris, acento Foundry Tan `#A8927C`, Host Grotesk + Geist Mono. Detalle en `docs/2-estilo/ESTILO.md`.

Temas alternativos (no se usan salvo que Ayrton lo pida):
| Archivo | Tema | Hasta |
|---|---|---|
| `linea-roja.css` | Negro + línea gris + acento rojo `#FF2E3F`, IBM Plex | default del 2026-11-11 al 2026-11-14 (reel de WiFi) |
| `cyber.css` | Azul-negro + lima, objetos sólidos (`--estilo: solido`), IBM Plex | anterior al 2026-11-11 |

**No se usan ni se proponen** salvo que Ayrton lo pida. Para usar uno en un video: reemplazar el bloque `:root { … }` y las `@font-face` de `videos/X/assets/marca.css` por los del tema, y en `videos/X/assets/escena3d.js` cambiar "Geist Mono"/"Host Grotesk" por "IBM Plex Mono"/"Plex Sans" (las letras de las texturas 3D). Las fuentes de Plex están en `videos/2026-11-wifi/assets/fonts/` (copiarlas a `assets/fonts/` del video y agregar sus `@font-face`).
