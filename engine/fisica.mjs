// Hornea una simulación de física (Rapier) a un JSON que la escena 3D reproduce como función del tiempo.
// Uso:  node engine/fisica.mjs videos/X/fisica.mjs [salida.json]   (por defecto videos/X/assets/fisica.json)
// El spec exporta { dur, fps?, gravedad?, crear(R, w) -> { nombre: RigidBody } }. Ver docs/FISICA.md.
import { pathToFileURL } from 'node:url';
import { writeFileSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import RAPIER from '@dimforge/rapier3d-compat';

const [specPath, outArg] = process.argv.slice(2);
if (!specPath) { console.error('uso: node engine/fisica.mjs videos/X/fisica.mjs [salida.json]'); process.exit(1); }
await RAPIER.init({});
const spec = (await import(pathToFileURL(resolve(specPath)).href)).default;
const fps = spec.fps ?? 60, dt = 1 / fps, n = Math.ceil(spec.dur * fps) + 1;
const w = new RAPIER.World({ x: 0, y: spec.gravedad ?? -9.81, z: 0 });
w.timestep = dt;
const cuerpos = spec.crear(RAPIER, w);
const nombres = Object.keys(cuerpos), porHandle = new Map();
for (const k of nombres) {
  const rb = cuerpos[k];
  for (let i = 0; i < rb.numColliders(); i++) porHandle.set(rb.collider(i).handle, k);
}
w.forEachCollider(c => c.setActiveEvents(RAPIER.ActiveEvents.COLLISION_EVENTS));
const q = new RAPIER.EventQueue(true), r4 = x => Math.round(x * 1e4) / 1e4;
const pose = Object.fromEntries(nombres.map(k => [k, []])), eventos = [];
const guardar = () => nombres.forEach(k => { const p = cuerpos[k].translation(), o = cuerpos[k].rotation(); pose[k].push(r4(p.x), r4(p.y), r4(p.z), r4(o.x), r4(o.y), r4(o.z), r4(o.w)); });
guardar();
for (let f = 1; f < n; f++) {
  w.step(q);
  q.drainCollisionEvents((h1, h2, ini) => {
    if (!ini) return;
    const a = porHandle.get(h1) ?? 'mundo', b = porHandle.get(h2) ?? 'mundo';
    const sp = k => { const v = cuerpos[k]?.linvel(); return v ? Math.hypot(v.x, v.y, v.z) : 0; };
    eventos.push({ t: r4(f * dt), a, b, v: r4(Math.max(sp(a), sp(b))) });   // v = velocidad del choque (m/s): sirve para el volumen del efecto
  });
  guardar();
}
const out = outArg ?? join(dirname(resolve(specPath)), 'assets', 'fisica.json');
writeFileSync(out, JSON.stringify({ fps, n, cuerpos: pose, eventos }));
console.log(`${nombres.length} cuerpos · ${n} cuadros a ${fps} fps · ${eventos.length} choques → ${out}`);
