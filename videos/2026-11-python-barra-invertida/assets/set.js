/* EL SET DE ESTE REEL — un solo espacio 3D y UNA cámara continua para todo el video (plano secuencia).
   Es el archivo que se reescribe en cada reel. Todo lo demás (index.html, compositions/<escena>.html, assets/tiempos.js) se genera solo.

   Cómo se lee:
     1) ESTACIONES: dónde está cada idea en el espacio. En diagonal hacia la izquierda y al fondo → todos los viajes van en la MISMA dirección.
     2) OBJETOS de cada estación (línea gris; un solo acento tan) y RÓTULOS HTML anclados a puntos 3D.
     3) CÁMARA: lista de poses en TIEMPO GLOBAL del video. Patrón: viajar (≈ 0,8–0,9 s) → retener QUIETA mientras la voz nombra → viajar.
     4) dibujar(T): qué hace cada objeto en el segundo T. Los tiempos salen de la voz: cuando('l02', 'palabra'), ESC.<escena>.t0 / .t1.
   Nunca escribir segundos a mano: si la voz cambia, todo se reacomoda solo. Reglas de cámara: docs/2-estilo/CAMARA.md. Funciones de E: docs/5-tecnica/THREEJS.md. */
import { plano } from './escena3d.js';
import { ESC, cuando } from './tiempos.js';

export const montar = (root, tl, id) => plano(root, tl, id, async (E) => {
  const { THREE, V, P } = E, R = E.rotulos();

  // ---------- 1) estaciones (metros; y = altura; z negativo = más al fondo) ----------
  const S = { A: new V(0, 0, 0), B: new V(-1.8, 0, -3.5), C: new V(-3.6, 0, -7) };
  const en = (s, x = 0, y = 0, z = 0) => new V(S[s].x + x, y, S[s].z + z);                     // punto relativo a una estación
  const add = (o, s, x = 0, y = 0, z = 0) => { o.position.copy(en(s, x, y, z)); E.scene.add(o); return o; };

  // ---------- 2) objetos y rótulos ----------
  // A · el objeto protagonista (portada y gancho): un cubo de línea con UN punto tan
  const cubo = add(E.contornear(E.caja(0.5, 0.5, 0.5, E.std())), 'A', 0, 0.25);
  add(new THREE.Mesh(new THREE.SphereGeometry(0.035, 20, 14), E.basic(P.acc)), 'A', 0.25, 0.5, 0.25);
  // Portada + gancho (anatomía fija del media kit): firma arriba a la izquierda, título de 3–5 palabras a 140 px con UNA palabra en tan.
  const finHook = ESC.gancho.t1 - 0.35;
  R.fijo('@ayrtonnacer', 'firma', 90, 262, -1, finHook, 'font-size: 60px;');
  R.fijo('Título de <span class="acc">cuatro</span> palabras', 'titular', 90, 350, -1, finHook, 'width: 900px; font-size: 140px; line-height: .98; letter-spacing: -.03em; text-align: left; text-wrap: balance;');

  // B · primer concepto: una notebook que escribe
  const lap = add(E.laptop(), 'B'); lap.updateMatrixWorld(true);
  const tEscribe = cuando('l02', 'concepto'), BITS = ['10110100', '01101001', '11010010'];
  R.anclado('primer <b>concepto</b>', 'rot', en('B', 0, 0.3), tEscribe, cuando('l03') - 0.3, '', 'arriba');

  // C · segundo concepto: un router que emite (ondas de radio = anillos)
  const router = add(E.router(), 'C'); router.updateMatrixWorld(true);
  const antena = router.localToWorld(router.userData.puntaAntena.clone());
  const tEmite = cuando('l03', 'segundo'), anillos = [0, 1, 2].map(() => E.anillo(P.acc, new V(0, 1, 0), 0.014));
  R.anclado('segundo <b>concepto</b>', 'rot', en('C', 0, 0.42), tEmite, ESC.payoff.t0 - 0.2, '', 'arriba');

  // payoff · las dos ideas juntas: un cable las conecta (los cables TOCAN los objetos: salen de un puerto real)
  const cable = E.cable(lap.localToWorld(new V(-0.17, 0.008, 0)), router.localToWorld(router.userData.puertoLado.clone().negate().setY(0.03)), P.hi);
  const tJunto = cuando('l04', 'funcionando');

  // ---------- 3) cámara (tiempo global). K(segundo, estación, posición relativa, hacia dónde mira, curva) ----------
  // curvas: 'io' viaje (arranca y frena suave) · 'out' llegada · 'in' salida que acelera · 'lin' retención o deriva lenta
  const K = (T, s, p, l, e) => ({ t: T, p: [S[s].x + p[0], p[1], S[s].z + p[2]], l: [S[s].x + l[0], l[1], S[s].z + l[2]], e });
  const tB = ESC.explica.t0, tC = cuando('l03'), tG = ESC.payoff.t0;
  const CAM = [
    K(0, 'A', [1.71, 1.56, 2.98], [0, 0.62, 0]),                                  // cuadro 0 = portada: plano medio en tres cuartos, leve picado
    K(tB - 0.45, 'A', [1.5, 1.41, 2.63], [0, 0.6, 0], 'lin'),                     // gancho: dolly in lento (único lugar donde la cámara deriva)
    K(tB + 0.45, 'B', [0.3, 0.42, 1.35], [0, 0.03, 0], 'io'),                     // TRAVELLING A → B (0,9 s; el pico cae en el cambio de escena)
    K(tC - 0.45, 'B', [0.3, 0.42, 1.35], [0, 0.03, 0], 'lin'),                    // RETENCIÓN: quieta mientras la voz explica
    K(tC + 0.45, 'C', [0.8, 0.22, 2.3], [0, 0.02, 0], 'io'),                       // TRAVELLING B → C: llega en contrapicado (agranda el router)
    K(tG, 'C', [0.8, 0.22, 2.3], [0, 0.02, 0], 'lin'),                             // RETENCIÓN
    { t: tG + 0.9, p: [0, 5, 8], l: [-1, -1, -3.5], e: 'io' },            // GRÚA: sube al plano general en picado (las ideas juntas)
    { t: ESC.payoff.t1, p: [0, 5, 8], l: [-1, -1, -3.5], e: 'lin' },      // RETENCIÓN ≥ 2,5 s
  ];
  const GOLPES = [[tB + 0.45, 0.006], [tC + 0.45, 0.006, 2]];                    // temblor chiquito al aterrizar en cada estación

  // ---------- 4) un cuadro: qué se ve en el segundo T ----------
  return (T) => {
    E.ruta(T, CAM, GOLPES);
    // B y C aparecen recién cuando la cámara viaja hacia ellas: nada se asoma detrás del título del gancho
    E.pop(lap, T, tB - 0.4, 0.5); E.pop(router, T, tB - 0.4, 0.5);
    // B: los unos y ceros se tipean cuando la voz dice "concepto"
    const n = Math.floor(E.st(tEscribe, tEscribe + 1.2, T) * 24); let resto = n;
    lap.userData.pantalla.texto(BITS.map((l) => { const k = Math.min(8, Math.max(0, resto)); resto -= 8; return l.slice(0, k); }).join('\n') + (n < 24 ? '_' : ''), undefined, 54);
    // C: tres anillos se expanden desde la antena cuando la voz dice "segundo"
    anillos.forEach((a, i) => a.emitir((T - (tEmite + 0.5 * i)) / 1.6, 0.6, antena));
    // payoff: el cable crece de la notebook al router
    cable.set(E.io(tJunto - 0.6, tJunto + 0.5, T));
    R.dibujar(T);
  };
});
