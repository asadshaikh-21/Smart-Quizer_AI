import express from "express";
import Quiz from "../models/Quiz.js";
import QuizAttempt from "../models/QuizAttempt.js";
import authMiddleware from "../middleware/authMiddleware.js";

const router = express.Router();

// Create Quiz (for admin testing)
router.post("/", async (req, res) => {
  try {
    const quiz = await Quiz.create(req.body);
    res.json(quiz);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Get Quiz by Difficulty
router.get("/:difficulty", authMiddleware, async (req, res) => {
  try {
    const quiz = await Quiz.findOne({ difficulty: req.params.difficulty });
    res.json(quiz);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Submit Quiz
router.post("/submit/:quizId", authMiddleware, async (req, res) => {
  try {
    const { answers } = req.body;

    const quiz = await Quiz.findById(req.params.quizId);

    if (!quiz) {
      return res.status(404).json({ message: "Quiz not found" });
    }

    let score = 0;

    quiz.questions.forEach((q, index) => {
      if (q.correctAnswer === answers[index]) {
        score++;
      }
    });

    await QuizAttempt.create({
      user: req.user,
      quiz: quiz._id,
      score,
      totalQuestions: quiz.questions.length,
    });

    res.json({
      score,
      totalQuestions: quiz.questions.length,
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;