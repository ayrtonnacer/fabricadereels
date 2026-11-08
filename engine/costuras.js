// Costuras: transiciones entre escenas con velocidad igualada a ambos lados del corte (docs/MOVIMIENTO.md).
// Idea tomada de las reglas de movimiento de HyperFrames (heygen-com/hyperframes, Apache-2.0), reescrita para este motor.
// Principio: cortar en el pico de velocidad; la escena que sale acelera y la que entra sigue en la MISMA dirección y frena.
// Nunca se ven las dos escenas a la vez (no es un fundido): el corte cae a mitad del movimiento.
//
// Uso: en video.json, en la escena que SALE:  "salida": "curva-izq"   (o {"tipo":"curva","dir":"izq","blur":8})
//   curva-izq|der|arriba|abajo · zoom (atravesar) · zoom-inverso (llegada/payoff) · foco (rack focus) · latigazo-izq|der · oscuro (dip cut) · corte
// lib.js lo aplica solo; sin "salida" no cambia nada.
import { clamp } from './lib.js';

const p4in = x => x ** 4, p4out = x => 1 - (1 - x) ** 4, p3in = x => x ** 3, p2in = x => x * x, p2out = x => 1 - (1 - x) ** 2;
const expoOut = x => x >= 1 ? 1 : 1 - 2 ** (-10 * x);
const DIR = { izq: [-1, 0], der: [1, 0], arriba: [0, -1], abajo: [0, 1] };

// Duraciones (s) de cada lado del corte. La entrada es igual o más larga que la salida.
export const TIEMPOS = {
  curva: [0.32, 0.36], zoom: [0.2, 0.5], 'zoom-inverso': [0.22, 0.5], foco: [0.25, 0.32], latigazo: [0.15, 0.2], oscuro: [0.1, 0], corte: [0, 0],
};

export function parse(s) {
  if (!s) return null;
  if (typeof s === 'object') return { dir: 'izq', ...s };
  const [tipo, ...r] = s.split('-'); const rest = r.join('-');
  if (tipo === 'zoom' && rest === 'inverso') return { tipo: 'zoom-inverso' };
  return { tipo, dir: rest || 'izq' };
}

// Filtro SVG de desenfoque direccional (para latigazos: barrido solo horizontal o vertical).
let svgBlur = null;
function blurDir(px, horiz) {
  if (!svgBlur) {
    document.body.insertAdjacentHTML('beforeend', '<svg width="0" height="0" style="position:absolute"><filter id="costura-mb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur id="costura-mbg" stdDeviation="0 0"/></filter></svg>');
    svgBlur = document.getElementById('costura-mbg');
  }
  svgBlur.setAttribute('stdDeviation', horiz ? `${px} 0` : `0 ${px}`);
  return 'url(#costura-mb)';
}

// Estado visual de un lado de la costura. lado: 'sale' (k: 0→1 hasta el corte) | 'entra' (k: 0→1 desde el corte).
function estado(c, lado, k) {
  const [dx, dy] = DIR[c.dir] || DIR.izq, T = 230 * (c.recorrido ?? 1);   // recorrido parcial ≈12 % del cuadro, nunca fuera de pantalla
  let x = 0, y = 0, s = 1, o = 1, b = 0, f = '', bri = 1;
  switch (c.tipo) {
    case 'curva': {
      if (lado === 'sale') { const e = p4in(k); x = dx * T * e; y = dy * T * e; o = 1 - clamp((k - 0.4) / 0.6); b = (c.blur ?? 8) * e; }
      else { const e = p4out(k); x = -dx * T * (1 - e); y = -dy * T * (1 - e); o = 0.35 + 0.65 * clamp(k / 0.45); b = (c.blur ?? 8) * (1 - e); }
      break;
    }
    case 'zoom': {        // empuje hacia adelante: todo CRECE a ambos lados (signo del zoom igual)
      if (lado === 'sale') { const e = p3in(k); s = 1 + 0.2 * e; b = (c.blur ?? 10) * e; o = 1 - 0.85 * k; }
      else { const e = expoOut(k); s = 0.75 + 0.25 * e; b = (c.blur ?? 10) * (1 - e); o = 0.15 + 0.85 * e; }
      break;
    }
    case 'zoom-inverso': { // llegada: todo se ACHICA a ambos lados
      if (lado === 'sale') { const e = p3in(k); s = 1 - 0.2 * e; b = (c.blur ?? 10) * e; o = 1 - 0.85 * k; }
      else { const e = expoOut(k); s = 1.25 - 0.25 * e; b = (c.blur ?? 10) * (1 - e); o = 0.15 + 0.85 * e; }
      break;
    }
    case 'foco': {        // rack focus: el corte se VE, tapado por un pico de desenfoque; la escena saliente no se apaga
      if (lado === 'sale') { const e = p2in(k); b = (c.blur ?? 10) * e; s = 1 + 0.06 * e; }
      else { const e = p2out(k); b = (c.blur ?? 10) * (1 - e); s = 1.06 - 0.06 * e; }
      break;
    }
    case 'latigazo': {    // barrido corto con desenfoque direccional; lo que llega aterriza borroso y se aclara
      const horiz = dy === 0, W = 420;
      if (lado === 'sale') { const e = p3in(k); x = dx * W * e; y = dy * W * e; f = blurDir(40 * e, horiz); }
      else { const e = expoOut(k); x = -dx * W * (1 - e); y = -dy * W * (1 - e); f = blurDir(40 * (1 - clamp(k / 0.65)), horiz); }
      break;
    }
    case 'oscuro': { if (lado === 'sale') bri = 1 - 0.4 * clamp(k * 3); break; }  // se oscurece ~40 % 3 cuadros antes del corte seco
  }
  const filt = [f, b > 0.05 ? `blur(${b.toFixed(2)}px)` : '', bri < 1 ? `brightness(${bri.toFixed(3)})` : ''].filter(Boolean).join(' ');
  return { transform: (x || y || s !== 1) ? `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)})` : '', opacity: o, filter: filt };
}

// Devuelve el estilo a aplicar a la escena actual (y a su canvas 3D) o null si no está en una costura.
export function costura(SC, cur, lt) {
  const i = SC.indexOf(cur), prev = SC[i - 1];
  const out = parse(cur.salida), inn = prev && parse(prev.salida);
  if (out && SC[i + 1]) { const d = (TIEMPOS[out.tipo] || [0])[0]; if (d && lt > cur.d - d) return estado(out, 'sale', clamp((lt - (cur.d - d)) / d)); }
  if (inn) { const d = (TIEMPOS[inn.tipo] || [0, 0])[1]; if (d && lt < d) return estado(inn, 'entra', clamp(lt / d)); }
  return null;
}

// Chequeo estático (lo usa engine/revisar.py vía la misma lista): ping-pong de direcciones y cantidad de tipos.
export const RESERVADOS = { arriba: 'elevación: una conclusión o revelación', zoom: 'ir más hondo en la misma idea', 'zoom-inverso': 'llegada: algo grande aterriza (payoff)' };
