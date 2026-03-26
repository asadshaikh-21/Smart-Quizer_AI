import axios from "axios";
import { load } from "cheerio";
import pdf from "pdf-parse-debugging-disabled";

// -------------------- URL extraction --------------------
export async function extractFromUrl(url) {
  if (!/^https?:\/\//i.test(url)) {
    throw new Error("Invalid URL. Must start with http:// or https://");
  }

  // ✅ Wikipedia shortcut (avoids 403 from scraping HTML)
  if (url.includes("wikipedia.org/wiki/")) {
    const title = decodeURIComponent(url.split("/wiki/")[1] || "").split("#")[0];
    const apiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(
      title
    )}`;

    try {
      const { data } = await axios.get(apiUrl, {
        timeout: 15000,
        headers: {
          "User-Agent": "SmartQuizzer/1.0 (Educational Project)",
          Accept: "application/json",
        },
      });

      const extracted = (data?.extract || "").trim();
      if (extracted) return extracted;
    } catch {
      // fallback to HTML scraping below
    }
  }

  // ✅ Generic HTML fetch with browser-like headers
  const { data: html } = await axios.get(url, {
    timeout: 20000,
    maxRedirects: 5,
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
      Accept:
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.9",
    },
  });

  const $ = load(html);
  $("script, style, nav, footer, header, noscript").remove();

  const text = $("body").text().replace(/\s+/g, " ").trim();
  return text;
}

// -------------------- PDF extraction --------------------
export async function extractFromPdf(buffer) {
  if (!buffer) throw new Error("No PDF buffer provided");

  // ✅ ESM-safe pdf-parse call for Node v22
  const data = await pdfParse.default(buffer);

  const text = (data?.text || "").replace(/\s+/g, " ").trim();
  return text;
}