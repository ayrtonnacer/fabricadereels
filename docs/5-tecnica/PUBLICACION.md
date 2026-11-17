# Estado de los videos, panel y publicación programada
Pedido de Ayrton (2026-11-17): una interfaz para dejar programados los videos en sus redes, unida a su **Tasker CRM**. Esto es lo que ya está y la propuesta para lo que falta. **Nada se publica sin que Ayrton lo pida.**

## Lo que ya está en este repo
- Cada video tiene en `video.json`: `"estado"` (`guion` → `animando` → `listo` → `programado` → `publicado`) y `"publicar": { "fecha": "", "redes": ["instagram", "tiktok", "youtube"], "links": {} }`.
- `descripcion.md` en cada video: el texto para publicar, fuentes, créditos y hashtags.
- `python engine/reel.py estado` muestra la tabla; `--json` la da como datos; `--guardar` la escribe en **`videos/estado.json`** (se sube a GitHub: es lo que puede leer un panel).
- `python engine/reel.py entregar videos/X` deja `portada.jpg` y una copia liviana.

## Qué falta para programar publicaciones (y por qué no es solo "una pantalla")
1. **El mp4 tiene que estar en una dirección pública.** `final.mp4` no se sube a GitHub (pesa). Las plataformas publican desde una URL. Opciones: adjuntarlo a una "release" de GitHub, o subirlo a un almacenamiento (Vercel Blob, Supabase Storage).
2. **Permisos de cada red**:
   | Red | Cómo se publica por programa | Requisito |
   |---|---|---|
   | Instagram Reels | Graph API de Meta | cuenta Profesional (creador o empresa) vinculada a una página de Facebook + app de Meta con permiso de publicación |
   | YouTube Shorts | YouTube Data API | proyecto de Google con OAuth; es la más simple; permite fecha de publicación |
   | TikTok | Content Posting API | app aprobada por TikTok (sin auditoría, los videos quedan privados) |
3. **Algo que dispare a la hora programada** (una tarea programada).
4. **La música**: la firma tiene copyright. Publicar por API con esa música puede terminar en video silenciado; desde la app se puede usar la biblioteca oficial. Es un motivo para definir una pista propia antes de automatizar.

## Tres caminos, del más simple al más propio
| Camino | Qué es | A favor | En contra |
|---|---|---|---|
| **A. Servicio de programación** (Metricool, Buffer, Later; o el conector vidIQ que ya está en Claude) | se sube el mp4 y la descripción, se elige fecha y redes | funciona hoy, ellos mantienen los permisos de cada red | plan pago para varias redes; el panel no es tuyo |
| **B. Pestaña "Reels" en Tasker CRM + servicio A** (recomendado) | Tasker CRM lee `videos/estado.json` de este repo (igual que ya sincroniza con GitHub) y muestra el calendario: qué reel está en qué etapa, fecha, redes, link; la publicación real la hace el servicio | todo se ve y se planifica en tu CRM; poco código; sin pelear con las APIs | dos lugares (CRM para planificar, servicio para publicar) |
| **C. Todo propio** | Tasker CRM con backend (hoy guarda en el navegador): almacenamiento del video, claves de cada red, tarea programada que publica | un solo lugar, sin abono | semanas de trabajo y mantenimiento; aprobaciones de Meta y TikTok; hay que agregarle servidor al CRM |

**Recomendación**: empezar por **B**. Tasker CRM es una app Next.js que guarda en el navegador y sincroniza con un repo de GitHub; sumarle una pestaña que lea `videos/estado.json` es chico y no cambia su arquitectura. Si después de un mes de publicar así querés automatizar del todo, se pasa a C empezando por YouTube.

## Para hacerlo
Es un trabajo sobre el repo `tasker-crm` (otra sesión, con ese repo abierto): pestaña "Reels" que lee `https://raw.githubusercontent.com/ayrtonnacer/fabricadereels/main/videos/estado.json`, con vista de calendario y columnas por estado. De este lado solo hay que correr `python engine/reel.py estado --guardar` al entregar cada reel (ya está en la lista de `entregar`).
