# Pronunciación
Piper lee mal siglas y palabras en inglés. Se corrige con `engine/audio/pronunciacion.json`:
- `reemplazos`: palabra → respelling fonético ("Parrot"→"Párrot"). `estado: sin_verificar` hasta que Ayrton la escuche y confirme; pasar a `ok`.
- `prohibidas`: palabras que no deben estar en la voz; `voz.py` avisa y propone alternativa.
Proceso: escribir el texto natural en `video.json`; `voz.py` aplica el diccionario; escuchar; si una palabra suena mal, agregarla al diccionario (en el mismo commit). Tips: acento escrito para marcar sílaba tónica; separar siglas por letras ("u ese be").
