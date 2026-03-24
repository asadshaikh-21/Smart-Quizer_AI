import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const token = localStorage.getItem("sq_token");

  const isAuthPage =
    location.pathname === "/login" || location.pathname === "/register";

  function logout() {
    localStorage.removeItem("sq_token");
    navigate("/login");
  }

  const navLinkClass = ({ isActive }) =>
    `rounded-xl px-3 py-2 text-sm font-medium transition ${
      isActive
        ? "bg-white/10 ring-1 ring-white/15 text-white"
        : "text-white/70 hover:text-white hover:bg-white/5"
    }`;

  return (
    <header className="sticky top-0 z-50">
      <div className="bg-slate-950/80 backdrop-blur-xl border-b border-white/10">
        <nav nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">

          {/* Brand */}
          <Link to={token ? "/dashboard" : "/login"} className="flex items-center gap-2">
            <div className="h-9 w-9 rounded-xl bg-white/10 ring-1 ring-white/15 grid place-items-center">
              <span className="text-sm font-semibold text-white">SQ</span>
            </div>
            <div>
              <div className="text-base font-semibold text-white leading-none">
                SmartQuizzer
              </div>
              <div className="text-xs text-white/60">
                Adaptive AI Assessment
              </div>
            </div>
          </Link>

          {/* Center nav links (only when logged in) */}
          {token && !isAuthPage ? (
            <div className="hidden md:flex items-center gap-1">
              <NavLink to="/dashboard" className={navLinkClass}>
                Dashboard
              </NavLink>
              <NavLink to="/quiz" className={navLinkClass}>
                Adaptive Quiz
              </NavLink>
              <NavLink to="/ai" className={navLinkClass}>
                AI Helper
              </NavLink>
              <NavLink to="/analytics" className={navLinkClass}>
                Analytics
              </NavLink>
              <NavLink to="/generate" className={navLinkClass}>
                Generate
              </NavLink>
            </div>
          ) : (
            <div />
          )}

          {/* Right side buttons */}
          <div className="flex items-center gap-3">
            {!token ? (
              <>
                <Link
                  to="/login"
                  className="rounded-xl px-4 py-2 text-sm font-medium bg-white/10 ring-1 ring-white/15 text-white hover:bg-white/15 transition"
                >
                  Login
                </Link>

                <Link
                  to="/register"
                  className="rounded-xl px-4 py-2 text-sm font-medium bg-indigo-500/90 hover:bg-indigo-500 transition text-white shadow-[0_0_0_1px_rgba(255,255,255,0.15)]"
                >
                  Register
                </Link>
              </>
            ) : (
              <button
                onClick={logout}
                className="rounded-xl px-4 py-2 text-sm font-medium bg-white/10 ring-1 ring-white/15 text-white hover:bg-white/15 transition"
              >
                Logout
              </button>
            )}
          </div>

        </nav>
      </div>
    </header>
  );
}