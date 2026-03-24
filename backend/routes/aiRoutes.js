import express from "express";
import mongoose from "mongoose";
import multer from "multer";
import authMiddleware from "../middleware/authMiddleware.js";
import Question from "../models/Question.js";
import { extractFromUrl, extractFromPdf } from "../services/extractService.js";
import { generateQuestionsFromText } from "../services/geminiService.js";

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

function normalizeDifficulty(d) {
  if (typeof d === "string") {
    const value = d.trim().toLowerCase();

    if (["beginner", "easy", "basic", "1"].includes(value)) {
      return "Beginner";
    }
    if (["intermediate", "medium", "2"].includes(value)) {
      return "Intermediate";
    }
    if (["advanced", "hard", "3"].includes(value)) {
      return "Advanced";
    }
  }

  if (typeof d === "number") {
    if (d <= 1) return "Beginner";
    if (d === 2) return "Intermediate";
    if (d >= 3) return "Advanced";
  }

  return "Beginner";
}

function mapQuestionToSchema(q, extra = {}) {
  const questionText = (q.question || q.questionText || "").trim();

  const options = Array.isArray(q.options)
    ? q.options.map((opt) => String(opt).trim()).filter(Boolean)
    : [];

  const correctAnswer =
    typeof q.correctAnswer === "number"
      ? q.correctAnswer
      : typeof q.correctIndex === "number"
      ? q.correctIndex
      : typeof q.correctAnswerIndex === "number"
      ? q.correctAnswerIndex
      : 0;

  return {
    question: questionText,
    options,
    correctAnswer,
    difficulty: normalizeDifficulty(q.difficulty),
    topic: extra.topic || "General",
    sourceType: extra.sourceType || "text",
    sourceRef: extra.sourceRef || "",
    createdBy: extra.createdBy,
    batchId: extra.batchId,
  };
}

function isValidQuestion(q) {
  return (
    q.question &&
    q.question.length > 0 &&
    Array.isArray(q.options) &&
    q.options.length === 4 &&
    Number.isInteger(q.correctAnswer) &&
    q.correctAnswer >= 0 &&
    q.correctAnswer < q.options.length &&
    ["Beginner", "Intermediate", "Advanced"].includes(q.difficulty)
  );
}

// GET /api/content/batch/:batchId
router.get("/batch/:batchId", authMiddleware, async (req, res) => {
  try {
    const questions = await Question.find({
      batchId: req.params.batchId,
      createdBy: req.user,
    }).sort({ createdAt: 1 });

    res.json(questions);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// POST /api/content/generate
router.post("/generate", authMiddleware, async (req, res) => {
  try {
    const { method, text, url, topic, count } = req.body;

    let extracted = "";
    let sourceType = method;
    let sourceRef = "";

    if (method === "text") {
      extracted = (text || "").trim();
      sourceRef = "manual";
    } else if (method === "url") {
      if (!url) {
        return res.status(400).json({ message: "url is required" });
      }
      extracted = await extractFromUrl(url);
      sourceRef = url;
    } else {
      return res.status(400).json({ message: "method must be text or url" });
    }

    if (!extracted || extracted.length < 200) {
      return res.status(400).json({
        message: "Content too short to generate questions.",
      });
    }

    const questions = await generateQuestionsFromText({
      text: extracted,
      topic: topic || "General",
      count: Number(count) || 10,
    });

    const batchId = new mongoose.Types.ObjectId();

    const docs = questions
      .map((q) =>
        mapQuestionToSchema(q, {
          topic: topic || "General",
          sourceType,
          sourceRef,
          createdBy: req.user,
          batchId,
        })
      )
      .filter(isValidQuestion);

    if (docs.length === 0) {
      return res.status(400).json({
        message: "AI generated no valid questions.",
      });
    }

    const saved = await Question.insertMany(docs);

    res.json({
      message: "Questions generated & saved",
      count: saved.length,
      batchId,
    });
  } catch (err) {
    const msg = err?.message || "Server error";

    if (
      msg.includes("429") ||
      msg.toLowerCase().includes("quota") ||
      msg.toLowerCase().includes("too many requests")
    ) {
      return res.status(429).json({
        message: "Gemini quota exceeded. Please wait about 1 minute and try again.",
        detail: msg,
      });
    }

    res.status(500).json({ message: msg });
  }
});

// POST /api/content/generate/pdf
router.post(
  "/generate/pdf",
  authMiddleware,
  upload.single("file"),
  async (req, res) => {
    try {
      const { topic, count } = req.body;

      if (!req.file) {
        return res.status(400).json({ message: "file is required" });
      }

      const extracted = await extractFromPdf(req.file.buffer);

      if (!extracted || extracted.length < 200) {
        return res.status(400).json({
          message: "PDF text too short to generate questions.",
        });
      }

      const questions = await generateQuestionsFromText({
        text: extracted,
        topic: topic || "General",
        count: Number(count) || 10,
      });

      const batchId = new mongoose.Types.ObjectId();

      const docs = questions
        .map((q) =>
          mapQuestionToSchema(q, {
            topic: topic || "General",
            sourceType: "pdf",
            sourceRef: req.file.originalname || "uploaded-pdf",
            createdBy: req.user,
            batchId,
          })
        )
        .filter(isValidQuestion);

      if (docs.length === 0) {
        return res.status(400).json({
          message: "AI generated no valid questions from PDF.",
        });
      }

      const saved = await Question.insertMany(docs);

      res.json({
        message: "PDF questions generated & saved",
        count: saved.length,
        batchId,
      });
    } catch (err) {
      const msg = err?.message || "Server error";

      if (
        msg.includes("429") ||
        msg.toLowerCase().includes("quota") ||
        msg.toLowerCase().includes("too many requests")
      ) {
        return res.status(429).json({
          message: "Gemini quota exceeded. Please wait about 1 minute and try again.",
          detail: msg,
        });
      }

      res.status(500).json({ message: msg });
    }
  }
);

export default router;