// GENERADO por engine/tiempos.py desde video.json y audio/palabras.json. NO EDITAR: cambiar video.json y correr `python engine/reel.py voz videos/X`.
export const DUR = 19;
// ESC.<escena> = { t0: segundo en que empieza, d: duración, t1: segundo en que termina }
export const ESC = {"portada": {"t0": 0.0, "d": 0.1, "t1": 0.1}, "gancho": {"t0": 0.1, "d": 3.5, "t1": 3.6}, "explica": {"t0": 3.6, "d": 7.4, "t1": 11.0}, "payoff": {"t0": 11.0, "d": 3.6, "t1": 14.6}, "cierre": {"t0": 14.6, "d": 4.4, "t1": 19.0}};
// VOZ.<línea> = { t0, t1 (inicio y fin de la frase, en segundos del video), escena, texto }
export const VOZ = {"l01": {"t0": 0.35, "t1": 2.76, "escena": "gancho", "texto": "Una frase corta que promete algo concreto."}, "l02": {"t0": 4.0, "t1": 6.07, "escena": "explica", "texto": "El primer concepto, con palabras simples."}, "l03": {"t0": 7.3, "t1": 9.71, "escena": "explica", "texto": "Después, el segundo, con un ejemplo cotidiano."}, "l04": {"t0": 11.3, "t1": 13.71, "escena": "payoff", "texto": "Y así se ve todo funcionando junto."}, "l05": {"t0": 14.9, "t1": 18.35, "escena": "cierre", "texto": "Dale me gusta y seguime para aprender más de tema."}};
// PAL = [línea, palabra, inicio, fin] de cada palabra dicha (tiempos exactos de Piper)
export const PAL = [];
const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
/* Segundo (tiempo global del video) en que la voz EMPIEZA a decir `palabra` dentro de la línea `linea` (k = 0 la primera vez, 1 la segunda…).
   Sin palabra: el inicio de la línea. Ej.: cuando('l03', 'router'). `python engine/reel.py revisar` avisa si la palabra no está en la línea. */
export function cuando(linea, palabra, k = 0) {
  const v = VOZ[linea]; if (!v) { console.error('cuando(): no existe la línea ' + linea); return 0; }
  if (!palabra) return v.t0;
  const hits = PAL.filter((p) => p[0] === linea && norm(p[1]) === norm(palabra));
  if (!hits[k]) { console.error(`cuando(): "${palabra}" no está en ${linea}`); return v.t0; }
  return hits[k][2];
}
/* Segundo en que la voz TERMINA de decir la palabra (o la línea). */
export function hasta(linea, palabra, k = 0) {
  const v = VOZ[linea]; if (!v) return 0; if (!palabra) return v.t1;
  const hits = PAL.filter((p) => p[0] === linea && norm(p[1]) === norm(palabra)); return hits[k] ? hits[k][3] : v.t1;
}
