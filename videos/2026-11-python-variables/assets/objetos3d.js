/* Objetos 3D del reel de variables (tema noir): piezas con volumen, no tarjetas. Referencias: docs/4-referencias/material/2026-11-17-refs-instagram-dinamismo/.
   La MEMORIA es un lugar (una torre de losas de vidrio); un VALOR es un objeto (orbe de cristal con su dato adentro, tira de metal, bandeja de cubos);
   un NOMBRE es un anillo de luz que se cierra alrededor del valor. El cajón vacío es lo que una variable NO es. Todo es función del tiempo (sin azar). */
export const O3D = (E) => {
  const { THREE, V, P } = E;
  const PI = Math.PI;
  const mk = (c, o = 1, add = false) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, toneMapped: false, depthWrite: false, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending });
  // texto con fondo transparente (se redibuja solo si cambia)
  const txt = (w, h) => { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const x = cv.getContext('2d'), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4; let last = '';
    return { tex, set(s, color = hex(P.hi), size = h * 0.62) { const k = s + color; if (k === last) return; last = k; x.clearRect(0, 0, w, h); x.font = `700 ${size}px "Geist Mono", monospace`; x.fillStyle = color; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s, w / 2, h / 2 + size * 0.04); tex.needsUpdate = true; } }; };
  const hex = (c) => '#' + c.getHexString();
  const circ = (r, n = 56, eje = 'y') => { const pr = []; for (let i = 0; i < n; i++) { const a = (i / n) * 2 * PI, b = ((i + 1) / n) * 2 * PI, f = (t) => eje === 'y' ? new V(r * Math.cos(t), 0, r * Math.sin(t)) : eje === 'x' ? new V(0, r * Math.cos(t), r * Math.sin(t)) : new V(r * Math.cos(t), r * Math.sin(t), 0); pr.push(f(a), f(b)); } return pr; };
  const bordes = (m, c = P.edge, px = 1, ang = 30) => { const e = new THREE.EdgesGeometry(m.geometry, ang).attributes.position.array, pr = []; for (let i = 0; i < e.length; i += 3) pr.push(new V(e[i], e[i + 1], e[i + 2])); const l = E.trazo(pr, c, px); m.add(l); return l; };
  const metal = () => new THREE.MeshStandardMaterial({ color: 0x151515, roughness: 0.32, metalness: 0.85 });

  // ORBE: esfera de cristal oscuro con contraluz, meridianos finos y el dato adentro. userData: num(str, acento), fade(k), acento(k)
  const orbe = (r = 0.3, t = '19', dim = false) => {
    const g = new THREE.Group(), base = dim ? 0.38 : 0.62;
    const shell = new THREE.Mesh(new THREE.SphereGeometry(r, 28, 20), new THREE.MeshStandardMaterial({ color: 0x161616, metalness: 0.95, roughness: 0.14, transparent: true, opacity: base, depthWrite: false })); shell.renderOrder = 1; g.add(shell);
    const l1 = E.trazo(circ(r * 1.003, 56, 'y'), P.edge, 1), l2 = E.trazo(circ(r * 1.003, 56, 'x'), P.edge, 1); l1.material.opacity = l2.material.opacity = dim ? 0.3 : 0.7; g.add(l1, l2);
    const tx = txt(256, 128); tx.set(t); const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx.tex, transparent: true, depthWrite: false, toneMapped: false, opacity: dim ? 0.55 : 1 })); sp.scale.set(r * 2.0, r, 1); sp.renderOrder = 2; g.add(sp);
    const glow = E.brillo(P.hi, r * 3.6, dim ? 0 : 0.2); glow.renderOrder = 0; g.add(glow);
    let ac = 0, cur = t;
    const pintar = () => { tx.set(cur, ac > 0.5 ? hex(P.acc) : hex(P.hi)); };
    g.userData = { r, num(s) { cur = s; pintar(); }, acento(k) { ac = k; pintar(); glow.material.color.copy(P.hi).lerp(P.acc, k); glow.material.opacity = (dim ? 0 : 0.2) + 0.25 * k; },
      fade(k) { shell.material.opacity = base * k; sp.material.opacity = (dim ? 0.55 : 1) * k; l1.material.opacity = l2.material.opacity = (dim ? 0.3 : 0.7) * k; glow.visible = k > 0.4; } };
    return g;
  };

  // ANILLO: la etiqueta (el nombre). Una banda de luz que se cierra alrededor del valor. userData: acento(k)
  const anillo = (r = 0.45, inc = 0.22) => {
    const g = new THREE.Group(), q = new THREE.Group(); q.rotation.x = PI / 2; g.add(q); g.rotation.set(0.5, 0, inc);
    const nucleo = new THREE.Mesh(new THREE.TorusGeometry(r, 0.012, 8, 72), E.basic(P.hi)), halo = new THREE.Mesh(new THREE.TorusGeometry(r, 0.038, 8, 48), mk(P.hi, 0.16, true)); q.add(nucleo, halo);
    const ptos = [0, 2.1, 4.2].map((a) => { const b = E.brillo(P.hi, 0.12, 0.9); b.position.set(r * Math.cos(a), r * Math.sin(a), 0); q.add(b); return b; });
    g.userData = { acento(k) { nucleo.material.color.copy(P.hi).lerp(P.acc, k); halo.material.color.copy(P.hi).lerp(P.acc, k); ptos.forEach((b) => b.material.color.copy(P.hi).lerp(P.acc, k)); } };
    return g;
  };

  // CAJÓN: caja de metal abierta y VACÍA (lo que una variable no es)
  const cajon = () => {
    const g = new THREE.Group(), W = 0.78, H = 0.5, D = 0.62, t = 0.022, M = metal(), parte = (w, h, d, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M); m.position.set(x, y, z); g.add(m); bordes(m); return m; };
    parte(W, t, D, 0, t / 2, 0); parte(W, H, t, 0, H / 2, -D / 2); parte(W, H, t, 0, H / 2, D / 2); parte(t, H, D, -W / 2, H / 2, 0); parte(t, H, D, W / 2, H / 2, 0);
    const tapa = new THREE.Group(); tapa.position.set(0, H, -D / 2); tapa.rotation.x = -2.05; g.add(tapa); const lid = new THREE.Mesh(new THREE.BoxGeometry(W, t, D), M); lid.position.z = D / 2; tapa.add(lid); bordes(lid);
    return g;
  };

  // TORRE: la memoria. Losas de vidrio apiladas entre cuatro columnas de luz, con otros valores tenues (la memoria está llena de datos). Altura 3,3 m.
  const torre = () => {
    const g = new THREE.Group(), L = 1.3, ys = [0.1, 0.75, 1.4, 2.05, 2.7], M = new THREE.MeshStandardMaterial({ color: 0x0b0b0b, roughness: 0.9, metalness: 0.15 });   // losas mates: el metal pulido quemaba el blanco
    ys.forEach((y) => { const s = new THREE.Mesh(new THREE.BoxGeometry(L, 0.03, L), M); s.position.y = y; g.add(s); bordes(s);
      g.add(E.trazo([new V(-L / 2, y + 0.016, 0), new V(L / 2, y + 0.016, 0), new V(0, y + 0.016, -L / 2), new V(0, y + 0.016, L / 2)], P.mid, 1).translateY(0)); });
    const col = []; for (const x of [-1, 1]) for (const z of [-1, 1]) col.push(new V(x * L / 2, 0.1, z * L / 2), new V(x * L / 2, 3.15, z * L / 2)); g.add(E.trazo(col, P.edge, 1.4));
    const extra = [[0, -0.47, -0.47, '7'], [1, 0.47, 0.47, '"a"'], [3, -0.47, 0.47, '3,5'], [4, 0.47, -0.47, '0'], [2, -0.47, 0.47, '42']];
    for (const [i, x, z, s] of extra) { const o = orbe(0.11, s, true); o.position.set(x, ys[i] + 0.015 + 0.11, z); g.add(o); }
    g.userData = { y: (i) => ys[i] + 0.015 + 0.3 };
    return g;
  };

  // TIRA de metal con letras en relieve (un texto) · BANDEJA con dos cubos (una lista)
  const tira = (s = '"hola"') => { const g = new THREE.Group(), b = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.26, 0.1), metal()); g.add(b); bordes(b);
    const tx = txt(512, 128); tx.set(s, hex(P.hi), 86); const f = new THREE.Mesh(new THREE.PlaneGeometry(0.64, 0.16), new THREE.MeshBasicMaterial({ map: tx.tex, transparent: true, toneMapped: false, depthWrite: false })); f.position.z = 0.052; g.add(f); return g; };
  const lista = () => { const g = new THREE.Group(), M = metal(), bar = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.03, 0.14), M); bar.position.y = -0.165; g.add(bar); bordes(bar);
    [['1', -0.19], ['2', 0.19]].forEach(([n, x]) => { const c = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.26, 0.26), M); c.position.set(x, 0, 0); g.add(c); bordes(c);
      const tx = txt(128, 128); tx.set(n, hex(P.hi), 90); const f = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 0.2), new THREE.MeshBasicMaterial({ map: tx.tex, transparent: true, toneMapped: false, depthWrite: false })); f.position.set(x, 0, 0.132); g.add(f); });
    return g; };

  // marca en el piso bajo un objeto que flota (ancla visual): círculo fino + punto de luz
  const marca = (r = 0.38) => { const g = new THREE.Group(); g.add(E.trazo(circ(r, 40), P.edge, 1)); const b = E.brillo(P.hi, 0.18, 0.7); b.position.y = 0.01; g.add(b); g.position.y = 0.004; return g; };
  return { orbe, anillo, cajon, torre, tira, lista, marca };
};
