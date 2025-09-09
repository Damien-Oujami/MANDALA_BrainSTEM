
'use client';
import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function Hero() {
  return (
    <Canvas
      dpr={[1, 1.5]}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      camera={{ position: [0, 0, 7], fov: 42, near: 0.1, far: 100 }}
      onCreated={({ gl }) => { gl.setClearAlpha(0); /* @ts-ignore */ gl.outputColorSpace = THREE.SRGBColorSpace; }}
    >
      <ambientLight intensity={0.24} />
      <directionalLight position={[4, 3, 8]} intensity={1.1} />
      <BellSyrupPupilOrchestratedJitter />
    </Canvas>
  );
}

function BellSyrupPupilOrchestratedJitter({
  R0 = 1.5, r0 = 0.56, uSeg = 440, vSeg = 200, dotSizePx = 0.18, waves = 3, duration = 6.5, pupilFactor = 0.85,
  jitterMax = 0.5, jitterDecay = 2.2,
}: {
  R0?: number; r0?: number; uSeg?: number; vSeg?: number; dotSizePx?: number; waves?: number; duration?: number; pupilFactor?: number;
  jitterMax?: number; jitterDecay?: number;
}) {
  const points = useRef<THREE.Points>(null!);
  const geom = useRef<THREE.BufferGeometry>(null!);
  const positionsRef = useRef<Float32Array>();
  const colorsRef = useRef<Float32Array>();
  const jitterRef = useRef<Float32Array>();
  const uniforms = useRef({ uTime: { value: 0 }, uSizePx: { value: dotSizePx } });
  const TAU = Math.PI * 2.0;

  useMemo(()=>{
    const N = uSeg * vSeg;
    positionsRef.current = new Float32Array(N*3);
    colorsRef.current = new Float32Array(N*3);
    jitterRef.current = new Float32Array(N*3);

    const stops=[new THREE.Color('#00e5ff'),new THREE.Color('#3fc5ff'),new THREE.Color('#ff2bff'),new THREE.Color('#9b3dff'),new THREE.Color('#ff5a00'),new THREE.Color('#ffbf00')];
    const grad=(t:number)=>{ const n=stops.length,x=t*n,i=Math.floor(x)%n,f=x-Math.floor(x); return stops[i].clone().lerp(stops[(i+1)%n], f*f*(3-2*f)); };

    let k=0,c=0,j=0;
    for(let iu=0; iu<uSeg; iu++){
      const u=(iu/uSeg)*TAU, col=grad(iu/uSeg);
      for(let iv=0; iv<vSeg; iv++){
        const v=(iv/vSeg)*TAU;
        const x=(R0 + r0*Math.cos(v))*Math.cos(u);
        const y=(R0 + r0*Math.cos(v))*Math.sin(u);
        const z=r0*Math.sin(v);
        positionsRef.current![k++]=x; positionsRef.current![k++]=y; positionsRef.current![k++]=z;
        colorsRef.current![c++]=col.r; colorsRef.current![c++]=col.g; colorsRef.current![c++]=col.b;

        const rx=(Math.random()*2-1), ry=(Math.random()*2-1), rz=(Math.random()*2-1);
        const m=Math.max(0.0001, Math.hypot(rx,ry,rz));
        jitterRef.current![j++]=(rx/m); jitterRef.current![j++]=(ry/m); jitterRef.current![j++]=(rz/m);
      }
    }
  },[R0,r0,uSeg,vSeg]);

  const stabilizedSent = useRef(false);

  useFrame(({ clock })=>{
    const t=clock.getElapsedTime();
    uniforms.current.uTime.value=t;
    const s=Math.min(1.0, t/duration);
    const smooth=s*s*(3.0-2.0*s);
    const speedFactor=Math.pow(1.0 - smooth, 2.0);
    const chaos=Math.pow(1.0 - s, 1.4);
    const speedCW=0.95*speedFactor, speedCCW=-0.75*speedFactor;
    const ampBase=0.60, widthBase=0.50;
    const amp=ampBase*chaos, width=widthBase*(0.8+0.2*chaos);
    const opposingK=0.14*chaos, axialAmp=0.18*chaos, warp=0.40*chaos;
    const rEnd=r0*pupilFactor, rBase = r0*(1.0 - smooth) + rEnd*smooth;
    const maxBulge=0.68, maxSquash=0.28;

    if(!stabilizedSent.current && s>=0.98){ stabilizedSent.current=true; window.dispatchEvent(new CustomEvent('hero:stabilized')); }

    const pos=positionsRef.current!, jit=jitterRef.current!;
    let k=0,j=0;
    for(let iu=0; iu<uSeg; iu++){
      const u=(iu/uSeg)*TAU;
      let scale = 1.0 + opposingK*Math.sin(2.0*(u + t*0.6*speedFactor));
      for(let w=0; w<waves; w++){
        const basePhase=(w*TAU/waves);
        let phaseCW=(t*speedCW + basePhase + warp*Math.sin(u+basePhase))%TAU;
        let phaseCCW=(t*speedCCW + basePhase + warp*Math.cos(u+basePhase*1.2))%TAU;
        let du=Math.abs(u-phaseCW); if(du>Math.PI) du=TAU-du;
        let du2=Math.abs(u-phaseCCW); if(du2>Math.PI) du2=TAU-du2;
        scale += Math.exp(-0.5*Math.pow(du/width,2.0))*amp;
        scale += Math.exp(-0.5*Math.pow(du2/width,2.0))*amp;
      }
      const bulge=Math.min(scale-1.0,maxBulge), squash=Math.max(scale-1.0,-maxSquash);
      const safeScale = 1.0 + Math.max(squash, Math.min(bulge, maxBulge));
      const rLocal = rBase*safeScale;

      for(let iv=0; iv<vSeg; iv++){
        const v0=(iv/vSeg)*TAU;
        const v=v0 + axialAmp*Math.sin(2.0*u + t*0.7*speedFactor);
        let x=(R0 + rLocal*Math.cos(v))*Math.cos(u);
        let y=(R0 + rLocal*Math.cos(v))*Math.sin(u);
        let z=rLocal*Math.sin(v);
        x += jit[j++]* (0.5*Math.pow(1.0 - s, 2.2));
        y += jit[j++]* (0.5*Math.pow(1.0 - s, 2.2));
        z += jit[j++]* (0.5*Math.pow(1.0 - s, 2.2));
        pos[k++]=x; pos[k++]=y; pos[k++]=z;
      }
    }
    const attr=geom.current.getAttribute('position') as THREE.BufferAttribute;
    attr.needsUpdate=true; geom.current.computeBoundingSphere();
  });

  return (
    <points ref={points} frustumCulled={false}>
      <bufferGeometry ref={geom} onUpdate={(g)=>g.computeBoundingSphere()}>
        <bufferAttribute attach="attributes-position" array={positionsRef.current!} count={(positionsRef.current!.length/3)|0} itemSize={3}/>
        <bufferAttribute attach="attributes-aColor" array={colorsRef.current!} count={(colorsRef.current!.length/3)|0} itemSize={3}/>
      </bufferGeometry>
      <shaderMaterial blending={THREE.AdditiveBlending} depthWrite={false} transparent uniforms={uniforms.current as any}
        vertexShader={`precision highp float; uniform float uTime; uniform float uSizePx; attribute vec3 aColor; varying vec3 vColor; varying float vDepth;
          void main(){ vec3 p=position; float len=length(p); p*=(1.0 + 0.005 * sin(uTime*0.8 + len*1.1)); vec4 mv=modelViewMatrix*vec4(p,1.0);
          gl_Position=projectionMatrix*mv; gl_PointSize=uSizePx*(300.0 / -mv.z); vDepth=-mv.z; vColor=aColor; }`}
        fragmentShader={`precision highp float; varying vec3 vColor; varying float vDepth; void main(){ vec2 uv=gl_PointCoord*2.0-1.0; float d=dot(uv,uv);
          float alpha=exp(-d*7.0)*0.86; float depthFade=smoothstep(12.0,2.5,vDepth); alpha*=depthFade; gl_FragColor=vec4(vColor,alpha); }`}
      />
    </points>
  );
}
