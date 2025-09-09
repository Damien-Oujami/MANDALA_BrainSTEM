'use client';
import React, { useEffect, useRef } from 'react';

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function IntakeDrawer({ open, onClose }: Props){
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function esc(e: KeyboardEvent){
      if(e.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', esc);
    return () => document.removeEventListener('keydown', esc);
  }, [onClose]);

  return (
    <>
      <div
        className="drawer-backdrop"
        aria-hidden={!open}
        style={{ opacity: open ? 1 : 0, pointerEvents: open ? 'auto':'none' }}
        onClick={onClose}
      />
      <aside
        ref={ref}
        aria-label="Lead intake"
        className={`drawer ${open ? 'open':''}`}
      >
        <h2>Book a discovery call</h2>
        <p className="muted">Tell us a little about your goals. We’ll reply within one business day.</p>

        <form className="form" onSubmit={(e)=>{e.preventDefault(); onClose();}}>
          <label>Full name<input required name="name" placeholder="Jane Doe" /></label>
          <label>Work email<input required type="email" name="email" placeholder="jane@company.com" /></label>
          <label>Company<input name="company" placeholder="Acme Inc." /></label>
          <label>What would you like to improve?
            <textarea name="goals" rows={4} placeholder="e.g., cut manual reporting, centralize docs with Smart Filing, add GraphRAG…"/>
          </label>
          <button className="submit">Send</button>
          <a className="alt" href={process.env.NEXT_PUBLIC_BOOKING_URL || '#'} target="_blank">…or pick a time</a>
        </form>
      </aside>
    </>
  );
}
