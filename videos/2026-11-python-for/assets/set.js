/* EL SET DEL REEL "El bucle for" — tema CLARO (prueba de estética, Ayrton 2026-11-21): estudio blanco infinito, esferas negras brillantes,
   tarjeta blanca mate, anillo tan (el for). Un tramo en negro ("adentro" del for). Plano secuencia; tiempos SIEMPRE desde la voz.
   Estaciones:  A (0,0,0) la fila de 5 nombres + la tarjeta de código, dentro de un campo de miles de esferas
                C (0.6,0,-4.2) adentro del for: tubo de vidrio que entrega una esfera por vez (fondo negro)
                D (2.7,0,-1.2) range(): una esfera sola que crea números de a uno
   Reglas: docs/2-estilo/CAMARA.md · funciones de E: docs/5-tecnica/THREEJS.md · tema claro: docs/2-estilo/ESTILO.md */
import { plano } from './escena3d.js';
import { ESC, cuando, hasta } from './tiempos.js';

export const montar = (root, tl, id) => plano(root, tl, id, async (E) => {
  const { THREE, V, P } = E, R = E.rotulos();
  const hex = (c) => '#' + c.getHexString();
  const S = { A: new V(0, 0, 0), C: new V(0.6, 0, -4.2), D: new V(2.7, 0, -1.2) };
  const en = (s, x = 0, y = 0, z = 0) => new V(S[s].x + x, y, S[s].z + z);

  // ---------- tiempos (todos de la voz) ----------
  const tL0 = ESC.lista.t0, tRe0 = ESC.recorre.t0, tA0 = ESC.adentro.t0, tR0 = ESC.rango.t0, tP0 = ESC.payoff.t0;
  const tCinco = cuando('l02', 'cinco'), tNombres = cuando('l02', 'nombres'), tL03 = cuando('l03'), tEscribir = cuando('l03', 'escribir'), tMil = cuando('l03', 'mil');
  const tOtra = cuando('l04', 'otra'), tFor = cuando('l04', 'for'), tCada = cuando('l04', 'cada'), tL05 = cuando('l05');
  const G = [cuando('l05', 'primero'), cuando('l05', 'siguiente')]; for (let k = 2; k < 5; k++) G.push(G[1] + 0.42 * (k - 1));   // saludos: el primero, el siguiente y los demás seguidos
  const TD = [cuando('l07', 'próximo'), cuando('l07', 'una'), cuando('l07', 'otra'), cuando('l07', 'vez'), cuando('l07', 'cuando')];   // el for pide: cae una esfera
  const tNing = cuando('l07', 'ninguno'), tFin = cuando('l07', 'termina');
  const tRango = cuando('l08', 'rango'), tCasi = cuando('l08', 'casi'), tCrean = cuando('l08', 'crean');
  const tMillon = cuando('l09', 'millón'), tCambia = cuando('l09', 'cambia'), tLista = cuando('l09', 'lista');

  // ---------- el campo: miles de esferas negras (una sola malla instanciada) ----------
  const RAD = 0.065, PASO = 0.3, FILA = [-2, -1, 0, 1, 2];
  const pos = [];
  for (let j = 0; j < 80; j++) for (let i = -30; i <= 30; i++) { if (j === 0 && Math.abs(i) <= 2) continue; pos.push([i * PASO, -j * PASO]); }
  const N = pos.length, dist = pos.map(([x, z]) => Math.hypot(x, z)), dMax = Math.max(...dist);
  const mCampo = E.negro(); mCampo.color.copy(P.blanco);   // el color real va por esfera (instanceColor)
  const campo = new THREE.InstancedMesh(new THREE.SphereGeometry(RAD, 12, 8), mCampo, N); E.scene.add(campo);
  const sh0 = E.sombra(0.26, 0.26, 0.42), shGeo = sh0.geometry.clone().rotateX(-Math.PI / 2);
  const sombras = new THREE.InstancedMesh(shGeo, sh0.material, N); E.scene.add(sombras);
  for (let n = 0; n < N; n++) campo.setColorAt(n, P.tinta);
  const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), SC = new V(), PO = new V(), CB = new THREE.Color();
  // presencia de cada esfera: se hunde y vuelve a salir en ola (cerca → lejos o al revés)
  const OLAS = [[tCinco, 0, 'in'], [tMil, 1, 'out'], [tOtra, 0, 'in'], [tP0 + 0.15, 1, 'out']];
  const presencia = (n, T) => { let v = 1; for (const [t, a, dir] of OLAS) { const f = dist[n] / dMax, dl = (dir === 'out' ? f : 1 - f) * 0.7; v += (a - v) * E.io(t + dl, t + dl + 0.45, T); } return v; };
  let blanco = false;
  const dibujarCampo = (T) => {
    for (let n = 0; n < N; n++) { const v = presencia(n, T), s = Math.max(0.0001, v);
      PO.set(pos[n][0], RAD * s, pos[n][1]); SC.setScalar(s); M4.compose(PO, Q, SC); campo.setMatrixAt(n, M4);
      PO.y = 0.003; M4.compose(PO, Q, SC); sombras.setMatrixAt(n, M4); }
    campo.instanceMatrix.needsUpdate = true; sombras.instanceMatrix.needsUpdate = true;
    const ola = T > tMillon && T < tMillon + 4.5;   // payoff: una onda de luz recorre el campo (blanco = "esta vuelta")
    if (ola || blanco) { const r = (T - tMillon) * 6;
      for (let n = 0; n < N; n++) { const w = ola ? Math.exp(-(((dist[n] - r) / 0.7) ** 2)) : 0; campo.setColorAt(n, CB.copy(P.tinta).lerp(P.blanco, w)); }
      campo.instanceColor.needsUpdate = true; blanco = ola; }
  };

  // ---------- A · la fila de la lista: 5 esferas con nombre ----------
  const NOMBRES = ['Ana', 'Beto', 'Caro', 'Dani', 'Eli'];
  const fila = FILA.map((i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(RAD, 24, 16), E.negro()); m.position.set(i * PASO, RAD, 0); E.scene.add(m);
    const s = E.sombra(0.26, 0.26, 0.42); s.position.x = i * PASO; E.scene.add(s); return { m, s }; });
  fila.forEach((f, k) => R.anclado(NOMBRES[k], 'pild', en('A', FILA[k] * PASO, 0.2, 0), tNombres + 0.12 * k, tEscribir + 0.2, 'font-size: 38px;', 'arriba'));
  const saludos = fila.map((f, k) => R.anclado(NOMBRES[k], 'pild', en('A', FILA[k] * PASO, 0.2, 0), tL05 - 0.2, tA0 - 0.45, 'font-size: 38px;', 'arriba'));

  // la tarjeta de código (blanca, mate): una textura propia con colores de marca
  const TW = 1152, TH = 720, cv = document.createElement('canvas'); cv.width = TW; cv.height = TH; const cx = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const tarjeta = new THREE.Group(); tarjeta.position.copy(en('A', 0, 0.92, -0.7));
  tarjeta.add(E.caja(1.14, 0.72, 0.03, E.std(), 0.02));
  const cara = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.6875), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); cara.position.z = 0.0161; tarjeta.add(cara);
  E.scene.add(tarjeta); const sombraT = E.sombra(1.1, 0.25, 0.18); sombraT.position.copy(en('A', 0, 0, -0.7)); E.scene.add(sombraT);
  let ultima = null;
  const pintar = (lineas, salida = [], pie = '') => {   // lineas: [[texto, color], …] por renglón; se redibuja solo si cambió
    const clave = JSON.stringify([lineas, salida, pie]); if (clave === ultima) return; ultima = clave;
    cx.fillStyle = hex(P.blanco); cx.fillRect(0, 0, TW, TH);
    cx.font = '600 30px "Geist Mono", monospace'; cx.fillStyle = hex(P.mid); cx.textBaseline = 'middle'; cx.fillText('main.py', 64, 62);
    cx.font = '600 52px "Geist Mono", monospace';
    lineas.forEach((l, r) => { let x = 64; for (const [t, c] of l) { cx.fillStyle = c; cx.fillText(t, x, 150 + r * 72); x += cx.measureText(t).width; } });
    if (salida.length) { cx.fillStyle = hex(P.edge); cx.fillRect(64, 386, TW - 128, 3); cx.font = '500 44px "Geist Mono", monospace'; cx.fillStyle = hex(P.mid);
      salida.forEach((s, r) => cx.fillText(s, 64, 442 + r * 56)); }
    if (pie) { cx.font = '600 34px "Geist Mono", monospace'; cx.fillStyle = hex(P.mid); cx.textAlign = 'right'; cx.fillText(pie, TW - 64, TH - 54); cx.textAlign = 'left'; }
    tex.needsUpdate = true; };
  const tin = hex(P.tinta), med = hex(P.mid), acc = hex(P.acc);
  const MUCHOS = ['Ana', 'Beto', 'Caro', 'Dani', 'Eli', 'Fede', 'Gabi', 'Hugo', 'Inés', 'Juan', 'Lola', 'Mati', 'Nora', 'Omar', 'Pía', 'Raúl', 'Sofi', 'Tomi'];
  const linPrint = (nom) => [['print(', tin], ['"Hola"', med], [', ', tin], [`"${nom}"`, med], [')', tin]];
  const codFor = (lista, accLista) => [[['nombres = ', tin], [lista, accLista ? acc : med]], [['for', accLista ? tin : acc], [' nombre ', tin], ['in', accLista ? tin : acc], [' nombres:', tin]], [['    print(', tin], ['"Hola"', med], [', nombre)', tin]]];
  const dibujarTarjeta = (T) => {
    if (T < tOtra) {   // cinco saludos escritos a mano… y después mil
      if (T < tMil) { const k = Math.floor(E.st(tEscribir, tEscribir + 1.4, T) * 5 + 0.999); pintar(NOMBRES.slice(0, Math.max(1, k)).map(linPrint)); }
      else { const s = Math.floor(E.io(tMil, tMil + 1.6, T) * 995), L = []; for (let r = 0; r < 5; r++) L.push(linPrint(MUCHOS[(s + r) % MUCHOS.length])); pintar(L, [], `línea ${s + 5} de 1000`); }
    } else if (T < tLista) {   // el for: tres líneas y la salida que se va llenando
      const k = G.filter((g) => T >= g).length; pintar(codFor('["Ana", "Beto", …]', false), NOMBRES.slice(0, k).map((n) => `Hola ${n}`).slice(-3));
    } else {   // payoff: cambia la lista, no el código
      const n = Math.floor(E.st(tLista + 0.3, ESC.payoff.t1, T) * 999999);
      pintar(codFor('range(1_000_000)', true), [`Hola ${Math.max(0, n - 2)}`, `Hola ${Math.max(0, n - 1)}`, `Hola ${n}`]);
    }
  };

  // el anillo del for (tan): se apoya sobre cada esfera
  const mFor = new THREE.MeshStandardMaterial({ color: P.acc, roughness: 0.35, metalness: 0.25 });
  const anillo = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.013, 12, 48), mFor); E.scene.add(anillo);

  // ---------- C · adentro: tubo de vidrio (la lista) que entrega una esfera por vez al for ----------
  const gC = new THREE.Group(); gC.position.copy(S.C); gC.position.y = 0.12; E.scene.add(gC);
  const tubo = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.62, 32, 1, true), E.vidrio(0.2)); tubo.position.y = 0.61; gC.add(tubo);
  for (const y of [0.3, 0.92]) { const b = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.006, 8, 40), E.std()); b.rotation.x = Math.PI / 2; b.position.y = y; gC.add(b); }
  const bolasC = NOMBRES.map(() => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.05, 24, 16), E.std()); gC.add(m); return m; });
  const anilloC = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.013, 12, 48), mFor); anilloC.rotation.x = Math.PI / 2; anilloC.position.y = 0.22; gC.add(anilloC);
  R.anclado('próximo', 'pild', en('C', 0.2, 0.62, 0), TD[0], tNing, '', 'izq');
  R.anclado('<b>fin</b>', 'pild grande', en('C', 0.2, 0.62, 0), tFin, tR0 - 0.1, '', 'izq');
  const dibujarC = (T) => {
    bolasC.forEach((b, j) => {
      const baja = TD.slice(0, j).reduce((a, t) => a + E.io(t + 0.1, t + 0.4, T), 0);   // la pila baja un lugar cada vez que sale una
      const u1 = E.io(TD[j], TD[j] + 0.35, T), u2 = E.io(TD[j] + 0.35, TD[j] + 0.8, T);
      const yPila = 0.352 + (j - baja) * 0.105;
      b.position.set(u2 * (0.24 + (4 - j) * 0.115), yPila + (0.1 - yPila) * u1, 0); });
    const pulso = [...TD, tNing].reduce((a, t) => a + 0.18 * Math.exp(-(((T - t - 0.05) / 0.12) ** 2)), 0);
    anilloC.scale.setScalar(1 + pulso);
  };

  // ---------- D · range(): una esfera sola que crea números de a uno ----------
  const bolaD = new THREE.Mesh(new THREE.SphereGeometry(0.12, 32, 20), E.negro()); bolaD.position.copy(en('D', 0, 0.12, 0)); E.scene.add(bolaD);
  const sombraD = E.sombra(0.48, 0.48, 0.5); sombraD.position.copy(en('D')); E.scene.add(sombraD);
  R.fijo('<span class="pild grande">range(1_000_000_000)</span>', '', 0, 300, tRango, tP0 - 0.1, 'width: 1080px; text-align: center;');
  R.fijo('<span class="pild grande"><b>48 bytes</b></span>', '', 0, 420, tCasi, tP0 - 0.1, 'width: 1080px; text-align: center;');
  const numeros = [0, 1, 2, 3, 4, 5, 6].map((n) => { const t = tCrean + 0.32 * n, p = en('D', 0.18, 0.03, 0); return { n, t, p, r: R.anclado(String(n), 'rot mono', p, t, t + 1.2, 'font-size: 54px;') }; });
  const dibujarD = (T) => { for (const q of numeros) { const u = E.out(q.t, q.t + 1.5, T); q.p.set(S.D.x + 0.18 + 0.55 * u, 0.03, S.D.z + 0.12 * u); } };

  // ---------- portada + gancho: firma y título (una palabra en tan) ----------
  const finHook = ESC.gancho.t1 - 0.35;
  R.fijo('@ayrtonnacer', 'firma', 90, 262, -1, finHook, 'font-size: 60px;');
  R.fijo('El bucle <span class="acc">for</span>', 'titular', 90, 350, -1, finHook, 'width: 900px; font-size: 150px; line-height: .98; letter-spacing: -.03em; text-align: left;');

  // ---------- cámara (tiempo global) ----------
  const K = (t, p, l, e) => ({ t, p, l, e });
  const gancho = [0, 0.86, 2.9], ganchoL = [0, 0.1, -2.6];
  const lista = [0.5, 1.1, 3.9], listaL = [0, 0.14, -0.1];                  // plano medio de la fila, tres cuartos
  const tarj = [0.15, 0.95, 2.6], tarjL = [0, 0.82, -0.7];                  // la tarjeta de código, de frente y legible
  const general = [2.2, 2.1, 5.2], generalL = [0, 0.2, -2.4];               // zoom out: "mil"
  const via = (x) => [x - 0.15, 0.72, 1.6], viaL = (x) => [x + 0.1, 0.12, -0.1];   // travelling lateral con el anillo (x = la esfera que saluda)
  const frente = [0.6, 0.45, 1.0], frenteL = [0.6, 0.45, 0], cruza = [0.6, 0.45, -0.7], cruzaL = [0.6, 0.45, -2.2];
  const cC = [S.C.x + 0.9, 0.42, S.C.z + 2.4], cCL = [S.C.x + 0.3, 0.46, S.C.z];   // contrapicado del tubo
  const orbita = (a, r = 0.62, h = 1.65) => [S.D.x + r * Math.sin(a), h, S.D.z + r * Math.cos(a)], dL = [S.D.x, 0.1, S.D.z];
  const alto = [0.6, 3.4, 5.6], altoL = [0, 0, -4.5], fin = [0, 1.05, 3.1], finL = [0, 0.42, -1.2];
  const CAM = [
    K(0, gancho, ganchoL),
    K(tL0 - 0.35, [0, 0.8, 2.5], [0, 0.1, -2.6], 'lin'),                     // gancho: push-in lento mientras se lee el título
    K(tL0 + 0.55, lista, listaL, 'io'),                                       // GRÚA que baja a la fila (0,9 s)
    K(tL03 - 0.5, [0.42, 1.06, 3.7], listaL, 'lin'),                          // retención con deriva mínima: los cinco nombres
    K(tL03 + 0.35, tarj, tarjL, 'io'),                                        // dolly out corto: aparece la tarjeta
    K(tMil - 0.35, [0.15, 0.95, 2.75], tarjL, 'lin'),
    K(tMil + 0.75, general, generalL, 'io'),                                  // ZOOM OUT: mil nombres = el campo vuelve
    K(tOtra - 0.4, [2.4, 2.2, 5.5], generalL, 'lin'),
    K(tFor + 0.3, tarj, tarjL, 'io'),                                         // dolly in: el for (tres líneas)
    K(tL05 - 0.5, [0.15, 0.95, 2.45], tarjL, 'lin'),
    K(G[0] - 0.1, via(-0.6), viaL(-0.6), 'io'),                               // baja a la fila (grúa corta)
    K(G[4] + 0.2, via(0.6), viaL(0.6), 'lin'),                                // TRAVELLING lateral acompañando al anillo
    K(tA0 - 0.6, via(0.6), viaL(0.6), 'lin'),
    K(tA0, frente, frenteL, 'io'),                                            // frente al anillo (crece y se para)
    K(tA0 + 0.5, cruza, cruzaL, 'in'),                                        // lo ATRAVIESA: pasa a negro
    K(tA0 + 1.3, cC, cCL, 'out'),                                             // llega al tubo en contrapicado
    K(tFin - 0.3, [cC[0] - 0.08, cC[1] + 0.03, cC[2] - 0.1], cCL, 'lin'),
    K(tFin + 0.6, [S.C.x + 0.88, 0.43, S.C.z + 2.2], [S.C.x + 0.36, 0.46, S.C.z], 'io'),   // dolly in: termina solo
    K(tR0 - 0.15, [S.C.x + 0.87, 0.43, S.C.z + 2.16], [S.C.x + 0.36, 0.46, S.C.z], 'lin'),
    K(tR0 + 0.3, orbita(0), dL, 'io'),                                        // LATIGAZO al cenital de range()
    ...[1, 2, 3, 4, 5, 6].map((k) => K(tR0 + 0.3 + (tP0 - tR0 - 0.3) * k / 6, orbita(-0.11 * k), dL, 'lin')),   // giro lento
    K(tP0 + 1.0, alto, altoL, 'io'),                                          // GRÚA arriba: el campo entero
    K(tCambia - 0.25, [0.5, 3.3, 5.4], altoL, 'lin'),
    K(tCambia + 0.75, fin, finL, 'io'),                                       // baja a la tarjeta: cambia la lista
    K(ESC.payoff.t1, [0, 1.02, 2.95], finL, 'lin'),
  ];
  const GOLPES = [[tL0 + 0.55, 0.005], [tA0 + 1.3, 0.005, 2], [tP0 + 1.0, 0.005, 3]];

  // ---------- un cuadro ----------
  return (T) => {
    E.ruta(T, CAM, GOLPES);
    E.fondo(E.io(tA0 + 0.2, tA0 + 0.42, T) * (1 - E.io(tR0 - 0.05, tR0 + 0.15, T)));   // negro solo adentro del for
    const enA = T < tA0 + 0.35 || T > tP0, enC = T > tA0 + 0.2 && T < tR0 + 0.1, enD = T > tR0 - 0.1 && T < tP0 + 0.6;
    campo.visible = sombras.visible = enA; if (enA) dibujarCampo(T);
    fila.forEach((f, k) => { f.m.visible = f.s.visible = enA; const w = T < tP0 ? E.out(G[k], G[k] + 0.2, T) : 0; f.m.material.color.copy(P.tinta).lerp(P.blanco, w); });
    E.pop(tarjeta, T, tEscribir - 0.15, 0.45); if (T > tA0 + 0.3 && T < tP0 + 0.3) tarjeta.visible = false; sombraT.visible = tarjeta.visible; if (tarjeta.visible) dibujarTarjeta(T);
    // anillo A: aparece con "cada", salta de esfera en esfera y al final se para de frente para atravesarlo
    const qa = E.pop(anillo, T, tCada, 0.4); if (T > tA0 + 0.35) anillo.visible = false;
    if (qa > 0 && anillo.visible) { let x = FILA[0] * PASO, salto = 0;
      for (let k = 1; k < 5; k++) { const u = E.io(G[k] - 0.3, G[k] - 0.02, T); x += (FILA[k] - FILA[k - 1]) * PASO * u; salto += Math.sin(Math.PI * u) * 0.08; }
      const up = E.io(tA0 - 0.6, tA0, T); anillo.position.set(x, 0.2 + salto + 0.25 * up, 0.15 * up);
      anillo.rotation.x = Math.PI / 2 * (1 - up); anillo.scale.setScalar(qa * (1 + 1.4 * up)); }
    saludos.forEach((r, k) => { const h = T >= G[k] ? 'Hola ' + NOMBRES[k] : NOMBRES[k]; if (r.d.textContent !== h) r.d.textContent = h; });
    gC.visible = enC; if (enC) dibujarC(T);
    bolaD.visible = sombraD.visible = enD; if (enD) dibujarD(T);
    R.dibujar(T);
  };
}, { estilo: 'claro' });
