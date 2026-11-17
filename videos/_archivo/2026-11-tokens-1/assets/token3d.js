/* Objetos del reel "Qué son los tokens", sobre assets/escena3d.js (estética Scale: placas negras, aristas grises, acento tan solo en lo que se nombra).
   Todo es función del tiempo local (sin azar ni reloj). Unidades: metros. Los objetos miran a +z.
   - ficha({txt, id, back})   un token: placa con su texto (monoespaciada; el espacio se dibuja como "·" gris) y su número (ID) debajo.
                               userData: w, verId(p), acento(p) (0 gris → 1 tan), borde(p) (opacidad del contorno), girar(p) (0 frente → 1 dorso con `back`)
   - fila(fichas, gap)        acomoda fichas en fila centrada; userData.abrir(gap) cambia la separación (gap 0 = el texto entero)
   - marco(w, h)              contorno suelto (la "placa" del mensaje entero) con set(p)
   - cubito(s, acento)        token chiquito para contar (barras de inglés/español)
   - pop / quitar             entradas y salidas por escala */
export function K3(E) {
  const { THREE, P, V, clamp, EASE } = E;
  const hex = (c) => '#' + c.getHexString();
  const K = {}, CW = 0.075, H = 0.17, PAD = 0.025, PPM = 900;   // ancho por carácter, alto, margen, píxeles por metro de textura
  K.CW = CW; K.H = H;
  const tex = (w, h, dibujar) => { const cv = document.createElement('canvas'); cv.width = Math.round(w * PPM); cv.height = Math.round(h * PPM); const x = cv.getContext('2d'); dibujar(x, cv.width, cv.height);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };
  const textoMono = (x, txt, cx, cy, fs, color, gris) => {   // carácter por carácter: el espacio es un punto medio gris (se ve que el espacio es parte del token)
    x.font = `600 ${fs}px "Geist Mono", monospace`; x.textBaseline = 'middle'; x.textAlign = 'center';
    const adv = fs * 0.6, x0 = cx - (txt.length - 1) * adv / 2;
    [...txt].forEach((ch, i) => { x.fillStyle = ch === ' ' ? gris : color; x.fillText(ch === ' ' ? '·' : ch, x0 + i * adv, cy + fs * 0.04); });
  };
  const plano = (w, h, t, z) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false })); m.position.z = z; return m; };
  const mats = (g) => { const out = []; g.traverse((o) => { if (o.isLineSegments2 || (o.material && o.material.isLineMaterial)) out.push(o.material); }); return out; };

  K.ficha = ({ txt = '', id = null, back = null, size = 1, img = null } = {}) => {   // img = { tex, uv: [u0, v0, u1, v1] }: ficha cuadrada con un pedazo de foto
    const g = new THREE.Group(), w = img ? H * size : (txt.length * CW + 2 * PAD) * size, h = H * size, d = 0.04 * size;
    const caja = E.caja(w, h, d, E.std(0)); g.add(caja); E.contornear(g);
    const lineas = mats(g);
    const fs = (CW / 0.6) * size * PPM;
    const frente = (color) => tex(w, h, (x, W, Hh) => textoMono(x, txt, W / 2, Hh / 2, fs, color, hex(P.mid)));
    const tBlanco = frente(hex(P.hi)), tAcc = frente(hex(P.acc));
    const cara = plano(w, h, img ? img.tex : tBlanco, d / 2 + 0.001); g.add(cara);
    if (img) { const [u0, v0, u1, v1] = img.uv, uv = cara.geometry.attributes.uv; uv.setXY(0, u0, v1); uv.setXY(1, u1, v1); uv.setXY(2, u0, v0); uv.setXY(3, u1, v0); uv.needsUpdate = true; }
    let num = null;
    if (id !== null) { const s = String(id), wn = Math.max(w, s.length * 0.05 * size + 0.02);
      const tn = tex(wn, 0.09 * size, (x, W, Hh) => { x.font = `500 ${0.07 * size * PPM}px "Geist Mono", monospace`; x.fillStyle = hex(P.acc); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s, W / 2, Hh / 2 + 2); });
      num = plano(wn, 0.09 * size, tn, 0); num.position.y = -h / 2 - 0.075 * size; num.material.opacity = 0; num.visible = false; g.add(num); }
    let dorso = null;
    if (back !== null) { const L = String(back).split('\n');
      const tb = tex(w, h, (x, W, Hh) => { const f = (L.length > 1 ? 0.042 * size : Math.min(0.07 * size, w * 0.86 / (L[0].length * 0.6))) * PPM; x.font = `600 ${f}px "Geist Mono", monospace`; x.fillStyle = hex(P.acc); x.textAlign = 'center'; x.textBaseline = 'middle'; L.forEach((l, i) => x.fillText(l, W / 2, Hh / 2 + (i - (L.length - 1) / 2) * f * 1.15 + 2)); });
      dorso = plano(w, h, tb, -d / 2 - 0.001); dorso.rotation.x = Math.PI; g.add(dorso); }
    const pivote = new THREE.Group(); pivote.add(g);   // el giro va en `g`; `pivote` es el que se ubica en la escena
    pivote.userData = {
      w, h, txt, id,
      verId: (p) => { if (!num) return; num.material.opacity = clamp(p); num.visible = p > 0.01; num.position.y = -h / 2 - 0.075 * size - 0.03 * (1 - clamp(p)); },
      acento: (p) => { if (!img) cara.material.map = p > 0.5 ? tAcc : tBlanco; lineas.forEach((m) => m.color.copy(P.edge).lerp(P.acc, clamp(p))); },
      borde: (p) => lineas.forEach((m) => { m.opacity = clamp(p); }),
      girar: (p) => { g.rotation.x = Math.PI * EASE.io(clamp(p)); if (num) num.visible = num.visible && p < 0.5; },
    };
    return pivote;
  };
  K.fila = (fichas, gap = 0.06) => {
    const g = new THREE.Group(); fichas.forEach((f) => g.add(f));
    const abrir = (gp) => { const tot = fichas.reduce((s, f) => s + f.userData.w, 0) + gp * (fichas.length - 1); let x = -tot / 2;
      fichas.forEach((f) => { f.position.x = x + f.userData.w / 2; x += f.userData.w + gp; }); return tot; };
    g.userData = { fichas, abrir, ancho: abrir(gap) }; return g;
  };
  K.marco = (w, h, color = P.edge, px = P.px) => {
    const x = w / 2, y = h / 2, c = [[-x, -y], [x, -y], [x, y], [-x, y]].map(([a, b]) => new V(a, b, 0.021));
    const l = E.trazo([c[0], c[1], c[1], c[2], c[2], c[3], c[3], c[0]], color, px);
    l.userData.set = (p) => { l.material.opacity = clamp(p); l.visible = p > 0.01; }; return l;
  };
  K.cubito = (s = 0.042, acento = false) => { const g = new THREE.Group(); g.add(E.caja(s, s, s, E.std(0))); E.contornear(g, acento ? P.acc : P.edge); return g; };
  K.pop = (o, t, t0, d = 0.35, s = 1) => { const q = EASE.out(clamp((t - t0) / d)); o.scale.setScalar(Math.max(0.001, s * q)); o.visible = q > 0.002; return q; };
  K.quitar = (o, t, t0, d = 0.3, s = 1) => { const q = 1 - EASE.in(clamp((t - t0) / d)); o.scale.setScalar(Math.max(0.001, s * q)); o.visible = q > 0.002; return q; };
  return K;
}
