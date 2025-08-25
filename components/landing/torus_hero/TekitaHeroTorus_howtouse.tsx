import TekitaHeroTorus from "./TekitaHeroTorus";

export default function Page() {
  return (
    <main className="bg-[#05080f] text-white">
      <TekitaHeroTorus className="h-[80svh] w-full" intensity={0.95} speed={1}/>
      {/* your CTA section below */}
    </main>
  );
}
