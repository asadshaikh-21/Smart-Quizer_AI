import mongoose from "mongoose";

const quizSessionSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },

    currentDifficulty: {
      type: String,
      enum: ["Beginner", "Intermediate", "Advanced"],
      default: "Beginner",
    },

    isCompleted: {
      type: Boolean,
      default: false,
    },

    batchId: {
      type: mongoose.Schema.Types.ObjectId,
      default: null,
    },

    askedQuestionIds: [
      { type: mongoose.Schema.Types.ObjectId, ref: "Question" },
    ],

    responses: [
      {
        questionId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: "Question",
          required: true,
        },
        selectedAnswer: {
          type: Number,
          required: true,
        },
        isCorrect: {
          type: Boolean,
          required: true,
        },
        difficulty: {
          type: String,
          enum: ["Beginner", "Intermediate", "Advanced"],
          required: true,
        },
        timeTakenMs: {
          type: Number,
          default: 0,
        },
        answeredAt: {
          type: Date,
          default: Date.now,
        },
      },
    ],
  },
  { timestamps: true }
);

const QuizSession =
  mongoose.models.QuizSession ||
  mongoose.model("QuizSession", quizSessionSchema);

export default QuizSession;