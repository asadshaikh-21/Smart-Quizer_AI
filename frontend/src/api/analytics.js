const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const analyticsApi = {
  async getSummary() {
    const token = localStorage.getItem("sq_token");

    const res = await fetch(`${API_BASE}/api/analytics/summary`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.message || "Failed to load analytics");
    }

    return data;
  },
};