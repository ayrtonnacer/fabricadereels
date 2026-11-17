/* Librería 3D de la fábrica de reels (three.js r187, local). Objetos de redes con la identidad HackTheBox, listos para reusar.
   Todo es función del tiempo local `t` (determinístico; sin reloj ni azar). Guía de uso y criterios: docs/5-tecnica/THREEJS.md.

   Uso en una composición (script de la escena):
     import('./assets/escena3d.js').then(async (M) => {
       const E = await M.crear(root);                       // renderer transparente 1080×1920, cámara, luces, entorno, piso
       const lap = E.laptop(); E.scene.add(lap);            // objetos: laptop, router, globo, cable, onda, anillo, pared, paquete
       E.animar(tl, 4.6, (t) => { E.ruta(t, [...]); ... }); // dibuja en cada cuadro; ruta() mueve la cámara entre posiciones
       window.__timelines['id'] = tl;                       // registrar AL FINAL (la construcción es asíncrona)
     });
   Unidades: metros (notebook ≈ 0,34 m). Piso en y = 0. La imagen sube `dy` px para dejar libre la franja de subtítulos.
   Look: Neutral tone mapping (conserva el lima de marca), entorno procedural (RoomEnvironment) de baja intensidad, luz key + contraluz celeste,
   aristas biseladas, sombras de contacto; los neones (ondas, anillos, paquetes) son MeshBasic sin tone mapping para que el lima sea exacto. */
import * as THREE from './three.module.js';
import { RoundedBoxGeometry } from './RoundedBoxGeometry.js';
import { RoomEnvironment } from './RoomEnvironment.js';
import { LineSegments2 } from './LineSegments2.js';
import { LineSegmentsGeometry } from './LineSegmentsGeometry.js';
import { LineMaterial } from './LineMaterial.js';
export { THREE };

const css = (v, d) => (getComputedStyle(document.documentElement).getPropertyValue(v).trim() || d);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const EASE = {
  lin: (x) => x,
  out: (x) => 1 - Math.pow(1 - x, 3),
  expo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  io: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  in: (x) => x * x * x,
};

export async function crear(root, opts = {}) {
  const { fov = 40, dy = 170, canvas = root.querySelector('canvas'), piso = true } = opts;
  try { await document.fonts.load('700 48px "Geist Mono"'); await document.fonts.load('700 48px "Host Grotesk"'); } catch (e) { /* sin fuentes: cae a monospace */ }
  const V = THREE.Vector3;
  const P = {
    bg: new THREE.Color(css('--bg', '#0B111C')), hondo: new THREE.Color(css('--bg-hondo', '#060A11')), line: new THREE.Color(css('--line', '#24344B')),
    acc: new THREE.Color(css('--acc', '#FD2B3C')), sky: new THREE.Color(css('--sky', '#F5F6F8')), ok: new THREE.Color(css('--ok', '#2EE08C')),
    warn: new THREE.Color(css('--warn', '#FFB020')), text: new THREE.Color(css('--text', '#E8EEF7')), panel: new THREE.Color(css('--panel', '#111A28')),
  };
  const LINEA = css('--estilo', 'linea') === 'linea';   // tema "línea": negro + contornos gruesos; "solido": objetos rellenos con entorno
  P.plate = new THREE.Color(css('--plate', '#0A0D12')); P.hi = new THREE.Color(css('--hi', '#FAFAFA')); P.edge = new THREE.Color(css('--edge', '#A1A1AA')); P.mid = new THREE.Color(css('--mid', '#52525B'));
  P.px = parseFloat(css('--trazo-px', '2.2')); P.trazo = P.edge; P.piso = P.mid; P.muted = P.edge;   // trazo = arista gris; blanco (P.hi / P.sky) solo para resaltar
  if (LINEA) { P.sky = P.hi; P.hondo = P.plate; P.bg = P.plate; }
  const hex = (c) => '#' + c.getHexString();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false); renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = 1.0;   // colores de marca exactos
  const scene = new THREE.Scene(); scene.fog = new THREE.Fog(new THREE.Color(css('--fog', '#' + P.hondo.getHexString())), 9, 34);
  const cam = new THREE.PerspectiveCamera(fov, 1080 / 1920, 0.05, 80);
  cam.setViewOffset(1080, 1920, 0, dy, 1080, 1920);          // sube la imagen dy px (franja de subtítulos y 1120–1320)
  // iluminación: entorno procedural (reflejos y relleno) + key + contraluz celeste que recorta las siluetas
  const pmrem = new THREE.PMREMGenerator(renderer);
  if (!LINEA) { scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.4; }   // el entorno cuesta ≈ +30 % de render y en línea no se ve
  scene.add(new THREE.HemisphereLight(0xcfe0ff, 0x1a2638, 1.1));
  const sun = new THREE.DirectionalLight(0xfff4e6, 2.0); sun.position.set(2.5, 5, 4); scene.add(sun);
  const rim = new THREE.DirectionalLight(0x6ec9ff, 1.5); rim.position.set(-3, 3, -4); scene.add(rim);
  const E = { THREE, P, LINEA, renderer, scene, cam, EASE, clamp, V };
  // en línea, el "relleno" es negro puro (tapa lo de atrás) y el objeto se dibuja con su contorno (E.contornear)
  E.std = (c, r = 0.55, m = 0.15) => { if (!LINEA) return new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
    const k = new THREE.MeshBasicMaterial({ color: P.plate, toneMapped: false, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }); k.userData.contorno = true; return k; };
  const LM = []; E.trazoMat = (color, w) => { const m = new LineMaterial({ color, linewidth: w, transparent: true, toneMapped: false }); m.resolution.set(1080, 1920); return m; };
  E.trazo = (pts, color = P.edge, w = P.px) => {   // línea gruesa (px) por pares de puntos [a0,a1, b0,b1…]: las líneas de WebGL miden 1 px y en video no se ven
    const g = new LineSegmentsGeometry(); g.setPositions(pts.flatMap((p) => [p.x, p.y, p.z])); const l = new LineSegments2(g, E.trazoMat(color, w)); l.computeLineDistances(); return l; };
  E.contornear = (obj, color = P.edge, w = P.px, umbral) => {   // agrega contorno grueso a cada malla con relleno negro (aristas marcadas, no facetas)
    if (!LINEA) return obj; const ms = []; obj.traverse((o) => { if (o.isMesh && o.material.userData.contorno) ms.push(o); });
    for (const m of ms) { const e = new THREE.EdgesGeometry(m.geometry, umbral ?? (m.geometry.type === 'BoxGeometry' || m.geometry.type === 'PlaneGeometry' ? 30 : 12)), g = new LineSegmentsGeometry(); g.setPositions(e.attributes.position.array);
      let mat = E.trazoMat(color, w);
      if (E.LUZ && color === P.edge) { mat = E.trazoMat(new THREE.Color(1, 1, 1), w); mat.vertexColors = true; g.setColors(E.luzColores(e.attributes.position.array, m.geometry)); }   // luz de contorno
      const l = new LineSegments2(g, mat); l.computeLineDistances(); m.add(l); m.material.userData.contorno = false; }
    return obj; };
  // LUZ DE CONTORNO (banco estético, NIVEL ≥ 2): en estilo línea no hay sombreado, así que la luz se dibuja en las aristas.
  // Una luz a contraluz arriba-izquierda-atrás: las aristas de ese lado van a blanco (P.hi), las opuestas bajan a gris oscuro.
  E.LUZ = (window.NIVEL || 0) >= 2;
  const LUZ_DIR = new THREE.Vector3(-0.55, 0.75, -0.35).normalize(), cSombra = P.mid.clone().lerp(P.edge, 0.35);
  E.luzColores = (pos, geo) => { geo.computeBoundingBox(); const bb = geo.boundingBox, c = bb.getCenter(new THREE.Vector3()), h = bb.getSize(new THREE.Vector3()).multiplyScalar(0.5).addScalar(1e-6), out = new Float32Array(pos.length), col = new THREE.Color(), n = new THREE.Vector3();
    for (let i = 0; i < pos.length; i += 3) { n.set((pos[i] - c.x) / h.x, (pos[i + 1] - c.y) / h.y, (pos[i + 2] - c.z) / h.z); const k = clamp(0.5 + 0.5 * n.dot(LUZ_DIR) / 1.2), q = k * k * (3 - 2 * k);
      col.copy(cSombra).lerp(P.hi, q); out[i] = col.r; out[i + 1] = col.g; out[i + 2] = col.b; }
    return out; };
  // halo de contraluz: mancha de luz suave detrás del protagonista (separa el objeto del fondo, como un rim light de estudio). Neutro: el acento queda para el significado.
  E.halo = (r = 1.6, op = 0.16) => { const cv = document.createElement('canvas'); cv.width = cv.height = 256; const x = cv.getContext('2d'), gr = x.createRadialGradient(128, 128, 0, 128, 128, 128);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 256, 256);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, opacity: op, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
    m.renderOrder = -1; return m; };
  E.basic = (c, o = 1) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, toneMapped: false });
  E.caja = (w, h, d, mat, r) => new THREE.Mesh(LINEA ? new THREE.BoxGeometry(w, h, d) : new RoundedBoxGeometry(w, h, d, 3, r === undefined ? Math.min(w, h, d) * 0.25 : r), mat);   // sólido: aristas biseladas; línea: aristas vivas

  // piso de líneas en perspectiva: tiras con ancho en metros (las cercanas gruesas, las lejanas finas; convergen al horizonte)
  if (piso) {
    const N = 26, w = LINEA ? 0.0035 : 0.006, pos = [], quad = (x0, z0, x1, z1) => pos.push(x0, 0.001, z0, x1, 0.001, z0, x1, 0.001, z1, x0, 0.001, z0, x1, 0.001, z1, x0, 0.001, z1);
    for (let i = -N; i <= N; i++) { quad(i - w, -N, i + w, N); quad(-N, i - w, N, i + w); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    const g = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: LINEA ? P.piso : 0x2f4a70, transparent: true, opacity: LINEA ? 0.55 : 0.7, side: THREE.DoubleSide })); scene.add(g); E.piso = g;
  }
  // sombra de contacto (falsa y barata): mancha suave bajo el objeto; ancla los objetos al piso
  E.sombra = (w, d, op = 0.6) => {
    const cv = document.createElement('canvas'); cv.width = cv.height = 128; const x = cv.getContext('2d'), g = x.createRadialGradient(64, 64, 4, 64, 64, 62);
    g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128);
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, opacity: op, depthWrite: false, toneMapped: false }));
    m.rotation.x = -Math.PI / 2; m.position.y = 0.003; return m;
  };

  // textura de texto (pantallas): se redibuja solo cuando cambia el texto; admite varias líneas ('\n')
  E.textoTex = (w, h, fondo = LINEA ? css('--plate', '#0A0D12') : '#070B12') => {
    const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const ctx = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4; let last = null;
    const api = { tex, texto(str, color = hex(P.acc), size = h * 0.2, alinear = 'left') {
      if (str === last) return; last = str;
      ctx.fillStyle = fondo; ctx.fillRect(0, 0, w, h); ctx.font = `700 ${size}px "Geist Mono", monospace`; ctx.fillStyle = color;
      ctx.textAlign = alinear; ctx.textBaseline = 'middle'; const L = str.split('\n'), lh = size * 1.3, y0 = h / 2 - (L.length - 1) * lh / 2, x0 = alinear === 'center' ? w / 2 : w * 0.16;
      L.forEach((l, i) => ctx.fillText(l, x0, y0 + i * lh + size * 0.04)); tex.needsUpdate = true; } };
    api.texto(''); return api;
  };

  // ---------- objetos ----------
  E.laptop = () => {   // ≈ 34 cm; frente hacia +z; sin antena (las notebooks no tienen una a la vista). userData: pantalla (texto), emisor (punto 3D de donde "sale" la onda)
    const g = new THREE.Group();
    const base = E.caja(0.34, 0.016, 0.23, E.std(0x34465f, 0.45, 0.55), 0.006); base.position.y = 0.008; g.add(base);
    const teclas = new THREE.Mesh(new THREE.PlaneGeometry(0.29, 0.11), E.std(0x1b2840, 0.8, 0.1)); teclas.rotation.x = -Math.PI / 2; teclas.position.set(0, 0.0165, 0.035); g.add(teclas); E.contornear(teclas, P.mid, P.px);
    const lid = new THREE.Group(); lid.position.set(0, 0.016, -0.115); lid.rotation.x = -0.28;
    const marco = E.caja(0.34, 0.225, 0.01, E.std(0x34465f, 0.45, 0.55), 0.005); marco.position.y = 0.1125; lid.add(marco);
    const T = E.textoTex(512, 320); const pant = new THREE.Mesh(new THREE.PlaneGeometry(0.31, 0.195), new THREE.MeshBasicMaterial({ map: T.tex, toneMapped: false })); pant.position.set(0, 0.1125, 0.0056); lid.add(pant);
    g.add(lid); E.contornear(g); g.add(E.sombra(0.62, 0.48)); g.userData = { pantalla: T, lid, emisor: new V(0, 0.232, -0.177) }; return g;
  };
  E.router = () => {   // ≈ 42 cm; dos antenas (los routers sí las tienen); pantallita frontal con texto. userData: puertoTrasero, puertoLado, puntaAntena
    const g = new THREE.Group();
    const body = E.caja(0.42, 0.06, 0.26, E.std(0x2d4268, 0.4, 0.4), 0.014); body.position.y = 0.03; g.add(body);
    for (const x of [-0.14, 0.14]) {
      const a = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.26, 14), E.std(0x44577a, 0.4, 0.5)); a.position.set(x, 0.19, -0.08); a.rotation.z = -x * 0.5; g.add(a); }
    const T = E.textoTex(256, 64); const pant = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.04), new THREE.MeshBasicMaterial({ map: T.tex, toneMapped: false })); pant.position.set(0, 0.032, 0.1305); g.add(pant);
    for (const x of [-0.17, -0.15]) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.006, 10, 10), E.basic(P.acc)); l.position.set(x, 0.05, 0.131); g.add(l); }
    E.contornear(g); g.add(E.sombra(0.7, 0.5));
    g.userData = { pantalla: T, puertoTrasero: new V(0, 0.03, -0.13), puertoLado: new V(-0.21, 0.03, 0.0), puntaAntena: new V(-0.14 + 0.065, 0.31, -0.08) }; return g;
  };
  E.globo = () => { const g = new THREE.Group(); g.add(new THREE.Mesh(new THREE.SphereGeometry(0.3, 40, 28), E.std(0x10233f, 0.35, 0.3)));
    if (LINEA) { const wg = new LineSegmentsGeometry(); wg.setPositions(new THREE.WireframeGeometry(new THREE.SphereGeometry(0.303, 14, 10)).attributes.position.array); const w = new LineSegments2(wg, E.trazoMat(P.edge, P.px)); w.computeLineDistances(); g.add(w); return g; }
    const w = new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(0.303, 14, 10)), new THREE.LineBasicMaterial({ color: P.sky, transparent: true, opacity: 0.65 })); g.add(w); return g; };
  E.pared = (w, h, d, c = 0x4a6088) => { const g = new THREE.Group(); const m = E.caja(w, h, d, E.std(c, 0.7, 0.05), Math.min(w, h, d) * 0.15); m.position.y = h / 2; g.add(m);
    if (LINEA) { m.position.y = 0; const o = new THREE.Group(); o.position.y = h / 2; o.add(m); g.add(o); g.remove(m); E.contornear(o, P.edge, P.px); return g; }
    const l = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d)), new THREE.LineBasicMaterial({ color: 0x8aa0c8, transparent: true, opacity: 0.45 })); l.position.y = h / 2; g.add(l); return g; };
  E.paquete = (c = P.acc, s = 0.045) => new THREE.Mesh(new RoundedBoxGeometry(s, s, s, 2, s * 0.2), E.basic(c));
  E.cable = (A, B, color = P.sky, r = 0.011, holgura = 0.12) => {   // cable con caída natural (holgura = flecha / largo): crece de A hacia B con set(p) p 0..1; si cuelga hasta el piso se apoya en él. Extremos SOBRE los objetos.
    const dir = new V().subVectors(B, A), len = dir.length(), side = new V(-dir.z, 0, dir.x).normalize(), N = 80, pts = [];
    for (let i = 0; i <= N; i++) { const s = i / N, q = new V().lerpVectors(A, B, s);
      q.y -= 4 * holgura * len * s * (1 - s);                                 // parábola de caída (aprox. de la catenaria)
      q.addScaledVector(side, 0.2 * holgura * len * Math.sin(Math.PI * s) * Math.sin(2 * Math.PI * s + 0.6));   // curvatura lateral suave: no es un plano perfecto
      { const h = q.y - (r + 0.003); q.y = r + 0.003 + 0.5 * (h + Math.sqrt(h * h + 1e-4)); }   // apoyado en el piso sin atravesarlo (máximo suave: sin quiebres)
      pts.push(q); }
    const path = new THREE.CatmullRomCurve3(pts), RAD = 12, m = new THREE.Mesh(new THREE.TubeGeometry(path, N, r, RAD, false), E.basic(color)); scene.add(m);
    const cnt = N * RAD * 6, set = (p) => { m.geometry.setDrawRange(0, Math.floor(clamp(p) * N) * RAD * 6); m.visible = p > 0.001; }; set(0);
    return { mesh: m, set, A, B, len, at: (s) => path.getPointAt(clamp(s)) };
  };
  E.onda = ({ A, B, amp = 0.08, lambda = 0.4, up = new V(0, 1, 0), s0 = 0, s1 = 1, color = P.acc, radius = 0.011, N = 200, glow = true, opacity = 1 }) => {
    // senoide de A a B (fase global: tramos [s0,s1] distintos empalman sin cortes); set(p) la dibuja de a poco
    const dir = new V().subVectors(B, A), L = dir.length(), u = dir.clone().normalize(), side = up.clone().sub(u.clone().multiplyScalar(up.dot(u))).normalize(), pts = [];
    for (let i = 0; i <= N; i++) { const d = (s0 + (s1 - s0) * i / N) * L; pts.push(A.clone().addScaledVector(u, d).addScaledVector(side, amp * Math.sin(2 * Math.PI * d / lambda))); }
    const path = new THREE.CatmullRomCurve3(pts), g = new THREE.Group(), mk = (r, o, add) => { const m = new THREE.Mesh(new THREE.TubeGeometry(path, N, r, 6, false), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: o, toneMapped: false, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: !add })); g.add(m); return m; };
    const core = mk(radius, opacity, false), halo = glow ? mk(radius * 3.2, 0.16 * opacity, true) : null; scene.add(g);
    const cnt = N * 6 * 6, vis = (p) => { const c = Math.floor(clamp(p) * N) * 36; core.geometry.setDrawRange(0, Math.min(c, cnt)); if (halo) halo.geometry.setDrawRange(0, Math.min(c, cnt)); g.visible = p > 0.001; };
    vis(0); return { group: g, set: vis, opacity: (o) => { core.material.opacity = o; if (halo) halo.material.opacity = 0.16 * o; }, at: (s) => path.getPointAt(clamp(s)), L };
  };
  E.anillo = (color = P.acc, normal = new V(0, 1, 0), grosor = 0.012) => {   // anillo de onda con grosor constante: emitir(p, rmax, centro)
    const m = new THREE.Mesh(new THREE.TorusGeometry(1, 0.01, 6, 128), E.basic(color, 0)); m.quaternion.setFromUnitVectors(new V(0, 0, 1), normal.clone().normalize()); m.visible = false; scene.add(m); let last = -1;
    return { mesh: m, emitir(p, rmax = 2, centro) { if (centro) m.position.copy(centro); if (p <= 0 || p >= 1) { m.visible = false; return 0; } const r = 0.06 + p * rmax;
      if (Math.abs(r - last) > 0.004) { m.geometry.dispose(); m.geometry = new THREE.TorusGeometry(1, grosor / r, 6, 128); last = r; } m.scale.setScalar(r); m.material.opacity = (1 - p) * 0.95; m.visible = true; return r; } };
  };

  // ---------- cámara y dibujo ----------
  E.ruta = (t, K) => {   // K = [{ t, p:[x,y,z], l:[x,y,z], e }]: de cada punto al siguiente con la easing `e` del destino
    let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], k = (EASE[b.e || 'io'])(clamp((t - a.t) / Math.max(1e-6, b.t - a.t)));
    const mix = (u, v) => u.map((x, j) => x + (v[j] - x) * k);
    cam.position.set(...mix(a.p, b.p)); const l = mix(a.l, b.l); cam.lookAt(...l); E._mira = new V(...l);
  };
  E.label = (el, v, dx = 0, dyp = 0) => {   // ubica un elemento HTML (position:absolute) sobre un punto 3D
    cam.updateMatrixWorld();   // la matriz de la cámara se actualiza al renderizar: sin esto el rótulo usa la del cuadro anterior
    const p = v.clone().project(cam); el.style.left = ((p.x * 0.5 + 0.5) * 1080 + dx) + 'px'; el.style.top = ((-p.y * 0.5 + 0.5) * 1920 + dyp) + 'px'; };
  // Física horneada (engine/fisica.mjs): posa los objetos según el tiempo local t, con interpolación entre cuadros. Sin reloj ni azar.
  E.fisica = (data, mapa) => {   // mapa = { nombre: Object3D }
    const Q0 = new THREE.Quaternion(), Q1 = new THREE.Quaternion();
    return (t) => {
      const u = clamp(t * data.fps, 0, data.n - 1), i = Math.min(Math.floor(u), data.n - 2), k = u - i;
      for (const nom in mapa) {
        const a = data.cuerpos[nom], o = i * 7, m = mapa[nom];
        m.position.set(a[o] + (a[o + 7] - a[o]) * k, a[o + 1] + (a[o + 8] - a[o + 1]) * k, a[o + 2] + (a[o + 9] - a[o + 2]) * k);
        Q0.set(a[o + 3], a[o + 4], a[o + 5], a[o + 6]); Q1.set(a[o + 10], a[o + 11], a[o + 12], a[o + 13]);
        m.quaternion.copy(Q0).slerp(Q1, k);
      }
    };
  };
  // ---------- ÓPTICA (banco estético, NIVEL ≥ 3): desenfoque de profundidad + desenfoque de movimiento ----------
  // Profundidad: se renderiza a una textura con su profundidad; un pase de pantalla completa desenfoca cada píxel según su distancia al plano de foco
  //   (círculo de confusión ∝ |z − foco| / z, como una lente real). El foco por defecto es el punto que mira la cámara (ruta → l); E.foco(t) lo cambia (rack focus).
  // Movimiento: obturador de 180° (1/60 s a 30 fps). Si la cámara mueve la imagen más de ~3 px en ese lapso, se promedian K sub-tomas dentro del obturador.
  //   Todo depende solo de t (determinístico).
  E.POST = (window.NIVEL || 0) >= 3; E.apertura = 30; E.cocMax = 12; E.foco = null; E.mbMax = 5;
  let post = null;
  if (E.POST) {
    const W = 1080, H = 1920, mk = (depth) => { const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType, samples: 0 }); if (depth) { rt.depthTexture = new THREE.DepthTexture(W, H); rt.depthTexture.type = THREE.UnsignedIntType; } rt.texture.colorSpace = THREE.SRGBColorSpace; return rt; };   // en sRGB: las mezclas (halo, piso) se ven igual que sin posproceso
    const rtS = mk(true), rtA = mk(false), quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)), oscene = new THREE.Scene(), ocam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1); oscene.add(quad);
    const vs = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }';
    const acum = new THREE.ShaderMaterial({ uniforms: { tex: { value: null }, w: { value: 1 } }, vertexShader: vs, fragmentShader: 'uniform sampler2D tex; uniform float w; varying vec2 vUv; void main(){ gl_FragColor = texture2D(tex, vUv) * w; }',
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneFactor, depthTest: false, depthWrite: false, toneMapped: false });
    const dof = new THREE.ShaderMaterial({ uniforms: { tex: { value: null }, dep: { value: rtS.depthTexture }, near: { value: cam.near }, far: { value: cam.far }, foco: { value: 3 }, ap: { value: 34 }, cmax: { value: 16 }, res: { value: new THREE.Vector2(W, H) } },
      vertexShader: vs, transparent: true, premultipliedAlpha: true, blending: THREE.NoBlending, depthTest: false, depthWrite: false, toneMapped: false,
      fragmentShader: `#include <packing>
        uniform sampler2D tex, dep; uniform float near, far, foco, ap, cmax; uniform vec2 res; varying vec2 vUv;
        float zv(vec2 uv){ return -perspectiveDepthToViewZ(texture2D(dep, uv).x, near, far); }
        float coc(float z){ return z > far * 0.98 ? cmax * 0.0 : min(cmax, ap * abs(z - foco) / max(z, 0.05)); }
        void main(){
          float c0 = coc(zv(vUv)); vec4 acc = texture2D(tex, vUv); float wsum = 1.0;
          // salida rápida: si ni este píxel ni su vecindario (4 sondas al radio máximo) están desenfocados, no hay nada que mezclar
          float cv = max(max(coc(zv(vUv + vec2(cmax, 0.) / res)), coc(zv(vUv - vec2(cmax, 0.) / res))), max(coc(zv(vUv + vec2(0., cmax) / res)), coc(zv(vUv - vec2(0., cmax) / res))));
          float rmax = max(c0, cv);
          if (rmax > 0.75) {
            for (int i = 1; i < 24; i++) {               // disco de Vogel: 24 muestras en el radio que hace falta acá (sin copias sueltas)
              float r = sqrt(float(i) / 24.0) * rmax, a = float(i) * 2.39996;
              vec2 o = vec2(cos(a), sin(a)) * r, uv = vUv + o / res;
              float cs = coc(zv(uv));
              float w = smoothstep(r - 1.5, r + 0.5, min(cs, max(c0, cs * step(zv(uv), zv(vUv)))));   // una muestra aporta si su propio círculo llega hasta acá (sin halos de lo enfocado sobre lo desenfocado)
              acc += texture2D(tex, uv) * w; wsum += w; }
          }
          gl_FragColor = acc / wsum;
        }` });
    // el foco: cerca de 0 = fondo sin profundidad (transparente) no se desenfoca
    const P5 = [new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()];
    const pantalla = (pts) => { cam.updateMatrixWorld(); return pts.map((v) => { const q = v.clone().project(cam); return [q.x * 540, q.y * 960]; }); };
    post = { rtS, rtA, quad, oscene, ocam, acum, dof, P5, pantalla };
  }
  const muestras = (fn, t) => {   // cuántas sub-tomas pide el movimiento de cámara en el obturador [t − 1/120, t + 1/120]
    const dt = 1 / 60, m = E._mira || new V(0, 0.5, 0), pts = [-1, 1].flatMap((sx) => [-1, 1].map((sy) => new V(m.x + sx * 0.4, m.y + sy * 0.4, m.z))).concat([m.clone()]);
    fn(t - dt / 2); const a = post.pantalla(pts); fn(t + dt / 2); const b = post.pantalla(pts);
    const px = Math.max(...a.map((q, i) => Math.hypot(q[0] - b[i][0], q[1] - b[i][1])));
    const K = Math.max(1, Math.min(E.mbMax, Math.ceil(px / 4)));
    return { K, obt: K === 1 ? 0 : Math.min(1, 4 * (K - 1) / Math.max(px, 1e-6)) };   // obturador acortado: sub-tomas a ≤ 4 px (sin copias visibles)
  };
  const dibujar = (fn, t) => {
    if (!post) { fn(t); renderer.render(scene, cam); return; }
    const { K, obt } = muestras(fn, t), { rtS, rtA, quad, oscene, ocam, acum, dof } = post;
    if (K > 1) { renderer.setRenderTarget(rtA); renderer.setClearColor(0x000000, 0); renderer.clear(); }
    for (let k = 0; k < K; k++) {   // la última sub-toma es la del centro (su profundidad alimenta el foco)
      const u = K === 1 ? 0 : (((k + 1) % K) / (K - 1) - 0.5) * obt; fn(t + u / 60);
      renderer.setRenderTarget(rtS); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
      if (K > 1) { quad.material = acum; acum.uniforms.tex.value = rtS.texture; acum.uniforms.w.value = 1 / K; renderer.setRenderTarget(rtA); renderer.autoClear = false; renderer.render(oscene, ocam); renderer.autoClear = true; }
    }
    const m = E._mira || new V(0, 0.5, 0), fz = E.foco ? E.foco(t) : m.clone().sub(cam.position).dot(cam.getWorldDirection(new V()));
    quad.material = dof; Object.assign(dof.uniforms, {}); dof.uniforms.tex.value = K > 1 ? rtA.texture : rtS.texture; dof.uniforms.foco.value = fz; dof.uniforms.ap.value = E.apertura; dof.uniforms.cmax.value = E.cocMax;
    renderer.setRenderTarget(null); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(oscene, ocam);
  };
  E.animar = (tl, dur, fn) => {
    const st = { t: 0 }, draw = () => dibujar(fn, st.t);
    tl.to(st, { t: dur, duration: dur, ease: 'none', onUpdate: draw }, 0); draw();
  };
  return E;
}
