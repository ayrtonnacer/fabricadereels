#!/usr/bin/env node
// Render determinístico: abre la página del video, avanza window.__render(t) cuadro a cuadro y codifica con ffmpeg.
//   node engine/render.mjs <video-dir> preview 1.5 20 40      -> <video-dir>/frames/preview_<t>.jpg   (revisar SIEMPRE antes del render completo)
//   node engine/render.mjs <video-dir> scenes [s1 s5 ...]      -> <video-dir>/out/<id>.mp4  (un archivo por escena; sin ids = todas)
//   node engine/render.mjs <video-dir> join                    -> <video-dir>/out/mudo.mp4  (concat sin recodificar)
// Variables: WORKERS (default: núcleos, entre 2 y 4), GPU=1 (usar GPU real en vez de SwiftShader).
import { createRequire } from 'node:module';
import os from 'node:os';
import { servir, REPO } from './servidor.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { Buffer } from 'node:buffer';
const { chromium } = createRequire(import.meta.url)('playwright');

const [dirArg, mode, ...args] = process.argv.slice(2);
if (!dirArg || !mode) { console.error(fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1, 7).join('\n')); process.exit(1); }
const VDIR = path.resolve(dirArg);
const REL = path.relative(REPO, VDIR);
const FPS = 30, W = 1080, H = 1920;
const OUT = path.join(VDIR, 'out'), FR = path.join(VDIR, 'frames');
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(FR, { recursive: true });

if (mode === 'join') {
  const cfg = JSON.parse(fs.readFileSync(path.join(VDIR, 'video.json'), 'utf8'));
  const list = cfg.scenes.map(s => { const f = path.join(OUT, `${s.id}.mp4`); if (!fs.existsSync(f)) { console.error('falta', f); process.exit(1); } return `file '${f}'`; }).join('\n');
  fs.writeFileSync(path.join(OUT, 'list.txt'), list);
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(OUT, 'list.txt'), '-c', 'copy', path.join(OUT, 'mudo.mp4')], { stdio: 'inherit' });
  process.exit(r.status ?? 1);
}

const server = await servir();
const port = server.address().port;
const launch = process.env.GPU ? {} : { args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] };
const browser = await chromium.launch(launch);
async function newPage() {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error') console.error('[page]', m.text()); });
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  await page.goto(`http://127.0.0.1:${port}/${REL}/index.html`);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 90000 });
  page._cdp = await page.context().newCDPSession(page);   // captura directa de Chrome: ~20 % más rápida que page.screenshot
  return page;
}

if (mode === 'preview') {
  const page = await newPage();
  for (const t of args) {
    await page.evaluate(t => window.__render(t), +t);
    await page.screenshot({ path: path.join(FR, `preview_${t}.jpg`), type: 'jpeg', quality: 92 });
  }
} else if (mode === 'scenes') {
  const probe = await newPage();
  let scenes = await probe.evaluate(() => window.__scenes);
  await probe.close();
  if (args.length) scenes = scenes.filter(s => args.includes(s.id));
  const queue = [...scenes];
  async function worker() {
    const page = await newPage();
    while (queue.length) {
      const s = queue.shift(), n = Math.round(s.d * FPS), tmp = path.join(OUT, `${s.id}.part.mp4`);
      const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
      const done = new Promise(r => ff.on('exit', r)); const t0 = Date.now();
      for (let i = 0; i < n; i++) {
        await page.evaluate(t => window.__render(t), s.t0 + i / FPS);     // t = cuadro / fps: nunca el reloj
        const buf = Buffer.from((await page._cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92 })).data, 'base64');
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      }
      ff.stdin.end();
      if ((await done) === 0) { fs.renameSync(tmp, path.join(OUT, `${s.id}.mp4`)); console.log(`${s.id}: ${n} cuadros en ${((Date.now() - t0) / 1000).toFixed(1)}s`); }
      else console.error(`${s.id}: ffmpeg falló`);
    }
  }
  await Promise.all(Array.from({ length: +(process.env.WORKERS || Math.max(2, Math.min(4, os.cpus().length))) }, worker));
}
await browser.close(); server.close();
