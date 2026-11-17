/* EL SET — "Qué son las variables en Python". Una variable es una ETIQUETA (placa con hilo blanco) que apunta a un VALOR (bloque gris).
   Corriente: hacia la DERECHA y al fondo (el reel anterior iba a la izquierda). Estaciones:
     A gancho: la caja (lo que NO es) y una etiqueta colgada de un valor.
     B nombre: la memoria (una losa); la etiqueta "edad" apunta al 19; arriba, el código edad = 19 se ilumina en orden (valor, después nombre).
     C cuenta: edad + 1 → la etiqueta se da vuelta y muestra 19 → = 20.
     D tipo: tres valores (19, "hola", [1, 2]) con su tipo grabado; la etiqueta pasa del 19 al texto.
     E compartida: dos etiquetas (precio, total) a un solo valor 250; el fantasma de una copia aparece y se borra.
   payoff: grúa al plano general; la caja del gancho desaparece y las etiquetas se encienden en tan.
   Todos los tiempos salen de la voz (cuando / ESC). Reglas: docs/2-estilo/CAMARA.md · funciones: docs/5-tecnica/THREEJS.md. */
import { plano } from './escena3d.js';
import { ESC, cuando } from './tiempos.js';
import { K3 } from './token3d.js';

export const montar = (root, tl, id) => plano(root, tl, id, async (E) => {
  const { THREE, V, P } = E, R = E.rotulos(), K = K3(E);

  // ---------- 1) estaciones ----------
  const S = { A: new V(0, 0, 0), B: new V(1.4, 0, -2.2), C: new V(2.5, 0, -2.0), D: new V(3.6, 0, -4.6), E: new V(5.0, 0, -7.0) };
  const en = (s, x = 0, y = 0, z = 0) => new V(S[s].x + x, y, S[s].z + z);
  const G = {}; for (const k of 'ABCDE') { G[k] = new THREE.Group(); E.scene.add(G[k]); }   // un grupo por estación: se oculta cuando la cámara está en otra
  const add = (o, s, x = 0, y = 0, z = 0) => { o.position.copy(en(s, x, y, z)); G[s].add(o); return o; };

  // ---------- piezas propias ----------
  const VAL = 1.3, TAG = 1.0, HV = K.H * VAL, HT = K.H * TAG, TY = HV + 0.36;   // TY = altura de la etiqueta sobre su valor            // valor: placa grande; etiqueta: placa chica
  const valor = (txt, s, x, z = 0) => add(K.ficha({ txt, size: VAL }), s, x, HV / 2, z);
  const etiqueta = (txt, s, x, y, z = 0, back = null) => add(K.ficha({ txt, size: TAG, back }), s, x, y, z);
  // hilo blanco de la etiqueta al valor: un cilindro que se estira entre dos puntos (se mueve por cuadro, no se crea)
  const hilo = (s) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 8), E.basic(P.hi)); m.visible = false; G[s].add(m);
    const up = new V(0, 1, 0), d = new V();
    return { m, set(a, b, p) { if (p <= 0.002) { m.visible = false; return; } const q = new V().lerpVectors(a, b, Math.min(1, p)); d.subVectors(q, a);
      const L = d.length(); if (L < 1e-4) { m.visible = false; return; } m.visible = true; m.position.copy(a).addScaledVector(d, 0.5); m.scale.set(1, L, 1); m.quaternion.setFromUnitVectors(up, d.normalize()); } };
  };
  const bajo = (o) => new V(o.position.x, o.position.y - o.userData.h / 2, o.position.z);    // borde inferior de una placa
  const sobre = (o) => new V(o.position.x, o.position.y + o.userData.h / 2, o.position.z);   // borde superior
  const losa = (w, d) => { const g = new THREE.Group(), m = E.caja(w, 0.03, d, E.std()); m.position.y = 0.015; g.add(m); E.contornear(g, P.mid); return g; };

  // ---------- 2) objetos y rótulos por estación ----------
  // A · gancho: la caja (lo que NO es una variable) y una etiqueta colgada de un valor
  const caja = new THREE.Group(); { const m = E.caja(0.5, 0.42, 0.5, E.std()); m.position.y = 0.21; caja.add(m); E.contornear(caja); }
  add(caja, 'A', -0.42, 0, 0); caja.rotation.y = 0.35;
  const vA = valor('19', 'A', 0.42), tA = etiqueta('edad', 'A', 0.42, TY), hA = hilo('A');
  const finHook = ESC.gancho.t1 - 0.35;
  R.fijo('@ayrtonnacer', 'firma', 90, 262, -1, finHook, 'font-size: 60px;');
  R.fijo('Una variable es una <span class="acc">etiqueta</span>', 'titular', 90, 350, -1, finHook, 'width: 900px; font-size: 140px; line-height: .98; letter-spacing: -.03em; text-align: left; text-wrap: balance;');
  const tCaja = cuando('l01', 'caja');
  R.anclado('<span class="chip err">✕ caja</span>', '', en('A', -0.42, 0.21, 0.3), tCaja, ESC.gancho.t1 + 0.3);

  // B · la memoria: losa; la etiqueta "edad" apunta al 19
  const memoria = add(losa(1.7, 0.9), 'B');
  const vB = valor('19', 'B', 0), tB = etiqueta('edad', 'B', 0, TY), hB = hilo('B');
  const t02 = { nombre: cuando('l02', 'nombre'), apunta: cuando('l02', 'apunta'), valor: cuando('l02', 'valor'), memoria: cuando('l02', 'memoria') };
  R.anclado('memoria', 'rot', en('B', 0.55, 0.05, 0.45), t02.memoria, cuando('l04') - 0.4, 'color: var(--muted); font-size: 46px;', 'arriba');
  const t03 = { asignar: cuando('l03', 'asignar'), crea: cuando('l03', 'crea'), asocia: cuando('l03', 'asocia') };
  const cod = R.anclado('edad = 19', 'rot mono', en('B', 0, 1.02), t03.asignar, cuando('l04') - 0.4, 'font-size: 64px;', 'arriba');

  // C · la cuenta: edad + 1 = 20 (la etiqueta se da vuelta y muestra su valor)
  const cy = 0.55, CS = 1.4, eC = add(K.ficha({ txt: 'edad', size: CS, back: '19' }), 'C', -0.5175, cy), mas = add(K.ficha({ txt: '+ 1', size: CS }), 'C', 0, cy), igual = add(K.ficha({ txt: '= 20', size: CS }), 'C', 0.5175, cy);
  const t04 = { nombre: cuando('l04', 'nombre'), valor: cuando('l04', 'valor') }, t05 = { mas: cuando('l05', 'más'), veinte: cuando('l05', 'veinte') };

  // D · el tipo vive en el valor: tres valores con su tipo; la etiqueta pasa del número al texto
  const losaD = add(losa(3.0, 0.9), 'D');
  const vN = valor('19', 'D', -1.0), vT = valor('"hola"', 'D', 0.0), vL = valor('[1, 2]', 'D', 1.05);
  const t06 = { tipo: cuando('l06', 'tipo'), numero: cuando('l06', 'número'), texto: cuando('l06', 'texto'), lista: cuando('l06', 'lista') };
  const finD = ESC.compartida.t0 + 0.4;
  R.anclado('int', 'rot mono', en('D', -1.0, 0.03, 0.38), t06.numero, finD, 'color: var(--muted);');
  R.anclado('str', 'rot mono', en('D', 0.0, 0.03, 0.38), t06.texto, finD, 'color: var(--muted);');
  R.anclado('list', 'rot mono', en('D', 1.05, 0.03, 0.38), t06.lista, finD, 'color: var(--muted);');
  const tD = etiqueta('edad', 'D', -1.0, TY), hD = hilo('D');
  const t07 = cuando('l07'), t08 = { pasar: cuando('l08', 'pasar'), texto: cuando('l08', 'texto') };

  // E · dos etiquetas, un solo valor; la copia que NO se hace
  const losaE = add(losa(1.9, 0.9), 'E');
  const vE = valor('250', 'E', 0), e1 = etiqueta('precio', 'E', -0.42, TY), e2 = etiqueta('total', 'E', 0.42, TY), h1 = hilo('E'), h2 = hilo('E');
  const fantasma = valor('250', 'E', 0.62); fantasma.userData.borde(0.35);
  const t10 = { dos: cuando('l10', 'dos'), mismo: cuando('l10', 'mismo') }, t11 = { copia: cuando('l11', 'copia'), solo: cuando('l11', 'solo') };
  R.anclado('total = precio', 'rot mono', en('E', 0, 1.0), cuando('l10'), ESC.payoff.t0, 'font-size: 56px;', 'arriba');

  const t12 = { guarda: cuando('l12', 'guarda'), nombra: cuando('l12', 'nombra') };
  const etiquetas = [tA, tB, eC, tD, e1, e2];

  // ---------- 3) cámara ----------
  const Kp = (T, s, p, l, e) => ({ t: T, p: [S[s].x + p[0], p[1], S[s].z + p[2]], l: [S[s].x + l[0], l[1], S[s].z + l[2]], e });
  const v1 = cuando('l02') - 0.85, v2 = cuando('l03') - 0.6, v3 = cuando('l04') - 0.5, v4 = cuando('l06') - 0.55, v5 = cuando('l08') - 0.5,
    v6 = cuando('l09') - 0.5, v7 = cuando('l10') - 0.5, v8 = cuando('l11') - 0.4, v9 = cuando('l12') - 0.5;
  const CAM = [   // poses calculadas para que lo que se lee caiga entre y 200 y 1100 (fuera de los subtítulos)
    Kp(0, 'A', [3.59, 3.17, 6.21], [0, 0.84, 0]),                        // portada: medio en tres cuartos, leve picado
    Kp(v1, 'A', [3.3, 2.95, 5.75], [0, 0.82, 0], 'lin'),                 // gancho: push-in lento
    Kp(v1 + 0.85, 'B', [0.44, 0.85, 3.1], [0, 0.18, 0], 'io'),           // TRAVELLING A → B: llega de frente a la memoria
    Kp(v2, 'B', [0.44, 0.85, 3.1], [0, 0.18, 0], 'lin'),                 // retención (l02)
    Kp(v2 + 0.75, 'B', [1.49, 0.26, 3.19], [0, 0.38, 0], 'out'),         // DOLLY IN en contrapicado: el código y la etiqueta (l03)
    Kp(v3, 'B', [1.49, 0.26, 3.19], [0, 0.38, 0], 'lin'),
    Kp(v3 + 0.8, 'C', [0, 0.96, 4.38], [0, 0.34, 0], 'io'),        // TRAVELLING lateral a la cuenta (l04–l05)
    Kp(v4, 'C', [0, 0.96, 4.38], [0, 0.34, 0], 'lin'),
    Kp(v4 + 0.85, 'D', [1.26, 3.49, 6.02], [0.2, -0.04, 0], 'io'),         // TRAVELLING + GRÚA a los tipos, en picado (los tres juntos)
    Kp(v5, 'D', [1.26, 3.49, 6.02], [0.2, -0.04, 0], 'lin'),
    Kp(v5 + 0.8, 'D', [-0.88, 1.32, 4.39], [-0.5, 0.22, 0], 'io'),      // dolly in: la etiqueta que se mueve (l08)
    Kp(v6, 'D', [-0.88, 1.32, 4.39], [-0.5, 0.22, 0], 'lin'),
    Kp(v6 + 0.7, 'D', [1.73, 0.47, 3.86], [-0.5, 0.24, 0], 'out'),       // contrapicado: el 19 quedó solo, el hilo va al texto (l09)
    Kp(v7, 'D', [1.73, 0.47, 3.86], [-0.5, 0.24, 0], 'lin'),
    Kp(v7 + 0.85, 'E', [1.14, 1.21, 3.87], [0.1, 0.36, 0], 'io'),        // TRAVELLING a las dos etiquetas (l10)
    Kp(v8, 'E', [1.14, 1.21, 3.87], [0.1, 0.36, 0], 'lin'),
    Kp(v8 + 0.8, 'E', [0.6, 3.44, 2.86], [0.1, -0.02, 0], 'out'),        // GRÚA ascendente: los dos hilos llegan al mismo bloque (l11)
    Kp(v9, 'E', [0.6, 3.44, 2.86], [0.1, -0.02, 0], 'lin'),
    { t: v9 + 0.7, p: [3.0, 5.5, 2.0], l: [1.5, 0, -2.5], e: 'in' },      // GRÚA: sube por encima del set (se ve todo el recorrido)…
    Kp(v9 + 1.5, 'A', [1.76, 1.26, 3.76], [0, 0.22, 0], 'out'),           // …y baja de vuelta al gancho: la caja se borra, la etiqueta queda (cierra el loop)
    Kp(ESC.payoff.t1, 'A', [1.76, 1.26, 3.76], [0, 0.22, 0], 'lin'),
  ];
  const GOLPES = [[v1 + 0.85, 0.006], [v3 + 0.8, 0.006, 2], [v4 + 0.85, 0.006, 3], [v7 + 0.85, 0.006, 4]];

  // ---------- 4) un cuadro ----------
  const tmp = new V();
  return (T) => {
    E.ruta(T, CAM, GOLPES);
    // cada estación se ve mientras la cámara está cerca; en el plano general (payoff) se ven todas
    const gen = T > v9;
    G.A.visible = T < v1 + 1.2 || gen; G.B.visible = (T > v1 - 0.5 && T < v4 + 1.0) || gen; G.C.visible = (T > v3 - 0.6 && T < v4 + 1.0) || gen;
    G.D.visible = T > v4 - 0.6; G.E.visible = T > v7 - 0.6;
    // A (visible desde el cuadro 0): el hilo ya está tendido. La caja se va en el payoff, cuando la voz dice "guarda".
    hA.set(bajo(tA), sobre(vA), 1); tA.userData.acento(1);
    K.quitar(caja, T, t12.guarda, 0.45);
    // B: aparecen cuando la cámara viaja hacia ellas
    E.pop(memoria, T, v1 + 0.2, 0.5);
    E.pop(tB, T, t02.nombre, 0.3); tB.userData.acento(E.st(t02.nombre, t02.nombre + 0.2, T) * (1 - E.st(t02.memoria, t02.memoria + 0.3, T)) + E.st(t03.asocia, t03.asocia + 0.2, T) * (1 - E.st(v3, v3 + 0.3, T)));
    hB.set(bajo(tB), sobre(vB), E.out(t02.apunta, t02.apunta + 0.45, T));
    E.pop(vB, T, t02.valor, 0.3); vB.userData.acento(E.st(t03.crea, t03.crea + 0.2, T) * (1 - E.st(t03.asocia, t03.asocia + 0.2, T)));
    // el código se enciende en orden: primero el valor, después el nombre
    const html = T < t03.crea ? 'edad = 19' : T < t03.asocia ? 'edad = <b>19</b>' : '<b>edad</b> = 19';
    if (cod.d.innerHTML !== html) cod.d.innerHTML = html;
    // C: edad + 1 = 20
    E.pop(eC, T, t04.nombre, 0.3); eC.userData.acento(1 - E.st(t04.valor, t04.valor + 0.3, T)); eC.userData.girar(E.st(t04.valor, t04.valor + 0.5, T));
    E.pop(mas, T, t05.mas, 0.3); E.pop(igual, T, t05.veinte, 0.3); igual.userData.acento(E.st(t05.veinte, t05.veinte + 0.2, T));
    // D: tres valores en la palabra que los nombra; la etiqueta pasa del 19 al texto
    E.pop(losaD, T, v4 + 0.1, 0.5); E.pop(vN, T, t06.numero, 0.3); E.pop(vT, T, t06.texto, 0.3); E.pop(vL, T, t06.lista, 0.3);
    E.pop(tD, T, t07 - 0.1, 0.3);
    const k = E.io(t08.pasar, t08.texto + 0.1, T);
    tD.position.copy(en('D', -1.0 + 1.0 * k, TY + 0.22 * Math.sin(Math.PI * k)));
    tD.userData.acento(E.st(t07 - 0.1, t07 + 0.2, T));
    hD.set(bajo(tD), sobre(k < 0.5 ? vN : vT), E.out(t07, t07 + 0.4, T) * Math.abs(1 - 2 * k));   // el hilo se despega del 19 y se vuelve a pegar en el texto
    // E: precio apunta al 250; aparece total y apunta al MISMO; la copia fantasma se asoma y se borra
    E.pop(losaE, T, v7 + 0.1, 0.5); E.pop(vE, T, v7 + 0.2, 0.3); E.pop(e1, T, v7 + 0.3, 0.3);
    h1.set(bajo(e1), sobre(vE), E.out(v7 + 0.45, v7 + 0.85, T));
    E.pop(e2, T, t10.dos, 0.3); h2.set(bajo(e2), sobre(vE), E.out(t10.mismo, t10.mismo + 0.4, T));
    e2.userData.acento(E.st(t10.dos, t10.dos + 0.2, T));
    const qf = E.pop(fantasma, T, t11.copia, 0.25) * (1 - E.st(t11.copia + 0.6, t11.copia + 0.9, T)); fantasma.visible = qf > 0.01; fantasma.scale.setScalar(Math.max(0.001, qf));
    // payoff: todas las etiquetas en tan cuando la voz dice "nombra"
    const enc = E.st(t12.nombra, t12.nombra + 0.25, T);
    if (enc > 0) etiquetas.forEach((t) => t.userData.acento(enc));
    R.dibujar(T);
  };
});
