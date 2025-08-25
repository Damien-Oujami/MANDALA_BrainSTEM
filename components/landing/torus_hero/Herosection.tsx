"use client";
import React from "react";
import StarfieldCanvas from "./StarfieldCanvas";
import TekitaHeroTorus from "./TekitaHeroTorus"; // from our earlier message

export default function HeroSection() {
  return (
    <section className="relative h-[85svh] w-full overflow-hidden bg-[#05080f]">
      {/* depth layer 0: stars */}
      <StarfieldCanvas className="absolute inset-0 z-0" density={1.0} drift={0.35} twinkle={0.35} />

      {/* depth layer 1: breathing torus */}
      <div className="absolute inset-0 z-10">
        <TekitaHeroTorus className="h-full w-full" intensity={0.95} speed={1.0} />
      </div>

      {/* depth layer 2: your copy/CTA */}
      <div className="relative z-20 flex h-full items-center justify-center">
        <div className="px-6 text-center">
          <h1 className="text-white/95 tracking-tight font-extrabold text-5xl md:text-7xl">
            tekita
          </h1>
          <p className="mt-4 text-lg md:text-xl text-white/70">
            Lacing Intelligence
          </p>
          <div className="mt-8 flex gap-3 justify-center">
            <a
              href="#contact"
              className="rounded-xl bg-white/10 px-6 py-3 text-white/90 backdrop-blur hover:bg-white/15 transition"
            >
              Get in touch
            </a>
            <a
              href="#work"
              className="rounded-xl bg-cyan-500/90 px-6 py-3 text-black font-semibold hover:bg-cyan-400 transition"
            >
              See work
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
