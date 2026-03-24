import { useState } from "react";
import { contentApi } from "../api/content";
import { useNavigate } from "react-router-dom";

export default function GenerateQuestions() {
  const [method, setMethod] = useState("text"); // text | url | pdf
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [topic, setTopic] = useState("General");
  const [count, setCount] = useState(12);
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  async function handleGenerate() {
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      let res;

      if (method === "pdf") {
        if (!file) throw new Error("Please choose a PDF file.");
        res = await contentApi.generatePdf({ file, topic, count });
      } else {
        res = await contentApi.generate({
          method,
          text,
          url,
          topic,
          count,
        });
      }

      setResult(res);

      if (!res?.batchId) {
        throw new Error("batchId not returned from backend");
      }

      navigate(`/preview/${String(res.batchId)}`);
    } catch (e) {
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white relative">
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
              Generate • AI Question Builder
            </div>

            <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
              Generate{" "}
              <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                Questions
              </span>
            </h1>

            <p className="mt-2 text-white/70 max-w-2xl">
              Create batch-wise quizzes from text, URL, or PDF using Gemini. You’ll be redirected to a preview page after generation.
            </p>
          </div>

          <button
            onClick={() => navigate("/quiz")}
            className="rounded-xl px-5 py-3 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
          >
            Go to Quiz
          </button>
        </div>

        <div className="mt-8 rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
          <div className="p-6 sm:p-8 space-y-6">
            <div className="flex flex-wrap gap-3">
              <TabButton active={method === "text"} onClick={() => setMethod("text")}>
                Text
              </TabButton>
              <TabButton active={method === "url"} onClick={() => setMethod("url")}>
                URL
              </TabButton>
              <TabButton active={method === "pdf"} onClick={() => setMethod("pdf")}>
                PDF
              </TabButton>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="text-sm text-white/70">Topic</label>
                <input
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35"
                  placeholder="e.g. Calculus"
                />
              </div>

              <div>
                <label className="text-sm text-white/70">Count</label>
                <input
                  type="number"
                  value={count}
                  onChange={(e) => setCount(Number(e.target.value))}
                  className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60"
                  min={1}
                  max={50}
                />
                <div className="mt-1 text-xs text-white/45">Max 50 recommended.</div>
              </div>
            </div>

            {method === "text" && (
              <div>
                <label className="text-sm text-white/70">Paste Text (min ~200 chars)</label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="mt-2 w-full min-h-[160px] rounded-2xl bg-slate-950/40 p-4 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35 resize-y"
                  placeholder="Paste content here..."
                />
              </div>
            )}

            {method === "url" && (
              <div>
                <label className="text-sm text-white/70">URL</label>
                <input
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35"
                  placeholder="https://example.com/article"
                />
              </div>
            )}

            {method === "pdf" && (
              <div>
                <label className="text-sm text-white/70">Upload PDF</label>
                <div className="mt-2 rounded-xl bg-slate-950/40 ring-1 ring-white/10 px-4 py-3">
                  <input
                    type="file"
                    accept="application/pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="w-full text-sm text-white/70 file:mr-4 file:rounded-lg file:border-0 file:bg-white/10 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-white/15"
                  />
                  <div className="mt-2 text-xs text-white/45">
                    {file ? `Selected: ${file.name}` : "Choose a PDF to generate questions from its content."}
                  </div>
                </div>
              </div>
            )}

            <div className="flex flex-wrap items-center justify-end gap-3">
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="rounded-xl px-6 py-3 text-sm font-semibold bg-emerald-500/90 hover:bg-emerald-500 transition shadow-lg shadow-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Generating..." : "Generate & Save"}
              </button>
            </div>

            {error && (
              <div className="rounded-2xl bg-red-500/10 ring-1 ring-red-500/25 px-5 py-4 text-sm text-red-200">
                {error}
              </div>
            )}

            {result && (
              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 px-5 py-4">
                <div className="font-semibold text-white">{result.message}</div>
                <div className="text-sm mt-1 text-white/80">
                  Saved: <b>{result.count}</b> questions
                </div>
                <div className="text-xs text-white/55 mt-2 break-words">
                  Batch ID: {String(result.batchId || "")}
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
            Tip: Use Preview to verify quality, then start an Adaptive Quiz using that batch.
          </div>
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}

function TabButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={
        active
          ? "rounded-xl px-4 py-2 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20"
          : "rounded-xl px-4 py-2 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition"
      }
    >
      {children}
    </button>
  );
}