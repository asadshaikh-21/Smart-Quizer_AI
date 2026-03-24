const BASE = import.meta.env.VITE_API_BASE_URL;

function getToken() {
  return localStorage.getItem("sq_token");
}

async function jsonRequest(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data?.message || data?.error?.message || "Request failed");
  }

  return data;
}

export const aiApi = {
  ask: (prompt) => jsonRequest("/api/ai", { type: "ask", prompt }),

  explain: ({ questionText, options, correctIndex, selectedAnswer }) =>
    jsonRequest("/api/ai", {
      type: "explain",
      questionText,
      options,
      correctIndex,
      selectedAnswer,
    }),

  generate: ({ method, text, url, topic, count }) =>
    jsonRequest("/api/content/generate", {
      method,
      text,
      url,
      topic,
      count,
    }),

  async generatePdf({ file, topic, count }) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("topic", topic);
    formData.append("count", String(count));

    const res = await fetch(`${BASE}/api/content/generate/pdf`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
      body: formData,
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new Error(data?.message || data?.error?.message || "PDF generation failed");
    }

    return data;
  },
};