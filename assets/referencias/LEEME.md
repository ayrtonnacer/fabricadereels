# Videos de referencia
Acá se guardan los videos de otros creadores que Ayrton pasa como referencia (mp4, mov, webm), junto a su medición en `docs/referencias/externos/<nombre>/` (ver `docs/MEDICION.md`). Son contenido de terceros: se usan para estudiar técnica (planos, transiciones, ritmo, sonido), no se republican ni se copian sus imágenes, marcas o textos. Si el repo se hace público, conviene sacarlos del historial o volver a ignorarlos en `.gitignore`.

Cómo cargarlos:
1. **Adjuntarlos en el chat** (quedan en una carpeta de subidas de la sesión; Claude los copia acá con un nombre claro), o
2. **Dejarlos en esta carpeta** y avisar el nombre del archivo.

Para bajarlos de YouTube/Instagram/TikTok/Pinterest a tu compu (desde la sesión el proxy los bloquea):
```
yt-dlp -f "bv*[height<=1080]+ba/b" -o "assets/referencias/%(title).40s.%(ext)s" "<link>"
```
Con recortar 10–30 s del tramo que te gusta alcanza.

Analizadas hasta ahora: ver `docs/referencias/BIBLIA-DE-ESTILO.md`.
