import React, { useEffect, useRef } from "react";

/**
 * TekitaHeroTorus
 * - Animated, breathing torus/spiral made of glowing dots + strokes
 * - Palette: cyan → magenta → orange (tekita)
 * - No copy rendered; layer your own content on top with absolute children
 *
 * Props:
 *  - className: wrapper styling (use to set height)
 *  - intensity: 0..1 overall glow strength
 *  - speed: global animation speed multiplier
 */
export default function TekitaHeroTorus({
  className = "h-[70svh] w-full",
  intensity = 0.9,
  speed = 1.0,
}: {
  className?: string;
  intensity?: number;
  speed?: number;
}) {
  const ref = useRef<HTMLCanvasElement | null>(null);
  const raf = useRef<number | null>(null);

  useEffect(() => {
    const canvas = ref.current!;
    const ctx = canvas.getContext("2d", { alpha: true })!;
    let w = 0,
      h = 0,
      dpr = 1;

    const prefersReduce =
      typeof window !== "undefined" &&
      window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = canvas.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect.width * dpr));
      h = Math.max(1, Math.floor(rect.height * dpr));
      canvas.width = w;
      canvas.height = h;
    }
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    // ------- palette (tekita cyan→magenta→orange) -------
    const stops = [
      { t: 0.00, c: [  0, 188, 212] }, // cyan-ish
      { t: 0.35, c: [120,  60, 240] }, // violet
      { t: 0.62, c: [220,  30, 120] }, // magenta
      { t: 0.85, c: [255, 120,  40] }, // orange
      { t: 1.00, c: [255, 180,  60] }, // amber
    ];
    const lerp = (a:number,b:number,t:number)=>a+(b-a)*t;
    function grad(t:number){
      t = (t%1+1)%1;
      for (let i=0;i<stops.length-1;i++){
        const a=stops[i], b=stops[i+1];
        if (t>=a.t && t<=b.t){
          const u=(t-a.t)/(b.t-a.t);
          const r=Math.round(lerp(a.c[0],b.c[0],u));
          const g=Math.round(lerp(a.c[1],b.c[1],u));
          const bch=Math.round(lerp(a.c[2],b.c[2],u));
          return `rgba(${r},${g},${bch},1)`;
        }
      }
      const c = stops[stops.length-1].c;
      return `rgba(${c[0]},${c[1]},${c[2]},1)`;
    }

    // ------- animation -------
    let t0 = performance.now();
    const DOTS_ARC = 1000;       // dots per loop
    const RINGS = 52;            // number of nested spirals
    const baseThickness = 0.8;   // dot size scaler
    const glow = Math.max(0, Math.min(1, intensity));

    function draw(now:number){
      const dt = (now - t0) / 1000;
      const T = dt * 0.25 * speed; // global phase
      ctx.setTransform(1,0,0,1,0,0);
      // subtle vignette background
      ctx.clearRect(0,0,w,h);
      const bg = ctx.createRadialGradient(w*0.65,h*0.35,Math.min(w,h)*0.1,w*0.5,h*0.5,Math.max(w,h)*0.7);
      bg.addColorStop(0,"rgba(10,18,28,1)");
      bg.addColorStop(1,"rgba(4,7,12,1)");
      ctx.fillStyle = bg;
      ctx.fillRect(0,0,w,h);

      ctx.save();
      ctx.translate(w/2, h/2);

      const minSide = Math.min(w,h);
      const scale = minSide * 0.36;

      // breathing torus parameters
      const breath = prefersReduce ? 0.2 : 0.35 + 0.05*Math.sin(T*2.0);
      const R = 1.0;                           // major radius (normalized)
      const r = breath;                         // minor radius (breathing)
      const twist = 1.2 + 0.1*Math.sin(T*1.3); // spiral twist along torus
      const swirl = 0.9 + 0.08*Math.cos(T*0.7);

      // pre-glow
      ctx.globalCompositeOperation = "lighter";

      for (let k=0; k<RINGS; k++){
        const ringPhase = (k / RINGS);
        const angleShift = T*2.0 + ringPhase * Math.PI*2*swirl;
        const dotCount = DOTS_ARC;
        for (let i=0; i<dotCount; i++){
          const u = i / dotCount;           // [0,1)
          const theta = (u*Math.PI*2*twist) + angleShift;
          const phi   = (u*Math.PI*2);      // around the torus

          // torus parametric (normalized) → (x,y,z)
          const cx = (R + r*Math.cos(phi)) * Math.cos(theta);
          const cy = (R + r*Math.cos(phi)) * Math.sin(theta);
          const cz =  r * Math.sin(phi);

          // gentle rotation in time for parallax
          const rot = T*0.35;
          const x =  (cx*Math.cos(rot) - cz*Math.sin(rot));
          const y =  cy;
          const z =  (cx*Math.sin(rot) + cz*Math.cos(rot));

          // fake perspective
          const depth = 1.6 + z; // keep positive
          const px = (x/depth) * scale;
          const py = (y/depth) * scale;

          // color along ring with phase + depth
          const hueT = (u + ringPhase*0.25 + 0.05*z) % 1;
          ctx.fillStyle = grad(hueT);

          // size & alpha with depth and ring index
          const sz = (baseThickness * (1.0 + 0.7*(1 - ringPhase))) * (1.2/depth);
          const a = (0.12 + 0.75*(1 - ringPhase)) * (prefersReduce ? 0.6 : 1.0);

          // glow dot
          ctx.globalAlpha = a * (0.35 + 0.65*glow);
          ctx.beginPath();
          ctx.arc(px, py, sz*2.2, 0, Math.PI*2);
          ctx.fill();

          // crisp core
          ctx.globalAlpha = a;
          ctx.beginPath();
          ctx.arc(px, py, sz, 0, Math.PI*2);
          ctx.fill();
        }
      }

      ctx.restore();
      if (!prefersReduce) raf.current = requestAnimationFrame(draw);
    }

    raf.current = requestAnimationFrame(draw);
    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
      ro.disconnect();
    };
  }, [intensity, speed]);

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* background canvas */}
      <canvas ref={ref} className="absolute inset-0 block w-full h-full" />
      {/* slot for your content */}
      {/* <div className="relative z-10 flex items-center justify-center h-full">
          <h1 className="text-white/90 text-5xl md:text-7xl font-semibold tracking-tight">
            tekita
          </h1>
        </div> */}
    </div>
  );
}
