# Videos de referencia (NO van a git)
Acá se dejan los videos de otros creadores que queremos analizar (mp4, mov, webm). Pesan y no son nuestros, por eso están ignorados por git (`.gitignore`).

Cómo cargarlos:
1. **Adjuntarlos en el chat** (si la app lo permite): quedan en una carpeta de subidas y se analizan desde ahí; o
2. **Dejarlos en esta carpeta** y avisar el nombre del archivo.

Para bajarlos de YouTube/Instagram/TikTok a tu compu (desde la sesión no se puede, el proxy bloquea YouTube):
```
yt-dlp -f "bv*[height<=1080]+ba/b" -o "assets/referencias/%(title).40s.%(ext)s" "<link>"
```
Con recortar 10–30 s del tramo que te gusta alcanza. El análisis queda en `referencias/<nombre>/` (ver `docs/ANALISIS-REFERENCIAS.md`).
