import { apiFetch } from "./client";

export const authApi = {
  login: (payload) => apiFetch("/api/auth/login", { method: "POST", body: payload }),
  register: (payload) => apiFetch("/api/auth/register", { method: "POST", body: payload }),
};