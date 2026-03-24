import { Link } from "react-router-dom";

export default function Dashboard() {
  const name = localStorage.getItem("sq_name") || "Learner"; // optional (safe)
  const email = localStorage.getItem("sq_email") || "";     // optional (safe)

  return (
    <div className="min-h-screen bg-slate-950 text-white relative">
      {/* background glow (same theme) */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
        <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
      </div>

      <main className="relative z-10 mx-auto max-w-6xl px-6 py-10">
        {/* Top row */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Dashboard • Adaptive Engine
            </div>

            <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
              Welcome back,{" "}
              <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                {name}
              </span>
            </h1>

            <p className="mt-3 max-w-2xl text-white/70">
              Start a new adaptive session, generate a fresh batch, or review your analytics.
              Your learning path updates in real-time.
              {email ? <span className="text-white/50"> ({email})</span> : null}
            </p>
          </div>

          <div className="flex gap-3">
            <Link
              to="/quiz"
              className="rounded-xl px-5 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
            >
              Start Adaptive Quiz
            </Link>

            <Link
              to="/analytics"
              className="rounded-xl px-5 py-3 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
            >
              View Analytics
            </Link>
          </div>
        </div>

        {/* Stats row */}
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Current Mode" value="Adaptive" hint="Difficulty adjusts in real-time" />
          <StatCard title="AI Model" value="Gemini 2.5" hint="Fast explain + pro generation" />
          <StatCard title="Sessions" value="Tracked" hint="Performance analytics enabled" />
          <StatCard title="Next Step" value="Quiz" hint="Start /quiz to continue" />
        </div>

        {/* Main grid */}
        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          {/* Quick actions */}
          <div className="lg:col-span-2 rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
            <div className="p-6 sm:p-8">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="text-xl font-semibold">Quick actions</h2>
                  <p className="mt-1 text-sm text-white/65">
                    Jump into learning or create new content.
                  </p>
                </div>
                <div className="h-10 w-10 rounded-xl bg-indigo-500/15 ring-1 ring-indigo-400/20 grid place-items-center">
                  <span className="text-sm font-semibold text-indigo-200">SQ</span>
                </div>
              </div>

              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                <ActionCard
                  title="Adaptive Quiz"
                  desc="Start a session and let the engine adjust difficulty."
                  to="/quiz"
                  primary
                  cta="Start now"
                />
                <ActionCard
                  title="AI Helper"
                  desc="Ask doubts, get explanations, and learn concepts."
                  to="/ai"
                  cta="Open helper"
                />
                <ActionCard
                  title="Generate Questions"
                  desc="Create a new batch using AI-powered generation."
                  to="/generate"
                  cta="Generate"
                />
                <ActionCard
                  title="Analytics"
                  desc="Track accuracy, progression and session history."
                  to="/analytics"
                  cta="View"
                />
              </div>
            </div>

            <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
              Tip: After every quiz session, open AI Helper for concept reinforcement.
            </div>
          </div>

          {/* Right: roadmap card */}
          <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
            <div className="p-6 sm:p-8">
              <h2 className="text-xl font-semibold">Today’s plan</h2>
              <p className="mt-1 text-sm text-white/65">
                A quick loop for rapid improvement.
              </p>

              <div className="mt-6 space-y-3">
                <Step n="1" title="Take 8–10 questions" desc="Start a short adaptive session." />
                <Step n="2" title="Review explanations" desc="Open AI Helper for weak concepts." />
                <Step n="3" title="Check your analytics" desc="See accuracy + difficulty progression." />
              </div>

              <div className="mt-6 rounded-xl bg-white/5 ring-1 ring-white/10 px-4 py-4">
                <div className="text-xs text-white/55">Suggested focus</div>
                <div className="mt-1 text-sm font-semibold">
                  Consistency over intensity
                </div>
                <div className="mt-1 text-sm text-white/65">
                  10 minutes daily beats 2 hours once a week.
                </div>
              </div>
            </div>

            <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
              You’re building a portfolio-grade project — keep iterating.
            </div>
          </div>
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}

function StatCard({ title, value, hint }) {
  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-5 py-4 backdrop-blur-xl">
      <div className="text-xs text-white/55">{title}</div>
      <div className="mt-1 text-lg font-semibold">{value}</div>
      <div className="mt-1 text-sm text-white/65">{hint}</div>
    </div>
  );
}

function ActionCard({ title, desc, to, cta, primary }) {
  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 p-5">
      <div className="text-sm font-semibold">{title}</div>
      <div className="mt-1 text-sm text-white/65">{desc}</div>

      <Link
        to={to}
        className={
          primary
            ? "mt-4 inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
            : "mt-4 inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
        }
      >
        {cta}
      </Link>
    </div>
  );
}

function Step({ n, title, desc }) {
  return (
    <div className="rounded-xl bg-white/5 ring-1 ring-white/10 px-4 py-4">
      <div className="flex items-start gap-3">
        <div className="h-8 w-8 rounded-lg bg-indigo-500/15 ring-1 ring-indigo-400/20 grid place-items-center text-sm font-semibold text-indigo-200">
          {n}
        </div>
        <div>
          <div className="text-sm font-semibold">{title}</div>
          <div className="mt-1 text-sm text-white/65">{desc}</div>
        </div>
      </div>
    </div>
  );
}