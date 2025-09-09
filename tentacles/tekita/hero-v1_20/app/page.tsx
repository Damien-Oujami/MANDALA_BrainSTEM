
'use client';
import React, { useEffect, useState } from 'react';
import Hero from '../components/HeroOrchestratedJitter';
import Carousel from '../components/CarouselStackedHuge';

export default function Page(){
  const [showBrand, setShowBrand] = useState(false);
  const [fadeBrandOut, setFadeBrandOut] = useState(false);
  const [docked, setDocked] = useState(false);
  const [blur, setBlur] = useState(false);
  const [showCTA, setShowCTA] = useState(false);
  const [ctaSlide, setCtaSlide] = useState(false);
  const [ctaPinned, setCtaPinned] = useState(false);
  const [startCarousel, setStartCarousel] = useState(false);

  useEffect(()=>{
    const onStabilize = () => {
      setShowBrand(true);
      setTimeout(()=> setFadeBrandOut(true), 900);
      setTimeout(()=> { setDocked(true); setFadeBrandOut(false); }, 1500);
      setTimeout(()=> setBlur(true), 1600);
      setTimeout(()=> setShowCTA(true), 1700);
      setTimeout(()=> setCtaSlide(true), 2300);
      setTimeout(()=> { setCtaPinned(true); setStartCarousel(true); }, 3300); // start AFTER pin
    };
    window.addEventListener('hero:stabilized', onStabilize as any);
    return ()=> window.removeEventListener('hero:stabilized', onStabilize as any);
  },[]);

  return (
    <div className="stage">
      <div className="edge-glow" />
      <div className={"canvas-wrap" + (blur ? " blurred" : "")}>
        <Hero />
      </div>
      <div className={"brand" + (showBrand ? " show" : "") + (fadeBrandOut ? " fadeout" : "") + (docked ? " docked" : "")}>
        <h1>tekita</h1>
      </div>
      <div className={"cta" + (showCTA ? " show" : "") + (ctaSlide ? " slide" : "") + (ctaPinned ? " pinned" : "")}>
        <a href="#contact" id="cta-primary">Book a call</a>
      </div>
      <Carousel start={startCarousel} />
    </div>
  );
}
