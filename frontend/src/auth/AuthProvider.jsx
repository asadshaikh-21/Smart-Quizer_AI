import { createContext, useContext, useMemo, useState } from "react";
import { loginApi, registerApi } from "../api/endpoints";

const AuthContext = createContext(null);

export default function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("sq_token"));
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("sq_user");
    return raw ? JSON.parse(raw) : null;
  });

  const login = async (email, password) => {
    const res = await loginApi({ email, password });

    const jwt = res?.data?.token || res?.data?.accessToken || res?.token;
    const u = res?.data?.user || res?.user || null;

    if (!jwt) throw new Error("Token not found in response.");

    localStorage.setItem("sq_token", jwt);
    localStorage.setItem("sq_user", JSON.stringify(u));
    setToken(jwt);
    setUser(u);
    return res;
  };

  const register = async (name, email, password) => {
    return await registerApi({ name, email, password });
  };

  const logout = () => {
    localStorage.removeItem("sq_token");
    localStorage.removeItem("sq_user");
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ token, user, login, register, logout }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}