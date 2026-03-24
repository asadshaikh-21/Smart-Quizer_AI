import jwt from "jsonwebtoken";
import User from "../models/User.js";

const protect = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization || "";
    const [scheme, token] = authHeader.split(" ");

    if (!scheme || !token || scheme.toLowerCase() !== "bearer") {
      return res.status(401).json({ message: "Not authorized, no token" });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    const userId = decoded.id || decoded._id || decoded.userId;

    if (!userId) {
      return res.status(401).json({ message: "Not authorized, invalid token payload" });
    }

    const user = await User.findById(userId).select("-password");

    if (!user) {
      return res.status(401).json({ message: "User not found" });
    }

    req.user = user; // <-- THIS is the real fix
    next();
  } catch (err) {
  console.error("GENERATE ERROR STACK:", err);
  const msg = err?.message || "Server error";

  if (
    msg.includes("429") ||
    msg.toLowerCase().includes("quota") ||
    msg.toLowerCase().includes("too many requests")
  ) {
    return res.status(429).json({
      message: "Gemini quota exceeded. Please wait ~1 minute and try again.",
      detail: msg,
    });
  }

  res.status(500).json({ message: msg });
}
};

export default protect;