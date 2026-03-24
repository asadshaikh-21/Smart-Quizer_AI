import { Routes, Route } from "react-router-dom";
import ExplainPage from "./pages/ExplainPage";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import AdaptiveQuiz from "./pages/AdaptiveQuiz";
import Analytics from "./pages/Analytics";
import AiHelper from "./pages/AiHelper";
import GenerateQuestions from "./pages/GenerateQuestions";
import PreviewQuestions from "./pages/PreviewQuestions";
import Welcome from "./pages/Welcome"; // ✅ ADD THIS

import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white relative">
      <Navbar />

      <Routes>
        {/* ✅ Landing page */}
        <Route path="/" element={<Welcome />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/preview/:batchId" element={<PreviewQuestions />} />
        <Route path="/ai/explain" element={<ExplainPage />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/quiz"
          element={
            <ProtectedRoute>
              <AdaptiveQuiz />
            </ProtectedRoute>
          }
        />

        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          }
        />

        <Route
          path="/ai"
          element={
            <ProtectedRoute>
              <AiHelper />
            </ProtectedRoute>
          }
        />

        <Route
          path="/generate"
          element={
            <ProtectedRoute>
              <GenerateQuestions />
            </ProtectedRoute>
          }
        />

        {/* default */}
        <Route path="*" element={<Login />} />
      </Routes>
    </div>
  );
}