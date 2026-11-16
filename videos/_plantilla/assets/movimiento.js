// Biblioteca de movimientos puros: todo es función del tiempo local t (determinista, sin Math.random ni reloj) → compatible con el contrato de HyperFrames.
// Escrita para este repo a partir de las ideas de docs/4-referencias/material/2026-11-onetake.md (las fórmulas son matemática estándar: resorte amortiguado, smootherstep, easing exponencial).
// Uso:  import * as M from './assets/movimiento.js';  const k = M.resorte(t - t0); el.style... = ...  /  en three.js: cámara.position.x += M.temblor(t, tGolpe).x
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const seg = (t, a, b) => clamp((t - a) / Math.max(1e-9, b - a));                  // 0→1 entre a y b
export const suave = (u) => u * u * u * (u * (u * 6 - 15) + 10);                          // smootherstep
export const expoOut = (u) => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u));
export const expoInOut = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u < 0.5 ? Math.pow(2, 20 * u - 10) / 2 : (2 - Math.pow(2, -20 * u + 10)) / 2);
export const sineInOut = (u) => -(Math.cos(Math.PI * u) - 1) / 2;

// Resorte: respuesta a un escalón (0→1) con amortiguación z y frecuencia w (rad/s). z<1 rebota un poco; z=1 sin rebote.
export function resorte(tau, z = 0.6, w = 20) {
  if (tau <= 0) return 0;
  if (z < 1) { const wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * tau) * (Math.cos(wd * tau) + (z * w / wd) * Math.sin(wd * tau)); }
  if (z === 1) return 1 - Math.exp(-w * tau) * (1 + w * tau);
  const q = w * Math.sqrt(z * z - 1), r1 = -z * w + q, r2 = -z * w - q;
  return 1 - (r2 * Math.exp(r1 * tau) - r1 * Math.exp(r2 * tau)) / (r2 - r1);
}
const anillo = (tau, d, w) => (tau > 0 ? Math.exp(-d * tau) * Math.sin(w * tau) : 0);

// Entradas "con carácter": la opacidad se adelanta al movimiento (no es un fundido: llega con desplazamiento y escala).
export function entra(t, t0, { z = 0.6, w = 22, dy = 26, s0 = 0.94 } = {}) { const k = resorte(t - t0, z, w); return { op: clamp(1.5 * k), y: (1 - k) * dy, s: s0 + (1 - s0) * k }; }
export function popIn(t, t0) { return entra(t, t0, { z: 0.62, w: 18, dy: 36 }); }
export function sale(t, t1, { dur = 0.35, dist = 40, blur = 6 } = {}) { const k = suave(seg(t, t1, t1 + dur)); return { op: 1 - k, y: -dist * k, s: 1 + 0.04 * k, blur: blur * k }; }
export function letra(t, t0, i, { paso = 0.055, z = 0.5, w = 24, dy = 30 } = {}) { return entra(t, t0 + i * paso, { z, w, dy }); }   // escalonado por letra
// Aterrizaje: aplastar y vibrar (escala x/y), para el momento en que algo cae o golpea.
export function impacto(t, tGolpe, { decay = 7, w = 22, ax = 0.13, ay = 0.16 } = {}) { const r = anillo(t - tGolpe, decay, w); return { sx: 1 + ax * r, sy: 1 - ay * r }; }
// Estirar según la velocidad (px/s) para sugerir movimiento.
export function estirar(vx, vy) { const v = Math.hypot(vx, vy); return { sx: 1 + Math.min(0.0012 * v, 0.45), sy: 1 - Math.min(0.0008 * v, 0.3), ang: Math.atan2(vy, vx) }; }

// Temblor de cámara decreciente y determinista, SOLO desde el golpe (antes es cero). amp en px (o en unidades de mundo si se escala).
export function temblor(t, tGolpe, { amp = 12, decay = 9, f = 19, sem = 1 } = {}) {
  const tau = t - tGolpe; if (tau <= 0) return { x: 0, y: 0, rot: 0 };
  const h = (n) => { const s = Math.sin(n * 12.9898 + sem * 78.233) * 43758.5453; return s - Math.floor(s); };   // pseudoazar por semilla, sin reloj
  const e = amp * Math.exp(-decay * tau);
  return { x: e * Math.sin(2 * Math.PI * tau * f * (1 + 0.1 * h(1))), y: 0.7 * e * Math.sin(2 * Math.PI * tau * f * (1.31 + 0.1 * h(2))), rot: 0.0015 * e * Math.sin(2 * Math.PI * tau * f * (0.77 + 0.1 * h(3))) };
}
// Latigazo: desplazamiento 0→dist con curva exponencial (arranca y frena fuerte): para pasar de un punto a otro "de golpe".
export const latigazo = (t, t0, dur, dist) => dist * expoInOut(seg(t, t0, t0 + dur));
// Empuje lento: 1 → 1+cant. OJO: en una pausa NO usarlo (la pausa tiene que estar quieta; docs/2-estilo/CAMARA.md regla 9).
export const empuje = (t, t0, t1, cant = 0.07) => 1 + cant * seg(t, t0, t1);
// Flotación de mano: dos senos lentos; `env` la apaga en las pausas (env=0 → cámara 100 % quieta).
export function mano(t, { amp = 3, f1 = 0.31, f2 = 0.47 } = {}, env = 1) { return { x: env * amp * Math.sin(2 * Math.PI * f1 * t), y: env * amp * 0.7 * Math.sin(2 * Math.PI * f2 * t + 1.3) }; }
export const envMano = (t, entra0, entra1, sale0, sale1) => suave(seg(t, entra0, entra1)) * (1 - suave(seg(t, sale0, sale1)));

// Cámara por claves {t, x, y, zoom, rot, e}: el zoom se interpola en escala logarítmica (un zoom ×2 y otro ×0,5 pesan igual).
const CURVAS = { io: suave, out: expoOut, expo: expoInOut, sine: sineInOut, lin: (u) => u };
export function camara(t, K) {
  let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
  const a = K[i], b = K[i + 1], k = (CURVAS[b.e || 'io'])(seg(t, a.t, b.t)), d = (o, p, v) => (o[p] ?? v);
  return { x: lerp(d(a, 'x', 0), d(b, 'x', 0), k), y: lerp(d(a, 'y', 0), d(b, 'y', 0), k), rot: lerp(d(a, 'rot', 0), d(b, 'rot', 0), k), zoom: Math.exp(lerp(Math.log(d(a, 'zoom', 1)), Math.log(d(b, 'zoom', 1)), k)) };
}
// Cámara que SIGUE un punto con adelanto: devuelve dónde mirar `ade` segundos antes de que el sujeto llegue (f(t) → [x,y,z]).
export const mirarAdelantado = (f, t, ade = 0.1) => f(t + ade);

// ---- límites con arrastre (carry): el objeto de una escena se vuelve la siguiente ----
// Un rectángulo A se transforma en B (x,y,w,h,r): la tarjeta que crece hasta ser la página.
export function morfar(t, t0, t1, A, B, e = expoOut) { const k = e(seg(t, t0, t1)); const o = {}; for (const c of ['x', 'y', 'w', 'h', 'r']) o[c] = lerp(A[c] ?? 0, B[c] ?? 0, k); return o; }
// Cámara que empuja hasta que `obj` (rect {x,y,w,h}) llena el cuadro W×H: devuelve la matriz [s,0,0,s,tx,ty] para aplicar al "mundo".
export function atravesar(t, t0, t1, obj, W = 1080, H = 1920, cubrir = true) {
  const k = expoInOut(seg(t, t0, t1)), sFin = (cubrir ? Math.max : Math.min)(W / obj.w, H / obj.h), s = Math.pow(sFin, k);
  const cx = obj.x + obj.w / 2, cy = obj.y + obj.h / 2, px = lerp(cx, W / 2, k), py = lerp(cy, H / 2, k); return [s, 0, 0, s, px - s * cx, py - s * cy];
}
// Círculo que se abre desde un punto hasta cubrir el cuadro (radio).
export function iris(t, t0, t1, cx, cy, W = 1080, H = 1920) { const far = Math.max(Math.hypot(cx, cy), Math.hypot(W - cx, cy), Math.hypot(cx, H - cy), Math.hypot(W - cx, H - cy)) + 2; return far * expoOut(seg(t, t0, t1)); }
// Salto en arco de un lugar a otro (aterrizar con `impacto`).
export function salto(t, t0, t1, a, b, alto = 200) { const k = suave(seg(t, t0, t1)); return { x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k) - alto * Math.sin(Math.PI * k) }; }
// Un grupo converge en uno (cierre/lockup): item i de n, con retraso de 0,08 s por ítem y arco.
export function juntar(t, t0, t1, i, n, a, b, { retraso = 0.08, arco = 120, giro = 0.4 } = {}) { const k = suave(seg(t, t0 + i * retraso, t1 + i * retraso)), bump = Math.sin(Math.PI * k), o = i - (n - 1) / 2; return { x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k) - arco * bump, rot: giro * bump * o }; }
