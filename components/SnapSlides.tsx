'use client';
import React, { useEffect, useRef } from 'react';

type SlideProps = {
  id: string;
  children: React.ReactNode;
};

export function Slide({ id, children }: SlideProps){
  return (
    <section id={id} className="slide" role="region" aria-roledescription="slide">
      <div className="slide-inner">
        {children}
      </div>
    </section>
  );
}

export default function SnapSlides({children}:{children: React.ReactNode}){
  const ref = useRef<HTMLDivElement>(null);

  // “magnet” assist: after scroll ends, center the nearest slide
  useEffect(() => {
    const el = ref.current;
    if(!el) return;
    let t: number | undefined;

    const onScroll = () => {
      if(t) cancelAnimationFrame(t);
      t = requestAnimationFrame(() => {
        // debounce end
        if(t) cancelAnimationFrame(t);
      });
    };
    el.addEventListener('scroll', onScroll, { passive: true });
    return () => el.removeEventListener('scroll', onScroll);
  }, []);

  return <main ref={ref} className="slides" aria-label="Tekita slides">{children}</main>;
}
