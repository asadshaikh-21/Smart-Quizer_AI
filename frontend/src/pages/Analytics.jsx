import { useEffect, useState } from "react";
import { analyticsApi } from "../api/analytics";

export default function Analytics() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  async function load() {
    try {
      const res = await analyticsApi.getSummary();
      setData(res);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 text-white relative">
        {/* background glow */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
          <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
          <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
        </div>

        <main className="relative z-10 mx-auto max-w-5xl px-6 py-10">
          <div className="rounded-2xl bg-red-500/10 ring-1 ring-red-500/25 px-5 py-4 text-sm text-red-200">
            {error}
          </div>
        </main>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 text-white relative">
        {/* background glow */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
          <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
          <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
        </div>

        <main className="relative z-10 mx-auto max-w-5xl px-6 py-10">
          <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-6 py-5 text-sm text-white/70">
            Loading...
          </div>
        </main>
      </div>
    );
  }

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
        {/* Header */}
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            Analytics • Performance Summary
          </div>

          <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
            Analytics{" "}
            <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
              Summary
            </span>
          </h1>

          <p className="mt-2 text-white/70 max-w-2xl">
            Track your sessions, answers, accuracy and difficulty performance in one place.
          </p>
        </div>

        {/* Top stats */}
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <Card title="Total Sessions" value={data.totalSessions} />
          <Card title="Total Answers" value={data.totalAnswered} />
          <Card title="Total Correct" value={data.totalCorrect} />
          <Card title="Overall Accuracy" value={`${data.overallAccuracy}%`} />
          <Card title="Average Score" value={data.avgScore} />
        </div>

        {/* Difficulty breakdown */}
        <div className="mt-8 rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
          <div className="p-6 sm:p-8">
            <h2 className="text-lg font-semibold">Accuracy by Difficulty</h2>
            <p className="mt-1 text-sm text-white/65">
              See how you perform across difficulty levels.
            </p>

            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(data.accuracyByDifficulty).map(([key, value]) => (
              <Card key={key} title={key} value={`${value}%`} />
            ))}
          </div>
          </div>

          <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
            Tip: Use AI Helper after wrong answers to fix weak concepts quickly.
          </div>
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-5 py-4 backdrop-blur-xl">
      <div className="text-xs text-white/55">{title}</div>
      <div className="mt-1 text-xl sm:text-2xl font-semibold text-white">
        {value}
      </div>
    </div>
  );
}
function DifficultyCard({ title, value }) {
  const pct = Math.max(0, Math.min(100, value));

  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-5 py-4 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-3">
        <div className="text-sm font-semibold text-white/90">{title}</div>
        <div className="text-sm font-semibold text-white">{pct}%</div>
      </div>

      <div className="mt-3 h-2 w-full rounded-full bg-white/10 overflow-hidden ring-1 ring-white/10">
        <div
          className="h-full rounded-full bg-indigo-400/70 shadow-[0_0_18px_rgba(99,102,241,0.35)]"
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="mt-2 text-xs text-white/55">
        {pct >= 80
          ? "Strong"
          : pct >= 50
          ? "Improving"
          : "Needs focus"}
      </div>
    </div>
  );
}