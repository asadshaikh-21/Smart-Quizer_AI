import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthProvider";

export default function Login() {
  const navigate = useNavigate();
  const { login, token } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  // Redirect if already logged in
  useEffect(() => {
    if (token) {
      navigate("/dashboard");
    }
  }, [token, navigate]);

  async function handleSubmit(e) {
    e.preventDefault();
    setErr("");
    setLoading(true);

    try {
      await login(email, password);
    } catch (error) {
      setErr(error.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen bg-slate-950 text-white relative overflow-hidden flex flex-col">
      {/* background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl" />
        <div className="absolute top-24 left-20 h-[380px] w-[380px] rounded-full bg-cyan-500/15 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_55%)]" />
      </div>

      <main className="relative z-10 flex-1 flex items-center overflow-hidden">
        <div className="mx-auto w-full max-w-6xl px-6">
          <div className="grid items-center gap-10 lg:grid-cols-2">
            
            {/* left */}
            <div className="hidden lg:block">
              <div className="inline-flex items-center gap-2 rounded-full bg-white/5 ring-1 ring-white/10 px-3 py-1 text-xs text-white/70">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                Portfolio-grade Adaptive Intelligence
              </div>

              <h1 className="mt-4 text-4xl font-semibold tracking-tight">
                Learn smarter with{" "}
                <span className="bg-gradient-to-r from-indigo-300 via-cyan-300 to-fuchsia-300 bg-[length:300%_300%] animate-gradient bg-clip-text text-transparent">
                  AI-powered adaptive assessment
                </span>
              </h1>

              <p className="mt-4 max-w-md text-white/70">
                SmartQuizzer adjusts difficulty in real-time, tracks performance analytics,
                and provides AI explanations.
              </p>
            </div>

            {/* right */}
            <div className="mx-auto w-full max-w-md">
              <div className="rounded-2xl bg-white/5 ring-1 ring-white/10 shadow-2xl backdrop-blur-xl">
                <div className="p-6 sm:p-8">
                  <h2 className="text-2xl font-semibold">Welcome back</h2>

                  {err && (
                    <div className="mt-5 rounded-xl bg-red-500/10 ring-1 ring-red-500/25 px-4 py-3 text-sm text-red-200">
                      {err}
                    </div>
                  )}

                  <form onSubmit={handleSubmit} className="mt-6 space-y-4">
                    <div>
                      <label className="text-sm text-white/70">Email</label>

                      <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        type="email"
                        placeholder="you@example.com"
                        className="mt-2 w-full rounded-xl bg-slate-950/40 px-4 py-3 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60"
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
                          className="w-full rounded-xl bg-slate-950/40 px-4 py-3 pr-12 text-sm outline-none ring-1 ring-white/10 focus:ring-2 focus:ring-indigo-500/60"
                          required
                        />

                        <button
                          type="button"
                          onClick={() => setShowPass((s) => !s)}
                          className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg px-3 py-1 text-xs text-white/70 hover:bg-white/10"
                        >
                          {showPass ? "Hide" : "Show"}
                        </button>
                      </div>
                    </div>

                    <button
                      disabled={loading}
                      className="w-full rounded-xl bg-indigo-500/90 py-3 text-sm font-semibold transition-all hover:bg-indigo-500 disabled:opacity-60"
                    >
                      {loading ? "Logging in..." : "Login"}
                    </button>

                    <p className="text-sm text-white/65 text-center">
                      No account?{" "}
                      <Link
                        to="/register"
                        className="text-indigo-200 hover:text-indigo-100"
                      >
                        Register
                      </Link>
                    </p>
                  </form>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}