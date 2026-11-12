/* Objetos del reel de tensores, sobre assets/escena3d.js (estilo línea: placas negras con aristas grises; el acento rojo solo para lo que se nombra).
   Todo es función del tiempo local (sin azar ni reloj). Unidades: metros. Los objetos "de pie" miran a +z (hacia la cámara).
   - celda(txt)        casilla con un número (escalar = 1 celda; vector = fila; matriz = grilla)
   - bloque(vals)      grilla de celdas con `set(p)` (aparecen de a una)
   - foto()            placa de píxeles 8×8 (la "cara"): `mix(m)` 0 = brillo, 1 = números
   - pila(foto, n)     n capas de una foto una detrás de otra (canales) con `set(p)`
   - eje(A, B)         línea gruesa blanca que crece de A a B (`set(p)`) */
export function T3(E) {
  const { THREE, P, V, clamp, EASE } = E;
  const hex = (c) => '#' + c.getHexString();
  const texNum = new Map();
  const planoNum = (txt, size, color) => {
    const k = txt + color; let m = texNum.get(k);
    if (!m) {
      const cv = document.createElement('canvas'); cv.width = cv.height = 192; const x = cv.getContext('2d');
      x.font = '700 76px "IBM Plex Mono", monospace'; x.fillStyle = color; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, 96, 100);
      const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
      m = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false }); texNum.set(k, m);
    }
    return new THREE.Mesh(new THREE.PlaneGeometry(size, size), m);
  };
  const T = {};
  T.celda = (txt, size = 0.14, borde = P.edge, color = hex(P.hi)) => {
    const g = new THREE.Group(), b = E.caja(size, size, 0.035, E.std(0x1b2840), 0); g.add(b); E.contornear(g, borde);
    const n = planoNum(txt, size * 0.92, color); n.position.z = 0.0195; g.add(n); return g;
  };
  T.bloque = (vals, size = 0.14, pitch = 0.16, borde = P.edge) => {
    const g = new THREE.Group(), R = vals.length, C = vals[0].length, cel = [];
    vals.forEach((fila, i) => fila.forEach((v, j) => { const c = T.celda(String(v), size, borde); c.position.set((j - (C - 1) / 2) * pitch, ((R - 1) / 2 - i) * pitch, 0); g.add(c); cel.push(c); }));
    const N = cel.length;
    g.userData.set = (p) => cel.forEach((c, k) => { const q = clamp((p * (N + 2) - k) / 2); c.visible = q > 0; c.scale.setScalar(Math.max(0.001, EASE.out(q))); });
    g.userData.set(0); g.userData.ancho = (C - 1) * pitch + size; g.userData.alto = (R - 1) * pitch + size; return g;
  };
  // placa de píxeles 8×8: el brillo es el dato (1..9); con mix(1) se ven los números
  const CARA = ['11111111', '19911991', '19911991', '11111111', '19111191', '11911911', '11199111', '11111111'];
  T.foto = (n = 8, cell = 0.1, datos = CARA) => {
    const g = new THREE.Group(), S = n * cell, cv = document.createElement('canvas'); cv.width = cv.height = n * 64; const x = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const placa = E.caja(S + 0.03, S + 0.03, 0.03, E.std(0x1b2840), 0); g.add(placa); E.contornear(g, P.edge);
    const cara = new THREE.Mesh(new THREE.PlaneGeometry(S, S), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); cara.position.z = 0.0165; g.add(cara);
    const bg = new THREE.Color(css('--plate', '#0A0D12')), ink = P.hi; let last = -1;
    const dibujar = (m) => {
      const k = Math.round(m * 24); if (k === last) return; last = k; m = k / 24;
      x.fillStyle = '#0A0D12'; x.fillRect(0, 0, cv.width, cv.height);
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
        const v = +datos[i][j] / 9, c = bg.clone().lerp(ink, 0.08 + 0.92 * v);
        x.globalAlpha = 1 - m; x.fillStyle = hex(c); x.fillRect(j * 64 + 3, i * 64 + 3, 58, 58);
        x.globalAlpha = m; x.fillStyle = v > 0.5 ? hex(P.acc) : '#71717a'; x.font = '700 40px "IBM Plex Mono", monospace'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(datos[i][j], j * 64 + 32, i * 64 + 36);
      }
      x.globalAlpha = 1; tex.needsUpdate = true;
    };
    dibujar(0); g.userData = { mix: dibujar, tam: S + 0.03 }; return g;
  };
  T.pila = (n = 3, sep = 0.14, tam = 8, cell = 0.1) => {   // n fotos una detrás de otra (el eje "canales")
    const g = new THREE.Group(), fs = [];
    for (let i = 0; i < n; i++) { const f = T.foto(tam, cell); f.position.z = -i * sep; g.add(f); fs.push(f); }
    g.userData = { fotos: fs, sep, set: (p) => fs.forEach((f, i) => { const q = EASE.out(clamp(p * 1.4 - i * 0.25)); f.visible = i === 0 || q > 0; f.position.z = -i * sep * q; }) };
    g.userData.set(1); return g;
  };
  T.copiar = (o) => { const ud = o.userData; o.userData = {}; const c = o.clone(true); o.userData = ud; return c; };   // clone() serializa userData (funciones y objetos): se esquiva
  T.eje = (A, B, color = P.hi, w = 3.2) => {
    const l = E.trazo([A, B], color, w); l.scale.set(0.001, 0.001, 0.001); E.scene.add(l);
    const d = new V().subVectors(B, A);
    l.userData.set = (p) => { l.visible = p > 0.001; l.scale.setScalar(Math.max(0.001, p)); l.position.copy(A).addScaledVector(d, 0); l.position.set(A.x * (1 - Math.max(0.001, p)), A.y * (1 - Math.max(0.001, p)), A.z * (1 - Math.max(0.001, p))); };
    l.userData.set(0); return l;
  };
  return T;
}
function css(v, d) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim() || d; }
