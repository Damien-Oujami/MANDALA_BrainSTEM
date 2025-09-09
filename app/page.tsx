'use client';
import React, { useState } from 'react';
import StickyHeader from '../components/StickyHeader';
import IntakeDrawer from '../components/IntakeDrawer';
import SnapSlides, { Slide } from '../components/SnapSlides';

// ⬇️ import your existing hero exactly as-is
import Hero from '../components/HeroOrchestratedJitter';          // <— keep your current file path
import Carousel from '../components/CarouselStackedHuge';  // <— your existing center copy

export default function Page(){
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* fixed brand + CTA */}
      <StickyHeader onBook={() => setOpen(true)} />
      <IntakeDrawer open={open} onClose={() => setOpen(false)} />

      {/* your animated donut as the underlay */}
      <div className="hero-underlay" aria-hidden>
        <Hero />
      </div>

      {/* slides with magnetic center snap */}
      <SnapSlides>
        {/* Slide 0 – your carousel, unchanged */}
        <Slide id="slide-0">
          <div style={{display:'grid', placeItems:'center'}}>
            <Carousel />
          </div>
        </Slide>

        {/* Slide 1 – simple translucent metric bar (placeholder content) */}
        <Slide id="slide-1">
          <div className="glass" style={{padding:'28px', width:'min(900px,92vw)'}}>
            <h2 className="hero-line" style={{fontSize:'clamp(24px,4.6vw,48px)'}}>Ship outcomes faster. Own your stack.</h2>
            <div className="metrics" style={{marginTop:16}}>
              <Metric k="Speed" v="+3–5×" />
              <Metric k="Quality" v="↑ Consistency" />
              <Metric k="Busywork" v="–40–80%" />
            </div>
          </div>
        </Slide>

        {/* Slide 2 – Smart Filing + GraphRAG summary card */}
        <Slide id="slide-2">
          <div className="glass" style={{padding:'28px', width:'min(1000px,92vw)'}}>
            <h2 className="hero-line" style={{fontSize:'clamp(24px,4.6vw,48px)'}}>Smart Filing + Weighted GraphRAG</h2>
            <p className="muted" style={{textAlign:'center', marginTop:8}}>
              Auto‑organize content, link concepts, and surface deadlines via excite / inhibit signals.
            </p>
            <PipelineSketch />
          </div>
        </Slide>

        {/* Slide 3 – Offer / CTA helper */}
        <Slide id="slide-3">
          <div className="glass" style={{padding:'28px', width:'min(860px,92vw)'}}>
            <h2 className="hero-line" style={{fontSize:'clamp(26px,5vw,52px)'}}>Your AI Transformation Partner</h2>
            <ul style={{margin:'16px auto 0', maxWidth:700, color:'#dfe7f1', lineHeight:1.5}}>
              <li>Discovery → Opportunity map → Pilot in weeks, not quarters.</li>
              <li>Smart Filing baseline + bespoke automations + training your team.</li>
              <li>Own your data. No black‑box lock‑in.</li>
            </ul>
            <div style={{display:'grid', placeItems:'center', marginTop:18}}>
              <button className="tekita-cta glow" onClick={()=>setOpen(true)}>Book a call</button>
            </div>
          </div>
        </Slide>
      </SnapSlides>
    </>
  );
}

/** tiny presentational bits to avoid new deps */
function Metric({k, v}:{k:string; v:string}){
  return (
    <div className="glass" style={{padding:'14px 16px'}}>
      <div style={{color:'#9afff4', fontSize:12, letterSpacing:.4}}>{k}</div>
      <div style={{color:'#fff', fontSize:20, fontWeight:800}}>{v}</div>
    </div>
  );
}

// simple inline SVG sketch so the “graph” looks sleek & translucent
function PipelineSketch(){
  return (
    <svg viewBox="0 0 920 220" width="100%" height="220" style={{display:'block', marginTop:16}}>
      <defs>
        <linearGradient id="g" x1="0" x2="1">
          <stop offset="0" stopColor="#17c6f6" stopOpacity=".9"/>
          <stop offset=".5" stopColor="#a653ff" stopOpacity=".9"/>
          <stop offset="1" stopColor="#ff6a3d" stopOpacity=".9"/>
        </linearGradient>
      </defs>
      <g fill="none" stroke="url(#g)" strokeWidth="2.2" opacity=".9">
        <rect x="20" y="30" width="200" height="60" rx="12" />
        <text x="120" y="66" textAnchor="middle" fill="#dfe7f1" style={{font: '600 14px Montserrat'}}>Ingest</text>

        <path d="M220,60 C260,60 280,110 320,110" />
        <rect x="320" y="80" width="210" height="60" rx="12" />
        <text x="425" y="116" textAnchor="middle" fill="#dfe7f1" style={{font: '600 14px Montserrat'}}>
          Smart Filing (normalize + classify)
        </text>

        <path d="M530,110 C570,110 600,60 640,60" />
        <rect x="640" y="30" width="260" height="60" rx="12" />
        <text x="770" y="66" textAnchor="middle" fill="#dfe7f1" style={{font: '600 14px Montserrat'}}>
          GraphRAG (excite / inhibit / resonate)
        </text>

        <path d="M770,90 C770,140 530,170 340,170"/>
        <rect x="280" y="140" width="120" height="60" rx="12" />
        <text x="340" y="176" textAnchor="middle" fill="#dfe7f1" style={{font: '600 14px Montserrat'}}>
          Alerts
        </text>

        <path d="M400,170 C550,170 680,170 820,170" />
        <rect x="820" y="140" width="80" height="60" rx="12" />
        <text x="860" y="176" textAnchor="middle" fill="#dfe7f1" style={{font: '600 14px Montserrat'}}>
          Team
        </text>
      </g>
    </svg>
  );
}
