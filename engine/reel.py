#!/usr/bin/env python3
"""Un comando por etapa para hacer un reel (paso a paso en docs/5-tecnica/FLUJO.md). Desde la raíz del repo:

  python engine/reel.py nuevo AAAA-MM-tema       crea videos/AAAA-MM-tema desde la plantilla
  python engine/reel.py guion videos/X           revisa SOLO guion y voz (ritmo, gancho, CTA, palabras prohibidas): antes del OK de Ayrton
  python engine/reel.py voz videos/X             voz (Piper) + subtítulos + tiempos (index.html, assets/tiempos.js, planos que falten)
  python engine/reel.py revisar videos/X         reglas del canal (verificar.py) + contrato de HyperFrames (check)
  python engine/reel.py cuadros videos/X [t,t…]  cuadros clave en UNA hoja (out/cuadros/contact-sheet.jpg). MIRARLA antes de renderizar
  python engine/reel.py encuadre "px,py,pz" "lx,ly,lz" "x,y,z" […]   dónde cae en pantalla un punto 3D con esa cámara (sin renderizar)
  python engine/reel.py render videos/X          efectos + render mudo + mezcla → final.mp4
  python engine/reel.py audio videos/X           solo efectos + mezcla (si cambió el sonido y no la imagen)
  python engine/reel.py medir videos/X           mide final.mp4 y lo compara con las metas (cámara, continuidad, graves, volumen)
  python engine/reel.py entregar videos/X        copia liviana + portada + medición a docs/4-referencias/propios/ y lista lo que falta
  python engine/reel.py estado [--json] [--guardar]   tabla de todos los videos y su etapa; --guardar la escribe en videos/estado.json (la lee el panel/CRM)
"""
import json, math, os, re, shutil, subprocess, sys, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]; PY = sys.executable; E = RAIZ / 'engine'


def run(cmd, cwd=RAIZ, ok=(0,)):
    print('\n$ ' + ' '.join(str(c) for c in cmd)); r = subprocess.run([str(c) for c in cmd], cwd=cwd)
    if r.returncode not in ok: sys.exit(f'\n✕ falló: {" ".join(str(c) for c in cmd)} (corregir y volver a correr este paso)')
    return r.returncode


def video(arg):
    V = Path(arg) if Path(arg).is_dir() else RAIZ / 'videos' / arg
    if not (V / 'video.json').exists(): sys.exit(f'no encuentro {arg}/video.json (videos: {", ".join(p.parent.name for p in sorted((RAIZ / "videos").glob("*/video.json")))})')
    return V.resolve()


def cfg(V): return json.loads((V / 'video.json').read_text())
def dur(V): return sum(s['d'] for s in cfg(V)['scenes'])


def c_nuevo(a): run(['bash', E / 'nuevo.sh', a[0]])
def c_guion(a): run([PY, E / 'verificar.py', video(a[0]), '--guion'])


def c_voz(a):
    V = video(a[0]); run([PY, E / 'audio/voz.py', V]); run([PY, E / 'subtitulos.py', V]); run([PY, E / 'tiempos.py', V])
    print('\nSi voz.py marcó ⚠ (una línea se pasa de su escena o pisa a otra): ajustar "t" o "d" en video.json y volver a correr este comando.')


def c_revisar(a):
    V = video(a[0]); r = run([PY, E / 'verificar.py', V], ok=(0, 1)); run(['npx', 'hyperframes', 'check'], cwd=V)
    if r: sys.exit('\n✕ verificar.py encontró errores (arriba).')


def tiempos_clave(V):
    """Cuadros que hay que mirar: el 0 (miniatura), el inicio y el medio de cada escena, la mitad de cada frase de voz y el final."""
    c = cfg(V); ts, t = {0.0}, 0.0
    for s in c['scenes']:
        if s['d'] > 0.3: ts |= {round(t + 0.1, 2), round(t + s['d'] / 2, 2)}
        t += s['d']
    for l in c.get('voz', {}).get('lineas', []): ts.add(round(l['t'] + 1.0, 2))
    ts.add(round(t - 0.4, 2)); ts = sorted(x for x in ts if 0 <= x < t)
    out = []
    for x in ts:   # no dos cuadros a menos de 0,6 s (salvo el 0)
        if not out or x - out[-1] >= 0.6: out.append(x)
    return out


def c_cuadros(a):
    V = video(a[0]); ts = a[1] if len(a) > 1 else ','.join(f'{x:g}' for x in tiempos_clave(V))
    run(['npx', 'hyperframes', 'snapshot', '--at', ts, '--no-end', '-o', 'out/cuadros'], cwd=V)
    print(f'\nMIRAR: {V / "out/cuadros/contact-sheet.jpg"}  (y cada cuadro en out/cuadros/). Lista de qué mirar: docs/5-tecnica/FLUJO.md → paso 7.')


def c_encuadre(a):
    """Proyección igual a la de escena3d.js (FOV vertical 40°, imagen subida dy = 170 px)."""
    v = lambda s: [float(x) for x in s.split(',')]
    p, l, pts = v(a[0]), v(a[1]), [v(x) for x in a[2:]]; dy = float(os.environ.get('DY', 170))
    sub = lambda u, w: [u[i] - w[i] for i in range(3)]; dot = lambda u, w: sum(u[i] * w[i] for i in range(3))
    def nrm(u): n = math.sqrt(dot(u, u)); return [x / n for x in u]
    cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
    f = nrm(sub(l, p)); r = nrm(cross(f, [0, 1, 0])); u = cross(r, f); tg = math.tan(math.radians(20))
    print(f'cámara en {p} mirando a {l}  (zona segura de la imagen: x 60–1020, y 200–1100; subtítulos en y 1120–1320)')
    for q in pts:
        d = sub(q, p); z = dot(d, f)
        if z <= 0: print(f'  {q} → detrás de la cámara'); continue
        x, y = (dot(d, r) / (z * tg * 1080 / 1920) * .5 + .5) * 1080, (-dot(d, u) / (z * tg) * .5 + .5) * 1920 - dy
        est = 'ok' if 60 <= x <= 1020 and 200 <= y <= 1100 else 'FUERA DE CUADRO' if not (0 <= x <= 1080 and 0 <= y <= 1920) else 'fuera de la zona segura'
        print(f'  {q} → x {x:6.0f}  y {y:6.0f}  a {z:5.2f} m  {est}')


def c_audio(a):
    V = video(a[0]); run([PY, E / 'audio/sfx.py', V]); run([PY, E / 'audio/mezcla.py', V])


def c_render(a):
    V = video(a[0]); r = run([PY, E / 'verificar.py', V], ok=(0, 1))
    if r and '--igual' not in a: sys.exit('\n✕ hay errores de verificar.py: corregirlos antes de renderizar (o agregar --igual para renderizar una prueba)')
    (V / 'out').mkdir(exist_ok=True); t0 = time.time()
    run(['npx', 'hyperframes', 'render', '--workers', '4', '-o', 'out/mudo.mp4'], cwd=V); seg = time.time() - t0; d = dur(V)
    print(f'\nrender: {seg:.0f} s para {d:.1f} s de video = {seg / d:.1f} s por segundo' + ('  ⚠ más de 3: simplificar el set (docs/5-tecnica/THREEJS.md)' if seg / d > 3 else ''))
    c_audio(a)


def c_medir(a):
    V = video(a[0]); f = V / 'final.mp4'
    if not f.exists(): sys.exit(f'falta {f} → python engine/reel.py render {a[0]}')
    an = V / 'analisis'; an.mkdir(exist_ok=True); tr = an / 'transcripcion.txt'
    tr.write_text(' '.join(l['texto'] for l in cfg(V)['voz']['lineas']))
    run([PY, E / 'analisis/medir.py', f, an, '--transcripcion', tr]); run([PY, E / 'analisis/comparar.py', an / 'metricas.json'], ok=(0, 1))
    run([PY, E / 'analisis/arrastre.py', f, '--escenas', V / 'video.json'], ok=(0, 1)); run([PY, E / 'analisis/barro.py', f], ok=(0, 1))
    if '--escuchar' in a: run([PY, E / 'audio/escuchar.py', f, '--video', V], ok=(0, 1))
    print('\nLas metas son una ALARMA, no un objetivo: lo que queda fuera se justifica en plan.md o se corrige (docs/5-tecnica/MEDICION.md).'
          '\nPronunciación (baja un modelo la 1.ª vez): python engine/reel.py medir ' + a[0] + ' --escuchar')


def c_entregar(a):
    V = video(a[0]); f = V / 'final.mp4'; falta = []
    if not f.exists(): sys.exit(f'falta {f}')
    D = RAIZ / 'docs/4-referencias/propios' / V.name; D.mkdir(parents=True, exist_ok=True)
    q = lambda *x: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *[str(i) for i in x]], check=True)
    q('-i', f, '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '30', '-preset', 'slow', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', D / 'final-960.mp4')
    q('-i', f, '-frames:v', '1', '-q:v', '2', D / 'portada.jpg'); shutil.copy(D / 'portada.jpg', V / 'portada.jpg')
    for n in ('metricas.json', 'INFORME.md', 'hoja_resumen.jpg'):
        if (V / 'analisis' / n).exists(): shutil.copy(V / 'analisis' / n, D / n)
        elif n == 'metricas.json': falta.append(f'medir el reel: python engine/reel.py medir {a[0]}')
    if not (V / 'descripcion.md').exists(): falta.append('descripcion.md (texto para publicar, fuentes y créditos: voz Piper es_AR-daniela, CC BY-SA 4.0)')
    r = subprocess.run([PY, E / 'verificar.py', V], capture_output=True, text=True)
    if r.returncode: falta.append('verificar.py tiene errores: python engine/reel.py revisar ' + a[0])
    print(f'copia liviana y portada en {D.relative_to(RAIZ)}/  ·  portada también en {V.name}/portada.jpg')
    print('Antes de darlo por terminado:\n' + '\n'.join(f'  ☐ {x}' for x in falta + [
        'repasar docs/1-canal/PREFERENCIAS.md contra el video', 'correcciones de Ayrton → docs/1-canal/BITACORA.md + PREFERENCIAS.md (y DECISIONES.md)',
        'palabras nuevas → engine/audio/pronunciacion.json', 'estado del video en video.json ("listo"), fila en videos/LEEME.md y `python engine/reel.py estado --guardar`', 'commit y push']))


def c_estado(a):
    filas = []
    for vj in sorted((RAIZ / 'videos').glob('*/video.json')) + sorted((RAIZ / 'videos/_archivo').glob('*/video.json')):
        V = vj.parent
        if V.name == '_plantilla': continue
        c = json.loads(vj.read_text()); d = sum(s['d'] for s in c['scenes']); pub = c.get('publicar', {})
        etapa = c.get('estado') or ('archivo' if V.parent.name == '_archivo' else 'final' if (V / 'final.mp4').exists() else 'animado' if (V / 'compositions').exists() else 'guion')
        filas.append({'video': V.name, 'titulo': c.get('titulo', ''), 'estado': etapa, 'duracion_s': round(d, 1), 'final_mp4': (V / 'final.mp4').exists(),
                      'descripcion': (V / 'descripcion.md').exists(), 'publicar': pub, 'carpeta': str(V.relative_to(RAIZ))})
    if '--guardar' in a: (RAIZ / 'videos/estado.json').write_text(json.dumps(filas, ensure_ascii=False, indent=1) + '\n'); print('→ videos/estado.json')
    if '--json' in a: print(json.dumps(filas, ensure_ascii=False, indent=1)); return
    print(f'{"video":32} {"estado":11} {"dur":>6}  mp4  título')
    for f in filas: print(f'{f["video"]:32} {f["estado"]:11} {f["duracion_s"]:6.1f}  {"sí " if f["final_mp4"] else "no "}  {f["titulo"]}')
    print('\n(estados: guion → animando → listo → programado → publicado · archivo = versión vieja. Se cambia en video.json → "estado")')


CMD = {'nuevo': (c_nuevo, 1), 'guion': (c_guion, 1), 'voz': (c_voz, 1), 'revisar': (c_revisar, 1), 'cuadros': (c_cuadros, 1), 'encuadre': (c_encuadre, 3),
       'render': (c_render, 1), 'audio': (c_audio, 1), 'medir': (c_medir, 1), 'entregar': (c_entregar, 1), 'estado': (c_estado, 0)}
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in CMD or len(sys.argv) - 2 < CMD[sys.argv[1]][1]: sys.exit(__doc__)
    CMD[sys.argv[1]][0](sys.argv[2:])
