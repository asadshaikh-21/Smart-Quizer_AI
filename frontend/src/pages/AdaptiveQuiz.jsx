import { useEffect, useMemo, useState } from "react";
import QuestionCard from "../components/QuestionCard";
import { adaptiveApi } from "../api/adaptive";
import { useLocation, useNavigate } from "react-router-dom";

export default function AdaptiveQuiz() {
  const location = useLocation();
  const navigate = useNavigate();
  const batchId = location.state?.batchId || null;

  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [error, setError] = useState(null);

  const canSubmit = useMemo(
    () =>
      !!sessionId &&
      !!question &&
      typeof selectedIndex === "number" &&
      !loading,
    [sessionId, question, selectedIndex, loading]
  );

  async function startQuiz() {
    setError(null);
    setFeedback(null);
    setSelectedIndex(null);
    setQuestion(null);
    setLoading(true);

    try {
      const data = await adaptiveApi.start({ batchId });

      const sid = data?.sessionId || data?.session || data?.id || null;

      const q =
        data?.question ||
        (Array.isArray(data?.nextQuestion) ? data.nextQuestion[0] : null);

      setSessionId(sid);
      setQuestion(q);
    } catch (e) {
      setError(e.message || "Failed to start quiz");
      setQuestion(null);
      setSessionId(null);
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (!canSubmit) return;

    setError(null);
    setLoading(true);

    try {
      const payload = {
        sessionId,
        questionId: question?._id,
        selectedAnswer: selectedIndex,
        batchId,
      };

      const data = await adaptiveApi.answer(payload);

      const nextQ = Array.isArray(data?.nextQuestion)
        ? data.nextQuestion[0]
        : data?.question || null;

      const status =
        typeof data?.correct === "boolean"
          ? data.correct
            ? "✅ Correct!"
            : "❌ Wrong!"
          : "";

      const explanation = data?.explanation ? `\n\n${data.explanation}` : "";
      setFeedback(`${status}${explanation}`.trim());

      setSelectedIndex(null);
      setQuestion(nextQ);
    } catch (e) {
      setError(e.message || "Failed to submit answer");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    startQuiz();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleExplain = () => {
    if (!question) return;
    navigate("/ai", { state: { question, batchId, sessionId } });
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
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Adaptive Quiz • Session-based Engine
            </div>

            <h1 className="mt-4 text-3xl sm:text-4xl font-semibold tracking-tight">
              Adaptive{" "}
              <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                Quiz
              </span>
            </h1>

            <p className="mt-2 text-white/70 max-w-2xl">
              Answer questions and the difficulty will adjust in real-time based on your performance.
            </p>
          </div>

          <button
            type="button"
            onClick={startQuiz}
            disabled={loading}
            className="rounded-xl px-5 py-3 text-sm font-semibold bg-white/10 ring-1 ring-white/15 hover:bg-white/15 transition disabled:opacity-50"
          >
            {loading ? "Restarting..." : "Restart"}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-2xl bg-red-500/10 ring-1 ring-red-500/25 px-5 py-4 text-sm text-red-200">
            {error}
          </div>
        )}

        {/* Feedback */}
        {feedback && (
          <div className="mt-6 rounded-2xl bg-emerald-500/10 ring-1 ring-emerald-400/25 px-5 py-4 text-sm text-emerald-100 whitespace-pre-line">
            <div className="font-semibold">Feedback</div>
            <div className="mt-1 text-white/80">{feedback}</div>
          </div>
        )}

        {/* Question area */}
        <div className="mt-8">
          {question ? (
            <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden">
              <div className="p-6 sm:p-8">
                <QuestionCard
                  question={question}
                  selectedIndex={selectedIndex}
                  onSelect={setSelectedIndex}
                />

                {/* actions */}
                <div className="mt-6 flex flex-wrap gap-3 justify-end">
                  <button
                    type="button"
                    onClick={handleExplain}
                    disabled={loading || !question}
                    className="rounded-xl px-5 py-3 text-sm font-semibold bg-fuchsia-500/80 hover:bg-fuchsia-500 transition shadow-lg shadow-fuchsia-500/20 disabled:opacity-50"
                  >
                    Explain with AI
                  </button>

                  <button
                    type="button"
                    onClick={submitAnswer}
                    disabled={!canSubmit}
                    className="rounded-xl px-5 py-3 text-sm font-semibold bg-indigo-500/90 hover:bg-indigo-500 transition shadow-lg shadow-indigo-500/20 disabled:opacity-50"
                  >
                    {loading ? "Submitting..." : "Submit"}
                  </button>
                </div>
              </div>

              <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
                Tip: Use “Explain with AI” after answering to strengthen concepts quickly.
              </div>
            </div>
          ) : (
            <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl p-6 sm:p-8">
              <div className="text-lg font-semibold">No question loaded</div>
              <div className="text-sm text-white/65 mt-1">
                Click Restart to start the quiz.
              </div>
            </div>
          )}
        </div>

        <p className="mt-10 text-center text-xs text-white/45">
          © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
        </p>
      </main>
    </div>
  );
}