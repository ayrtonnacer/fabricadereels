// Cámara 3D estilo After Effects para three.js (docs/CAMARA-3D.md).
// Todo es función pura del tiempo global T → determinístico cuadro a cuadro (render.mjs llama __render(T)).
//
//   const rig = new Rig(THREE, cam);
//   rig.toma({t0:0, t1:4, tipo:'fpv', curva:[[x,y,z],...], banking:0.6});
//   rig.toma({t0:4.4, t1:8, tipo:'orbita', centro:[0,1,0], radio:6, desde:-40, hasta:60, alto:2});
//   rig.toma({t0:8, t1:11, tipo:'mover', de:{pos,look}, a:{pos,look}});   // dolly / grúa / push-in / truck
//   rig.toma({t0:11, t1:13, tipo:'cenital', centro:[0,0,0], alto:14, giro:[0,30]});
//   rig.toma({t0:13, t1:15, tipo:'vertigo', centro:[0,1,0], de:4, a:12, fov:45});   // dolly zoom: el sujeto quieto, el fondo se estira
//   Entre el t1 de una toma y el t0 de la siguiente la cámara viaja sola (transición): hueco corto + distancia larga = latigazo.
//   const vel = rig.aplicar(T);           // posiciona la cámara; devuelve la velocidad (para el desenfoque de movimiento)
//   blur.render(T, t => rig.aplicar(t));  // render con desenfoque de movimiento real (sub-cuadros promediados)
import { clamp, eio, eo } from './lib.js';

const lerp = (a, b, k) => a + (b - a) * k;
const L3 = (a, b, k) => [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)];
export const EASE = {
  lineal: x => x,
  suave: eio,                                   // ease-in-out (el "Easy Ease" de AE)
  salida: eo,                                   // arranca rápido y frena
  entrada: x => x * x * x,                      // arranca lento y acelera (antes de un latigazo)
  latigazo: x => x < .5 ? 16 * x ** 5 : 1 - (-2 * x + 2) ** 5 / 2,   // casi quieto → pico violento → casi quieto
  llegada: x => x >= 1 ? 1 : 1 - 2 ** (-10 * x),   // expo.out: aterriza con cola larga (llegadas)
  acelera: x => x ** 4,                          // power4.in: la mitad que SALE de un corte
  frena: x => 1 - (1 - x) ** 4,                  // power4.out: la mitad que ENTRA (mismo pico de velocidad que 'acelera')
  // "empujón" (nudge curve): rampa lenta 20 % del tiempo/10 % del recorrido → ráfaga lineal 18 %/65 % → cola larga 62 %/25 %.
  // Para reacomodar o desplazar sin el golpe seco de un ease-in-out.
  empujon: x => x < .2 ? .1 * (x / .2) ** 3 : x < .38 ? .1 + .65 * (x - .2) / .18 : .75 + .25 * (1 - (1 - (x - .38) / .62) ** 4),
};
const ease = e => typeof e === 'function' ? e : (EASE[e] || eio);

// Ruido determinístico suave (suma de senos) para cámara en mano / dron. amp en unidades del mundo.
export function temblor(T, amp = 0.02, frec = 1) {
  const f = frec, s = Math.sin;
  return [
    amp * (s(T * 2.1 * f + 1.3) * .6 + s(T * 5.3 * f + .2) * .3 + s(T * 11.7 * f) * .1),
    amp * (s(T * 1.7 * f + 4.1) * .6 + s(T * 4.9 * f + 2.2) * .3 + s(T * 13.1 * f + 1) * .1),
    amp * (s(T * 1.3 * f + 2.7) * .6 + s(T * 6.1 * f + .9) * .4),
  ];
}

// Remapeo de tiempo (speed ramp): tramos [[t, velocidad], ...] → tiempo de la acción.
// Ej.: rampa(T, [[0,1],[3,0.25],[4,2.5],[5,1]]) = cámara lenta en 3 s y aceleración antes de 5 s.
export function rampa(T, tramos) {
  let acc = 0;
  for (let i = 0; i < tramos.length; i++) {
    const [ta, va] = tramos[i], nx = tramos[i + 1];
    if (!nx) return acc + (T - ta) * va;
    const [tb, vb] = nx;
    if (T <= tb) { const d = T - ta; return acc + va * d + (vb - va) * d * d / (2 * (tb - ta)); }
    acc += (va + vb) / 2 * (tb - ta);
  }
  return T;
}

// Interpolación Catmull-Rom (camino suave por puntos, como el "auto Bézier" de AE).
function catmull(P, u) {
  const n = P.length - 1, x = clamp(u) * n, i = Math.min(n - 1, Math.floor(x)), k = x - i;
  const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(n, i + 2)];
  const k2 = k * k, k3 = k2 * k;
  return [0, 1, 2].map(j => 0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * k + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * k2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * k3));
}
// Reparametriza por longitud de arco → velocidad constante a lo largo del camino.
function arco(P, N = 200) {
  const pts = [], len = [0];
  for (let i = 0; i <= N; i++) pts.push(catmull(P, i / N));
  for (let i = 1; i <= N; i++) len.push(len[i - 1] + Math.hypot(...[0, 1, 2].map(j => pts[i][j] - pts[i - 1][j])));
  const tot = len[N];
  return s => { const d = clamp(s) * tot; let i = 1; while (i < N && len[i] < d) i++; const k = (d - len[i - 1]) / ((len[i] - len[i - 1]) || 1); return L3(pts[i - 1], pts[i], k); };
}

// Pose = {pos:[x,y,z], look:[x,y,z], fov, roll(grados)}
function poseToma(s, k) {
  const e = ease(s.ease)(k);
  switch (s.tipo) {
    case 'fpv': {   // dron en primera persona: sigue la curva mirando hacia adelante e inclinándose en las curvas
      s._f ||= arco(s.curva);
      const u = e, a = s._f(u), b = s._f(Math.min(1, u + 0.02)), c = s._f(Math.min(1, u + 0.06));
      const look = L3(a, c, 1);
      // banking: curvatura horizontal (giro de la dirección) → roll
      const d1 = [b[0] - a[0], b[2] - a[2]], d2 = [c[0] - b[0], c[2] - b[2]];
      const giro = Math.atan2(d1[0] * d2[1] - d1[1] * d2[0], d1[0] * d2[0] + d1[1] * d2[1]);
      return { pos: a, look, fov: s.fov ?? 62, roll: clamp(giro * (s.banking ?? 0.6) * 180 / Math.PI * 6, -25, 25) };
    }
    case 'orbita': {  // arc shot alrededor de un centro
      const ang = lerp(s.desde, s.hasta, e) * Math.PI / 180, r = lerp(s.radio, s.radioFin ?? s.radio, e);
      const c = s.centro, h = lerp(s.alto ?? 0, s.altoFin ?? s.alto ?? 0, e);
      return { pos: [c[0] + Math.sin(ang) * r, c[1] + h, c[2] + Math.cos(ang) * r], look: s.mira || c, fov: lerp(s.fov ?? 35, s.fovFin ?? s.fov ?? 35, e), roll: s.roll ?? 0 };
    }
    case 'cenital': { // plano cenital (top-down) con giro lento opcional
      const g = (s.giro ? lerp(s.giro[0], s.giro[1], e) : 0) * Math.PI / 180, c = s.centro, h = lerp(s.alto, s.altoFin ?? s.alto, e);
      const eps = 0.002 * h;  // evita el lookAt degenerado mirando justo hacia abajo
      return { pos: [c[0] + Math.sin(g) * eps, c[1] + h, c[2] + Math.cos(g) * eps], look: c, fov: s.fov ?? 40, roll: 0 };
    }
    case 'vertigo': { // dolly zoom (Hitchcock): la cámara avanza o retrocede y el fov compensa → el sujeto queda igual, el fondo se estira
      // distancia·tan(fov/2) = constante. de/a: distancias al sujeto; fov: el fov inicial.
      const c = s.centro, dir = s.direccion || [0, 0, 1], f0 = s.fov ?? 40, d0 = s.de, d = lerp(s.de, s.a, e);
      const fov = 2 * Math.atan(Math.tan(f0 * Math.PI / 360) * d0 / d) * 180 / Math.PI;
      const n = Math.hypot(...dir) || 1;
      return { pos: [c[0] + dir[0] / n * d, c[1] + dir[1] / n * d, c[2] + dir[2] / n * d], look: c, fov, roll: s.roll ?? 0 };
    }
    default: {        // 'mover': dolly / truck / grúa / push-in entre dos poses (opcional: puntos intermedios 'via')
      const P = [s.de.pos, ...(s.via || []), s.a.pos];
      s._m ||= P.length > 2 ? arco(P) : (u => L3(P[0], P[1], u));
      return { pos: s._m(e), look: L3(s.de.look, s.a.look, e), fov: lerp(s.de.fov ?? 40, s.a.fov ?? s.de.fov ?? 40, e), roll: lerp(s.de.roll ?? 0, s.a.roll ?? 0, e) };
    }
  }
}
const mezcla = (A, B, k) => ({ pos: L3(A.pos, B.pos, k), look: L3(A.look, B.look, k), fov: lerp(A.fov, B.fov, k), roll: lerp(A.roll, B.roll, k) });

export class Rig {
  constructor(THREE, cam) { this.T3 = THREE; this.cam = cam; this.tomas = []; this.transiciones = {}; this._v = new THREE.Vector3(); this.extra = null; }
  toma(s) { this.tomas.push(s); this.tomas.sort((a, b) => a.t0 - b.t0); return this; }
  // ease de la transición que SALE de la toma i (por defecto 'suave'; 'latigazo' para whip pan)
  transicion(i, e) { this.transiciones[i] = e; return this; }
  pose(T) {
    const S = this.tomas;
    for (let i = 0; i < S.length; i++) {
      const s = S[i], n = S[i + 1];
      if (T < s.t0) return poseToma(s, 0);
      if (T <= s.t1) return poseToma(s, (T - s.t0) / (s.t1 - s.t0));
      if (n && T < n.t0) return mezcla(poseToma(s, 1), poseToma(n, 0), ease(this.transiciones[i] || 'suave')((T - s.t1) / (n.t0 - s.t1)));
    }
    return poseToma(S[S.length - 1], 1);
  }
  // Coloca la cámara en el tiempo T. `extra(T,pose)` permite sumar temblor o empujes. Devuelve velocidad aproximada (u/s + grados/s).
  aplicar(T) {
    let p = this.pose(T);
    if (this.extra) p = this.extra(T, p) || p;
    this._set(p);
    const q = this.pose(T - 1 / 30);
    const dv = Math.hypot(p.pos[0] - q.pos[0], p.pos[1] - q.pos[1], p.pos[2] - q.pos[2]) * 30;
    const a = [p.look[0] - p.pos[0], p.look[1] - p.pos[1], p.look[2] - p.pos[2]], b = [q.look[0] - q.pos[0], q.look[1] - q.pos[1], q.look[2] - q.pos[2]];
    const cos = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / (Math.hypot(...a) * Math.hypot(...b) || 1);
    const dw = Math.acos(clamp(cos, -1, 1)) * 180 / Math.PI * 30 + Math.abs(p.roll - q.roll) * 30;
    this.vel = dv + dw * 0.05;
    return this.vel;
  }
  _set(p) {
    const c = this.cam;
    c.position.set(...p.pos); c.up.set(0, 1, 0); c.lookAt(this._v.set(...p.look));
    c.rotateZ(-p.roll * Math.PI / 180);
    if (c.fov !== p.fov) { c.fov = p.fov; c.updateProjectionMatrix(); }
  }
}

// Desenfoque de movimiento real: promedia sub-cuadros dentro del obturador (180° = medio cuadro).
// Dibuja en un <canvas> 2D superpuesto al de WebGL; si la cámara va lenta usa 1 muestra (sin costo extra).
export class MotionBlur {
  constructor(renderer, scene, cam, { obturador = 0.5, max = 10, umbral = 2, fps = 30 } = {}) {
    Object.assign(this, { renderer, scene, cam, obturador, max, umbral, fps });
    const gl = renderer.domElement;
    this.cv = document.createElement('canvas'); this.cv.width = gl.width; this.cv.height = gl.height; this.cv.id = 'glmb';
    this.cv.style.cssText = 'position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;display:none';
    gl.after(this.cv); this.ctx = this.cv.getContext('2d');
  }
  ocultar() { this.cv.style.display = 'none'; }
  // colocar(t) posiciona cámara/objetos en el tiempo t y devuelve la velocidad. Devuelve true (ya renderizó).
  render(T, colocar, fuerza = 1) {
    const v = colocar(T), n = Math.round(clamp((v * fuerza - this.umbral) / 6, 0, 1) * (this.max - 1)) + 1;
    if (n <= 1) { this.renderer.render(this.scene, this.cam); this.cv.style.display = 'none'; return true; }
    const ctx = this.ctx, gl = this.renderer.domElement, dt = this.obturador / this.fps;
    ctx.globalCompositeOperation = 'source-over';
    for (let i = 0; i < n; i++) {
      colocar(T - dt * (i / (n - 1)));
      this.renderer.render(this.scene, this.cam);
      ctx.globalAlpha = 1 / (i + 1);
      if (i === 0) ctx.clearRect(0, 0, this.cv.width, this.cv.height);
      ctx.drawImage(gl, 0, 0);
    }
    ctx.globalAlpha = 1; colocar(T);
    this.cv.style.display = 'block';
    return true;
  }
}

// Colores del tema (las reglas piden var(--acc), nunca colores fijos).
export function colorTema(nombre, fallback = '#9FEF00') {
  return (getComputedStyle(document.documentElement).getPropertyValue(nombre) || fallback).trim() || fallback;
}

// Cartel de texto como capa 3D (plano con textura de canvas, como una capa 3D de AE). Usa las fuentes del tema (SG/JB).
//   lineas: [{t:'texto', c:'--acc'|'--text'|..., peso:700, px:120, fuente:'SG'}]  ·  ancho: unidades del mundo
export function cartel(THREE, lineas, { ancho = 4, caja = true, pad = 60 } = {}) {
  const cv = document.createElement('canvas'), x = cv.getContext('2d');
  const L = lineas.map(l => ({ peso: 700, px: 110, fuente: 'SG', c: '--text', ...l }));
  const medir = l => { x.font = `${l.peso} ${l.px}px ${l.fuente}`; return x.measureText(l.t).width; };
  const W = Math.ceil(Math.max(...L.map(medir)) + pad * 2), H = Math.ceil(L.reduce((a, l) => a + l.px * 1.18, 0) + pad * 2 - L[L.length - 1].px * 0.18);
  cv.width = W; cv.height = H;
  if (caja) {
    x.fillStyle = 'rgba(17,26,40,.92)'; x.strokeStyle = colorTema('--line', '#24344B'); x.lineWidth = 4;
    x.beginPath(); x.roundRect(2, 2, W - 4, H - 4, 28); x.fill(); x.stroke();
  }
  let y = pad;
  x.textBaseline = 'top';
  for (const l of L) { x.font = `${l.peso} ${l.px}px ${l.fuente}`; x.fillStyle = l.c.startsWith('--') ? colorTema(l.c) : l.c; x.fillText(l.t, pad, y); y += l.px * 1.18; }
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(ancho, ancho * H / W), new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, side: THREE.DoubleSide }));
  m.userData.aspecto = H / W;
  return m;
}

// Destello para "zoom through" (atravesar un objeto y cortar): devuelve opacidad 0..1 alrededor de tCorte.
export function destello(T, tCorte, entra = 0.12, sale = 0.25) {
  if (T < tCorte) return clamp((T - (tCorte - entra)) / entra) ** 2;
  return 1 - eo(clamp((T - tCorte) / sale));
}
