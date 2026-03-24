import express from "express";
import authMiddleware from "../middleware/authMiddleware.js";
import { askGemini, explainQuestion } from "../services/geminiService.js";

const router = express.Router();

/**
 * POST /api/ai
 * body:
 *  - for ask: { type:"ask", prompt:"..." }
 *  - for explain: { type:"explain", questionText, options, correctIndex, selectedAnswer }
 */
router.post("/", authMiddleware, async (req, res) => {
  try {
    const { type } = req.body;

    // ASK
    if (type === "ask") {
      const { prompt } = req.body;
      if (!prompt || !prompt.trim()) {
        return res.status(400).json({ message: "prompt is required" });
      }

      const answer = await askGemini(prompt);
      return res.json({ answer });
    }

    // EXPLAIN
    if (type === "explain") {
      const { questionText, options, correctIndex, selectedAnswer } = req.body;

      if (!questionText || !Array.isArray(options) || options.length < 2) {
        return res.status(400).json({ message: "Invalid question payload" });
      }

      const explanation = await explainQuestion({
        questionText,
        options,
        correctIndex,
        selectedAnswer,
      });

      return res.json({ explanation });
    }

    return res.status(400).json({ message: "Invalid type. Use ask or explain." });
  } catch (err) {
    return res.status(500).json({ message: err.message || "AI error" });
  }
});

export default router;