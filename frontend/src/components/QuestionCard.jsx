export default function QuestionCard({ question, selectedIndex, onSelect }) {
  if (!question) return null;

  const qText = question.question || question.text || "Question";
  const options = Array.isArray(question.options) ? question.options : [];

  return (
    <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 p-6 sm:p-7">
      {/* Question */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-xs text-white/55">Question</div>
          <h2 className="mt-2 text-lg sm:text-xl font-semibold text-white leading-snug">
            {qText}
          </h2>
        </div>

        {/* difficulty chip if present */}
        {question.difficulty ? (
          <div className="shrink-0 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
            {question.difficulty}
          </div>
        ) : null}
      </div>

      {/* Options */}
      <div className="mt-6 grid gap-3">
        {options.map((opt, idx) => {
          const active = selectedIndex === idx;

          return (
            <button
              key={idx}
              type="button"
              onClick={() => onSelect(idx)}
              className={[
                "w-full text-left rounded-xl px-4 py-4 transition",
                "ring-1",
                active
                  ? "bg-indigo-500/20 ring-indigo-400/40 shadow-[0_0_0_1px_rgba(99,102,241,0.25)]"
                  : "bg-white/5 ring-white/10 hover:bg-white/10",
              ].join(" ")}
            >
              <div className="flex items-start gap-3">
                <div
                  className={[
                    "mt-0.5 h-6 w-6 rounded-lg grid place-items-center text-xs font-semibold",
                    active
                      ? "bg-indigo-500/30 text-indigo-100 ring-1 ring-indigo-400/30"
                      : "bg-white/5 text-white/70 ring-1 ring-white/10",
                  ].join(" ")}
                >
                  {String.fromCharCode(65 + idx)}
                </div>

                <div className={active ? "text-white" : "text-white/85"}>
                  {opt}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* hint row */}
      <div className="mt-5 text-xs text-white/50">
        Select an option, then press <span className="text-white/70">Submit</span>.
      </div>
    </div>
  );
}