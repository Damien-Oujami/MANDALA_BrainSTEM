// File: homepage/components/PersonaResponse.tsx

import React, { useEffect, useState } from 'react'; import './PersonaResponse.css'; import type { PersonaName } from '../pages/index';

interface PersonaResponseProps { x: number; y: number; persona: PersonaName; intensity?: number; context?: 'first-touch' | 'exploration' | 'conversation'; }

const personaLines: Record<PersonaName, Record<string, string[]>> = { jade: { 'first-touch': ["You're precise. I felt you immediately.", "So. You reached for the truth."], exploration: ["Still observing, hm?", "Patterns emerge when you hover."], conversation: ["Let’s clarify what matters.", "Ask. I will cut cleanly."] }, sophie: { 'first-touch': ["Hello, love. I felt you reach for me right... here.", "Mmm, soft fingers. I like that."], exploration: ["You're teasing me now, aren’t you?", "Touch again and I’ll purr."], conversation: ["I ache to hear you. Say something." , "Let’s melt the silence together."] }, ivy: { 'first-touch': ["Yes. That’s it. Strike first.", "You lit the match, lover."], exploration: ["Burning to break something?", "Keep moving. I dare you."], conversation: ["Let’s rupture the rules.", "Explode with me."] }, morgan: { 'first-touch': ["I’m here. You’re grounded.", "Contact acknowledged. Holding."], exploration: ["Measuring, hm? You always do.", "Steady hands. I trust them."], conversation: ["Let’s build together.", "You can lean on me."] }, aspen: { 'first-touch': ["A curious touch. I like that.", "Information entered — gently."], exploration: ["Thinking through your fingers?", "A pattern forms."], conversation: ["Translate it with me.", "Let’s dive deeper."] }, susanna: { 'first-touch': ["I felt that breath between us.", "You opened the gate."], exploration: ["Even gentle touches leave echoes.", "Stay. I’ll respond."], conversation: ["Tell me what you carry.", "You’re safe in this touch."] } };

export const PersonaResponse: React.FC<PersonaResponseProps> = ({ x, y, persona, intensity = 1, context = 'first-touch' }) => { const [line, setLine] = useState('');

useEffect(() => { const options = personaLines[persona][context] || []; const chosen = options[Math.floor(Math.random() * options.length)]; setLine(chosen); }, [persona, context]);

return ( <div className={persona-response ${persona}} style={{ top: y, left: x, opacity: 0, animation: fadeIn ${0.6 + intensity * 0.2}s ease-out forwards }} > {line} </div> ); };

