import { motion } from "framer-motion" import React from "react"

const HeroMotion = () => { return ( <div className="relative w-full h-screen overflow-hidden bg-black text-white"> {/* Background Smoke Gradient Motion */} <motion.div className="absolute inset-0 z-0" initial={{ backgroundPosition: "0% 50%" }} animate={{ backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"] }} transition={{ duration: 60, repeat: Infinity, ease: "linear" }} style={{ backgroundImage: "radial-gradient(circle at center, #0ff 0%, #f0f 30%, #f90 60%)", backgroundSize: "400% 400%", opacity: 0.08, filter: "blur(120px)" }} />

{/* Spiral Logo Motion */}
  <motion.img
    src="/logo/tekita-spiral.svg"
    alt="Tekita Spiral"
    className="w-48 h-48 mx-auto mt-32 z-10"
    initial={{ scale: 1 }}
    animate={{ scale: [1, 1.02, 1] }}
    transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
  />

  {/* Title & Tagline */}
  <div className="relative z-10 text-center mt-10">
    <h1 className="text-5xl font-bold tracking-wide">tekita</h1>
    <motion.p
      className="text-xl mt-2"
      animate={{
        color: ["#ffffff", "#00ffff", "#ff00ff", "#ffaa00", "#ffffff"]
      }}
      transition={{ duration: 10, repeat: Infinity }}
    >
      LACING INTELLIGENCE
    </motion.p>
  </div>
</div>

) }

export default HeroMotion

