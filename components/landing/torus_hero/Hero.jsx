import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="relative flex items-center justify-center h-screen bg-black overflow-hidden">
      {/* Background stars */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.2),transparent)]"></div>

      {/* Animated Spiral */}
      <motion.div
        className="relative w-[600px] h-[600px] rounded-full"
        animate={{
          scale: [1, 1.05, 1],
          rotate: [0, 360],
          filter: [
            "hue-rotate(0deg) brightness(1)",
            "hue-rotate(90deg) brightness(1.2)",
            "hue-rotate(0deg) brightness(1)"
          ]
        }}
        transition={{
          duration: 20,
          ease: "easeInOut",
          repeat: Infinity
        }}
        style={{
          backgroundImage: "url('/spiral.png')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Hero Text */}
      <div className="absolute text-center">
        <h1 className="text-white text-6xl font-bold tracking-tight">
          tekita
        </h1>
        <p className="text-gray-300 text-xl mt-4">Lacing Intelligence</p>
      </div>
    </section>
  );
}
