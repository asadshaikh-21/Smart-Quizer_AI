import { useEffect, useState } from "react";
import { startAdaptiveApi, answerAdaptiveApi } from "../api/endpoints";

export default function Quiz() {
  const [sessionId, setSessionId] = useState("");
  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState("");
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const start = async () => {
    setErr("");
    setLoading(true);
    try {
      const res = await startAdaptiveApi();
      setSessionId(res.data.sessionId || "");
      setQuestion(res.data.question || null);
      setExplanation("");
      setSelected("");
    } catch (e) {
      setErr(e?.response?.data?.message || e.message);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
  if (!selected || !question?._id || !sessionId) return;

  setErr("");
  setLoading(true);

  try {
    const opts = question?.options ?? [];
    const idx = opts.indexOf(selected);

    if (idx < 0) {
      setErr("Please select a valid option.");
      return;
    }

    const payload = {
      sessionId,
      questionId: question._id,
      selectedAnswer: idx, // number
    };

    const res = await answerAdaptiveApi(payload);

    const nextRaw =
      res.data.nextQuestion ||
      res.data.question ||
      res.data.currentQuestion ||
      res.data.next ||
      null;

    const next = Array.isArray(nextRaw) ? nextRaw[0] : nextRaw;

    if (next) setQuestion(next);

    setExplanation(res.data.explanation || res.data.aiExplanation || "");
    setSelected("");
  } catch (e) {
    setErr(e?.response?.data?.message || e.message);
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Adaptive Quiz</h1>
        <button
          onClick={start}
          className="px-3 py-2 rounded bg-gray-800 hover:bg-gray-700"
        >
          Restart
        </button>
      </div>

      {err && <div className="text-sm text-red-300">{err}</div>}
      {loading && <div className="text-sm text-gray-300">Loading…</div>}

      {question ? (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="text-lg font-semibold">
            {question.text || question.question}
          </div>

          <div className="mt-4 space-y-2">
            {(question.options || []).map((opt) => (
              <label
                key={opt}
                className={`block p-3 rounded border cursor-pointer ${
                  selected === opt
                    ? "border-indigo-500 bg-indigo-500/10"
                    : "border-gray-800 bg-gray-950"
                }`}
              >
                <input
                  type="radio"
                  name="opt"
                  className="mr-2"
                  checked={selected === opt}
                  onChange={() => setSelected(opt)}
                />
                {opt}
              </label>
            ))}
          </div>

          <button
            disabled={!selected || loading}
            onClick={submitAnswer}
            className="mt-4 px-4 py-2 rounded bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50"
          >
            Submit
          </button>

          {explanation && (
            <div className="mt-5 p-4 rounded bg-gray-950 border border-gray-800">
              <div className="font-semibold mb-1">AI Explanation</div>
              <div className="text-sm text-gray-200 whitespace-pre-wrap">
                {explanation}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="text-gray-300">No question loaded.</div>
      )}
    </div>
  );
}