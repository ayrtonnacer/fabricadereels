/* Librería 3D de la fábrica de reels (three.js r160, local). Objetos de redes con la identidad del tema, listos para reusar.
   Todo es función del tiempo local `t` (determinístico; sin reloj ni azar). Costo medido: ≈ +1 s de render por segundo de video (docs/CAMARA.md).

   Uso en una composición (script de la escena):
     import('./assets/escena3d.js').then(async (M) => {
       const E = await M.crear(root);                       // renderer transparente 1080×1920, cámara, luces, niebla, piso
       const lap = E.laptop(); E.scene.add(lap);            // objetos: laptop, router, globo, cable, onda, anillo, pared, paquete
       E.animar(tl, 4.6, (t) => { E.ruta(t, [...]); ... }); // dibuja en cada cuadro; ruta() mueve la cámara entre posiciones
       window.__timelines['id'] = tl;                       // registrar AL FINAL (la construcción es asíncrona)
     });
   Unidades: metros (notebook ≈ 0,34 m). Piso en y = 0. La imagen sube `dy` px para dejar libre la franja de subtítulos. */
import * as THREE from './three.module.js';
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
  try { await document.fonts.load('700 48px "IBM Plex Mono"'); await document.fonts.load('700 48px "Plex Sans"'); } catch (e) { /* sin fuentes: cae a monospace */ }
  const V = THREE.Vector3;
  const P = {
    bg: new THREE.Color(css('--bg', '#0B111C')), hondo: new THREE.Color(css('--bg-hondo', '#060A11')), line: new THREE.Color(css('--line', '#24344B')),
    acc: new THREE.Color(css('--acc', '#9FEF00')), sky: new THREE.Color(css('--sky', '#3BC9FF')), ok: new THREE.Color(css('--ok', '#2EE08C')),
    warn: new THREE.Color(css('--warn', '#FFB020')), text: new THREE.Color(css('--text', '#E8EEF7')), panel: new THREE.Color(css('--panel', '#111A28')),
  };
  const hex = (c) => '#' + c.getHexString();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false); renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene(); scene.fog = new THREE.Fog(P.hondo, 9, 34);
  const cam = new THREE.PerspectiveCamera(fov, 1080 / 1920, 0.05, 80);
  cam.setViewOffset(1080, 1920, 0, dy, 1080, 1920);          // sube la imagen dy px (franja de subtítulos y 1120–1320)
  scene.add(new THREE.HemisphereLight(0xcfe0ff, 0x1a2638, 2.0));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(2.5, 5, 4); scene.add(sun);
  const E = { THREE, P, renderer, scene, cam, EASE, clamp, V };
  E.std = (c, r = 0.55, m = 0.15) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
  E.basic = (c, o = 1) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o });

  // piso de líneas en perspectiva (el "piso de grilla" de la identidad)
  // (líneas como tiras con ancho en metros: las cercanas se ven gruesas, las lejanas finas y convergen al horizonte)
  if (piso) {
    const N = 26, w = 0.006, pos = [], quad = (x0, z0, x1, z1) => pos.push(x0, 0.001, z0, x1, 0.001, z0, x1, 0.001, z1, x0, 0.001, z0, x1, 0.001, z1, x0, 0.001, z1);
    for (let i = -N; i <= N; i++) { quad(i - w, -N, i + w, N); quad(-N, i - w, N, i + w); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    const g = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x2f4a70, transparent: true, opacity: 0.7, side: THREE.DoubleSide })); scene.add(g); E.piso = g;
  }

  // textura de texto (pantallas): se redibuja solo cuando cambia el texto
  E.textoTex = (w, h, fondo = '#070B12') => {
    const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const ctx = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4; let last = null;
    const api = { tex, texto(str, color = hex(P.acc), size = h * 0.3) {
      if (str === last) return; last = str;
      ctx.fillStyle = fondo; ctx.fillRect(0, 0, w, h); ctx.font = `700 ${size}px "IBM Plex Mono", monospace`; ctx.fillStyle = color;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(str, w / 2, h / 2 + size * 0.04); tex.needsUpdate = true; } };
    api.texto(''); return api;
  };

  // ---------- objetos ----------
  E.laptop = () => {   // ≈ 34 cm; frente hacia +z; la pantalla muestra texto (g.userData.pantalla.texto('1011'))
    const g = new THREE.Group();
    const base = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.016, 0.23), E.std(0x2a3a52, 0.5, 0.4)); base.position.y = 0.008; g.add(base);
    const teclas = new THREE.Mesh(new THREE.PlaneGeometry(0.29, 0.11), E.std(0x1b2840, 0.8, 0.1)); teclas.rotation.x = -Math.PI / 2; teclas.position.set(0, 0.0165, 0.035); g.add(teclas);
    const lid = new THREE.Group(); lid.position.set(0, 0.016, -0.115); lid.rotation.x = -0.28;
    const marco = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.225, 0.01), E.std(0x2a3a52, 0.5, 0.4)); marco.position.y = 0.1125; lid.add(marco);
    const T = E.textoTex(512, 320); const pant = new THREE.Mesh(new THREE.PlaneGeometry(0.31, 0.195), new THREE.MeshBasicMaterial({ map: T.tex })); pant.position.set(0, 0.1125, 0.0056); lid.add(pant);
    g.add(lid); g.userData = { pantalla: T, lid }; return g;
  };
  E.router = () => {   // ≈ 42 cm; dos antenas; pantallita frontal con texto
    const g = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.06, 0.26), E.std(0x2d4268, 0.5, 0.3)); body.position.y = 0.03; g.add(body);
    for (const x of [-0.14, 0.14]) { const a = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.26, 12), E.std(0x44577a)); a.position.set(x, 0.19, -0.08); a.rotation.z = -x * 0.5; g.add(a); }
    const T = E.textoTex(256, 64); const pant = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.04), new THREE.MeshBasicMaterial({ map: T.tex })); pant.position.set(0, 0.032, 0.1305); g.add(pant);
    for (const x of [-0.17, -0.15]) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.006, 8, 8), E.basic(P.acc)); l.position.set(x, 0.05, 0.131); g.add(l); }
    g.userData = { pantalla: T, antenas: [new V(-0.14 - 0.0, 0.32, -0.08), new V(0.14, 0.32, -0.08)] }; return g;
  };
  E.antena = () => { const g = new THREE.Group(); const m = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.2, 10), E.std(0x8a9bb8, 0.4, 0.5)); m.position.y = 0.1; g.add(m);
    const p = new THREE.Mesh(new THREE.SphereGeometry(0.016, 14, 14), E.basic(P.acc)); p.position.y = 0.205; g.add(p); g.userData = { punta: new V(0, 0.205, 0) }; return g; };
  E.globo = () => { const g = new THREE.Group(); g.add(new THREE.Mesh(new THREE.SphereGeometry(0.3, 28, 20), E.std(0x10233f, 0.6, 0.1)));
    const w = new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(0.303, 14, 10)), new THREE.LineBasicMaterial({ color: P.sky, transparent: true, opacity: 0.65 })); g.add(w); return g; };
  E.pared = (w, h, d, c = 0x4a6088) => { const g = new THREE.Group(); const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), E.std(c, 0.8, 0)); m.position.y = h / 2; g.add(m);
    const l = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry), new THREE.LineBasicMaterial({ color: 0x8aa0c8, transparent: true, opacity: 0.5 })); l.position.y = h / 2; g.add(l); return g; };
  E.paquete = (c = P.acc, s = 0.045) => new THREE.Mesh(new THREE.BoxGeometry(s, s, s), E.basic(c));
  E.cable = (A, B, color = P.sky, r = 0.011) => {   // cilindro que crece de A hacia B: set(p) con p 0..1
    const dir = new V().subVectors(B, A), len = dir.length(), geo = new THREE.CylinderGeometry(r, r, 1, 12); geo.translate(0, 0.5, 0);
    const m = new THREE.Mesh(geo, E.basic(color)); m.position.copy(A); m.quaternion.setFromUnitVectors(new V(0, 1, 0), dir.clone().normalize()); scene.add(m);
    const set = (p) => { m.scale.set(1, Math.max(1e-4, len * clamp(p)), 1); m.visible = p > 0.001; }; set(0); return { mesh: m, set, A, B, len, at: (s) => new V().lerpVectors(A, B, s) };
  };
  E.onda = ({ A, B, amp = 0.08, lambda = 0.4, up = new V(0, 1, 0), s0 = 0, s1 = 1, color = P.acc, radius = 0.011, N = 200, glow = true, opacity = 1 }) => {
    // senoide de A a B (fase global: tramos [s0,s1] distintos empalman sin cortes); set(p) la dibuja de a poco
    const dir = new V().subVectors(B, A), L = dir.length(), u = dir.clone().normalize(), side = up.clone().sub(u.clone().multiplyScalar(up.dot(u))).normalize(), pts = [];
    for (let i = 0; i <= N; i++) { const d = (s0 + (s1 - s0) * i / N) * L; pts.push(A.clone().addScaledVector(u, d).addScaledVector(side, amp * Math.sin(2 * Math.PI * d / lambda))); }
    const path = new THREE.CatmullRomCurve3(pts), g = new THREE.Group(), mk = (r, o, add) => { const m = new THREE.Mesh(new THREE.TubeGeometry(path, N, r, 6, false), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: o, blending: add ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: !add })); g.add(m); return m; };
    const core = mk(radius, opacity, false), halo = glow ? mk(radius * 3.2, 0.16 * opacity, true) : null; scene.add(g);
    const cnt = N * 6 * 6, vis = (p) => { const c = Math.floor(clamp(p) * N) * 36; core.geometry.setDrawRange(0, Math.min(c, cnt)); if (halo) halo.geometry.setDrawRange(0, Math.min(c, cnt)); g.visible = p > 0.001; };
    vis(0); return { group: g, set: vis, opacity: (o) => { core.material.opacity = o; if (halo) halo.material.opacity = 0.16 * o; }, at: (s) => path.getPointAt(clamp(s)), L };
  };
  E.anillo = (color = P.acc, normal = new V(0, 1, 0), grosor = 0.012) => {   // anillo de onda con grosor constante: emitir(p, rmax)
    const m = new THREE.Mesh(new THREE.TorusGeometry(1, 0.01, 6, 128), E.basic(color, 0)); m.quaternion.setFromUnitVectors(new V(0, 0, 1), normal.clone().normalize()); m.visible = false; scene.add(m); let last = -1;
    return { mesh: m, emitir(p, rmax = 2, centro) { if (centro) m.position.copy(centro); if (p <= 0 || p >= 1) { m.visible = false; return 0; } const r = 0.06 + p * rmax;
      if (Math.abs(r - last) > 0.004) { m.geometry.dispose(); m.geometry = new THREE.TorusGeometry(1, grosor / r, 6, 128); last = r; } m.scale.setScalar(r); m.material.opacity = (1 - p) * 0.95; m.visible = true; return r; } };
  };

  // ---------- cámara y dibujo ----------
  E.ruta = (t, K) => {   // K = [{ t, p:[x,y,z], l:[x,y,z], e }]: de cada punto al siguiente con la easing `e` del destino
    let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], k = (EASE[b.e || 'io'])(clamp((t - a.t) / Math.max(1e-6, b.t - a.t)));
    const mix = (u, v) => u.map((x, j) => x + (v[j] - x) * k);
    cam.position.set(...mix(a.p, b.p)); cam.lookAt(...mix(a.l, b.l));
  };
  E.label = (el, v, dx = 0, dyp = 0) => {   // ubica un elemento HTML (position:absolute) sobre un punto 3D
    cam.updateMatrixWorld();   // la matriz de la cámara se actualiza al renderizar: sin esto el rótulo usa la del cuadro anterior
    const p = v.clone().project(cam); el.style.left = ((p.x * 0.5 + 0.5) * 1080 + dx) + 'px'; el.style.top = ((-p.y * 0.5 + 0.5) * 1920 + dyp) + 'px'; };
  E.animar = (tl, dur, fn) => {
    const st = { t: 0 }, draw = () => { fn(st.t); renderer.render(scene, cam); };
    tl.to(st, { t: dur, duration: dur, ease: 'none', onUpdate: draw }, 0); draw();
  };
  return E;
}
