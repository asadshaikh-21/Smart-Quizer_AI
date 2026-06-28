export default function About() {
  const skills = [
    { category: "Programming", items: ["Java", "Python", "JavaScript"], icon: "⌨️" },
    { category: "Web", items: ["React", "Node.js", "Express", "MongoDB"], icon: "🌐" },
    { category: "AI / ML", items: ["NLP", "TensorFlow", "Gemini API", "LangChain"], icon: "🧠" },
    { category: "Tools", items: ["Git", "Postman", "Docker", "Cloud"], icon: "🛠️" },
  ];

  const projects = [
    {
      name: "SmartQuizzer",
      tag: "AI · Adaptive Learning",
      desc: "AI-powered adaptive learning platform with dynamic question generation and real-time difficulty adjustment using Gemini 2.5.",
      accent: "#7C6FE0",
    },
    {
      name: "CreatorJoy",
      tag: "RAG · LangChain",
      desc: "RAG pipeline with three-tier YouTube transcript fallback — YouTube API → Whisper → metadata — powered by FastAPI and ChromaDB.",
      accent: "#4EA8DE",
    },
    {
      name: "Peblo Notes",
      tag: "Full-Stack · AI",
      desc: "Next.js notes app with Gemini streaming chat, auto-save, and public sharing built on FastAPI and MongoDB.",
      accent: "#56CFB2",
    },
    {
      name: "WonderLust",
      tag: "MERN · Maps",
      desc: "Travel listing platform with authentication, user reviews, and interactive map integration.",
      accent: "#E07C6F",
    },
  ];

  const experience = [
    {
      company: "IBM SkillsBuild",
      role: "AI Intern",
      period: "Jun 2025 – Aug 2025",
      desc: "Worked on AI models, NLP pipelines, and cloud-based solutions across enterprise-grade tooling.",
    },
    {
      company: "Infosys",
      role: "AI Intern",
      period: "Sep 2025 – Dec 2025",
      desc: "Built ML solutions and automation workflows integrated into real-world production environments.",
    },
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0d0f1a 0%, #12162b 50%, #0d0f1a 100%)",
        color: "#e2e8f0",
        fontFamily: "'Inter', 'Segoe UI', sans-serif",
        padding: "2.5rem 1.5rem",
      }}
    >
      <div style={{ maxWidth: "1100px", margin: "0 auto" }}>

        {/* ── Hero ── */}
        <div style={{ marginBottom: "3rem", position: "relative" }}>
          {/* eyebrow */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              background: "rgba(124,111,224,0.12)",
              border: "1px solid rgba(124,111,224,0.3)",
              borderRadius: "999px",
              padding: "4px 14px",
              fontSize: "0.75rem",
              color: "#a89fe8",
              marginBottom: "1.25rem",
              letterSpacing: "0.05em",
              textTransform: "uppercase",
            }}
          >
            <span
              style={{
                width: "6px",
                height: "6px",
                borderRadius: "50%",
                background: "#7C6FE0",
                display: "inline-block",
                boxShadow: "0 0 6px #7C6FE0",
              }}
            />
            About Me
          </div>

          <h1
            style={{
              fontSize: "clamp(2rem, 5vw, 3.25rem)",
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: "1rem",
              background: "linear-gradient(135deg, #ffffff 40%, #7C6FE0 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Asad Shaikh
          </h1>

          <p
            style={{
              fontSize: "1.05rem",
              color: "#94a3b8",
              maxWidth: "560px",
              lineHeight: 1.7,
              marginBottom: "1.75rem",
            }}
          >
            Full-Stack Developer & AI/ML Engineer. B.Tech IT student building production-grade
            AI systems — from adaptive quizzing engines to RAG pipelines with real-world deployments.
          </p>

          {/* stat pills */}
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            {[
              { label: "Internships", value: "2" },
              { label: "Projects Shipped", value: "5+" },
              { label: "LeetCode", value: "150+" },
            ].map((s) => (
              <div
                key={s.label}
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: "12px",
                  padding: "10px 20px",
                  textAlign: "center",
                }}
              >
                <div style={{ fontSize: "1.4rem", fontWeight: 700, color: "#7C6FE0" }}>
                  {s.value}
                </div>
                <div style={{ fontSize: "0.72rem", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Skills ── */}
        <Section title="Skills" subtitle="Core technologies I build with">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "1rem" }}>
            {skills.map((s) => (
              <div key={s.category} style={glassCard}>
                <div style={{ fontSize: "1.5rem", marginBottom: "0.6rem" }}>{s.icon}</div>
                <div style={{ fontSize: "0.7rem", color: "#7C6FE0", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "0.4rem" }}>
                  {s.category}
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                  {s.items.map((item) => (
                    <span key={item} style={chip}>{item}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* ── Projects ── */}
        <Section title="Projects" subtitle="Things I've built and shipped">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "1rem" }}>
            {projects.map((p) => (
              <div
                key={p.name}
                style={{
                  ...glassCard,
                  borderTop: `2px solid ${p.accent}`,
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* glow blob */}
                <div
                  style={{
                    position: "absolute",
                    top: "-30px",
                    right: "-30px",
                    width: "100px",
                    height: "100px",
                    borderRadius: "50%",
                    background: p.accent,
                    opacity: 0.07,
                    filter: "blur(30px)",
                    pointerEvents: "none",
                  }}
                />
                <div style={{ fontSize: "0.68rem", color: p.accent, textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "0.5rem" }}>
                  {p.tag}
                </div>
                <div style={{ fontWeight: 700, fontSize: "1.05rem", marginBottom: "0.5rem", color: "#f1f5f9" }}>
                  {p.name}
                </div>
                <p style={{ fontSize: "0.85rem", color: "#94a3b8", lineHeight: 1.6 }}>{p.desc}</p>
              </div>
            ))}
          </div>
        </Section>

        {/* ── Experience ── */}
        <Section title="Experience" subtitle="Where I've applied my skills">
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {experience.map((e, i) => (
              <div key={i} style={{ ...glassCard, display: "flex", gap: "1.25rem", alignItems: "flex-start" }}>
                {/* timeline dot */}
                <div style={{ flexShrink: 0, marginTop: "4px" }}>
                  <div
                    style={{
                      width: "10px",
                      height: "10px",
                      borderRadius: "50%",
                      background: "#7C6FE0",
                      boxShadow: "0 0 8px #7C6FE0",
                    }}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "4px", marginBottom: "0.35rem" }}>
                    <div>
                      <span style={{ fontWeight: 700, color: "#f1f5f9" }}>{e.company}</span>
                      <span style={{ color: "#7C6FE0", marginLeft: "8px", fontSize: "0.85rem" }}>· {e.role}</span>
                    </div>
                    <span
                      style={{
                        fontSize: "0.7rem",
                        color: "#64748b",
                        background: "rgba(255,255,255,0.04)",
                        border: "1px solid rgba(255,255,255,0.07)",
                        borderRadius: "999px",
                        padding: "2px 10px",
                      }}
                    >
                      {e.period}
                    </span>
                  </div>
                  <p style={{ fontSize: "0.86rem", color: "#94a3b8", lineHeight: 1.6, margin: 0 }}>{e.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* ── Contact ── */}
        <Section title="Contact" subtitle="Let's connect">
          <div style={{ ...glassCard, display: "flex", flexWrap: "wrap", gap: "1rem" }}>
            {[
              { label: "Email", value: "shaikhasadimam@gmail.com", href: "mailto:shaikhasadimam@gmail.com", icon: "✉️" },
              { label: "GitHub", value: "asadshaikh-21", href: "https://github.com/asadshaikh-21", icon: "🐙" },
              { label: "LinkedIn", value: "asad-shaikh", href: "https://www.linkedin.com/in/asad-shaikh-9677522a2/", icon: "💼" },
            ].map((c) => (
              <a
                key={c.label}
                href={c.href}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  background: "rgba(124,111,224,0.08)",
                  border: "1px solid rgba(124,111,224,0.2)",
                  borderRadius: "12px",
                  padding: "10px 18px",
                  textDecoration: "none",
                  color: "#c4b8ff",
                  fontSize: "0.875rem",
                  transition: "background 0.2s",
                }}
              >
                <span>{c.icon}</span>
                <div>
                  <div style={{ fontSize: "0.65rem", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>{c.label}</div>
                  <div>{c.value}</div>
                </div>
              </a>
            ))}
          </div>
        </Section>

      </div>
    </div>
  );
}

/* ── helpers ── */

function Section({ title, subtitle, children }) {
  return (
    <div style={{ marginBottom: "2.75rem" }}>
      <div style={{ marginBottom: "1.25rem" }}>
        <h2 style={{ fontSize: "1.35rem", fontWeight: 700, color: "#f1f5f9", margin: 0 }}>{title}</h2>
        {subtitle && (
          <p style={{ fontSize: "0.82rem", color: "#64748b", margin: "4px 0 0" }}>{subtitle}</p>
        )}
      </div>
      {children}
    </div>
  );
}

const glassCard = {
  background: "rgba(255,255,255,0.04)",
  backdropFilter: "blur(12px)",
  border: "1px solid rgba(255,255,255,0.08)",
  borderRadius: "16px",
  padding: "1.25rem 1.5rem",
};

const chip = {
  background: "rgba(124,111,224,0.1)",
  border: "1px solid rgba(124,111,224,0.2)",
  borderRadius: "999px",
  padding: "3px 10px",
  fontSize: "0.75rem",
  color: "#a89fe8",
};