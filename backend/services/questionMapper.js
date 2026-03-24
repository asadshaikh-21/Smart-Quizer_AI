function mapDifficulty(value) {
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase();

    if (["beginner", "easy", "basic", "1"].includes(normalized)) {
      return "Beginner";
    }
    if (["intermediate", "medium", "2"].includes(normalized)) {
      return "Intermediate";
    }
    if (["advanced", "hard", "3"].includes(normalized)) {
      return "Advanced";
    }
  }

  if (typeof value === "number") {
    if (value === 1) return "Beginner";
    if (value === 2) return "Intermediate";
    if (value === 3) return "Advanced";
  }

  return "Beginner";
}

function normalizeOptions(options) {
  if (!Array.isArray(options)) return [];

  return options
    .map((opt) => String(opt).trim())
    .filter(Boolean)
    .slice(0, 4);
}

export function mapAIQuestionToSchema(rawQuestion, extra = {}) {
  const options = normalizeOptions(rawQuestion.options);

  const question =
    rawQuestion.question ||
    rawQuestion.questionText ||
    rawQuestion.text ||
    "";

  const correctAnswer =
    rawQuestion.correctAnswer ??
    rawQuestion.correctIndex ??
    rawQuestion.answerIndex ??
    0;

  return {
    question: String(question).trim(),
    options,
    correctAnswer: Number(correctAnswer),
    difficulty: mapDifficulty(rawQuestion.difficulty),
    topic: extra.topic || rawQuestion.topic || "General",
    batchId: extra.batchId || rawQuestion.batchId || null,
    createdBy: extra.createdBy || null,
  };
}

export function filterValidQuestions(questions) {
  return questions.filter((q) => {
    const hasQuestion = q.question && q.question.length > 0;
    const hasFourOptions = Array.isArray(q.options) && q.options.length >= 2;
    const validCorrectAnswer =
      Number.isInteger(q.correctAnswer) &&
      q.correctAnswer >= 0 &&
      q.correctAnswer < q.options.length;
    const validDifficulty = ["Beginner", "Intermediate", "Advanced"].includes(
      q.difficulty
    );

    return hasQuestion && hasFourOptions && validCorrectAnswer && validDifficulty;
  });
}