// Motor de animación determinístico: la página no usa reloj; render.mjs llama window.__render(t) cuadro a cuadro.
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export const eo=x=>1-Math.pow(1-x,3);
export const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
export const eb=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
export const hash=n=>{const s=Math.sin(n*127.1)*43758.5453;return s-Math.floor(s)};

export async function loadConfig(url='./video.json'){return await (await fetch(url)).json()}

// Fondo, canvas 3D opcional y barra de pasos (opcional).
export function mountShell(){
  document.body.insertAdjacentHTML('afterbegin',
   '<div id="bg"><div id="glowA"></div><div id="glowB"></div><div id="dots"></div></div>'+
   '<canvas id="gl" width="1080" height="1920"></canvas>'+
   '<div id="stepbar"><div class="lbl">Paso <b id="stepn">1</b> de <span id="stept">1</span></div><div class="segs"></div></div>');
}
let segs=null;
export function setupSteps(total){
  segs=document.querySelector('#stepbar .segs');segs.innerHTML='';
  document.getElementById('stept').textContent=total;
  for(let i=0;i<total;i++){const d=document.createElement('div');d.className='seg';d.innerHTML='<i></i>';segs.appendChild(d)}
}
// Calcula t0 de cada escena y devuelve la duración total.
export function timeline(SC){let acc=0;for(const s of SC){s.t0=acc;acc+=s.d;s.el=document.getElementById(s.id)}return acc}

// data-a="tipo:inicio:duración" (up|left|pop|fade) · data-show="t" · data-type="t" data-text="..." (tipeo a 30 car/s)
export function anim(sc,lt){
  sc.querySelectorAll('[data-a]').forEach(el=>{
    const [ty,s,d]=el.dataset.a.split(':');const p=clamp((lt-(+s))/(d?+d:0.5));
    let o=1,tr='none';
    if(ty==='up'){const e=eo(p);tr=`translateY(${(1-e)*70}px)`;o=e}
    else if(ty==='left'){const e=eo(p);tr=`translateX(${-(1-e)*90}px)`;o=e}
    else if(ty==='pop'){const e=eb(p);tr=`scale(${0.7+0.3*e})`;o=clamp(p*2)}
    else if(ty==='fade'){o=p}
    el.style.opacity=o;el.style.transform=tr;
  });
  sc.querySelectorAll('[data-show]').forEach(el=>{el.style.visibility=lt>=+el.dataset.show?'visible':'hidden'});
  const ty=[...sc.querySelectorAll('[data-type]')];
  let active=null;
  ty.forEach(el=>{
    const s=+el.dataset.type,txt=el.dataset.text;const n=Math.floor(clamp((lt-s)*30,0,txt.length));
    el.textContent=txt.slice(0,n);el.classList.remove('cur','off');if(lt>=s)active={el,typing:n<txt.length};
  });
  if(active){active.el.classList.add('cur');if(!active.typing&&Math.floor(lt*2.4)%2)active.el.classList.add('off')}
}

export function bg(T){
  const P=window.__loopPeriod;  // video en bucle: frecuencias enteras sobre el período para que el fondo empalme sin salto
  if(P){const w=(f)=>2*Math.PI*Math.max(1,Math.round(f*P/(2*Math.PI)))/P,k=Math.max(1,Math.round(14*P/44))*44/P;
    document.getElementById('dots').style.transform=`translate(0px,${(T*k)%44}px)`;
    const a=document.getElementById('glowA'),b=document.getElementById('glowB');
    a.style.left=(-300+Math.sin(T*w(0.35))*140)+'px';a.style.top=(-200+Math.cos(T*w(0.27))*160)+'px';
    b.style.left=(150+Math.cos(T*w(0.3))*160)+'px';b.style.top=(950+Math.sin(T*w(0.22))*180)+'px';return}
  document.getElementById('dots').style.transform=`translate(0px,${(T*14)%44}px)`;
  const a=document.getElementById('glowA'),b=document.getElementById('glowB');
  a.style.left=(-300+Math.sin(T*0.35)*140)+'px';a.style.top=(-200+Math.cos(T*0.27)*160)+'px';
  b.style.left=(150+Math.cos(T*0.3)*160)+'px';b.style.top=(950+Math.sin(T*0.22)*180)+'px';
}

// Registra window.__render/__scenes/__ready. `custom(id,lt)` anima elementos propios de la escena;
// `pose(id,lt,T)` (si devuelve true, ya renderizó él mismo) + `gl:{renderer,scene,cam}` solo si el video usa 3D (escena con gl:true).
export function installRender({SC,TOTAL,custom=()=>{},pose=null,gl=null}){
  const canvas=document.getElementById('gl');
  window.__render=(T)=>{
    T=Math.min(T,TOTAL-1e-6);
    let cur=SC[SC.length-1];for(const s of SC){if(T>=s.t0&&T<s.t0+s.d){cur=s;break}}
    const lt=T-cur.t0;
    SC.forEach(s=>s.el.style.display=s===cur?'block':'none');
    bg(T);
    const sb=document.getElementById('stepbar');const st=cur.el.dataset.step;
    if(st&&segs){sb.style.display='block';document.getElementById('stepn').textContent=st;
      segs.querySelectorAll('.seg i').forEach((e,i)=>{const n=i+1;e.style.width=(n<st?100:(n==st?eo(clamp(lt/0.6))*100:0))+'%'})}
    else sb.style.display='none';
    anim(cur.el,lt);custom(cur.id,lt);
    canvas.style.display=(cur.gl&&gl)?'block':'none';
    const mb=document.getElementById('glmb');if(mb&&!(cur.gl&&gl))mb.style.display='none';
    if(cur.gl&&gl&&pose){if(pose(cur.id,lt,T)!==true)gl.renderer.render(gl.scene,gl.cam)}  // pose()→true: ya renderizó (p. ej. MotionBlur)
  };
  window.__scenes=SC.map(s=>({id:s.id,t0:s.t0,d:s.d}));window.__total=TOTAL;
  window.__render(0);window.__ready=true;
}
