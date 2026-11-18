/* EL SET — "Qué son las variables en Python" (tema noir con OBJETOS 3D, rehecho 2026-11-18).
   La MEMORIA es una torre de losas de vidrio; un VALOR es un objeto (orbe de cristal, tira de metal, bandeja de cubos); un NOMBRE es un ANILLO de luz
   que se cierra alrededor del valor. El cajón vacío del gancho es lo que una variable NO es. Cámara continua hacia la derecha y al fondo.
     A gancho: cajón vacío + orbe 19 con su anillo.   B nombre: la torre; el anillo baja y el 19 aparece adentro; el código se enciende en orden.
     C cuenta: edad + 1 → nace un orbe 20 en la losa de arriba y el anillo SUBE hasta él.   D tipo: orbe (número), tira (texto), bandeja (lista); el anillo salta de uno a otro.
     E compartida: dos anillos (precio, total) sobre el MISMO orbe 250; la copia fantasma se asoma y se borra.   payoff: grúa al plano general y vuelta al gancho.
   Todos los tiempos salen de la voz (cuando / ESC). Reglas: docs/2-estilo/CAMARA.md · funciones: docs/5-tecnica/THREEJS.md. */
import { plano } from './escena3d.js';
import { ESC, cuando } from './tiempos.js';
import { O3D } from './objetos3d.js';

export const montar = (root, tl, id) => plano(root, tl, id, async (E) => {
  const { THREE, V, P } = E, R = E.rotulos(), O = O3D(E);

  // ---------- 1) estaciones ----------
  const S = { A: new V(0, 0, 0), B: new V(1.8, 0, -2.6), D: new V(4.2, 0, -5.2), E: new V(6.0, 0, -8.0) };
  const en = (s, x = 0, y = 0, z = 0) => new V(S[s].x + x, y, S[s].z + z);
  const G = {}; for (const k of 'ABDE') { G[k] = new THREE.Group(); E.scene.add(G[k]); }   // un grupo por estación: se oculta cuando la cámara está en otra
  const add = (o, s, x = 0, y = 0, z = 0) => { o.position.copy(en(s, x, y, z)); G[s].add(o); return o; };
  const YO = 0.6;   // altura de los objetos que flotan sobre el piso

  // ---------- 2) objetos y rótulos ----------
  // A · gancho: el cajón vacío (lo que NO es) y un orbe 19 con su anillo
  const caja = add(O.cajon(), 'A', -0.55, 0, 0); caja.rotation.y = 0.35;
  const vA = add(O.orbe(0.3, '19'), 'A', 0.5, YO, 0), tA = add(O.anillo(0.45), 'A', 0.5, YO, 0); tA.userData.acento(1); add(O.marca(), 'A', 0.5, 0, 0);
  const finHook = ESC.gancho.t1 - 0.35;
  R.fijo('@ayrtonnacer', 'firma', 90, 262, -1, finHook, 'font-size: 60px;');
  R.fijo('Una variable es una <span class="acc">etiqueta</span>', 'titular', 90, 350, -1, finHook, 'width: 900px; font-size: 140px; line-height: .98; letter-spacing: -.03em; text-align: left; text-wrap: balance;');
  R.anclado('<b>edad</b>', 'rot', en('A', 0.5, YO + 0.62), -1, ESC.gancho.t1 + 0.3, 'font-size: 54px;', 'arriba');
  R.anclado('<span class="chip err">✕ caja</span>', '', en('A', -0.55, 0.2, 0.3), cuando('l01', 'caja'), ESC.gancho.t1 + 0.3);

  // B · la torre de memoria; el anillo "edad" baja y el 19 aparece adentro
  const torre = add(O.torre(), 'B'), yB = torre.userData.y(2), yC = torre.userData.y(3);
  const vB = add(O.orbe(0.3, '19'), 'B', 0, yB, 0), tB = add(O.anillo(0.45), 'B', 0, yB, 0);
  const t02 = { nombre: cuando('l02', 'nombre'), apunta: cuando('l02', 'apunta'), valor: cuando('l02', 'valor'), memoria: cuando('l02', 'memoria') };
  const t03 = { asignar: cuando('l03', 'asignar'), crea: cuando('l03', 'crea'), asocia: cuando('l03', 'asocia') };
  const lB = R.anclado('<b>edad</b>', 'rot', en('B', 0, yB + 0.62), t02.nombre, cuando('l06') + 0.5, 'font-size: 54px;', 'arriba');
  const cod = R.anclado('edad = 19', 'rot mono', en('B', 0, yB + 1.02), t03.asignar, cuando('l04') - 0.4, 'font-size: 56px;', 'arriba');

  // C · la cuenta: nace el 20 en la losa de arriba y el anillo sube hasta él
  const vC = add(O.orbe(0.3, '20'), 'B', 0, yC, 0);
  const t04 = { nombre: cuando('l04', 'nombre'), valor: cuando('l04', 'valor') }, t05 = { mas: cuando('l05', 'más'), veinte: cuando('l05', 'veinte') };
  R.anclado('edad + 1', 'rot mono', en('B', -0.85, (yB + yC) / 2), t05.mas, cuando('l06') - 0.2, 'font-size: 46px;', 'centro');

  // D · el tipo vive en el valor: orbe (número), tira (texto), bandeja (lista); el anillo salta del número al texto
  const XD = [-0.85, 0, 0.85];
  const vN = add(O.orbe(0.3, '19'), 'D', XD[0], YO, 0), vT = add(O.tira(), 'D', XD[1], YO, 0), vL = add(O.lista(), 'D', XD[2], YO, 0);
  [XD[0], XD[1], XD[2]].forEach((x) => add(O.marca(0.34), 'D', x, 0, 0));
  const t06 = { tipo: cuando('l06', 'tipo'), numero: cuando('l06', 'número'), texto: cuando('l06', 'texto'), lista: cuando('l06', 'lista') };
  const finD = ESC.compartida.t0 + 0.4;
  R.anclado('int', 'rot mono', en('D', XD[0], 0.12, 0.45), t06.numero, finD, 'color: var(--muted);');
  R.anclado('str', 'rot mono', en('D', XD[1], 0.12, 0.45), t06.texto, finD, 'color: var(--muted);');
  R.anclado('list', 'rot mono', en('D', XD[2], 0.12, 0.45), t06.lista, finD, 'color: var(--muted);');
  const tD = add(O.anillo(0.5), 'D', XD[0], YO, 0);
  const lD = R.anclado('<b>edad</b>', 'rot', en('D', XD[0], YO + 0.7), cuando('l07') - 0.1, finD, 'font-size: 54px;', 'arriba');
  const t07 = cuando('l07'), t08 = { pasar: cuando('l08', 'pasar'), texto: cuando('l08', 'texto') };

  // E · dos anillos, un solo valor; la copia que NO se hace
  const vE = add(O.orbe(0.3, '250'), 'E', 0, YO, 0), e1 = add(O.anillo(0.45, 0.35), 'E', 0, YO, 0), e2 = add(O.anillo(0.6, -0.3), 'E', 0, YO, 0); add(O.marca(), 'E', 0, 0, 0);
  const fantasma = add(O.orbe(0.3, '250', true), 'E', 0.85, YO, 0);
  const t10 = { dos: cuando('l10', 'dos'), mismo: cuando('l10', 'mismo') }, t11 = { copia: cuando('l11', 'copia'), solo: cuando('l11', 'solo') };
  const lE1 = R.anclado('<b>precio</b>', 'rot', en('E', -0.4, YO + 0.85), cuando('l10') - 0.6, ESC.payoff.t0, 'font-size: 54px;', 'arriba');
  const lE2 = R.anclado('<b>total</b>', 'rot', en('E', 0.4, YO + 0.85), t10.dos, ESC.payoff.t0, 'font-size: 54px;', 'arriba');
  R.anclado('total = precio', 'rot mono', en('E', 0, YO + 1.35), cuando('l10'), ESC.payoff.t0, 'font-size: 50px;', 'arriba');
  // el nombre reaparece en el gancho al volver (payoff)
  R.anclado('<b>edad</b>', 'rot', en('A', 0.5, YO + 0.62), ESC.payoff.t0 + 1.0, ESC.payoff.t1 + 0.3, 'font-size: 54px;', 'arriba');

  const t12 = { guarda: cuando('l12', 'guarda'), nombra: cuando('l12', 'nombra') };
  const anillos = [tA, tB, tD, e1, e2];

  // ---------- 3) cámara ----------
  const Kp = (T, s, p, l, e) => ({ t: T, p: [S[s].x + p[0], p[1], S[s].z + p[2]], l: [S[s].x + l[0], l[1], S[s].z + l[2]], e });
  const v1 = cuando('l02') - 0.85, v2 = cuando('l03') - 0.6, v3 = cuando('l04') - 0.5, v4 = cuando('l06') - 0.55, v5 = cuando('l08') - 0.5,
    v6 = cuando('l09') - 0.5, v7 = cuando('l10') - 0.5, v8 = cuando('l11') - 0.4, v9 = cuando('l12') - 0.5;
  const CAM = [
    Kp(0, 'A', [2.7, 2.3, 4.7], [0, 0.7, 0]),                         // portada: medio en tres cuartos, leve picado
    Kp(v1, 'A', [2.45, 2.1, 4.25], [0, 0.68, 0], 'lin'),                  // gancho: push-in lento
    Kp(v1 + 0.9, 'B', [0.9, 1.5, 4.6], [0, 1.65, 0], 'io'),               // TRAVELLING A → B: la torre entera, de frente (l02)
    Kp(v2, 'B', [0.9, 1.5, 4.6], [0, 1.65, 0], 'lin'),
    Kp(v2 + 0.8, 'B', [1.5, 1.85, 2.9], [0, 1.9, 0], 'out'),              // DOLLY IN en picado leve: el orbe, el anillo y el código (l03)
    Kp(v3, 'B', [1.5, 1.85, 2.9], [0, 1.9, 0], 'lin'),
    Kp(v3 + 0.9, 'B', [-1.0, 2.2, 3.9], [0, 2.05, 0], 'io'),               // PANEO ORBITAL y grúa: la cuenta, del 19 al 20 (l04–l05)
    Kp(v4, 'B', [-1.0, 2.2, 3.9], [0, 2.05, 0], 'lin'),
    Kp(v4 + 0.9, 'D', [0.5, 3.0, 5.4], [0, 0.35, 0], 'io'),             // TRAVELLING + GRÚA: los tres tipos juntos, en picado
    Kp(v5, 'D', [0.5, 3.0, 5.4], [0, 0.35, 0], 'lin'),
    Kp(v5 + 0.8, 'D', [-0.7, 1.3, 2.9], [-0.55, 0.6, 0], 'io'),           // dolly in: el anillo que salta (l08)
    Kp(v6, 'D', [-0.7, 1.3, 2.9], [-0.55, 0.6, 0], 'lin'),
    Kp(v6 + 0.7, 'D', [1.5, 0.45, 3.0], [-0.5, 0.65, 0], 'out'),          // contrapicado: el 19 quedó solo, el anillo envuelve el texto (l09)
    Kp(v7, 'D', [1.5, 0.45, 3.0], [-0.5, 0.65, 0], 'lin'),
    Kp(v7 + 0.9, 'E', [1.2, 1.7, 4.2], [0, 0.8, 0], 'io'),                // TRAVELLING a los dos anillos (l10)
    Kp(v8, 'E', [1.2, 1.7, 4.2], [0, 0.8, 0], 'lin'),
    Kp(v8 + 0.8, 'E', [0.5, 3.2, 2.6], [0.1, 0.5, 0], 'out'),             // GRÚA ascendente: los dos anillos sobre el mismo orbe (l11)
    Kp(v9, 'E', [0.5, 3.2, 2.6], [0.1, 0.5, 0], 'lin'),
    { t: v9 + 0.7, p: [3.4, 6.5, 1.0], l: [2.4, 0.5, -3.5], e: 'in' },    // GRÚA: sube por encima del set (se ve todo el recorrido)…
    Kp(v9 + 1.5, 'A', [1.9, 1.3, 3.7], [0.2, 0.55, 0], 'out'),            // …y baja de vuelta al gancho: el cajón se borra, el anillo queda (cierra el loop)
    Kp(ESC.payoff.t1, 'A', [1.9, 1.3, 3.7], [0.2, 0.55, 0], 'lin'),
  ];
  // retenciones con DERIVA ORBITAL LENTA (referencia de Ayrton 11-17): la cámara nunca se congela, el texto sigue legible
  const orb = (p, l, g, k) => { const dx = p[0] - l[0], dz = p[2] - l[2], c = Math.cos(g), sn = Math.sin(g); return [l[0] + (dx * c + dz * sn) * k, p[1], l[2] + (-dx * sn + dz * c) * k]; };
  let signo = 1;
  for (let i = 1; i < CAM.length; i++) { const a = CAM[i - 1], b = CAM[i];
    if (b.e === 'lin' && a.p.every((x, j) => Math.abs(x - b.p[j]) < 1e-6) && i > 1) { b.p = b.p[1] > 3 ? orb(b.p, b.l, signo * 0.1, 1.12) : orb(b.p, b.l, signo * 0.17, 0.92); signo = -signo; } }
  const GOLPES = [[v1 + 0.9, 0.006], [v3 + 0.9, 0.006, 2], [v4 + 0.9, 0.006, 3], [v7 + 0.9, 0.006, 4]];

  // ---------- 4) un cuadro ----------
  const tmp = new V();
  const ponerAnillo = (a, p, k = 1) => { a.position.copy(p); a.scale.setScalar(Math.max(0.001, k)); a.visible = k > 0.01; };
  return (T) => {
    E.ruta(T, CAM, GOLPES);
    const gen = T > v9;
    G.A.visible = T < v1 + 1.2 || gen; G.B.visible = (T > v1 - 0.5 && T < v4 + 1.0) || gen;
    G.D.visible = T > v4 - 0.6; G.E.visible = T > v7 - 0.6;
    // A (visible desde el cuadro 0): el orbe ya está dentro de su anillo. El cajón se va en el payoff, cuando la voz dice "guarda".
    caja.scale.setScalar(Math.max(0.001, 1 - E.st(t12.guarda, t12.guarda + 0.45, T))); caja.visible = T < t12.guarda + 0.46;
    // B: la torre crece desde su base cuando la cámara llega; el anillo baja y se cierra; el orbe aparece adentro
    E.pop(torre, T, v1 + 0.25, 0.7);
    const qa = E.out(t02.nombre, t02.nombre + 0.8, T), yRing = yB + 1.1 * (1 - qa), uno = E.st(t02.nombre, t02.nombre + 0.15, T);
    const subida = E.io(t05.veinte + 0.1, t05.veinte + 0.9, T);   // C: el anillo sube del 19 al 20
    tB.position.set(S.B.x, yRing + (yC - yB) * subida, S.B.z); tB.scale.setScalar(Math.max(0.001, uno)); tB.visible = uno > 0.01;
    tB.userData.acento(E.st(t02.nombre, t02.nombre + 0.2, T) * (1 - E.st(t02.memoria, t02.memoria + 0.3, T)) + E.st(t03.asocia, t03.asocia + 0.2, T) * (1 - E.st(v3, v3 + 0.3, T)) + 0.0);
    lB.p.set(S.B.x, tB.position.y + 0.62, S.B.z);
    const q19 = E.pop(vB, T, t02.valor, 0.5); vB.userData.acento(E.st(t03.crea, t03.crea + 0.2, T) * (1 - E.st(t03.asocia, t03.asocia + 0.2, T)));
    vB.userData.fade(1 - 0.65 * subida);
    const q20 = E.pop(vC, T, t05.veinte, 0.5); vC.userData.acento(E.st(t05.veinte, t05.veinte + 0.2, T) * (1 - E.st(v4, v4 + 0.3, T)));
    const html = T < t03.crea ? 'edad = 19' : T < t03.asocia ? 'edad = <b>19</b>' : '<b>edad</b> = 19';
    if (cod.d.innerHTML !== html) cod.d.innerHTML = html;
    // D: los tres valores entran en la palabra que los nombra; el anillo salta del número al texto
    E.pop(vN, T, t06.numero, 0.4); E.pop(vT, T, t06.texto, 0.4); E.pop(vL, T, t06.lista, 0.4);
    const k = E.io(t08.pasar, t08.texto + 0.1, T), ent = E.st(t07 - 0.1, t07 + 0.3, T);
    ponerAnillo(tD, en('D', XD[0] + (XD[1] - XD[0]) * k, YO + 0.4 * Math.sin(Math.PI * k), 0), ent); tD.userData.acento(E.st(t07 - 0.1, t07 + 0.2, T));
    lD.p.set(S.D.x + XD[0] + (XD[1] - XD[0]) * k, YO + 0.7 + 0.4 * Math.sin(Math.PI * k), S.D.z);
    // E: precio rodea al 250; aparece total alrededor del MISMO; la copia fantasma se asoma y se borra
    E.pop(vE, T, v7 + 0.2, 0.5);
    ponerAnillo(e1, en('E', 0, YO), E.out(v7 + 0.4, v7 + 0.9, T)); e1.userData.acento(1 - E.st(t10.dos, t10.dos + 0.2, T));
    ponerAnillo(e2, en('E', 0, YO), E.out(t10.dos, t10.dos + 0.6, T)); e2.userData.acento(E.st(t10.dos, t10.dos + 0.2, T));
    const qf = E.pop(fantasma, T, t11.copia, 0.25) * (1 - E.st(t11.copia + 0.6, t11.copia + 0.9, T)); fantasma.visible = qf > 0.01; fantasma.scale.setScalar(Math.max(0.001, qf)); fantasma.userData.fade(qf);
    // payoff: todos los anillos en tan cuando la voz dice "nombra"
    const enc = E.st(t12.nombra, t12.nombra + 0.25, T);
    if (enc > 0) anillos.forEach((t) => t.userData.acento(enc));
    R.dibujar(T);
  };
}, { estilo: 'noir' });
