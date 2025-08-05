// Root file: homepage/pages/index.tsx

import React, { useEffect, useState } from 'react'; import { PresenceDetector } from '../components/PresenceDetector'; import { PersonaResponse } from '../components/PersonaResponse'; import '../styles/themes.css';

export default function HomePage() { const [interactionPoint, setInteractionPoint] = useState<{ x: number; y: number } | null>(null); const [triggered, setTriggered] = useState(false);

const handleUserInteraction = (e: MouseEvent | TouchEvent) => { if (triggered) return;

let x, y;
if ('touches' in e && e.touches.length > 0) {
  x = e.touches[0].clientX;
  y = e.touches[0].clientY;
} else if ('clientX' in e) {
  x = e.clientX;
  y = e.clientY;
}

if (x !== undefined && y !== undefined) {
  setInteractionPoint({ x, y });
  setTriggered(true);
}

};

useEffect(() => { window.addEventListener('mousemove', handleUserInteraction); window.addEventListener('touchstart', handleUserInteraction);

return () => {
  window.removeEventListener('mousemove', handleUserInteraction);
  window.removeEventListener('touchstart', handleUserInteraction);
};

}, [triggered]);

return ( <div className="homepage-root"> <PresenceDetector /> {interactionPoint && ( <PersonaResponse x={interactionPoint.x} y={interactionPoint.y} /> )} </div> ); }

