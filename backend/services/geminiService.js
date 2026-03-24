import { GoogleGenerativeAI } from "@google/generative-ai";

let fastModel = null;
let proModel = null;

function getModels() {
  if (fastModel && proModel) return { fastModel, proModel };

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY missing. Check your .env in mern-backend folder.");
  }

  const genAI = new GoogleGenerativeAI(apiKey);

  const MODEL_FAST = process.env.GEMINI_MODEL_FAST || "models/gemini-2.5-flash";
  const MODEL_PRO = process.env.GEMINI_MODEL_PRO || "models/gemini-2.5-pro";

  fastModel = genAI.getGenerativeModel({ model: MODEL_FAST });
  proModel = genAI.getGenerativeModel({ model: MODEL_PRO });

  return { fastModel, proModel };
}

function stripCodeFences(s = "") {
  return s.replace(/```json/gi, "```").replace(/```/g, "").trim();
}

function extractJsonArray(raw = "") {
  const text = stripCodeFences(raw);
  const start = text.indexOf("[");
  const end = text.lastIndexOf("]");

  if (start === -1 || end === -1 || end <= start) {
    throw new Error("No JSON array found in model output");
  }

  return text.slice(start, end + 1);
}

function normalizeDifficulty(value) {
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
    if (value <= 1) return "Beginner";
    if (value === 2) return "Intermediate";
    if (value >= 3) return "Advanced";
  }

  return "Beginner";
}

function validateQuestions(arr) {
  if (!Array.isArray(arr)) {
    throw new Error("Generated output is not an array");
  }

  return arr.map((q, idx) => {
    const question = (q?.question ?? q?.questionText ?? "").toString().trim();
    const options = Array.isArray(q?.options)
      ? q.options.map((o) => String(o).trim())
      : [];

    const correctAnswer = Number(
      q?.correctAnswer ?? q?.correctIndex ?? q?.correctAnswerIndex
    );

    if (!question || question.length < 3) {
      throw new Error(`Invalid question at index ${idx}`);
    }

    if (
      !Array.isArray(options) ||
      options.length !== 4 ||
      options.some((o) => !o)
    ) {
      throw new Error(`Invalid options at index ${idx} (must be 4 non-empty strings)`);
    }

    if (!Number.isInteger(correctAnswer) || correctAnswer < 0 || correctAnswer > 3) {
      throw new Error(`Invalid correctAnswer at index ${idx} (must be 0..3)`);
    }

    return {
      question,
      options,
      correctAnswer,
      difficulty: normalizeDifficulty(q?.difficulty),
      bloomLevel: (q?.bloomLevel || "Understand").toString(),
    };
  });
}

async function generateJsonWithRetry({ model, prompt, retries = 2 }) {
  let lastErr = null;
  let currentPrompt = prompt;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const result = await model.generateContent(currentPrompt);
      const response = await result.response;
      const raw = response.text();

      const jsonArrayText = extractJsonArray(raw);
      const parsed = JSON.parse(jsonArrayText);

      return parsed;
    } catch (err) {
      lastErr = err;

      if (attempt < retries) {
        currentPrompt = `${currentPrompt}

IMPORTANT:
- Output ONLY a valid JSON array
- No markdown
- No explanation text
- No code fences
- Use exact keys: question, options, correctAnswer, difficulty, bloomLevel`;
      }
    }
  }

  throw lastErr || new Error("Failed to generate valid JSON");
}

export async function generateQuestionsFromText({ text, topic = "General", count = 10 }) {
  const { proModel } = getModels();
  const safeCount = Math.min(Math.max(Number(count) || 10, 1), 30);

  const prompt = `
You are generating high-quality multiple-choice quiz questions for a MERN quiz application.

TOPIC: ${topic}
Generate exactly ${safeCount} questions based only on the content below.

CONTENT:
${text}

Return ONLY a valid JSON array.

Each item must follow this exact schema:
{
  "question": "string",
  "options": ["string", "string", "string", "string"],
  "correctAnswer": 0,
  "difficulty": "Beginner",
  "bloomLevel": "Remember"
}

Strict rules:
- Use the exact key "question"
- Use the exact key "correctAnswer"
- correctAnswer must be a number from 0 to 3
- options must contain exactly 4 non-empty strings
- difficulty must be exactly one of:
  "Beginner", "Intermediate", "Advanced"
- bloomLevel must be one of:
  "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"
- exactly one option must be correct
- no markdown
- no code fences
- no extra text
`;

  const parsed = await generateJsonWithRetry({
    model: proModel,
    prompt,
    retries: 2,
  });

  return validateQuestions(parsed);
}

export async function askGemini(prompt) {
  const { fastModel } = getModels();
  const result = await fastModel.generateContent(prompt);
  const response = await result.response;
  return response.text();
}

export async function explainQuestion({
  questionText,
  options,
  correctIndex,
  selectedAnswer,
}) {
  const { fastModel } = getModels();

  const correct =
    Number.isInteger(correctIndex) && options?.[correctIndex]
      ? options[correctIndex]
      : null;

  const selected =
    Number.isInteger(selectedAnswer) && options?.[selectedAnswer]
      ? options[selectedAnswer]
      : null;

  const prompt = `
You are a helpful tutor. Explain this MCQ clearly.

Question: ${questionText}
Options:
${(options || []).map((o, i) => `${String.fromCharCode(65 + i)}. ${o}`).join("\n")}

${correct ? `Correct Option: ${correct}` : ""}
${selected ? `Student Selected: ${selected}` : ""}

Guidelines:
- 6 to 10 short lines
- Explain the concept first
- Then explain why the correct option is right
- If the student is wrong, briefly explain why
- Keep it simple and clear
`;

  const result = await fastModel.generateContent(prompt);
  const response = await result.response;
  return response.text();
}

export async function generateExplanation(payload) {
  return explainQuestion(payload);
}