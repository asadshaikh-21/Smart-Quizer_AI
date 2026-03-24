import { api } from "./http";

export const registerApi = (payload) => api.post("/api/auth/register", payload);
export const loginApi = (payload) => api.post("/api/auth/login", payload);

export const startAdaptiveApi = (payload = {}) =>
  api.post("/api/adaptive/start", payload);

export const answerAdaptiveApi = (payload) =>
  api.post("/api/adaptive/answer", payload);

export const analyticsSummaryApi = () => api.get("/api/analytics/summary");