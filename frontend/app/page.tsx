import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-6 py-6 sm:px-10 lg:px-16">
        <header className="flex items-center justify-between">
          <Link
            className="flex items-center gap-3 rounded-md focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cyan-300"
            href="/"
            aria-label="BetBot home"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-300 font-black text-slate-950">
              B
            </span>
            <span className="text-lg font-bold tracking-tight">BetBot</span>
          </Link>
          <span className="rounded-full border border-slate-700 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Web foundation
          </span>
        </header>

        <section className="relative flex flex-1 items-center py-20">
          <div className="pointer-events-none absolute -right-32 top-1/2 h-96 w-96 -translate-y-1/2 rounded-full bg-cyan-400/15 blur-3xl" />
          <div className="relative max-w-3xl">
            <p className="mb-6 text-sm font-semibold uppercase tracking-[0.24em] text-cyan-300">
              Virtual betting for Discord communities
            </p>
            <h1 className="max-w-2xl text-5xl font-bold tracking-tight text-white sm:text-7xl">
              Bet together.
              <span className="block text-cyan-300">Have more fun.</span>
            </h1>
            <p className="mt-8 max-w-xl text-lg leading-8 text-slate-300 sm:text-xl">
              BetBot brings simple, server-based virtual betting to the
              communities you already enjoy. The web experience is being built
              alongside the Discord app.
            </p>
            <div className="mt-10 inline-flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-slate-300">
              <span
                className="h-2.5 w-2.5 rounded-full bg-amber-300"
                aria-hidden="true"
              />
              The web client is coming soon.
            </div>
          </div>
        </section>

        <footer className="border-t border-slate-800 py-6 text-sm text-slate-500">
          BetBot uses virtual currency only and is not a real-money gambling
          platform.
        </footer>
      </div>
    </main>
  );
}
