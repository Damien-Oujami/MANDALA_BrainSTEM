const geometry = new THREE.TorusGeometry(2, 0.6, 32, 100);
const material = new THREE.ShaderMaterial({
  uniforms: { time: { value: 0.0 }},
  vertexShader: `...`,
  fragmentShader: `...`,
});
const torus = new THREE.Mesh(geometry, material);
scene.add(torus);

// animate
function animate() {
  requestAnimationFrame(animate);
  torus.rotation.y += 0.002;
  torus.scale.setScalar(1 + 0.05 * Math.sin(clock.getElapsedTime()));
  renderer.render(scene, camera);
}
