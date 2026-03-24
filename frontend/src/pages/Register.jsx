import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

export default function Register() {
  const { register } = useAuth();
  const nav = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    setLoading(true);

    try {
      await register(name, email, password);
      nav("/login");
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-slate-950 text-white relative overflow-hidden flex flex-col">

      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
        <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
      </div>

      <main className="relative z-10 flex-1 flex items-center overflow-hidden">
        <div className="mx-auto w-full max-w-6xl px-6">
          <div className="grid items-center gap-10 lg:grid-cols-2">

            {/* Left marketing section */}
            <div className="hidden lg:block">
              <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                Portfolio-grade Adaptive Intelligence
              </div>

              <h1 className="mt-4 text-4xl font-semibold tracking-tight">
                Join the future of{" "}
                <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(99,102,241,0.35)]">
                  AI-powered adaptive learning
                </span>
                .
              </h1>

              <p className="mt-4 max-w-md text-white/70">
                Create your SmartQuizzer account and start mastering concepts
                with intelligent adaptive assessments.
              </p>

              <div className="mt-6 grid max-w-md grid-cols-2 gap-3 text-sm">
                <Feature label="Adaptive difficulty engine" />
                <Feature label="Gemini explanations" />
                <Feature label="Session analytics" />
                <Feature label="Batch-wise quizzes" />
              </div>
            </div>

            {/* Register card */}
            <div className="mx-auto w-full max-w-md">
              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl shadow-indigo-500/10 backdrop-blur-xl transition-all duration-500 hover:shadow-indigo-500/20">
                <div className="p-6 sm:p-8">

                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h2 className="text-2xl font-semibold">Create account</h2>
                      <p className="mt-1 text-sm text-white/65">
                        Start your adaptive learning journey.
                      </p>
                    </div>
                    <div className="h-10 w-10 rounded-xl bg-indigo-500/15 ring-1 ring-indigo-400/20 grid place-items-center">
                      <span className="text-sm font-semibold text-indigo-200">AI</span>
                    </div>
                  </div>

                  {err && (
                    <div className="mt-5 rounded-xl bg-red-500/10 ring-1 ring-red-500/25 px-4 py-3 text-sm text-red-200">
                      {err}
                    </div>
                  )}

                  <form onSubmit={onSubmit} className="mt-6 space-y-4">

                    <div>
                      <label className="text-sm text-white/70">Name</label>
                      <input
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        type="text"
                        placeholder="Your full name"
                        className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35"
                        required
                      />
                    </div>

                    <div>
                      <label className="text-sm text-white/70">Email</label>
                      <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        type="email"
                        placeholder="you@example.com"
                        className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35"
                        required
                      />
                    </div>

                    <div>
                      <label className="text-sm text-white/70">Password</label>
                      <div className="mt-2 relative">
                        <input
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          type={showPass ? "text" : "password"}
                          placeholder="••••••••"
                          className="w-full rounded-xl bg-slate-950/40 px-4 py-3 pr-12 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60 placeholder:text-white/35"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPass(!showPass)}
                          className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg px-3 py-1 text-xs text-white/70 hover:bg-white/10 transition"
                        >
                          {showPass ? "Hide" : "Show"}
                        </button>
                      </div>
                    </div>

                    <button
                      disabled={loading}
                      className="w-full rounded-xl bg-indigo-500/90 py-3 text-sm font-semibold
                                 transition-all duration-300 hover:bg-indigo-500
                                 hover:scale-[1.02] active:scale-[0.98]
                                 shadow-lg shadow-indigo-500/20
                                 disabled:opacity-60 disabled:cursor-not-allowed"
                    >
                      {loading ? "Creating account..." : "Create account"}
                    </button>

                    <p className="text-sm text-white/65 text-center">
                      Already have an account?{" "}
                      <Link
                        to="/login"
                        className="text-indigo-200 hover:text-indigo-100"
                      >
                        Login
                      </Link>
                    </p>

                  </form>
                </div>

                <div className="border-t border-white/10 px-6 py-4 text-xs text-white/55">
                  Join SmartQuizzer and unlock AI-driven adaptive learning.
                </div>

              </div>

              <p className="mt-4 text-center text-xs text-white/45">
                © {new Date().getFullYear()} SmartQuizzer • Built with MERN + Gemini
              </p>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function Feature({ label }) {
  return (
    <div className="rounded-xl bg-white/5 ring-1 ring-white/10 px-4 py-3 text-white/80">
      <div className="text-xs text-white/55">Feature</div>
      <div className="mt-1 text-sm font-medium">{label}</div>
    </div>
  );
}