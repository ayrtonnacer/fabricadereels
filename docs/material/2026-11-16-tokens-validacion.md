# Validación de datos del reel de tokens (2026-11-16)
Medido con `tiktoken` (tokenizadores públicos de OpenAI: `cl100k_base` = GPT-4, `o200k_base` = GPT-4o). El de Claude no es público.

## Lo que el artículo de NVIDIA simplifica o exagera
- **dark + ness / bright + ness (217, 655, 491)**: números inventados. Real (o200k): "darkness" sin espacio = dark|ness, pero " darkness" (en medio de una frase) = 1 token, y "brightness" = 1 token siempre. → No usar ese ejemplo.
- **"corta = 1 token, larga = 2+"**: la regla real es frecuencia (BPE): " seguridad", " humanidad", " velocidad" = 1 token; " oscuridad" = ' oscur'|'idad'.
- **"lie" con números distintos según el sentido**: falso para un tokenizador estándar (mismo token; el sentido lo resuelve el modelo por contexto).
- **"decenas de miles de tokens = una novela"**: una novela de ~90 000 palabras ≈ 110 000–130 000 tokens. Decenas de miles = un podcast de una hora (≈ 9 000 palabras ≈ 12 000 tokens).
- **"si acierta sigue, si falla se corrige"**: en realidad mide cuánta probabilidad le dio a la respuesta correcta (pérdida) y ajusta los pesos siempre.
- **">100x de cómputo con razonamiento"**: el artículo dice "puede requerir"; usar con "puede".

## Datos reales para el guion (o200k_base)
- Pedazo compartido: " nitidez" = ' nit'(27054) + 'idez'(36753); " lucidez" = ' luc'(34623) + 'idez'(36753). " opacidad" y " tenacidad" comparten 'acidad'(54690).
- Mayúsculas y espacios: "hola" = 122845, " hola" = 171847, " Hola" = 157464 → tres tokens distintos.
- Español vs inglés, mismo párrafo del artículo: inglés 36 tokens, español 48 (+33 %) con o200k; con cl100k 36 vs 56 (+56 %).
- Vocabulario: o200k_base = 200 019 tokens; cl100k_base = 100 277.
- Imágenes (ViT-B/16): parches de 16×16 píxeles; 224×224 → 196 tokens.
- Entrenamiento: Llama 3 (Meta, 2024) preentrenado con más de 15 billones (15T) de tokens.
- Generación autorregresiva: un token por paso; la entrada se procesa en paralelo (rápido), la salida de a uno (lento) → la salida cuesta varias veces más (ej. históricos: 4–5×; verificar precios el día de publicar). Los tokens de razonamiento se cobran como salida.
