import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";

export default function PreviewQuestions() {
  const { batchId } = useParams();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await apiFetch(`/api/content/batch/${batchId}`);
        setQuestions(data);
      } catch (e) {
        setError(e.message);
      }
    }
    load();
  }, [batchId]);

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 text-white relative">
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

  if (!questions.length) {
    return (
      <div className="min-h-screen bg-slate-950 text-white relative">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
          <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
          <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
        </div>

        <main className="relative z-10 mx-auto max-w-5xl px-6 py-10">
          <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-6 py-5 text-sm text-white/70">
            Loading questions...
          </div>
        </main>
      </div>
    );
  }

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
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Preview • Generated Batch
            </div>

            <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
              Generated{" "}
              <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                Questions
              </span>{" "}
              ({questions.length})
            </h1>

            <p className="mt-2 text-white/70 max-w-2xl">
              Review your AI-generated questions before starting the quiz.
            </p>
          </div>

          <button
            onClick={() => navigate("/quiz", { state: { batchId } })}
            className="rounded-xl px-6 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
          >
            Start Quiz (This Batch)
          </button>
        </div>

        <div className="mt-8 space-y-6">
          {questions.map((q, index) => (
            <div
              key={q._id}
              className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden"
            >
              <div className="p-6">
                <div className="font-semibold text-white mb-3">
                  {index + 1}. {q.question}
                </div>

                <div className="space-y-2">
                  {q.options.map((opt, i) => (
                    <div
                      key={i}
                      className="px-4 py-3 rounded-xl ring-1 ring-white/10 bg-white/5 text-white/85"
                    >
                      {opt}
                    </div>
                  ))}
                </div>

                <div className="mt-4 text-sm text-white/55">
                  Difficulty: <span className="text-white/80">{q.difficulty}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8">
          <button
            onClick={() => navigate("/quiz", { state: { batchId } })}
            className="rounded-xl px-6 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
          >
            Start Quiz (This Batch)
          </button>
        </div>
      </main>
    </div>
  );
}