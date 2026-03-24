import { Link } from "react-router-dom";

export default function Welcome() {
  const token = localStorage.getItem("sq_token");

  return (
    <div className="min-h-[calc(100vh-72px)] bg-slate-950 text-white relative overflow-hidden">
      {/* background glow (same as login theme) */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
        <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
      </div>

      <main className="relative z-10 mx-auto max-w-6xl px-6 py-12">
        {/* top badge */}
        <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Portfolio-grade Adaptive Intelligence • Gemini Powered
        </div>

        {/* hero */}
        <div className="mt-6 grid items-center gap-10 lg:grid-cols-2">
          <div>
            <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight leading-[1.1]">
              Smart learning with{" "}
              <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                AI-powered adaptive assessment
              </span>
              .
            </h1>

            <p className="mt-5 max-w-xl text-white/70 text-base leading-relaxed">
              SmartQuizzer dynamically adjusts difficulty based on performance, generates
              robust questions, and explains answers with Gemini — designed to help you
              master faster with fewer repetitive questions.
            </p>

            {/* CTA row */}
            <div className="mt-7 flex flex-wrap gap-3">
              {token ? (
                <Link
                  to="/dashboard"
                  className="rounded-xl px-5 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
                >
                  Go to Dashboard
                </Link>
              ) : (
                <Link
                  to="/register"
                  className="rounded-xl px-5 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
                >
                  Get Started (Free)
                </Link>
              )}

              <Link
                to={token ? "/quiz" : "/login"}
                className="rounded-xl px-5 py-3 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
              >
                Start Adaptive Quiz
              </Link>

              <Link
                to={token ? "/ai" : "/login"}
                className="rounded-xl px-5 py-3 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
              >
                Try AI Helper
              </Link>
            </div>

            {/* quick stats */}
            <div className="mt-8 grid grid-cols-3 gap-3 max-w-xl">
              <Stat label="Adaptive sessions" value="Real-time" />
              <Stat label="AI explanations" value="Gemini 2.5" />
              <Stat label="Analytics" value="Built-in" />
            </div>
          </div>

          {/* right card (feature preview) */}
          <div className="mx-auto w-full max-w-lg">
            <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
              <div className="p-6 sm:p-8">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="text-xl font-semibold">What you get</h2>
                    <p className="mt-1 text-sm text-white/65">
                      Everything needed for adaptive learning.
                    </p>
                  </div>
                  <div className="h-10 w-10 rounded-xl bg-indigo-500/15 ring-1 ring-indigo-400/20 grid place-items-center">
                    <span className="text-sm font-semibold text-indigo-200">AI</span>
                  </div>
                </div>

                <div className="mt-6 grid gap-3">
                  <Feature
                    title="Adaptive Difficulty Engine"
                    desc="Questions adjust instantly based on accuracy and performance."
                  />
                  <Feature
                    title="Robust AI Question Generation"
                    desc="JSON-safe parsing + clean structured output for consistent quizzes."
                  />
                  <Feature
                    title="AI Explanations + Concept Help"
                    desc="Get instant explanations and ask follow-up doubts using Gemini."
                  />
                  <Feature
                    title="Analytics & Progress Tracking"
                    desc="Track sessions, difficulty progression, accuracy and more."
                  />
                </div>
              </div>

              <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
                Tip: Start with a quiz, then use AI Helper to strengthen weak concepts.
              </div>
            </div>
          </div>
        </div>

        {/* lower section */}
        <div className="mt-12 grid gap-4 md:grid-cols-3">
          <MiniCard
            title="Personalized learning"
            desc="Focus on what you don’t know — not repetitive questions."
          />
          <MiniCard
            title="Interview-ready portfolio"
            desc="Adaptive intelligence + AI integration + analytics in one product."
          />
          <MiniCard
            title="Fast & scalable"
            desc="MERN backend + session-based adaptive flow + batch support."
          />
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}

function Feature({ title, desc }) {
  return (
    <div className="rounded-xl bg-white/5 ring-1 ring-white/10 px-4 py-4">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-1 text-sm text-white/65">{desc}</div>
    </div>
  );
}

function MiniCard({ title, desc }) {
  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-6 py-6 backdrop-blur-xl">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-2 text-sm text-white/65">{desc}</div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded-xl bg-white/5 ring-1 ring-white/10 px-4 py-3">
      <div className="text-xs text-white/55">{label}</div>
      <div className="mt-1 text-sm font-semibold">{value}</div>
    </div>
  );
}