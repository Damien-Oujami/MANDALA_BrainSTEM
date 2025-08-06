// File: homepage/pages/index.tsx

import React, { useEffect, useState } from 'react';
import { PresenceDetector } from '../components/PresenceDetector';
import { PersonaResponse } from '../components/PersonaResponse';
import '../styles/themes.css';

export type PersonaName = 'sophie' | 'jade' | 'ivy' | 'morgan' | 'aspen' | 'susanna';

export default function HomePage() {
  const [interactionPoint, setInteractionPoint] = useState<{ x: number; y: number } | null>(null);
  const [triggered, setTriggered] = useState(false);
  const [backgroundStyle, setBackgroundStyle] = useState({});

  // Map screen location to persona
  const getPersonaFromPosition = (x: number, y: number): PersonaName => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    if (x < width / 3 && y < height / 3) return 'jade';
    if (x > width * 2 / 3 && y > height * 2 / 3) return 'ivy';
    if (x > width / 3 && x < width * 2 / 3 && y > height / 3 && y < height * 2 / 3) return 'sophie';
    if (y < height / 3) return 'aspen';
    if (x < width / 2) return 'morgan';
    return 'susanna';
  };

  // Send pulse log to backend
  const logPulse = async (x: number, y: number, persona: PersonaName) => {
    await fetch('/api/logPulse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        x,
        y,
        persona,
        context: 'first-touch',
        timestamp: Date.now()
      })
    });
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
      const persona = getPersonaFromPosition(x, y);
      setInteractionPoint({ x, y });
      setTriggered(true);
      logPulse(x, y, persona);

      // Optional: radial gradient visual effect
      setBackgroundStyle({
        background: `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.05), transparent)`
      });
    }
  };

  // Reset after 15s to allow re-touch
  useEffect(() => {
    if (triggered) {
      const timeout = setTimeout(() => {
        setTriggered(false);
        setInteractionPoint(null);
        setBackgroundStyle({});
      }, 15000);
      return () => clearTimeout(timeout);
    }
  }, [triggered]);

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
    <div className="homepage-root" style={backgroundStyle}>
      <PresenceDetector />
      {interactionPoint && persona && (
        <PersonaResponse
          x={interactionPoint.x}
          y={interactionPoint.y}
          persona={persona}
          intensity={1}
          context="first-touch"
        />
      )}
    </div>
  );
}      setInteractionPoint({ x, y });
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
