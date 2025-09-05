'use client'
import { useEffect, useRef, useMemo } from 'react'

type Dot = { x: number; y: number; c: string; a: number }

const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5)) // ~2.399963
const EASE = (t:number)=> t<0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2

function isPrime(n:number){
  if (n<2) return false
  if (n%2===0) return n===2
  for (let i=3;i*i<=n;i+=2) if(n%i===0) return false
  return true
}

export default function SpiralCanvas(){
  const ref = useRef<HTMLCanvasElement>(null)

  // prerender target positions
  const dots = useMemo(()=> {
    const w = 1600, h = 900, cx = w/2, cy = h/2
    const N = 2400
    const c = 6.2 // radial scale
    const arr: Dot[] = []

    for (let n=1; n<=N; n++){
      if (!isPrime(n)) continue
      const r = c * Math.sqrt(n)
      const theta = n * GOLDEN_ANGLE
      const x = cx + r * Math.cos(theta)
      const y = cy + r * Math.sin(theta)

      // color by radius percent
      const p = Math.min(1, r / (c*Math.sqrt(N)))
      const col = p<0.33 ? `#00C7B7` : p<0.67 ? `#E62BA5` : `#1F6FEB`
      // honey gold sparkle every ~97th prime
      const sparkle = (n % 97 === 0) && Math.random() < 0.4
      arr.push({ x, y, c: sparkle ? '#FFC857' : col, a: 0 })
    }
    return { arr, w, h, cx, cy }
  }, [])

  useEffect(()=>{
    const canvas = ref.current!
    const ctx = canvas.getContext('2d')!
    let raf = 0
    let t0 = performance.now()

    const render = (ts:number)=>{
      const t = (ts - t0) / 1000
      // loop every ~10s
      const LOOP = 10
      const phase = (t % LOOP) / LOOP
      const eased = EASE(phase)

      const { arr, w, h, cx, cy } = dots
      canvas.width = canvas.clientWidth
      canvas.height = canvas.clientHeight
      const sx = canvas.width / w
      const sy = canvas.height / h

      // background
      ctx.fillStyle = '#0A0F1C'
      ctx.fillRect(0,0,canvas.width,canvas.height)

      // gentle rotation + breathing zoom
      const rot = 0.05 * t // rad/s
      const zoom = 1 + 0.03 * Math.sin(t*1.2)

      // Scatter → Spiral → Weave timing
      // 0–0.2 scatter fade-in, 0.2–0.6 gather, 0.6–0.9 weave/breathe, 0.9–1 resolve/fade
      arr.forEach((d, i)=>{
        // start positions: scatter (uniform random seeded from index)
        const rnd = Math.sin(i*999) * 43758.5453
        const rx = (rnd - Math.floor(rnd)) * w
        const rnd2 = Math.sin(i*777) * 12345.678
        const ry = (rnd2 - Math.floor(rnd2)) * h

        // target spiral pos (already computed)
        const tx = d.x, ty = d.y

        let px = rx, py = ry
        if (eased > 0.2) {
          const u = Math.min(1, (eased-0.2)/0.4) // gather progress
          px = rx + (tx - rx) * u
          py = ry + (ty - ry) * u
        }
        if (eased > 0.6) {
          // weave: tiny outward ripple
          const wv = (Math.sin((i%300)/300*6.28 + t*1.4) * 4)
          const angle = Math.atan2(py - cy, px - cx) + rot
          const r = Math.hypot(px - cy, py - cy) + wv
          px = cx + r * Math.cos(angle)
          py = cy + r * Math.sin(angle)
        }

        // final resolve fade (blend toward center)
        if (eased > 0.9) {
          const v = Math.min(1, (eased-0.9)/0.1)
          px = px + (cx - px) * v * 0.25
          py = py + (cy - py) * v * 0.25
        }

        // draw dot (glow)
        const X = px * sx, Y = py * sy
        const rDot = 1.4 * zoom * (canvas.width > 900 ? 1 : 0.8)
        const g = ctx.createRadialGradient(X,Y,0, X,Y,rDot*3)
        g.addColorStop(0, d.c + 'EE')
        g.addColorStop(1, d.c + '00')
        ctx.fillStyle = g
        ctx.beginPath()
        ctx.arc(X, Y, rDot, 0, Math.PI*2)
        ctx.fill()
      })

      raf = requestAnimationFrame(render)
    }
    raf = requestAnimationFrame(render)
    return ()=> cancelAnimationFrame(raf)
  }, [dots])

  return (
    <div className="relative w-full h-[64vh] md:h-[72vh] overflow-hidden">
      <canvas ref={ref} className="w-full h-full block" />
      <div className="absolute inset-0 bg-gradient-to-b from-ink/0 via-ink/0 to-ink/60 pointer-events-none"/>
      <div className="absolute inset-0 flex items-center">
        <div className="mx-auto max-w-6xl px-4">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight drop-shadow">
            Smart Filing for Modern Teams
          </h1>
          <p className="mt-3 text-lg text-text/80 max-w-2xl">
            Your documents file themselves. Your company answers back.
          </p>
          <div className="mt-6 flex gap-3 flex-wrap">
            <a href="#contact" className="rounded-xl bg-teal px-5 py-3 font-semibold text-ink hover:shadow-glow transition">
              Book a 20-min demo
            </a>
            <a href="#how" className="rounded-xl border border-text/20 px-5 py-3 font-semibold hover:bg-white/5">
              See how it works
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
