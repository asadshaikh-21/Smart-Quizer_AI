import express from "express";
import QuizSession from "../models/QuizSession.js";
import authMiddleware from "../middleware/authMiddleware.js";

const router = express.Router();

// GET /api/analytics/summary
router.get("/summary", authMiddleware, async (req, res) => {
  try {
    const userId = req.user._id;

    // Get all sessions of this user
    const sessions = await QuizSession.find({ user: userId });

    const totalSessions = sessions.length;

    if (totalSessions === 0) {
      return res.json({
        totalSessions: 0,
        totalAnswered: 0,
        totalCorrect: 0,
        overallAccuracy: 0,
        avgScore: 0,
        accuracyByDifficulty: {
          Beginner: 0,
          Intermediate: 0,
          Advanced: 0
        }
      });
    }

    let totalAnswered = 0;
    let totalCorrect = 0;
    let totalScore = 0;

    const diffStats = {
      Beginner: { answered: 0, correct: 0 },
      Intermediate: { answered: 0, correct: 0 },
      Advanced: { answered: 0, correct: 0 }
    };

    for (const s of sessions) {
      totalScore += s.score || 0;

      for (const r of s.responses || []) {
        totalAnswered++;
        if (r.isCorrect) totalCorrect++;

        const d = r.difficulty;
        if (diffStats[d]) {
          diffStats[d].answered++;
          if (r.isCorrect) diffStats[d].correct++;
        }
      }
    }

    const overallAccuracy =
      totalAnswered === 0 ? 0 : Math.round((totalCorrect / totalAnswered) * 100);

    const avgScore =
      totalSessions === 0 ? 0 : Number((totalScore / totalSessions).toFixed(2));

    const accuracyByDifficulty = {
      Beginner:
        diffStats.Beginner.answered === 0
          ? 0
          : Math.round((diffStats.Beginner.correct / diffStats.Beginner.answered) * 100),

      Intermediate:
        diffStats.Intermediate.answered === 0
          ? 0
          : Math.round((diffStats.Intermediate.correct / diffStats.Intermediate.answered) * 100),

      Advanced:
        diffStats.Advanced.answered === 0
          ? 0
          : Math.round((diffStats.Advanced.correct / diffStats.Advanced.answered) * 100)
    };

    res.json({
      totalSessions,
      totalAnswered,
      totalCorrect,
      overallAccuracy,
      avgScore,
      accuracyByDifficulty
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;