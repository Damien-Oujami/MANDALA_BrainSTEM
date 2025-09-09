
'use client';
import React, { useEffect, useState } from 'react';

const slides = [
  { line1: <>Identifying <span className='your-teal'>your</span></>, line2: <>AI Solutions</> },
  { line1: <>Designing <span className='your-magenta'>your</span></>, line2: <>Automated Workflow</> },
  { line1: <>Training <span className='your-violet'>your</span></>, line2: <>Team</> },
  { line1: <><span className='your-honey'>Your</span></>, line2: <>AI Transformation Partner</> },
];

export default function Carousel({ start=false }: { start?: boolean }){
  const [idx, setIdx] = useState(0);
  const [show, setShow] = useState(false);

  useEffect(()=>{
    if(!start) return;
    setShow(true);
    const int = setInterval(()=>{
      setShow(false);
      setTimeout(()=>{
        setIdx(i => (i+1) % slides.length);
        setShow(true);
      }, 280);
    }, 3000);
    return ()=> clearInterval(int);
  }, [start]);

  const s = slides[idx];
  return (
    <div className="carousel" aria-live="polite">
      <p className={"slide " + (show ? "show" : "")}>
        <span className="line">{s.line1}</span>
        <span className="line">{s.line2}</span>
      </p>
    </div>
  );
}
