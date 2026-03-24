const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export function getToken() {
  return localStorage.getItem("sq_token");
}

export async function apiFetch(path, { method = "GET", body, headers } = {}) {
  const token = getToken();

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const contentType = res.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await res.json()
    : await res.text();

  if (!res.ok) {
    const message =
      (data && data.message) ||
      (typeof data === "string" ? data : "Request failed");
    throw new Error(message);
  }

  return data;
}