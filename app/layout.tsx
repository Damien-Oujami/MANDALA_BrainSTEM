
import './styles/globals.css';
import React from 'react';
export const metadata = { title: 'tekita — hero v1.20', description: 'CTA pinned higher + carousel starts after pin' };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>{children}</body></html>);
}
