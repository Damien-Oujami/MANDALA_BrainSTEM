"use client";
import React, { useEffect, useRef } from "react";

type Props = {
  className?: string;
  density?: number;     // stars per 1000x1000 logical pixels
  drift?: number;       // 0..1 drift speed
  twinkle?: number;     // 0..1 twinkle strength
  palette?: string[];   // small accents among whites
};

export default function StarfieldCanvas({
  className = "absolute inset-0",
  density = 0.9,
  drift = 0.35,
  twinkle = 0.35,
  palette = ["#9adfff", "#a38bff", "#ffc877"],
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const raf = useRef<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext("2d", { alpha: true })!;

    let w = 0, h = 0, dpr = 1;
    let stars: {
      x: number; y: number; z: number; r: number; c: string; s: number;
    }[] = [];
    const reduce =
      typeof window !== "undefined" &&
      window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    function reseed() {
      const count = Math.max(80, Math.floor(density * (w * h) / (1000 * 1000)));
      stars = new Array(count).fill(0).map(() => {
        const z = Math.random() ** 2; // more small/“distant” stars
        const cPick = Math.random();
        const c =
          cPick < 0.08 ? palette[0] :
          cPick < 0.14 ? palette[1] :
          cPick < 0.18 ? palette[2] :
          "#ffffff";
        return {
          x: Math.random() * w,
          y: Math.random() * h,
          z,                  // 0..1 depth (0 = near, 1 = far)
          r: (0.6 + Math.random() * 1.6) * (1 - z) * dpr, // size by depth
          c,
          s: Math.random() * 6.283, // twinkle phase
        };
      });
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = canvas.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect.width * dpr));
      h = Math.max(1, Math.floor(rect.height * dpr));
      canvas.width = w;
      canvas.height = h;
      reseed();
    }
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    let t0 = performance.now();
    function tick(now: number) {
      const dt = (now - t0) / 1000;
      t0 = now;

      // clear with faint vignette
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      const bg = ctx.createRadialGradient(
        w * 0.6, h * 0.4, Math.min(w, h) * 0.15,
        w * 0.5, h * 0.5, Math.max(w, h) * 0.8
      );
      bg.addColorStop(0, "rgba(5,8,15,1)");
      bg.addColorStop(1, "rgba(3,5,10,1)");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, w, h);

      ctx.globalCompositeOperation = "lighter";

      for (const s of stars) {
        // parallax drift (wrap around edges)
        if (!reduce) {
          const vx = (0.5 - s.z) * drift * 8.0; // slower when far
          const vy = (0.5 - s.z) * drift * 5.0;
          s.x = (s.x + vx * dt * 60 + w) % w;
          s.y = (s.y + vy * dt * 60 + h) % h;
          s.s += (0.6 + 0.8 * (1 - s.z)) * dt; // twinkle phase
        }

        const a = reduce ? 0.7 : 0.6 + twinkle * 0.4 * (0.5 + 0.5 * Math.sin(s.s));
        ctx.globalAlpha = a * (0.5 + 0.5 * (1 - s.z));

        // soft glow
        ctx.beginPath();
        ctx.fillStyle = s.c;
        ctx.arc(s.x, s.y, s.r * 2.2, 0, Math.PI * 2);
        ctx.fill();

        // crisp core
        ctx.globalAlpha = Math.min(1, a + 0.2);
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
      }

      if (!reduce) raf.current = requestAnimationFrame(tick);
    }
    raf.current = requestAnimationFrame(tick);

    return () => {
      if (raf.current) cancelAnimationFrame(raf.current);
      ro.disconnect();
    };
  }, [density, drift, twinkle, palette]);

  return <canvas ref={canvasRef} className={className} />;
}
