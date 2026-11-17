#!/usr/bin/env python3
"""Revisa un video contra las reglas del canal que se pueden chequear SIN mirar la imagen (CLAUDE.md, docs/1-canal/PREFERENCIAS.md).
Uso: python engine/verificar.py videos/<video> [--guion]      (lo corre `python engine/reel.py revisar videos/<video>`)
  --guion   solo lo que se puede revisar antes de animar (guion, voz, CTA): para el checkpoint con Ayrton.
Salida:  ✕ = error (hay que corregirlo antes de renderizar)   ⚠ = aviso (mirarlo; se puede justificar)   ✓ = bien.
Lo que NO revisa (se mira en los cuadros): encuadre, texto pisado, palabras sueltas, que se entienda."""
import json, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
# números del canal (si cambian, cambian acá y en docs/3-guion/GUION.md)
PAL_S_MAX, PAL_S_META = 2.9, (2.4, 2.8)        # palabras por segundo del video completo (medido en los reels que funcionaron: 2,4–2,9)
HOOK_MAX_PAL, HOOK_MAX_S = 10, 3.5             # el gancho: ≤ 10 palabras y dicho antes de los 3,5 s
FRASE_MAX_PAL = 16                             # frases cortas (ideal ≤ 12)
DUR = (25, 65)                                 # duración razonable de un reel (s)
MULETILLAS = ['sabías que', 'en el mundo de', 'imaginá', 'imagina ', 'sumérgete', 'sumergite', 'desbloqueá', 'aquí está la clave', 'lo mejor de todo',
              'no vas a creer', 'esto cambia todo', 'el 99', 'hoy vamos a ver', 'en este video']
PROHIBIDO_JS = {r'Math\.random\s*\(': 'Math.random() (el render tiene que dar siempre el mismo cuadro)', r'Date\.now\s*\(|new Date\s*\(|performance\.now\s*\(': 'reloj real (Date/performance)',
                r'requestAnimationFrame|setTimeout\s*\(|setInterval\s*\(': 'bucle o temporizador en vivo (todo es función del tiempo T)', r'\bfetch\s*\(|https?://(?!hyperframes\.heygen\.com)': 'red o CDN (todo local)',
                r'<audio\b': '<audio> (el sonido lo mezcla mezcla.py)', r'OrbitControls': 'OrbitControls (la cámara va guionada con E.ruta)'}
PLACEHOLDERS = ['Título del video', 'Título de <span', 'URL o tema de origen', 'AAAA-MM']

norm = lambda x: re.sub(r'[^a-z0-9ñ ]', '', unicodedata.normalize('NFD', x.lower().replace('ñ', '\0')).encode('ascii', 'ignore').decode().replace('\0', 'ñ'))
npal = lambda x: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', x.lower()).encode('ascii', 'ignore').decode())


def revisar(V, solo_guion=False):
    V = Path(V); E, A, OK = [], [], []
    err, avi, ok = E.append, A.append, OK.append
    cfg = json.loads((V / 'video.json').read_text()); esc = cfg['scenes']; ids = [s['id'] for s in esc]
    total = sum(s['d'] for s in esc); lineas = sorted(cfg.get('voz', {}).get('lineas', []), key=lambda l: l['t'])
    dic = json.loads((RAIZ / 'engine/audio/pronunciacion.json').read_text())
    t0 = {}; acc = 0
    for s in esc: t0[s['id']] = acc; acc += s['d']

    # ---------- guion y voz ----------
    if not lineas: err('video.json no tiene líneas de voz (voz.lineas)')
    texto = ' '.join(l['texto'] for l in lineas); n = len(texto.split()); pps = n / total if total else 0
    if pps > PAL_S_MAX: err(f'ritmo: {n} palabras en {total:.1f} s = {pps:.2f} pal/s (máximo {PAL_S_MAX}). Recortar texto o alargar: entran {int(total * PAL_S_MAX)} palabras')
    elif not PAL_S_META[0] <= pps <= PAL_S_META[1]: avi(f'ritmo: {pps:.2f} pal/s ({n} palabras en {total:.1f} s); la meta es {PAL_S_META[0]}–{PAL_S_META[1]}')
    else: ok(f'ritmo {pps:.2f} pal/s ({n} palabras en {total:.1f} s)')
    if not DUR[0] <= total <= DUR[1]: avi(f'duración {total:.1f} s (lo habitual es {DUR[0]}–{DUR[1]} s)')
    if lineas:
        h = lineas[0]; hn = len(h['texto'].split()); fin = h['t'] + hn / 3.4
        if hn > HOOK_MAX_PAL or fin > HOOK_MAX_S + 0.5: avi(f'gancho largo: {hn} palabras, termina ≈ {fin:.1f} s (meta: ≤ {HOOK_MAX_PAL} palabras y ≤ 3 s) → «{h["texto"]}»')
        else: ok(f'gancho de {hn} palabras')
    for l in lineas:
        if l['escena'] not in ids: err(f'{l["id"]}: la escena "{l["escena"]}" no existe en video.json')
        for fr in re.split(r'(?<=[.!?…])\s+', l['texto']):
            if len(fr.split()) > FRASE_MAX_PAL: avi(f'{l["id"]}: frase de {len(fr.split())} palabras (ideal ≤ 12) → «{fr[:60]}…»')
        for p in dic['prohibidas']:
            if re.search(rf"(?<!\w){re.escape(p['palabra'])}(?!\w)", l['texto'], re.I): err(f'{l["id"]}: la voz dice "{p["palabra"]}" → usar "{p["usar"]}" ({p["motivo"]})')
        for m in MULETILLAS:
            if m in l['texto'].lower(): err(f'{l["id"]}: muletilla de IA «{m.strip()}» → reescribir')
    sinver = sorted({r['de'] for r in dic['reemplazos'] if r.get('estado') != 'ok' and re.search(rf"(?<!\w){re.escape(r['de'])}(?!\w)", texto, re.I)})
    if sinver: avi('pronunciación sin confirmar de oído por Ayrton: ' + ', '.join(sinver) + ' (ofrecerle variantes de audio)')
    # ---------- CTA (marca) ----------
    cta = next((l for l in reversed(lineas) if l['escena'] == ids[-1]), None)
    m = re.search(r'dale me gusta y seguime para aprender mas (de|sobre) (.+)', norm(cta['texto'])) if cta else None
    if ids[-1] != 'cierre': avi(f'la última escena es "{ids[-1]}", no "cierre" (bien solo si el reel termina en bucle, sin CTA)')
    elif not m: err(f'CTA: la última línea de voz tiene que ser "Dale me gusta y seguime para aprender más de/sobre <tema>." → hoy: «{cta["texto"] if cta else "(nada)"}»')
    else:
        ok(f'CTA en la voz: "…aprender más {m.group(1)} {m.group(2).strip()}"')
        c = V / 'compositions/cierre.html'
        if c.exists():
            vis = norm(re.sub(r'<[^>]+>', ' ', re.sub(r'<(style|script)\b.*?</\1>|<!--.*?-->', ' ', c.read_text(), flags=re.S)))
            vis = re.sub(r'\s+', ' ', vis); quiere = f'dale like y seguime para aprender mas {m.group(1)} {m.group(2).strip()}'
            if quiere not in vis: err(f'CTA: el texto de compositions/cierre.html no coincide con la voz. Tiene que decir «{quiere}» (en pantalla "like", en voz "me gusta")')
            else: ok('CTA en pantalla coincide con la voz')
    if re.search(r'guard[aá]lo', texto, re.I): err('la voz dice "guardalo" (no funciona en todas las plataformas)')
    if ids and (ids[0] != 'portada' or abs(esc[0]['d'] - 0.1) > 1e-6): err('la primera escena tiene que ser "portada" con d = 0.1 (fotograma de portada)')
    for p in PLACEHOLDERS:
        if p in json.dumps(cfg, ensure_ascii=False): avi(f'video.json todavía tiene el texto de la plantilla «{p}»')
    g = V / 'guion.md'
    if not g.exists() or 'concepto_unico: ""' in g.read_text(): avi('guion.md sin completar (concepto_unico vacío)')
    if solo_guion: return E, A, OK

    # ---------- configuración de marca ----------
    vz, au = cfg.get('voz', {}), cfg.get('audio', {})
    if vz.get('efecto', 'ninguno') != 'ninguno': err(f'voz.efecto = "{vz.get("efecto")}": la voz va limpia ("ninguno")')
    if 'daniela' not in vz.get('modelo', ''): avi(f'voz.modelo = {vz.get("modelo")} (la voz del canal es Daniela)')
    if 'can-you-hear-the-music' not in au.get('musica', ''): avi(f'audio.musica = {au.get("musica")} (la música firma es can-you-hear-the-music.mp3)')
    elif au.get('musica_desde', 0) != 0: avi('audio.musica_desde ≠ 0: Ayrton quiere la música desde el inicio (los violines)')
    if au.get('loudness', -14) != -14: err('audio.loudness tiene que ser -14 (LUFS)')
    if not cfg.get('subtitulos', {}).get('fondo'): avi('subtitulos.fondo vacío: los subtítulos llevan barra negra')
    # ---------- archivos y tiempos ----------
    for i in ids:
        if not (V / f'compositions/{i}.html').exists(): err(f'falta compositions/{i}.html → python engine/reel.py voz {V}')
    if not (V / 'compositions/subtitulos.html').exists(): err(f'faltan los subtítulos → python engine/reel.py voz {V}')
    tj = V / 'assets/tiempos.js'; idx = (V / 'index.html').read_text(); pal, dichas, por_id = [], {}, {l['id']: l for l in lineas}
    if tj.exists():
        js = tj.read_text(); m = re.search(r'^export const ESC = (\{.*\});$', js, re.M); esc_js = json.loads(m.group(1)) if m else {}
        if list(esc_js) != ids or any(abs(esc_js[i]['d'] - s['d']) > 1e-6 for i, s in zip(ids, esc)): err(f'assets/tiempos.js está viejo respecto de video.json → python engine/reel.py voz {V}')
        m = re.search(r'^export const PAL = (\[.*\]);$', js, re.M); pal = json.loads(m.group(1)) if m else []
        if not pal: err(f'assets/tiempos.js no tiene los tiempos por palabra → python engine/reel.py voz {V}')
        dichas = {}
        for l, w, a, b in pal: dichas.setdefault(l, []).append(npal(w))
        for l in lineas:
            if pal and len(dichas.get(l['id'], [])) != len(l['texto'].split()): err(f'{l["id"]}: el texto cambió después de generar la voz → python engine/reel.py voz {V}')
    elif 'ESCENAS:INICIO' in idx: err(f'falta assets/tiempos.js → python engine/reel.py voz {V}')
    mdur = re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', idx)
    if mdur and abs(float(mdur.group(1)) - total) > 0.01: err(f'index.html dura {mdur.group(1)} s y video.json {total:g} s → python engine/reel.py voz {V}')
    # ---------- código propio del video (lo que se escribe en cada reel) ----------
    BASE = {p.name for p in (RAIZ / 'videos/_plantilla/assets').glob('*') if p.name not in ('set.js',)} | {'tiempos.js'}
    propios = [p for p in list((V / 'compositions').glob('*.html')) + list((V / 'assets').glob('*.js')) if p.name not in BASE and p.name != 'subtitulos.html']
    ids_html = {}
    for p in propios:
        src = p.read_text(); rel = p.relative_to(V); cod = re.sub(r'/\*.*?\*/|<!--.*?-->|(?<![:\'"])//[^\n]*', '', src, flags=re.S)
        for rx, que in PROHIBIDO_JS.items():
            if re.search(rx, cod): err(f'{rel}: usa {que}')
        if re.search(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b(?![0-9a-zA-Z_-])', re.sub(r'#(root|[a-zA-Z][\w-]*)', lambda m: m.group(0) if re.fullmatch(r'#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}', m.group(0)) else '', cod)) or re.search(r'\b0x[0-9a-fA-F]{6}\b', cod) or re.search(r'rgba?\((?!0,\s*0,\s*0)', cod):
            avi(f'{rel}: tiene un color escrito a mano; usar var(--acc), var(--muted)… en HTML y P.acc, P.edge, P.hi… en 3D (docs/2-estilo/ESTILO.md)')
        for m in re.finditer(r'font(?:-size)?:[^;"\']*?\b(\d+)px', cod):
            if int(m.group(1)) < 36: avi(f'{rel}: texto de {m.group(1)} px (mínimo legible en el celular: 40 px)'); break
        if re.search(r'text-transform:\s*uppercase', cod) and re.search(r'letter-spacing:\s*\.?0?\.[1-9]', cod): err(f'{rel}: mayúsculas con espaciado amplio (se ve "hecho por IA")')
        if re.search(r'scanline|scan-line', cod, re.I): err(f'{rel}: líneas de escaneo (prohibidas)')
        if p.suffix == '.html':
            css = ' '.join(re.findall(r'<style>(.*?)</style>', src, re.S))
            if re.search(r'(?<![-\w])transform\s*:', css): err(f'{rel}: `transform` en CSS (lo prohíbe HyperFrames; mover con GSAP o con E.label)')
            for i in re.findall(r'\bid="([^"]+)"', src):
                if i != 'root' and i in ids_html and ids_html[i] != rel: avi(f'id="{i}" repetido en {ids_html[i]} y {rel} (los ids llevan prefijo de escena)')
                ids_html[i] = rel
            if p.stem in ids and "window.__timelines['" + p.stem + "']" not in src and 'window.__timelines["' + p.stem + '"]' not in src and 'montar(root, tl' not in src and 'plano(root, tl' not in src:
                err(f'{rel}: no registra su timeline (window.__timelines["{p.stem}"])')
        for l, w in re.findall(r'''(?:cuando|hasta)\(\s*['"](\w+)['"]\s*(?:,\s*['"]([^'"]+)['"])?''', cod):
            if l not in por_id: err(f'{rel}: cuando("{l}") → esa línea de voz no existe')
            elif w and pal and npal(w) not in dichas.get(l, []): err(f'{rel}: cuando("{l}", "{w}") → la línea {l} no dice "{w}" («{por_id[l]["texto"]}»)')
        if re.search(r'montar\(root,\s*tl,\s*[\d.]', cod): avi(f'{rel}: tiempos escritos a mano en montar(); usar el plano estándar (se borra el archivo y lo regenera reel.py voz)')
    todo = '\n'.join(p.read_text() for p in propios)
    visible = re.sub(r'/\*.*?\*/|<!--.*?-->', '', todo, flags=re.S)
    if len(re.findall(r'@ayrtonnacer', visible)) < 2: err('la firma @ayrtonnacer tiene que estar al inicio (gancho) y al final (cierre)')
    if re.search(r'@ayrtonnacer\s*[.·•]', visible): err('la firma va sola, sin punto ni adorno')
    for p in PLACEHOLDERS[:2]:
        if p in visible: avi(f'queda el texto de la plantilla «{p}» en pantalla')
    # ---------- sonido ----------
    s = V / 'sfx_events.py'
    if s.exists():
        src = re.sub(r'""".*?"""|#[^\n]*', '', s.read_text(), flags=re.S)
        if not (('apertura()' in src and 'cierre(' in src) or ("propio('boom-cinematico')" in src and "propio('chinn')" in src)): err('sfx_events.py: faltan los sonidos de marca (P.apertura() = boom en 0 s; P.cierre(...) = boom + chinn en el CTA)')
        for i in re.findall(r"S\[['\"](\w+)['\"]\]", src):
            if i not in ids: err(f'sfx_events.py usa la escena "{i}", que no está en video.json')
        for l, w in re.findall(r'''cuando\(\s*['"](\w+)['"]\s*(?:,\s*['"]([^'"]+)['"])?''', src):
            if l not in por_id: err(f'sfx_events.py: cuando("{l}") → esa línea no existe')
            elif w and pal and npal(w) not in dichas.get(l, []): err(f'sfx_events.py: cuando("{l}", "{w}") → la línea {l} no dice "{w}"')
        if re.search(r'\bglitch\(|ambient\(', src): avi('sfx_events.py usa glitch() o ambiente: Ayrton pidió sonido limpio')
    else: err('falta sfx_events.py')
    if not (RAIZ / 'assets/sfx/whoosh').exists() and not list((RAIZ / 'assets/sfx').glob('*/*/*')):
        avi('el banco de efectos reales no está bajado (se usarán los sintéticos) → bash engine/audio/bajar_sfx.sh')
    pl = V / 'plan.md'
    if not pl.exists() or '___' in pl.read_text(): avi('plan.md sin completar (quedan "___")')
    if not (V / 'descripcion.md').exists(): avi('falta descripcion.md (texto para publicar + créditos)')
    for f in ('escena3d.js', 'movimiento.js', 'marca.css'):
        a, b = V / 'assets' / f, RAIZ / 'videos/_plantilla/assets' / f
        if a.exists() and b.exists() and a.read_bytes() != b.read_bytes(): avi(f'assets/{f} es distinto del de la plantilla (bien si es a propósito; si se mejoró la librería, llevar el cambio a videos/_plantilla)')
    return E, A, OK


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1: sys.exit(__doc__)
    E, A, OK = revisar(args[0], '--guion' in sys.argv)
    for x in OK: print('  ✓', x)
    for x in A: print('  ⚠', x)
    for x in E: print('  ✕', x)
    print(f'\n{len(E)} error(es), {len(A)} aviso(s).' + (' Corregir los ✕ antes de seguir.' if E else ' Sin errores.'))
    sys.exit(1 if E else 0)


if __name__ == '__main__': main()
