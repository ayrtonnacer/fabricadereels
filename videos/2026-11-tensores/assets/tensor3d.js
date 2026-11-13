/* Objetos del reel "Qué es un tensor", sobre assets/escena3d.js (estilo línea: placas negras, aristas grises; rojo solo para lo que se nombra).
   Todo es función del tiempo local (sin azar ni reloj). Unidades: metros. Los objetos "de pie" miran a +z (hacia la cámara).
   - paisaje(sol)        función de brillo 0..1 de una foto de montañas (suave: no es pixel art); `sol` mueve el sol (cuadros de un video)
   - foto({...})         placa con la foto: `mix(m)` 0 = foto suave, 1 = cuadrícula N×N con el número de cada píxel (la "planilla")
   - celda(txt, ...)     casilla con un número; con `gris` muestra el tono del píxel detrás del número
   - fila(vals, ...)     casillas en fila con `set(p)` (aparecen de a una)
   - capas(...)          foto en color = 3 cuadrículas apiladas (tinte rojo, verde, azul) con `set(p)` que las separa en profundidad
   - onda(ancho, alto)   onda de sonido (línea blanca) que se dibuja con `set(p)`
   - caja(w,h,d,color)   contorno de una caja (el "cubo de números", el modelo) */
export function T3(E) {
  const { THREE, P, V, clamp, EASE } = E;
  const hex = (c) => '#' + c.getHexString();
  const T = {};
  const ss = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  // brillo por zona; con `canal` ('r','g','b') cada canal tiene valores propios (una foto en color real: cielo con más azul, sol con más rojo, monte con más verde)
  const ZONA = { gris: [0.5, 0.28, 0.98, 0.4, 0.22, 0.12], r: [0.42, 0.24, 0.99, 0.36, 0.2, 0.1], g: [0.48, 0.26, 0.93, 0.42, 0.32, 0.16], b: [0.62, 0.24, 0.78, 0.52, 0.2, 0.28] };
  T.paisaje = (sol = 0.3, canal = 'gris') => { const [c0, c1, cs, cm1, cm2, cl] = ZONA[canal]; return (u, v) => {   // v = 0 arriba
    let y = c0 + c1 * v;                                                        // cielo: más claro hacia el horizonte
    const ds = Math.hypot(u - sol, (v - 0.24) * 1.0); y = y + (cs - y) * (1 - ss(0.07, 0.085, ds));   // sol
    const h1 = 0.47 + 0.07 * Math.sin(6.3 * u + 1) + 0.035 * Math.sin(17 * u + 0.4);   // sierra lejana
    y = y + (cm1 - y) * ss(h1 - 0.004, h1 + 0.004, v);
    const h2 = 0.62 + 0.09 * Math.sin(4.1 * u + 2.2) + 0.025 * Math.sin(23 * u);       // sierra cercana
    y = y + (cm2 - y) * ss(h2 - 0.004, h2 + 0.004, v);
    const h3 = 0.84; y = y + (cl + 0.05 * Math.sin(30 * v) * (1 - Math.abs(u - 0.5)) - y) * ss(h3 - 0.003, h3 + 0.003, v);   // lago
    return clamp(y); }; };
  const texSuave = new Map(), texGrilla = new Map();
  T.texSuave = (sol = 0.3, canal = 'gris') => {
    const kk = sol + canal; if (texSuave.has(kk)) return texSuave.get(kk);
    const R = 384, cv = document.createElement('canvas'); cv.width = cv.height = R; const x = cv.getContext('2d'), im = x.createImageData(R, R), f = T.paisaje(sol, canal);
    for (let j = 0; j < R; j++) for (let i = 0; i < R; i++) { const g = Math.round(255 * (0.06 + 0.88 * f((i + 0.5) / R, (j + 0.5) / R))), k = 4 * (j * R + i); im.data[k] = im.data[k + 1] = im.data[k + 2] = g; im.data[k + 3] = 255; }
    x.putImageData(im, 0, 0); const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; texSuave.set(kk, t); return t;
  };
  T.valores = (N = 16, sol = 0.3, canal = 'gris') => { const f = T.paisaje(sol, canal), out = [];   // brillo 0..255 de cada píxel de la cuadrícula N×N (promedio de 4 muestras)
    for (let j = 0; j < N; j++) { const fila = []; for (let i = 0; i < N; i++) { let s = 0; for (const [a, b] of [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]) s += f((i + a) / N, (j + b) / N); fila.push(Math.round(255 * (0.06 + 0.88 * s / 4))); } out.push(fila); }
    return out; };
  T.texGrilla = (N = 16, sol = 0.3, canal = 'gris') => {
    const k = N + ':' + sol + canal; if (texGrilla.has(k)) return texGrilla.get(k);
    const C = 64, cv = document.createElement('canvas'); cv.width = cv.height = N * C; const x = cv.getContext('2d'), val = T.valores(N, sol, canal);
    x.fillStyle = '#0A0D12'; x.fillRect(0, 0, cv.width, cv.height);
    x.font = '600 21px "IBM Plex Mono", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle';
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const g = val[j][i]; x.fillStyle = `rgb(${g},${g},${g})`; x.fillRect(i * C + 2, j * C + 2, C - 4, C - 4); x.fillStyle = g > 140 ? '#0A0D12' : '#FAFAFA'; x.fillText(String(g), i * C + C / 2, j * C + C / 2 + 1); }
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; texGrilla.set(k, t); return t;
  };
  // placa con la foto: suave de lejos, cuadrícula con números de cerca (mix 0..1). tinte = color que multiplica (canales)
  T.foto = ({ S = 0.9, N = 16, sol = 0.3, tinte = null, borde = P.edge, canal = 'gris' } = {}) => {
    const g = new THREE.Group(), placa = E.caja(S + 0.03, S + 0.03, 0.03, E.std(0x1b2840), 0); g.add(placa); E.contornear(g, borde);
    const col = tinte ? new THREE.Color(tinte) : new THREE.Color(1, 1, 1);
    const suave = new THREE.Mesh(new THREE.PlaneGeometry(S, S), new THREE.MeshBasicMaterial({ map: T.texSuave(sol, canal), color: col, toneMapped: false, transparent: true }));
    const grilla = new THREE.Mesh(new THREE.PlaneGeometry(S, S), new THREE.MeshBasicMaterial({ map: T.texGrilla(N, sol, canal), color: col, toneMapped: false, transparent: true }));
    suave.position.z = 0.0165; grilla.position.z = 0.0195; g.add(suave, grilla);
    const mix = (m) => { grilla.material.opacity = m; grilla.visible = m > 0.002; suave.material.opacity = 1; };
    mix(0); g.userData = { mix, S, N, sol, centro: (i, j) => new V((i + 0.5) / N * S - S / 2, S / 2 - (j + 0.5) / N * S, 0.02) }; return g;
  };
  const texNum = new Map();
  const planoNum = (txt, size, color) => {
    const k = txt + color; let m = texNum.get(k);
    if (!m) { const cv = document.createElement('canvas'); cv.width = cv.height = 192; const x = cv.getContext('2d');
      x.font = `700 ${txt.length > 3 ? 62 : 76}px "IBM Plex Mono", monospace`; x.fillStyle = color; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, 96, 100);
      const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4; m = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false }); texNum.set(k, m); }
    return new THREE.Mesh(new THREE.PlaneGeometry(size, size), m);
  };
  T.celda = (txt, size = 0.14, borde = P.edge, gris = null) => {
    const g = new THREE.Group(), b = E.caja(size, size, 0.035, E.std(0x1b2840), 0); g.add(b); E.contornear(g, borde);
    let color = hex(P.hi);
    if (gris !== null) { const f = new THREE.Mesh(new THREE.PlaneGeometry(size * 0.9, size * 0.9), new THREE.MeshBasicMaterial({ color: new THREE.Color(gris, gris, gris), toneMapped: false })); f.position.z = 0.018; g.add(f); color = gris > 0.55 ? '#0A0D12' : hex(P.hi); }
    const n = planoNum(String(txt), size * 0.92, color); n.position.z = 0.0205; g.add(n); return g;
  };
  T.fila = (vals, size = 0.1, pitch = 0.11, opts = {}) => {
    const g = new THREE.Group(), cel = vals.map((v, j) => { const c = T.celda(v, size, opts.borde || P.edge, opts.gris ? opts.gris[j] : null); c.position.x = (j - (vals.length - 1) / 2) * pitch; g.add(c); return c; });
    const N = cel.length; g.userData.celdas = cel;
    g.userData.set = (p) => cel.forEach((c, k) => { const q = clamp((p * (N + 2) - k) / 2); c.visible = q > 0; c.scale.setScalar(Math.max(0.001, EASE.out(q))); });
    g.userData.set(0); return g;
  };
  T.capas = ({ S = 0.6, N = 16, sol = 0.3, sep = 0.2 } = {}) => {   // foto en color: 3 cuadrículas (R, G, B) que se separan en profundidad
    const g = new THREE.Group(), tintes = [0xff8080, 0x80ff9a, 0x80a8ff];
    const fs = tintes.map((t, i) => { const f = T.foto({ S, N, sol, tinte: t, canal: 'rgb'[i] }); f.userData.mix(1); g.add(f); return f; });
    g.userData = { fotos: fs, sep, S, set: (p) => fs.forEach((f, i) => { f.position.z = -i * sep * EASE.io(clamp(p)); }) };
    g.userData.set(1); return g;
  };
  T.copiar = (o) => { const ud = o.userData; o.userData = {}; const c = o.clone(true); o.userData = ud; return c; };   // clone() serializa userData: se esquiva
  T.caja = (w, h, d, color = P.acc, px = 3) => {   // contorno de una caja centrada en el origen; set(p) la dibuja
    const x = w / 2, y = h / 2, z = d / 2, c = [[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]].map((a) => new V(...a));
    const A = [0, 1, 1, 2, 2, 3, 3, 0, 4, 5, 5, 6, 6, 7, 7, 4, 0, 4, 1, 5, 2, 6, 3, 7], pts = A.map((i) => c[i]);
    const l = E.trazo(pts, color, px); l.userData.set = (p) => { l.visible = p > 0.01; l.material.opacity = clamp(p); }; l.userData.set(0); return l;
  };
  T.onda = (ancho = 0.9, alto = 0.18, n = 160) => {   // onda de sonido determinística (suma de senos con envolvente)
    const pts = [], q = (i) => { const u = i / n, env = 0.35 + 0.65 * Math.sin(Math.PI * u) ** 0.6; return new V((u - 0.5) * ancho, alto * env * (0.6 * Math.sin(2 * Math.PI * 9 * u) + 0.3 * Math.sin(2 * Math.PI * 23 * u + 1) + 0.15 * Math.sin(2 * Math.PI * 51 * u + 2)), 0); };
    for (let i = 0; i < n; i++) pts.push(q(i), q(i + 1));
    const l = E.trazo(pts, P.hi, 3); const tot = pts.length;
    l.userData.set = (p) => { l.visible = p > 0.005; l.geometry.instanceCount = Math.max(1, Math.floor(clamp(p) * tot / 2)); };
    l.userData.set(1); return l;
  };
  return T;
}
