"""Biblioteca de efectos de sonido sintéticos (sin samples, sin licencias). Estética: informática / radio / ciberseguridad.
Significado de cada sonido (usar siempre igual): whoosh=transición · pop=aparece algo · ding/chime=éxito · alert=aviso ·
buzz/powerdown=error o pérdida · powerup=algo se activa · thunk=confirmación (Enter, enchufar) · tick=tecla/dato ·
glitch=texto que 'tiembla' · riser=progreso · boom=golpe de apertura · sparkle=cierre/logro ·
impact/hit=remarcar una acción · bassdrop=momento épico/cámara lenta · braam=entrada dramática · ambient=base que evita el silencio · reverse(riser)=succión previa a un golpe."""
import numpy as np, wave
from scipy.signal import lfilter
SR = 48000
rng = np.random.default_rng(7)

def tt(d): return np.arange(int(SR*d))/SR
def env(n,a=0.003,d=0.1):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def sweep(f0,f1,d,decay=None,wave_='sine'):
    t=tt(d); f=f0*(f1/f0)**(t/d); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph) if wave_=='sine' else np.sign(np.sin(ph))*0.6
    return s*(env(len(t),0.004,decay or d/3))
def noise(d): return rng.standard_normal(int(SR*d))
def hp(x,a=0.95): return lfilter([1,-1],[1,-a],x)
def lp_sweep(x,c0,c1):
    n=len(x); c=np.linspace(c0,c1,n); a=1-np.exp(-2*np.pi*c/SR); y=np.zeros(n); s=0.0
    for i in range(n): s+=a[i]*(x[i]-s); y[i]=s
    return y
def whoosh(d=0.45,up=True):
    x=noise(d); y=lp_sweep(x,300,5000) if up else lp_sweep(x,5000,300)
    n=len(y); e=np.sin(np.pi*np.arange(n)/n)**2; y=y*e; return y/np.max(np.abs(y))*0.9
def tick():
    d=0.012; x=hp(noise(d))*env(int(SR*d),0.0005,0.003); s=np.sin(2*np.pi*rng.uniform(1500,2300)*tt(d))*env(int(SR*d),0.0005,0.004)
    return (x*0.5+s*0.8)
def thunk():
    s=sweep(180,70,0.12,0.04); return s+0.6*np.pad(tick(),(0,int(SR*0.108)))
def pop(f=900):
    return sweep(f,f*0.45,0.09,0.03)
def ding(f=1318.5,d=0.7):
    t=tt(d); return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t)+0.2*np.sin(2*np.pi*f*3*t))*env(len(t),0.003,0.18)
def chime():
    a=ding(1046.5,0.6); b=ding(1568,0.9); out=np.zeros(int(SR*1.1)); out[:len(a)]+=a*0.8; o=int(SR*0.09); out[o:o+len(b)]+=b; return out
def buzz():
    return sweep(150,140,0.28,0.12,'sq')
def alert():
    b=np.sin(2*np.pi*880*tt(0.11))*env(int(SR*0.11),0.003,0.06); out=np.zeros(int(SR*0.32)); out[:len(b)]+=b; o=int(SR*0.16); out[o:o+len(b)]+=b; return out
def powerdown(): return sweep(520,45,0.55,0.25)
def powerup(): return sweep(90,900,0.5,0.3)
def boom():
    s=sweep(130,38,0.9,0.28); n=lp_sweep(noise(0.9),2500,120)*env(int(SR*0.9),0.002,0.15); return s*1.0+n*1.2
def riser(d):
    n=lp_sweep(noise(d),200,6000)*np.linspace(0.05,1,int(SR*d))**2
    t=tt(d); f=200*(1500/200)**(t/d); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.linspace(0,0.6,len(t))**2
    return (n*0.7+s*0.5)
def glitch(d=0.09):
    x=noise(d); x=np.round(x*2)/2; x=np.repeat(x[::6],6)[:len(x)]; return x*env(len(x),0.001,0.05)
def sparkle(n=7):
    out=np.zeros(int(SR*0.7))
    for k in range(n):
        f=rng.uniform(2800,6500); t0=int(SR*k*0.055); d=0.18; s=np.sin(2*np.pi*f*tt(d))*env(int(SR*d),0.002,0.05)*0.5; out[t0:t0+len(s)]+=s
    return out

# ---- capas del diseño sonoro (docs/AUDIO.md): impactos, graves, ambiente, reverb, samples ----
from scipy.signal import fftconvolve
from pathlib import Path
import subprocess
SFX_DIR = Path(__file__).resolve().parents[2] / 'assets' / 'sfx'

def reverse(x): return x[::-1].copy()          # un riser invertido suena distinto y sirve de "succión" antes de un golpe
def reverb(x, tail=0.7, mix=0.3):
    n = int(SR * tail); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * tail / 4.5))
    ir = lp_sweep(ir, 6000, 900); ir /= np.max(np.abs(ir)) + 1e-9
    wet = fftconvolve(x, ir)[:len(x) + n]; wet = np.pad(wet, (0, len(x) + n - len(wet))); wet /= np.max(np.abs(wet)) + 1e-9
    out = np.pad(x, (0, n)) * (1 - mix) + wet * mix * np.max(np.abs(x)); return out
def impact():
    """Golpe fuerte (marca una acción importante). Más seco que boom() y con cola de reverb."""
    t = tt(0.9); s = np.sin(2 * np.pi * np.cumsum(110 * (32 / 110) ** (t / 0.9)) / SR) * env(len(t), 0.001, 0.3)
    n = lp_sweep(noise(0.5), 4000, 150) * env(int(SR * 0.5), 0.001, 0.08)
    x = s + np.pad(n, (0, len(s) - len(n))) * 0.9; return reverb(np.tanh(x * 1.6), 0.8, 0.25)
def hit(): return impact()[:int(SR * 0.35)] * 0.7   # como impact pero más corto y suave
def bassdrop(d=1.3):
    t = tt(d); f = 160 * (28 / 160) ** (t / d); s = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(len(t), 0.004, d / 2.2); return s
def braam(d=1.8):
    t = tt(d); x = sum(np.sign(np.sin(2 * np.pi * f * t + p)) * a for f, a, p in ((55, 1, 0), (55.6, .8, 1), (82.4, .6, 2), (110, .5, 3)))
    x = lp_sweep(x, 160, 1400) * env(len(t), 0.05, d / 2.5); return np.tanh(x * 0.6)
def ambient(d, lvl=0.05):
    """Cuarto/"room tone": ruido grave que respira + zumbido de 50 Hz. Evita el silencio muerto."""
    n = int(SR * d); t = np.arange(n) / SR
    x = lp_sweep(noise(d), 380, 380) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t)) + 0.35 * np.sin(2 * np.pi * 50 * t) + 0.15 * np.sin(2 * np.pi * 100 * t)
    return x / np.max(np.abs(x)) * lvl
REAL_KEY_GAIN = 0.8
_KEYS = None
def keys():
    """Teclas reales sueltas (lista de arrays) o [] si no existen. Se cargan una vez."""
    global _KEYS
    if _KEYS is None:
        d = SFX_DIR / 'propios' / 'teclas'; _KEYS = []
        for f in sorted(d.glob('k*.wav')) if d.is_dir() else []:
            with wave.open(str(f)) as w: _KEYS.append(np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768)
    return _KEYS
def propio(nombre, gain=1.0):
    """Sonido de assets/sfx/propios/<nombre> (mp3/wav de code-reel-studio: intro-whoosh, mouse-click, zoom-click); None si falta."""
    f = next((p for p in (SFX_DIR / 'propios').glob(nombre + '.*')), None) if (SFX_DIR / 'propios').is_dir() else None
    if f is None: return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, '<f4').astype(float); return x / (np.max(np.abs(x)) + 1e-9) * gain
def sample(cat, i=0, gain=1.0):
    """Primer sonido real de assets/sfx/<cat>/ (ver assets/sfx/LEEME.md); None si no hay, y se usa el sintético."""
    fs = sorted(p for p in (SFX_DIR / cat).glob('*') if p.suffix.lower() in ('.wav', '.mp3', '.flac', '.ogg')) if (SFX_DIR / cat).is_dir() else []
    if not fs: return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(fs[i % len(fs)]), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, '<f4').astype(float); return x / (np.max(np.abs(x)) + 1e-9) * gain


class Track:
    """Pista de efectos: put(t, sonido, ganancia). typing/enter/line son atajos de terminal."""
    def __init__(self, dur):
        self.buf = np.zeros(int(SR * dur))
    def put(self, t, x, g=1.0):
        i = int(t * SR)
        if i < 0: return
        x = x[:max(0, len(self.buf) - i)]; self.buf[i:i + len(x)] += x * g
    def ambient(self, t0=0, lvl=0.05):
        """Base de ambiente desde t0 hasta el final (que nunca suene vacío)."""
        self.put(t0, ambient(len(self.buf) / SR - t0, lvl))
    def typing(self, t0, n, rate=30, g=0.55):
        """Tipeo. Con teclas reales en assets/sfx/propios/teclas/ (cortar_teclas.py) usa tipeo grabado; si no, ticks sintéticos."""
        ks = keys(); last = -1
        for k in range(n):
            t = t0 + k / rate + rng.uniform(-0.008, 0.008) * (1 if ks else 0.5)
            if ks:
                j = int(rng.integers(len(ks)))
                while j == last and len(ks) > 1: j = int(rng.integers(len(ks)))
                last = j; self.put(t, ks[j], g * REAL_KEY_GAIN * rng.uniform(0.75, 1.0))
            else: self.put(t, tick(), g * rng.uniform(0.7, 1.0))
    def enter(self, t):
        ks = keys()
        if ks: self.put(t, max(ks, key=lambda a: float(np.sum(a ** 2))), 0.9 * REAL_KEY_GAIN)   # la tecla más 'pesada' del lote
        self.put(t, thunk(), 0.5 if ks else 0.9)
    def line(self, t): self.put(t, tick(), 0.25)
    def save(self, path):
        b = self.buf / np.max(np.abs(self.buf)) * 0.7
        with wave.open(str(path), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((b * 32767).astype('<i2').tobytes())
