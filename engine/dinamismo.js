// Piezas de dinamismo (docs/DINAMISMO.md). Todas son funciones puras del tiempo local `lt` de la escena (determinísticas).
import { clamp, eo, eio, eb } from './lib.js';
export const ramp = (lt, a, d) => clamp((lt - a) / d);

// Palabra gigante o "sello" con desenfoque de movimiento. Devuelve intensidad 0..1 (para desenfocar/oscurecer el fondo).
//   el: elemento (position:absolute; left:50%; top:Ypx). kind: 'big' (escala 1.35→1 + blur) | 'sello' (entra deslizando, rotado)
export function golpe(el, lt, t0, dur, kind = 'big') {
  const p = lt - t0;
  if (p < 0 || p > dur) { el.style.display = 'none'; return 0; }
  el.style.display = 'block';
  const e = eo(clamp(p / 0.22)), out = clamp((dur - p) / 0.16), vis = Math.min(1, e * 1.3) * out;
  if (kind === 'sello') {
    el.style.transform = `translate(-50%,-50%) translateX(${(1 - e) * -900 + (1 - out) * 900}px) rotate(-7deg)`;
    el.style.filter = `blur(${(1 - e) * 10}px)`;
  } else {
    el.style.transform = `translate(-50%,-50%) scale(${1.35 - 0.35 * e + 0.03 * (p / dur)})`;
    el.style.filter = `blur(${(1 - e) * 28}px)`;
  }
  el.style.opacity = vis;
  return vis;
}
// Fondo que se desenfoca y oscurece mientras hay palabra gigante.
export function atenuar(sceneEl, g) { sceneEl.style.filter = g > 0.01 ? `blur(${9 * g}px) brightness(${1 - 0.6 * g})` : 'none'; }

// Recuadro o subrayado que se "dibuja" de izquierda a derecha. el: elemento con borde (position:absolute).
export function resalte(el, lt, t0, d = 0.35, hasta = 1e9) {
  const p = eo(clamp((lt - t0) / d));
  el.style.opacity = lt >= t0 && lt < hasta ? 1 : 0;
  el.style.clipPath = `inset(0 ${(1 - p) * 100}% 0 0)`;
}

// Zoom lento (Ken Burns) del contenedor de la escena. a→b a lo largo de d segundos.
export function kenburns(el, lt, d, a = 1.0, b = 1.05, ox = '50%', oy = '50%') {
  el.style.transformOrigin = `${ox} ${oy}`;
  el.style.transform = `scale(${a + (b - a) * eio(clamp(lt / d))})`;
}

// Cursor de mouse con trayectoria. path = [[t, destino, click]] ; destino = [x,y] o "selector CSS" (centro del elemento).
// cur: <svg> flecha (position:absolute; left:0; top:0). rip: círculo de clic. Devuelve true si hubo un clic en este cuadro.
const last = { x: 540, y: 1700 };
function resolve(d) {
  if (Array.isArray(d)) return { x: d[0], y: d[1] };
  const el = document.querySelector(d); if (!el) return null;
  const r = el.getBoundingClientRect(); if (!r.width && !r.height) return null;
  return { x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 };
}
export function cursor(cur, rip, path, lt) {
  if (!path || !path.length || lt < path[0][0] - 0.3 || lt > path[path.length - 1][0] + 0.7) { cur.style.display = 'none'; rip.style.display = 'none'; return; }
  const pts = path.map(p => ({ t: p[0], c: p[2], ...(resolve(p[1]) || last) }));
  let a = pts[0], b = pts[0];
  for (let i = 0; i < pts.length; i++) { if (lt >= pts[i].t) { a = pts[i]; b = pts[Math.min(i + 1, pts.length - 1)]; } }
  const k = b === a ? 1 : eio(clamp((lt - a.t) / (b.t - a.t)));
  const x = a.x + (b.x - a.x) * k, y = a.y + (b.y - a.y) * k;
  const vis = clamp((lt - (path[0][0] - 0.3)) / 0.3) * clamp((path[path.length - 1][0] + 0.7 - lt) / 0.3);
  // presiona: breve achicamiento alrededor de cada clic
  let press = 1, ring = -1;
  for (const p of pts) if (p.c) { const dt = lt - p.t; if (dt > -0.06 && dt < 0.12) press = 0.82; if (dt >= 0 && dt < 0.5) ring = dt / 0.5; }
  cur.style.display = 'block'; cur.style.opacity = vis; cur.style.transform = `translate(${x}px,${y}px) scale(${press})`;
  if (ring >= 0) { rip.style.display = 'block'; rip.style.opacity = (1 - ring) * 0.9; rip.style.transform = `translate(${x - 45}px,${y - 45}px) scale(${0.3 + ring * 1.2})`; }
  else rip.style.display = 'none';
  last.x = x; last.y = y;
}

// Pop de elemento con rebote en el instante t0 (opacidad + escala). Para badges, íconos, chips.
export function pop(el, lt, t0, d = 0.4) {
  const p = clamp((lt - t0) / d), e = eb(p);
  el.style.opacity = clamp(p * 2.5); el.style.transform = `scale(${0.6 + 0.4 * e})`;
}
// Entrada deslizando desde un lado.
export function slide(el, lt, t0, d = 0.5, dx = 0, dy = 60) {
  const p = eo(clamp((lt - t0) / d));
  el.style.opacity = p; el.style.transform = `translate(${(1 - p) * dx}px,${(1 - p) * dy}px)`;
}
// Línea/flecha que se dibuja (SVG path con pathLength=1).
export function dibujar(path, lt, t0, d = 0.5) { const p = eo(clamp((lt - t0) / d)); path.style.strokeDasharray = 1; path.style.strokeDashoffset = 1 - p; path.style.opacity = p > 0 ? 1 : 0; }
