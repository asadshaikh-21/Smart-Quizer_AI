import { apiFetch } from "./client";

export const adaptiveApi = {
  start: (payload) => apiFetch("/api/adaptive/start", { method: "POST", body: payload }),
  answer: (payload) => apiFetch("/api/adaptive/answer", { method: "POST", body: payload }),
};