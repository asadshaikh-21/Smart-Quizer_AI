import mongoose from "mongoose";

const questionSchema = new mongoose.Schema(
  {
    question: {
      type: String,
      required: true,
      trim: true,
    },

    options: {
      type: [String],
      required: true,
      validate: {
        validator: function (arr) {
          return Array.isArray(arr) && arr.length >= 2;
        },
        message: "At least 2 options are required.",
      },
    },

    correctAnswer: {
      type: Number,
      required: true,
      min: 0,
    },

    difficulty: {
      type: String,
      enum: ["Beginner", "Intermediate", "Advanced"],
      required: true,
    },

    sourceType: {
      type: String,
      enum: ["text", "url", "pdf"],
      default: "text",
    },

    sourceRef: {
      type: String,
      default: "",
      trim: true,
    },

    topic: {
      type: String,
      default: "",
      trim: true,
    },

    createdBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },

    batchId: {
      type: mongoose.Schema.Types.ObjectId,
      index: true,
      required: true,
    },
  },
  { timestamps: true }
);

questionSchema.pre("validate", function () {
  if (
    Array.isArray(this.options) &&
    Number.isInteger(this.correctAnswer) &&
    this.correctAnswer >= this.options.length
  ) {
    throw new Error("correctAnswer index is out of range");
  }
});

const Question =
  mongoose.models.Question ||
  mongoose.model("Question", questionSchema);

export default Question;