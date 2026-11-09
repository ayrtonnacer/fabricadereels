/* Cámara 2.5D para motion graphics (docs/CAMARA.md).
   El set es HTML plano repartido en capas a distintas profundidades; una cámara con perspectiva viaja entre
   "estaciones". La profundidad sale del movimiento de cámara (paralaje), no de modelos 3D: renderiza rápido.

   Estructura en la escena:
     <div class="vista"><div class="cam"><div class="mundo">
        <div id="x-piso"  class="piso"  data-z="-900" data-rx="90" data-y="700"></div>   ← capa de fondo
        <div id="x-a"     class="tarjeta" data-x="0"   data-y="0"></div>                   ← estación (z = 0)
        <div id="x-polvo" class="puntos" data-z="500"></div>                               ← primer plano
     </div></div></div>

   Uso (dentro del <script> de la escena, con su timeline pausado `tl`):
     const cam = Camara(document.querySelector('#gancho'), tl, { perspectiva: 1600 });
     cam.poner({ z: -600, rx: 8 });                       // pose inicial (en t = 0)
     cam.ir(0, { z: 0, rx: 0 }, 2.4);                      // dolly-in: x, y, z, rx, ry, rz
     cam.mirar(2.6, '#x-b', { z: 150, ry: -6 }, 1.1);      // viajar a una estación (centrarla) y acercar
   Convenciones: x/y en px del mundo (0,0 = centro de pantalla). z de la cámara: + acerca, − aleja.
   rx inclina (mirar desde arriba/abajo), ry gira (órbita alrededor del plano z = 0), rz rola. */
(function () {
  function n(v, d) { return v === undefined || v === '' ? d : +v; }
  // DY: todo el set sube DY px para dejar libre la franja de subtítulos (y 1120–1320). Se ajusta con Camara(root, tl, { dy }).
  var DY = 170;
  function pose(p) {
    p = p || {};
    return {
      cam: { z: n(p.z, 0), rotationX: n(p.rx, 0), rotationY: n(p.ry, 0), rotationZ: n(p.rz, 0) },
      mundo: { x: -n(p.x, 0), y: -n(p.y, 0) - DY },
    };
  }
  window.Camara = function (root, tl, opts) {
    opts = opts || {};
    DY = opts.dy === undefined ? 170 : opts.dy;
    var vista = root.querySelector('.vista'), cam = root.querySelector('.cam'), mundo = root.querySelector('.mundo');
    gsap.set(vista, { perspective: opts.perspectiva || 1600 });
    gsap.set(cam, { transformOrigin: '50% 50% 0', transformPerspective: 0 });
    // Ubicar cada pieza del mundo: centrada en (data-x, data-y) a profundidad data-z, con giros opcionales.
    mundo.querySelectorAll(':scope > *').forEach(function (el) {
      var d = el.dataset;
      gsap.set(el, {
        xPercent: -50, yPercent: -50, x: n(d.x, 0), y: n(d.y, 0), z: n(d.z, 0),
        rotationX: n(d.rx, 0), rotationY: n(d.ry, 0), rotationZ: n(d.rz, 0), scale: n(d.s, 1),
      });
    });
    var api = {
      poner: function (p) { var q = pose(p); tl.set(cam, q.cam, 0); tl.set(mundo, q.mundo, 0); return api; },
      ir: function (t, p, dur, ease) {
        var q = pose(p), e = ease || 'power2.inOut', d = dur === undefined ? 1.2 : dur;
        tl.to(cam, Object.assign({ duration: d, ease: e }, q.cam), t);
        tl.to(mundo, Object.assign({ duration: d, ease: e }, q.mundo), t);
        return api;
      },
      // Centrar una estación (sus data-x/y) con un acercamiento y giro opcionales.
      mirar: function (t, sel, extra, dur, ease) {
        var el = root.querySelector(sel), d = el.dataset;
        return api.ir(t, Object.assign({ x: n(d.x, 0), y: n(d.y, 0) }, extra || {}), dur, ease);
      },
    };
    return api;
  };
})();
