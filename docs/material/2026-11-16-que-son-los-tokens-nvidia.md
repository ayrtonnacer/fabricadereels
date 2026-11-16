# Fuente: "What Are AI Tokens? The Language and Currency Powering Modern AI" (NVIDIA, blog)
Pasada por Ayrton el 2026-11-16 para el reel "qué son los tokens en IA". Resumen de lo usado (texto completo no copiado por derechos):
- Token = unidad chica de datos; la IA procesa tokens para aprender relaciones y predecir/generar/razonar.
- Tokenización: texto, imagen, audio, video → tokens. Palabra corta = 1 token; larga = 2 o más. Ejemplo del artículo: darkness = dark + ness (217, 655), brightness = bright + ness (491, 655); "ness" compartido ayuda a ver lo común. (Los números son ilustrativos.)
- Imágenes: píxeles/vóxeles → tokens discretos. Audio: espectrogramas o tokens semánticos.
- Entrenamiento: miles de millones/billones de tokens; se muestra una muestra y se pide predecir el siguiente; si falla, se corrige (convergencia). Luego post-entrenamiento.
- Inferencia: prompt → tokens de entrada → tokens de salida → formato final. Ventana de contexto = tope de tokens a la vez (miles: páginas; decenas de miles: una novela; millón+).
- Modelos de razonamiento generan tokens de razonamiento extra (>100x de cómputo).
- Economía: se cobra por tokens de entrada/salida; límites por minuto; "time to first token" y latencia entre tokens.
- Cuidado: la parte de NVIDIA (AI factories, 20x/25x, GPUs) es marketing; el ejemplo de "lie" con números distintos NO es cómo funciona un tokenizer estándar (el mismo token; el sentido se resuelve por contexto dentro del modelo) → no usarlo.
