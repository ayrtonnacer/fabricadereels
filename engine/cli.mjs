#!/usr/bin/env node
// reel — la herramienta de línea de comandos de la fábrica. Un solo punto de entrada para todo el flujo.
//   npx reel <comando> …      (o: node engine/cli.mjs <comando> …)
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { REPO, servir } from './servidor.mjs';

const AYUDA = `reel — fábrica de reels de @ayrtonnacer

  reel nuevo <tema> [--titulo "…"]     copia la plantilla a videos/AAAA-MM-<tema>
  reel revisar <video> [--quietud]     chequeos antes de renderizar (reglas, determinismo, tramos quietos)
  reel ver <video> [--puerto 8080]     visor en el navegador: reproducir, saltar escenas, cuadro a cuadro
  reel preview <video> <t> [<t>…]      cuadros sueltos → <video>/frames/ (mirarlos siempre)
  reel render <video> [escenas…]       todo: revisar → voz → efectos → escenas → unir → mezcla → final.mp4
  reel voz | efectos | mezcla <video>  un paso suelto del audio
  reel analizar <archivo> [--nombre x] video de referencia → referencias/x/analisis.md
  reel ayuda

<video> es la carpeta (videos/2026-11-tema) o solo su nombre (2026-11-tema).
Variables: WORKERS=n (render en paralelo), GPU=1 (usar la GPU real), PYTHON=python3.`;

const PY = process.env.PYTHON || 'python3';
const [cmd, ...args] = process.argv.slice(2);
const bandera = (n, def = null) => { const i = args.indexOf(n); return i < 0 ? def : (args[i + 1] && !args[i + 1].startsWith('--') ? args.splice(i, 2)[1] : (args.splice(i, 1), true)); };

function video(a) {
  if (!a) salir('Falta el video. Ej.: reel revisar videos/2026-11-tema');
  for (const p of [a, path.join(REPO, a), path.join(REPO, 'videos', a)]) if (fs.existsSync(path.join(p, 'video.json'))) return path.resolve(p);
  salir(`No encuentro ${a} (busco una carpeta con video.json)`);
}
function salir(m, c = 1) { console.error(m); process.exit(c); }
function correr(prog, argv, { opcional = false } = {}) {
  const r = spawnSync(prog, argv, { stdio: 'inherit', cwd: REPO });
  if (r.status !== 0 && !opcional) salir(`✕ falló: ${prog} ${argv.join(' ')}`, r.status || 1);
  return r.status === 0;
}
const paso = m => console.log(`\n── ${m}`);

switch (cmd) {
  case 'nuevo': {
    const tema = args[0]; if (!tema) salir('reel nuevo <tema>');
    const titulo = bandera('--titulo', tema), hoy = new Date().toISOString().slice(0, 7);   // CLI, no render: el reloj acá está bien
    const dst = path.join(REPO, 'videos', `${hoy}-${tema.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`);
    if (fs.existsSync(dst)) salir(`Ya existe ${path.relative(REPO, dst)}`);
    fs.cpSync(path.join(REPO, 'videos/_plantilla'), dst, { recursive: true, filter: s => !/\/(out|frames|audio)(\/|$)|\.mp4$/.test(s) });
    const vj = path.join(dst, 'video.json'), cfg = JSON.parse(fs.readFileSync(vj, 'utf8'));
    cfg.titulo = titulo; cfg.fecha = hoy; fs.writeFileSync(vj, JSON.stringify(cfg, null, 1) + '\n');
    const ih = path.join(dst, 'index.html'); fs.writeFileSync(ih, fs.readFileSync(ih, 'utf8').replace(/<title>[^<]*<\/title>/, `<title>${titulo}</title>`));
    console.log(`✓ ${path.relative(REPO, dst)}\n  1) escribir el guion en guion.md y aprobarlo  2) video.json  3) index.html  4) reel revisar  5) reel ver / preview  6) reel render`);
    break;
  }
  case 'revisar': correr(PY, ['engine/revisar.py', video(args[0]), ...args.slice(1)]); break;
  case 'preview': correr('node', ['engine/render.mjs', video(args[0]), 'preview', ...args.slice(1)]); break;
  case 'voz': correr(PY, ['engine/audio/voz.py', video(args[0])]); break;
  case 'efectos': case 'sfx': correr(PY, ['engine/audio/sfx.py', video(args[0])]); break;
  case 'mezcla': correr(PY, ['engine/audio/mezcla.py', video(args[0])]); break;
  case 'analizar': correr(PY, ['engine/analizar_video.py', ...args]); break;
  case 'ver': {
    const v = video(args[0]), puerto = +bandera('--puerto', 8080), host = bandera('--host', '127.0.0.1');
    await servir(puerto, host);
    console.log(`Visor: http://${host === '0.0.0.0' ? 'localhost' : host}:${puerto}/engine/visor.html?v=${path.relative(REPO, v)}\n(ctrl+c para cerrar)`);
    break;
  }
  case 'render': {
    const v = video(args[0]), escenas = args.slice(1).filter(a => !a.startsWith('--')), cfg = JSON.parse(fs.readFileSync(path.join(v, 'video.json'), 'utf8'));
    paso('revisar'); correr(PY, ['engine/revisar.py', v]);
    const modelo = path.join(REPO, 'assets/voces/es_AR-daniela-high.onnx');
    if (cfg.voz?.lineas?.length) {
      paso('voz');
      if (fs.existsSync(modelo)) correr(PY, ['engine/audio/voz.py', v]);
      else console.log(`· falta el modelo de voz (${path.relative(REPO, modelo)}): ${fs.existsSync(path.join(v, 'audio/voz.wav')) ? 'uso la voz.wav que ya estaba' : 'el video sale sin voz'}`);
    }
    if (fs.existsSync(path.join(v, 'sfx_events.py'))) { paso('efectos'); correr(PY, ['engine/audio/sfx.py', v]); }
    paso(escenas.length ? `escenas ${escenas.join(' ')}` : 'escenas (todas)'); correr('node', ['engine/render.mjs', v, 'scenes', ...escenas]);
    paso('unir'); correr('node', ['engine/render.mjs', v, 'join']);
    paso('mezcla'); if (!correr(PY, ['engine/audio/mezcla.py', v], { opcional: true })) console.log('· sin audio: queda out/mudo.mp4');
    const fin = path.join(v, 'final.mp4');
    console.log(fs.existsSync(fin) ? `\n✓ ${path.relative(REPO, fin)}` : `\n✓ ${path.relative(REPO, path.join(v, 'out/mudo.mp4'))} (sin audio)`);
    break;
  }
  case undefined: case 'ayuda': case '-h': case '--help': console.log(AYUDA); break;
  default: salir(`Comando desconocido: ${cmd}\n\n${AYUDA}`);
}
