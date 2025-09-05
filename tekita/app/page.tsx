import SpiralCanvas from '@/components/SpiralCanvas'

export default function Page(){
  return (
    <main className="min-h-screen">
      {/* NAV */}
      <nav className="sticky top-0 z-40 backdrop-blur bg-ink/70 border-b border-white/5">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <a className="font-semibold text-xl">tekita</a>
          <div className="hidden md:flex gap-6 text-sm">
            <a href="#how">How it works</a>
            <a href="#benefits">Benefits</a>
            <a href="#serve">Who we serve</a>
            <a href="#pricing">Pricing</a>
            <a href="#faq">FAQ</a>
            <a href="#contact" className="rounded-xl border border-white/15 px-3 py-1.5 hover:bg-white/5">Book demo</a>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section><SpiralCanvas/></section>

      {/* KPI STRIP */}
      <section className="border-y border-white/5 bg-white/5">
        <div className="mx-auto max-w-6xl px-4 py-6 grid sm:grid-cols-3 gap-4 text-center">
          <div><div className="text-2xl font-extrabold">30–50%</div><div className="text-white/70 text-sm">faster responses</div></div>
          <div><div className="text-2xl font-extrabold">0</div><div className="text-white/70 text-sm">lost documents</div></div>
          <div><div className="text-2xl font-extrabold">≥99%</div><div className="text-white/70 text-sm">consistent naming</div></div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="mx-auto max-w-6xl px-4 py-16 grid md:grid-cols-2 gap-10">
        <div>
          <h2 className="text-3xl font-bold">Built for teams drowning in PDFs</h2>
          <ul className="mt-4 space-y-2 text-white/80">
            <li>• Email threads hide critical files</li>
            <li>• Expiring COIs / approvals / renewals</li>
            <li>• Inconsistent folders across projects</li>
            <li>• Time wasted answering “Where is it?”</li>
          </ul>
        </div>
        <div>
          <h3 className="text-xl font-semibold">Tekita does the filing for you</h3>
          <ol className="mt-4 space-y-3 text-white/80 list-decimal list-inside">
            <li><b>Ingest</b> — watch inbox/Drive, drag-and-drop</li>
            <li><b>Classify</b> — doc type, project, vendor, dates</li>
            <li><b>Route</b> — create folders, rename, move</li>
            <li><b>Index</b> — Graph-RAG for “ask-the-company” Q&A</li>
            <li><b>Notify</b> — Slack/Email: what, where, and why</li>
          </ol>
        </div>
      </section>

      {/* BENEFITS, WHO WE SERVE, PRICING, FAQ, CONTACT — add your copy or use the earlier block */}
      {/* ... */}
    </main>
  )
}
