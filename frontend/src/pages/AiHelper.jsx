import { useState } from "react";
import { aiApi } from "../api/ai";

export default function AiHelper() {
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const data = await aiApi.ask(prompt);
      setAnswer(data.answer || data.response || data.result || "No response");
    } catch (e) {
      setError(e.message || "Failed to ask AI");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white relative">
      {/* background glow (same theme) */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
        <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
      </div>

      <main className="relative z-10 mx-auto max-w-5xl px-6 py-10">
        {/* Header */}
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            AI Helper • Gemini Explanations
          </div>

          <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
            AI{" "}
            <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
              Helper
            </span>
          </h1>

          <p className="mt-2 text-white/70 max-w-2xl">
            Ask anything. Get step-by-step explanations and concept clarification using Gemini.
          </p>
        </div>

        {/* Main card */}
        <div className="mt-8 rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
          <div className="p-6 sm:p-8">
            <label className="text-sm text-white/70">Your question</label>

            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="mt-2 w-full min-h-[160px] rounded-2xl bg-slate-950/40 p-4 text-sm outline-none
                         ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60
                         placeholder:text-white/35 resize-y"
              placeholder="Ask anything... e.g., Explain binary search with an example"
            />

            <div className="mt-4 flex flex-wrap gap-3 justify-end">
              <button
                type="button"
                onClick={handleAsk}
                disabled={loading || !prompt.trim()}
                className="rounded-xl px-5 py-3 text-sm font-semibold
                           bg-indigo-500/90 hover:bg-indigo-500 transition
                           shadow-lg shadow-indigo-500/20
                           disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Asking..." : "Ask AI"}
              </button>
            </div>

            {/* Error */}
            {error && (
              <div className="mt-6 rounded-2xl bg-red-500/10 ring-1 ring-red-500/25 px-5 py-4 text-sm text-red-200">
                {error}
              </div>
            )}

            {/* Answer */}
            {answer && (
              <div className="mt-6 rounded-2xl bg-white/5 ring-1 ring-white/10 px-5 py-4 whitespace-pre-line">
                <div className="text-sm font-semibold text-white">Answer</div>
                <div className="mt-2 text-sm text-white/80 leading-relaxed">
                  {answer}
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
            Tip: Ask follow-ups like “give me 3 practice questions” or “explain step-by-step”.
          </div>
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}