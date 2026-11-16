/* LA FÁBRICA DE TOKENS (v2 del reel de tokens, parte 1): UN solo set 3D — una línea de montaje que se aleja en el eje z con 5 estaciones —
   y UNA cámara continua que la recorre. Cada composición (gancho, corte, comparten, mayus, idioma, foto, payoff) monta el mismo set y lo
   dibuja en el TIEMPO GLOBAL del video (T = inicio de la escena + t local): así los cortes entre composiciones no se ven (plano continuo).
   Todo es función de T (sin reloj ni azar). Rótulos HTML anclados a puntos 3D (se mueven con la cámara: paralaje real).
   Sin cinta ni línea de montaje (Ayrton: estorbaba el texto). Estaciones en diagonal hacia la izquierda y al fondo (media kit, "ley del vector": todos los viajes en la MISMA dirección, la corriente = izquierda): A (0, 0) · B (−1.8, −3.5) · C (−3.6, −7) · D (−5.4, −10.5) · E (−7.2, −14).
   Tiempos: salen de audio/palabras.json (voz) — escena + tiempo de la palabra. */
export async function montar(root, tl, T0, dur) {
  const [M, Km, Tm] = await Promise.all([import('./escena3d.js'), import('./token3d.js'), import('./tensor3d.js')]);
  const E = await M.crear(root), K = Km.K3(E), Tn = Tm.T3(E), { THREE, V, P, clamp, EASE } = E;
  const hud = root.querySelector('.hud');
  const st = (a, b, x) => clamp((x - a) / Math.max(1e-6, b - a));
  const io = (a, b, x) => EASE.io(st(a, b, x)), out = (a, b, x) => EASE.out(st(a, b, x));
  const ventana = (T, a, b, f = 0.25) => out(a, a + f, T) * (1 - st(b, b + f, T));   // aparece en a, se va en b
  const S = { A: new V(0, 0, 0), B: new V(-1.8, 0, -3.5), C: new V(-3.6, 0, -7), D: new V(-5.4, 0, -10.5), E: new V(-7.2, 0, -14) };
  const en = (s, x, y, z = 0) => new V(S[s].x + x, y, S[s].z + z);
  const add = (o, s, x, y, z = 0) => { o.position.copy(en(s, x, y, z)); E.scene.add(o); return o; };
  const todas = [];   // fichas que giran en el payoff (en orden de la línea)

  // ---------- rótulos HTML ----------
  const R = [];
  const rotulo = (html, cls, css = '') => { const a = document.createElement('div'); a.className = 'ancla'; const d = document.createElement('div'); d.className = cls; d.innerHTML = html; d.style.cssText = css; a.appendChild(d); hud.appendChild(a); return { a, d }; };
  const anclado = (html, cls, p, a0, a1, css = '', dy = 0) => R.push({ ...rotulo(html, cls, css), p, a0, a1, dy });
  const fijo = (html, cls, top, a0, a1, css = '') => { const r = rotulo(html, cls, css); r.a.style.top = top + 'px'; R.push({ ...r, a0, a1, fijo: true }); return r; };

  // ---------- A: el mensaje y la cuchilla ----------
  const TOK = [['hola', 122845], [',', 11], [' ¿', 12873], ['qué', 23535], [' tal', 4858], ['?', 30]];
  const fA = TOK.map(([txt, id]) => K.ficha({ txt, id, back: String(id) })), filaA = add(K.fila(fA, 0), 'A', 0, 0.6);
  const anchoA = filaA.userData.ancho, marcoA = add(K.marco(anchoA + 0.06, K.H + 0.06), 'A', 0, 0.6);
  const hoja = add(E.trazo([new V(0, -0.16, 0.05), new V(0, 0.16, 0.05)], P.acc, 4), 'A', 0, 0.6);
  const bordesA = []; { let x = -anchoA / 2; fA.forEach((f) => { x += f.userData.w; bordesA.push(x); }); bordesA.pop(); }
  todas.push(...fA);
  // hook según el media kit (docs/media-kit): firma 60 px en tan arriba a la izquierda (y 262), título de 3–5 palabras, 140 px, alineado a la izquierda desde y 350, una sola palabra en tan
  const tit = fijo('La IA lee <span class="acc">números</span>', 'titular', 350, -1, 3.7, 'width: 900px; font-size: 140px; line-height: .98; letter-spacing: -.03em; text-align: left; text-wrap: balance; white-space: normal;');
  const firma = fijo('@ayrtonnacer', 'firma', 262, -1, 3.7, 'font-size: 60px;');
  for (const r of [tit, firma]) { r.a.style.left = '90px'; r.a.style.transform = 'none'; r.a.style.whiteSpace = 'normal'; }
  const ids = fijo(TOK.map(([, id], i) => `<span class="n">${id}${i < 5 ? ',' : ']'}</span>`).join(' ').replace('<span class="n">', '<span class="n">['), 'mono', 960, 2.7, 3.8, 'font: 500 40px var(--mono); color: var(--acc); letter-spacing: -.02em;');
  const idsN = ids.d.querySelectorAll('.n');
  anclado('6 <b>tokens</b>', 'rot', en('A', 0, 0.98), 6.9, 10.2);

  // ---------- B: palabras comunes enteras, raras partidas; "idez" comparte número ----------
  const seg = add(K.ficha({ txt: ' seguridad', id: 28287, back: '28287' }), 'B', 0, 1.02);
  const par = (a, b, y) => { const fs = [K.ficha({ txt: a[0], id: a[1], back: String(a[1]) }), K.ficha({ txt: b[0], id: b[1], back: String(b[1]) })], f = add(K.fila(fs, 0), 'B', 0, y);
    const mc = add(K.marco(f.userData.ancho + 0.05, K.H + 0.05), 'B', 0, y); return { f, fs, mc }; };
  const pa = par([' nit', 27054], ['idez', 36753], 0.62), pb = par([' luc', 34623], ['idez', 36753], 0.24);
  todas.push(seg, ...pa.fs, ...pb.fs);
  const xr = pa.fs[1].position.x + pa.fs[1].userData.w / 2 + 0.06;
  const lazo = add(E.trazo([new V(xr, 0.62, 0.03), new V(xr + 0.07, 0.62, 0.03), new V(xr + 0.07, 0.62, 0.03), new V(xr + 0.07, 0.24, 0.03), new V(xr + 0.07, 0.24, 0.03), new V(xr, 0.24, 0.03)], P.acc, 3), 'B', 0, 0);
  anclado('tokenizador de GPT-4o', 'mono', en('B', 0, 1.3), 11.3, 18.3, 'font: 500 40px var(--mono); color: var(--muted);');

  // ---------- C: mayúscula y espacio cambian el número ----------
  const DC = [['hola', 122845, 19.6], ['Hola', 157464, 20.15], [' hola', 171847, 20.85]];
  const fC = DC.map(([txt, id], i) => add(K.ficha({ txt, id, back: String(id), size: 1.35 }), 'C', 0, 1.14 - i * 0.4));
  todas.push(...fC);

  // ---------- D: el mismo texto en inglés (36) y en español (48) ----------
  const CS = 0.03, PI_ = 0.037, X0 = -0.44;
  const barra = (n, y, extra) => Array.from({ length: n }, (_, k) => { const col = Math.floor(k / 2), fil = k % 2; return add(K.cubito(CS, col >= extra), 'D', X0 + col * PI_, y - fil * PI_); });
  const en36 = barra(36, 0.95, 99), es48 = barra(48, 0.55, 18);
  anclado('inglés <b>36</b>', 'rot mono', en('D', X0, 1.04), 25.35, 29.9, '', 'izq');
  anclado('español <b>48</b>', 'rot mono', en('D', X0, 0.64), 25.9, 29.9, '', 'izq');
  anclado('+33 %', '', en('D', X0 + 20.5 * PI_, 0.62), 27.65, 29.9, 'font: 700 64px var(--sans); color: var(--acc);', 'arriba');

  // ---------- E: la foto se divide en cuadraditos de 16×16 píxeles ----------
  const SF = 0.9, NF = 14, c = SF / NF, YF = 0.85, foto = add(Tn.foto({ S: SF }), 'E', 0, YF);
  { const pts = []; for (let k = 1; k < NF; k++) { const u = -SF / 2 + k * c; pts.push(new V(u, -SF / 2, 0.022), new V(u, SF / 2, 0.022), new V(-SF / 2, u, 0.022), new V(SF / 2, u, 0.022)); }
    var grilla = add(E.trazo(pts, P.hi, 1.4), 'E', 0, YF); }
  const J = 7, I0 = 6, tex = Tn.texSuave(0.3, 'gris'), yJ = YF + SF / 2 - (J + 0.5) * c, gapF = 0.022, anchoF = NF * c + (NF - 1) * gapF;
  const VEC = (i) => [((i * 37) % 100 - 50) / 100, ((i * 61 + 20) % 100 - 50) / 100, ((i * 83 + 45) % 100 - 50) / 100].map((v) => v.toFixed(2)).join('\n');
  const parches = Array.from({ length: NF }, (_, i) => add(K.ficha({ img: { tex, uv: [i / NF, 1 - (J + 1) / NF, (i + 1) / NF, 1 - J / NF] }, back: VEC(i), size: c / K.H }), 'E', 0, 0));
  todas.push(...parches);
  const pc = en('E', -SF / 2 + (I0 + 0.5) * c, yJ), marca = add(K.marco(c, c, P.acc, 5), 'E', pc.x - S.E.x, pc.y, 0.01);
  anclado('<b>16 × 16</b> píxeles', 'rot', new V(pc.x, pc.y + c * 0.9, 0 + S.E.z), 33.8, 35.5);
  anclado('224 × 224 = <b>196 tokens</b>', 'rot', en('E', 0, 1.42), 36.4, 38.6);

  // ---------- cámara: estación por estación, sin cortes ----------
  const K_ = (T, s, p, l, e) => ({ t: T, p: [S[s].x + p[0], p[1], S[s].z + p[2]], l: [S[s].x + l[0], l[1], S[s].z + l[2]], e });
  // Vocabulario (docs/CINE.md): plano general / medio / detalle · travelling (la cámara viaja) · dolly in/out (se acerca/aleja) · grúa (sube/baja)
  // picado (desde arriba, mirando hacia abajo) · contrapicado (desde abajo, mirando hacia arriba) · paneo (gira sobre sí misma)
  const CAM = [
    K_(0, 'A', [0.35, 0.95, 4.6], [0, 0.5, 0]), K_(3.5, 'A', [0.2, 0.9, 4.3], [0, 0.5, 0], 'lin'), K_(4.1, 'A', [0, 0.78, 4.3], [0, 0.58, 0], 'in'),   // gancho: plano medio frontal, dolly in lento
    K_(4.7, 'A', [0, 0.74, 4.0], [0, 0.58, 0], 'out'), K_(6.1, 'A', [0, 0.74, 3.95], [0, 0.58, 0], 'lin'), K_(6.9, 'A', [0.5, 1.15, 5.5], [0, 0.5, 0], 'io'), K_(10.3, 'A', [0.4, 1.12, 5.4], [0, 0.5, 0], 'lin'),   // dolly out + leve picado
    { t: 10.65, p: [-1.2, 2.6, 2.2], l: [-1.6, 0.9, -2.6], e: 'in' },                                                            // grúa por encima de A…
    K_(11.05, 'B', [0.15, 0.42, 2.6], [0, 1.0, 0], 'out'), K_(13.0, 'B', [0.1, 0.5, 2.55], [0, 1.0, 0], 'lin'),                // …y baja a un CONTRAPICADO de "seguridad"
    K_(13.6, 'B', [0.35, 0.95, 4.7], [0, 0.62, 0], 'io'), K_(18.6, 'B', [0.25, 0.93, 4.6], [0, 0.62, 0], 'lin'),               // dolly out a plano general de las 3 palabras
    K_(19.4, 'C', [-0.5, 2.2, 3.4], [0, 0.6, 0], 'io'), K_(24.0, 'C', [-0.35, 1.6, 3.7], [0, 0.6, 0], 'lin'),                  // travelling a C: PICADO que baja lento
    K_(24.8, 'D', [1.1, 0.35, 2.9], [0.05, 0.75, 0], 'io'), K_(27.3, 'D', [0.9, 0.4, 2.85], [0.05, 0.75, 0], 'lin'),           // travelling a D: contrapicado lateral
    K_(27.8, 'D', [0.15, 0.85, 3.0], [0.12, 0.66, 0], 'io'), K_(30.2, 'D', [0.1, 0.84, 2.95], [0.12, 0.66, 0], 'lin'),         // dolly in frontal al +33 %
    K_(31.0, 'E', [0.3, 0.98, 3.25], [0, 0.82, 0], 'io'), K_(33.4, 'E', [0.2, 0.95, 3.15], [0, 0.82, 0], 'lin'),               // travelling a la foto
    { t: 33.9, p: [pc.x, pc.y + 0.05, S.E.z + 1.7], l: [pc.x, pc.y, S.E.z], e: 'io' }, { t: 35.4, p: [pc.x, pc.y + 0.05, S.E.z + 1.62], l: [pc.x, pc.y, S.E.z], e: 'lin' },   // dolly in: plano detalle del cuadradito
    K_(35.95, 'E', [0, 0.78, 3.45], [0, 0.6, 0], 'io'), K_(37.8, 'E', [0, 0.78, 3.35], [0, 0.6, 0], 'lin'),                    // dolly out
    { t: 38.9, p: [3.9, 11.4, 10.6], l: [-2.6, -1.9, -5.0], e: 'io' }, { t: 42.6, p: [3.7, 11.0, 10.1], l: [-2.6, -1.9, -5.0], e: 'lin' },   // grúa al plano general en picado de toda la fábrica
  ];
  const GOLPES = [[6.9, 0.006], [11.05, 0.006, 2], [19.4, 0.006, 3], [24.8, 0.006, 4], [31.0, 0.006, 5]];

  // ---------- final: la pantalla se llena de números (después de "todo es una lista de números") ----------
  const CAMPO = (T0 + dur) > 41.5; let celdas = [];
  if (CAMPO) {
    const COLS = 5, ROWS = 14, TF = 41.95, lcg = (n) => { let x = (n * 2654435761) >>> 0; x ^= x >>> 15; x = Math.imul(x, 2246822519) >>> 0; x ^= x >>> 13; return (x >>> 0) / 4294967296; };   // azar determinista por celda
    const fondo = document.createElement('div'); fondo.style.cssText = 'position:absolute;inset:0;background:#000;opacity:0'; hud.insertBefore(fondo, hud.firstChild); celdas.fondo = fondo;
    const REALES = [122845, 11, 12873, 23535, 4858, 30, 157464, 171847, 28287, 27054, 36753, 34623];
    for (let r = 0; r < ROWS; r++) for (let q = 0; q < COLS; q++) {
      const i = r * COLS + q, d = document.createElement('div'); d.style.cssText = `position:absolute;left:${q * 216}px;top:${r * 137 + 30}px;width:216px;text-align:center;font:600 46px var(--mono);letter-spacing:-.02em;opacity:0`; hud.insertBefore(d, fondo.nextSibling);
      const dist = Math.hypot((q - 2) / 2.5, (r - 6.5) / 7); celdas.push({ d, i, t0: TF + 0.15 + dist * 1.1 + lcg(i + 7) * 0.25, real: i % 7 === 3 }); }
    celdas.valor = (i, k) => { const u = lcg(i * 131 + k * 17 + 3); return celdas[i].real ? String(REALES[(i + k) % REALES.length]) : String(Math.floor(10 + u * (u < 0.5 ? 989 : 199989))); };
  }

  E.animar(tl, dur, (t) => {
    const T = T0 + t;
    E.ruta(T, CAM, GOLPES);
    // A
    const T1 = 5.05, T2 = 6.0, u = st(T1, T2, T), xh = -anchoA / 2 - 0.05 + (anchoA + 0.1) * EASE.io(u);
    hoja.position.x = S.A.x + xh; hoja.visible = T > T1 - 0.05 && T < T2 + 0.1; hoja.material.opacity = 1 - st(T2, T2 + 0.1, T);
    const ab = io(6.1, 6.9, T); filaA.userData.abrir(0.085 * ab); marcoA.userData.set(1 - ab);
    fA.forEach((f, i) => { f.userData.borde(Math.max(ab, T > T1 && xh > bordesA[Math.max(0, i - 1)] ? 0.7 : 0)); f.userData.verId(out(8.15 + 0.08 * i, 8.45 + 0.08 * i, T));
      f.userData.acento((T > 2.85 + 0.09 * i && T < 3.7) || (T > 8.15 + 0.08 * i && T < 8.8 + 0.08 * i) ? 1 : 0); });
    idsN.forEach((n, i) => { const q = out(2.8 + 0.09 * i, 3.02 + 0.09 * i, T); n.style.opacity = q; n.style.display = 'inline-block'; n.style.transform = `translateY(${18 * (1 - q)}px)`; });
    // B
    K.pop(seg, T, 11.05, 0.4); seg.userData.verId(st(12.0, 12.3, T)); seg.userData.acento(T > 11.9 && T < 12.8 ? 1 : 0);
    [[pa, 13.25, 13.85], [pb, 13.4, 14.05]].forEach(([w, tp, tq], k) => { K.pop(w.f, T, tp, 0.35); K.pop(w.mc, T, tp, 0.35); const q = io(tq, tq + 0.5, T); w.f.userData.abrir(0.07 * q); w.mc.userData.set(1 - q);
      w.fs.forEach((f) => { f.userData.borde(q); f.userData.verId(st(14.5 + 0.15 * k, 14.8 + 0.15 * k, T)); }); w.fs[1].userData.acento(T > 15.9 ? 1 : 0); });
    lazo.visible = T > 17.05; lazo.material.opacity = st(17.05, 17.3, T);
    // C
    fC.forEach((f, i) => { K.pop(f, T, DC[i][2], 0.35); f.userData.verId(st(DC[i][2] + 0.25, DC[i][2] + 0.55, T)); f.userData.acento(T > 22.2 && T < 23.4 ? 1 : 0); });
    // D
    en36.forEach((cb, k) => K.pop(cb, T, 25.3 + 0.022 * k, 0.2)); es48.forEach((cb, k) => K.pop(cb, T, 25.9 + 0.026 * k, 0.2));
    // E (la foto aparece recién cuando la cámara viaja hacia ella: no se asoma detrás de las otras estaciones)
    K.pop(foto, T, 29.8, 0.7);
    grilla.visible = T > 33.1; grilla.material.opacity = 0.55 * st(33.1, 33.5, T);
    marca.userData.set(st(33.8, 34.0, T) * (1 - st(35.7, 35.9, T)));
    parches.forEach((f, i) => { const q = io(35.8 + 0.05 * i, 36.5 + 0.05 * i, T), x0 = -SF / 2 + (i + 0.5) * c, x1 = -anchoF / 2 + c / 2 + i * (c + gapF);
      f.position.set(S.E.x + x0 + (x1 - x0) * q, yJ + (0.22 - yJ) * q + 0.12 * Math.sin(Math.PI * q), S.E.z + 0.03 + 0.1 * Math.sin(Math.PI * q)); f.visible = T > 35.8; f.userData.borde(q); });
    // payoff: todas las fichas de la línea giran y muestran su número (texto → ID; cuadradito → vector)
    todas.forEach((f, i) => f.userData.girar(st(40.55 + 0.035 * i, 41.0 + 0.035 * i, T)));
    if (CAMPO) { const k0 = T - 41.95;
      celdas.fondo.style.opacity = 0.93 * out(41.9, 42.5, T);
      for (const c of celdas) { const q = out(c.t0, c.t0 + 0.25, T);
        if (q <= 0.001) { c.d.style.opacity = 0; continue; }
        const k = Math.floor(T * (3 + 6 * st(42, 44, T)) + c.i * 0.31);   // la lluvia de números se acelera hacia el final
        if (c.k !== k) { c.k = k; c.d.textContent = celdas.valor(c.i, k); }
        c.d.style.opacity = q * (c.real ? 1 : 0.55); c.d.style.color = c.real ? 'var(--acc)' : 'var(--muted)'; c.d.style.transform = `translateY(${(1 - q) * 24}px)`; } }
    // rótulos
    E.cam.updateMatrixWorld();
    for (const r of R) { const o = ventana(T, r.a0, r.a1); r.a.style.opacity = o; r.a.style.display = o > 0.001 ? 'block' : 'none';
      if (!r.fijo && o > 0.001) { E.label(r.a, r.p); r.a.style.transform = r.dy === 'izq' ? 'translate(0,-100%)' : r.dy === 'arriba' ? 'translate(-50%,-100%)' : 'translate(-50%,-50%)'; } }
  });
}
