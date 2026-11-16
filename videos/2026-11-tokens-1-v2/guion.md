# Guion — Qué son los tokens (parte 1): la IA lee números
Aprobado por Ayrton el 2026-11-16 (versión técnica, serie de 2). Datos validados en `docs/4-referencias/material/2026-11-16-tokens-validacion.md`.

| Escena | Tiempo | Voz |
|---|---|---|
| gancho | 0.1–4.1 s | La inteligencia artificial no lee tu mensaje: lee números. |
| corte | 4.1–10.9 s | Primero, un tokenizador lo corta en pedazos llamados tokens, y a cada uno le da un número fijo. |
| comparten | 10.9–19.3 s | Las palabras comunes entran enteras. Las raras se parten, y dos palabras distintas pueden compartir un pedazo, con el mismo número. |
| mayus | 19.3–24.9 s | Ojo: una mayúscula o un espacio adelante ya cambian el número del token. |
| idioma | 24.9–31.1 s | Y el español gasta más: el mismo texto ocupa un tercio más de tokens que en inglés. |
| foto | 31.1–38.1 s | Con una foto pasa igual: se divide en cuadraditos de dieciséis por dieciséis píxeles, y cada uno es un token. |
| payoff | 38.1–42.5 s | Para la inteligencia artificial, todo es una lista de números. |
| cierre | 42.5–47.5 s | Dale me gusta y seguime para aprender más sobre inteligencia artificial. |

Cambios de palabras después de escuchar con Whisper: "asigna" → "da" (sonaba "asina"), "párrafo" → "texto" ("parafora"), línea de mayúsculas simplificada (62 % → 100 % entendida), "se corta en" → "se divide en".
