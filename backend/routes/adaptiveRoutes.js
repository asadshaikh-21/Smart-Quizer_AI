import express from "express";
import Question from "../models/Question.js";
import QuizSession from "../models/QuizSession.js";
import authMiddleware from "../middleware/authMiddleware.js";
import { generateExplanation } from "../services/geminiService.js";

const router = express.Router();

function getNextDifficulty(currentDifficulty, isCorrect) {
  const levels = ["Beginner", "Intermediate", "Advanced"];
  let index = levels.indexOf(currentDifficulty);

  if (index === -1) index = 0;

  if (isCorrect) {
    index = Math.min(index + 1, levels.length - 1);
  } else {
    index = Math.max(index - 1, 0);
  }

  return levels[index];
}

/**
 * POST /api/adaptive/start
 * Body: { batchId?: string }
 */
router.post("/start", authMiddleware, async (req, res) => {
  try {
    const { batchId } = req.body || {};

    const session = await QuizSession.create({
      user: req.user,
      batchId: batchId || null,
      askedQuestionIds: [],
    });

    const filter = { difficulty: session.currentDifficulty };
    if (session.batchId) {
      filter.batchId = session.batchId;
    }

    const question = await Question.findOne(filter).sort({ createdAt: 1 });

    if (!question) {
      return res.status(404).json({
        message: "No questions found for this difficulty and batch.",
      });
    }

    session.askedQuestionIds.push(question._id);
    await session.save();

    return res.json({
      sessionId: session._id,
      question,
    });
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }
});

/**
 * POST /api/adaptive/answer
 * Body: { sessionId, questionId, selectedAnswer:number, timeTakenMs?:number }
 */
router.post("/answer", authMiddleware, async (req, res) => {
  try {
    const { sessionId, questionId, selectedAnswer, timeTakenMs } = req.body;

    if (typeof selectedAnswer !== "number") {
      return res.status(400).json({
        message: "selectedAnswer must be a number",
      });
    }

    const session = await QuizSession.findOne({
      _id: sessionId,
      user: req.user,
    });

    if (!session || session.isCompleted) {
      return res.status(400).json({
        message: "Session invalid or completed",
      });
    }

    const question = await Question.findById(questionId);

    if (!question) {
      return res.status(404).json({
        message: "Question not found",
      });
    }

    const alreadyAnswered = session.responses.some(
      (r) => String(r.questionId) === String(question._id)
    );

    if (alreadyAnswered) {
      return res.status(400).json({
        message: "This question has already been answered in this session",
      });
    }

    const isCorrect = question.correctAnswer === selectedAnswer;
    let explanation = null;

    if (!isCorrect) {
      explanation = await generateExplanation({
        question: question.question,
        options: question.options,
        correctAnswer: question.correctAnswer,
        selectedAnswer,
      });
    }

    session.responses.push({
      questionId: question._id,
      selectedAnswer,
      isCorrect,
      difficulty: session.currentDifficulty,
      timeTakenMs: typeof timeTakenMs === "number" ? timeTakenMs : 0,
    });

    session.currentDifficulty = getNextDifficulty(
      session.currentDifficulty,
      isCorrect
    );

    const nextFilter = {
      difficulty: session.currentDifficulty,
      _id: { $nin: session.askedQuestionIds },
    };

    if (session.batchId) {
      nextFilter.batchId = session.batchId;
    }

    let nextQuestion = await Question.findOne(nextFilter).sort({ createdAt: 1 });

    if (!nextQuestion) {
      const fallbackFilter = {
        _id: { $nin: session.askedQuestionIds },
      };

      if (session.batchId) {
        fallbackFilter.batchId = session.batchId;
      }

      nextQuestion = await Question.findOne(fallbackFilter).sort({ createdAt: 1 });
    }

    if (!nextQuestion) {
      session.isCompleted = true;
      await session.save();

      return res.json({
        correct: isCorrect,
        explanation,
        nextDifficulty: session.currentDifficulty,
        nextQuestion: [],
        completed: true,
      });
    }

    session.askedQuestionIds.push(nextQuestion._id);
    await session.save();

    return res.json({
      correct: isCorrect,
      explanation,
      nextDifficulty: session.currentDifficulty,
      nextQuestion: [nextQuestion],
      completed: false,
    });
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }
});

export default router;