import dotenv from "dotenv";
dotenv.config();

const KEY = process.env.GEMINI_API_KEY;

if (!KEY) {
  console.error("Missing GEMINI_API_KEY in .env");
  process.exit(1);
}

async function main() {
  const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${KEY}`;

  const res = await fetch(url);
  const data = await res.json();

  if (!res.ok) {
    console.error("List models failed:", res.status, data);
    process.exit(1);
  }

  const models = data.models || [];
  console.log("Total models:", models.length);

  // Print only those that support generateContent
  const usable = models.filter((m) =>
    (m.supportedGenerationMethods || []).includes("generateContent")
  );

  console.log("\nModels that support generateContent:\n");
  for (const m of usable) {
    console.log(`${m.name}  =>  ${(m.supportedGenerationMethods || []).join(", ")}`);
  }

  console.log("\nSuggested model:", usable[0]?.name || "(none found)");
}

main().catch((e) => console.error(e));