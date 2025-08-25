"use client";
import { motion } from "framer-motion";

export default function TekitaHero() {
  return (
    <section className="relative flex items-center justify-center h-screen bg-[#05080f] overflow-hidden">
      {/* Background subtle stars */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-black via-[#0b0f1c] to-black opacity-90"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.15),transparent_70%)]"></div>
      </div>

      {/* Animated Spiral */}
      <motion.div
        className="relative w-[600px] h-[600px] rounded-full"
        animate={{
          scale: [1, 1.05, 1],
          rotate: [0, 360],
          filter: [
            "hue-rotate(0deg) brightness(1)",
            "hue-rotate(90deg) brightness(1.2)",
            "hue-rotate(180deg) brightness(1)",
            "hue-rotate(0deg) brightness(1)",
          ],
        }}
        transition={{
          duration: 30,
          ease: "linear",
          repeat: Infinity,
        }}
        style={{
          backgroundImage: "url('/spiral.png')", // put your torus spiral image here
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Hero Content */}
      <div className="absolute text-center px-4">
        <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight drop-shadow-lg">
          tekita
        </h1>
        <p className="text-lg md:text-xl text-gray-300 mt-4">
          Lacing Intelligence
        </p>
      </div>
    </section>
  );
}
