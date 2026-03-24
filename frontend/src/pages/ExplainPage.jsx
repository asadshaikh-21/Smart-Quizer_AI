import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { aiApi } from "../api/ai";

export default function ExplainPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const question = location.state?.question || null;

  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runExplain() {
    if (!question) return;

    setLoading(true);
    setError("");
    setExplanation("");

    try {
      const data = await aiApi.explain({
        questionText: question.questionText,
        options: question.options,
        correctIndex: question.correctIndex,
        selectedAnswer: null, // optional, if you want pass selected index too
      });

      setExplanation(data.explanation || "No explanation returned.");
    } catch (e) {
      setError(e.message || "Failed to generate explanation");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    runExplain();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!question) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="text-2xl font-bold">Explain</h1>
        <div className="mt-4 p-4 rounded-2xl border bg-red-50 text-red-700">
          No question received. Go back and click Explain again.
        </div>

        <button
          type="button"
          onClick={() => navigate(-1)}
          className="mt-4 px-4 py-2 rounded-xl bg-gray-900 text-white"
        >
          Back
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">AI Explanation</h1>

        <button
          type="button"
          onClick={() => navigate(-1)}
          className="px-4 py-2 rounded-xl bg-gray-900 text-white hover:bg-black"
        >
          Back to Quiz
        </button>
      </div>

      {/* Question Preview */}
      <div className="mt-6 p-5 rounded-2xl border bg-white">
        <div className="text-lg font-semibold">{question.questionText}</div>

        <div className="mt-4 grid gap-2">
          {question.options?.map((op, idx) => (
            <div
              key={idx}
              className="p-3 rounded-xl border bg-gray-50 text-sm"
            >
              <span className="font-semibold mr-2">
                {String.fromCharCode(65 + idx)}.
              </span>
              {op}
            </div>
          ))}
        </div>
      </div>

      {/* Explain Result */}
      <div className="mt-6 p-5 rounded-2xl border bg-gray-50">
        <div className="flex items-center justify-between gap-3">
          <div className="font-semibold">Explanation</div>

          <button
            type="button"
            onClick={runExplain}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-50"
          >
            {loading ? "Generating..." : "Regenerate"}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-red-50 text-red-700 border border-red-200">
            {error}
          </div>
        )}

        {!error && !loading && explanation && (
          <div className="mt-4 whitespace-pre-line text-sm leading-relaxed text-gray-900">
            {explanation}
          </div>
        )}

        {loading && (
          <div className="mt-4 text-sm text-gray-600">Thinking...</div>
        )}
      </div>
    </div>
  );
}