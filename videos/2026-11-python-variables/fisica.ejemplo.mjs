// Ejemplo de spec: 6 cubos que caen sobre el piso. Copiar a videos/X/fisica.mjs y adaptar.
export default {
  dur: 4, fps: 60,
  crear(R, w) {
    w.createCollider(R.ColliderDesc.cuboid(5, 0.1, 5).setTranslation(0, -0.1, 0).setRestitution(0.3));   // piso (sin cuerpo = fijo)
    const c = {};
    for (let i = 0; i < 6; i++) {   // posiciones fijas, nada de Math.random: el resultado tiene que repetirse
      const rb = w.createRigidBody(R.RigidBodyDesc.dynamic().setTranslation(((i % 3) - 1) * 0.12, 0.6 + i * 0.22, 0).setCcdEnabled(true));
      w.createCollider(R.ColliderDesc.cuboid(0.05, 0.05, 0.05).setRestitution(0.35).setFriction(0.6), rb);
      c['cubo' + i] = rb;
    }
    return c;
  },
};
