import mongoose from "mongoose";

const quizHistorySchema = new mongoose.Schema(
  {
    user_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    score: {
      type: Number,
      required: true,
    },
    total_questions: {
      type: Number,
      required: true,
    },
  },
  { timestamps: true }
);

export default mongoose.model("QuizHistory", quizHistorySchema);