import mongoose from "mongoose";

const moderationSchema = new mongoose.Schema(
  {
    content_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Content",
      required: true,
    },
    flagged_reason: {
      type: String,
    },
    status: {
      type: String,
      default: "pending",
    },
  },
  { timestamps: true }
);

export default mongoose.model("Moderation", moderationSchema);