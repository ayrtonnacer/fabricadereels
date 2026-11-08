// Servidor estático de la raíz del repo (lo usan render.mjs y el visor). Solo lectura, solo archivos dentro del repo.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

export const REPO = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.woff2': 'font/woff2', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };

export function servir(puerto = 0, host = '127.0.0.1') {
  const srv = http.createServer((req, res) => {
    const url = req.url.split('?')[0];
    if (url === '/') { res.writeHead(302, { Location: '/engine/visor.html' }); return res.end(); }
    if (url === '/__videos') {                  // lista para el visor: carpetas de videos/ con video.json
      const vs = fs.readdirSync(path.join(REPO, 'videos')).filter(d => fs.existsSync(path.join(REPO, 'videos', d, 'video.json'))).sort()
        .map(d => { const c = JSON.parse(fs.readFileSync(path.join(REPO, 'videos', d, 'video.json'), 'utf8')); return { v: `videos/${d}`, titulo: c.titulo || d, final: fs.existsSync(path.join(REPO, 'videos', d, 'final.mp4')) }; });
      res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify(vs));
    }
    const p = path.join(REPO, decodeURIComponent(url));
    if (!p.startsWith(REPO + path.sep) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    const tam = fs.statSync(p).size, tipo = TIPOS[path.extname(p)] || 'application/octet-stream', rango = req.headers.range;
    if (rango) {                               // rangos: el visor necesita poder saltar dentro del audio
      const [a, b] = rango.replace('bytes=', '').split('-'), ini = +a, fin = b ? +b : tam - 1;
      res.writeHead(206, { 'Content-Type': tipo, 'Content-Range': `bytes ${ini}-${fin}/${tam}`, 'Accept-Ranges': 'bytes', 'Content-Length': fin - ini + 1 });
      return fs.createReadStream(p, { start: ini, end: fin }).pipe(res);
    }
    res.writeHead(200, { 'Content-Type': tipo, 'Content-Length': tam, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(puerto, host, () => r(srv)));
}
