'use client';
import React from 'react';

type Props = {
  onBook?: () => void;
};

export default function StickyHeader({ onBook }: Props) {
  return (
    <header
      aria-label="Tekita header"
      className="tekita-header"
    >
      <a href="/" className="tekita-brand" aria-label="tekita home">tekita</a>

      <button
        className="tekita-cta"
        onClick={onBook}
        aria-label="Book a call"
      >
        Book a call
      </button>
    </header>
  );
}
