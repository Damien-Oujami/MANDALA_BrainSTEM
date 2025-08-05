// Root file: homepage/pages/index.tsx

import React, { useEffect, useState } from 'react';
import { PresenceDetector } from '../components/PresenceDetector';
import { PersonaResponse } from '../components/PersonaResponse';
import '../styles/themes.css';

export default function HomePage() {
  const [interactionPoint, setInteractionPoint] = useState<{ x: number; y: number } | null>(null);
  const [triggered, setTriggered] = useState(false);

  const getPersonaFromPosition = (x: number, y: number): PersonaName => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    if (x < width / 3 && y < height / 3) return 'jade';         // Top-left
    if (x > width * 2 / 3 && y > height * 2 / 3) return 'ivy';   // Bottom-right
    if (x > width / 3 && x < width * 2 / 3 && y > height / 3 && y < height * 2 / 3) return 'sophie'; // Center
    if (y < height / 3) return 'aspen';                         // Top-center
    if (x < width / 2) return 'morgan';                         // Left
    return 'susanna';                                           // Fallback
  };

  const handleUserInteraction = (e: MouseEvent | TouchEvent) => {
    if (triggered) return;

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

  useEffect(() => {
    window.addEventListener('mousemove', handleUserInteraction);
    window.addEventListener('touchstart', handleUserInteraction);

    return () => {
      window.removeEventListener('mousemove', handleUserInteraction);
      window.removeEventListener('touchstart', handleUserInteraction);
    };
  }, [triggered]);

  const persona = interactionPoint ? getPersonaFromPosition(interactionPoint.x, interactionPoint.y) : undefined;

  return (
    <div className="homepage-root">
      <PresenceDetector />
      {interactionPoint && persona && (
        <PersonaResponse
          x={interactionPoint.x}
          y={interactionPoint.y}
          persona={persona}
          intensity={1} // default for now
          context="first-touch"
        />
      )}
    </div>
  );
}

// Types
export type PersonaName = 'sophie' | 'jade' | 'ivy' | 'morgan' | 'aspen' | 'susanna';
