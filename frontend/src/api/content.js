const BASE = import.meta.env.VITE_API_BASE_URL;

function getToken() {
  return localStorage.getItem("sq_token");
}

async function request(path, { method = "POST", body, isFormData = false } = {}) {
  const headers = {};
  if (!isFormData) headers["Content-Type"] = "application/json";

  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      ...headers,
      Authorization: `Bearer ${getToken()}`,
    },
    body: isFormData ? body : JSON.stringify(body),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data?.message || `Request failed (${res.status})`);
  }
  return data;
}

export const contentApi = {
  // JSON: method="text" or "url"
  generate: ({ method, text, url, topic, count }) =>
    request("/api/content/generate", {
      body: { method, text, url, topic, count },
    }),

  // PDF: multipart/form-data
  generatePdf: ({ file, topic, count }) => {
    const fd = new FormData();
    fd.append("file", file);
    if (topic) fd.append("topic", topic);
    if (count) fd.append("count", String(count));

    return request("/api/content/generate/pdf", {
      body: fd,
      isFormData: true,
    });
  },

  getBatch: (batchId) =>
    request(`/api/content/batch/${batchId}`, { method: "GET" }),
};