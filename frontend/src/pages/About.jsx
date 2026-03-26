export default function About() {
  return (
    <div className="px-6 py-10 text-white max-w-6xl mx-auto space-y-8">

      {/* Header */}
      <div className="space-y-3">
        <h1 className="text-3xl font-bold">
          About Me
        </h1>
        <p className="text-gray-300 max-w-2xl">
          Software Developer focused on building AI-powered applications and scalable
          full-stack systems. Passionate about adaptive learning, automation, and modern web architecture.
        </p>
      </div>

      {/* Profile Card */}
      <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6">
        <h2 className="text-xl font-semibold">Asad Shaikh</h2>
        <p className="text-gray-400 mt-1">
          Full-Stack Developer · AI/ML Enthusiast
        </p>

        <p className="mt-4 text-gray-300">
          B.Tech IT student experienced in MERN stack and machine learning.
          Built real-world AI systems like SmartQuizzer with adaptive learning
          and Gemini integration.
        </p>
      </div>

      {/* Skills */}
      <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Skills</h2>

        <div className="grid md:grid-cols-4 gap-4 text-sm text-gray-300">
          <div>
            <p className="font-medium text-white">Programming</p>
            <p>Java, Python, JavaScript</p>
          </div>

          <div>
            <p className="font-medium text-white">Web</p>
            <p>React, Node, Express, MongoDB</p>
          </div>

          <div>
            <p className="font-medium text-white">AI/ML</p>
            <p>NLP, TensorFlow, Gemini API</p>
          </div>

          <div>
            <p className="font-medium text-white">Tools</p>
            <p>Git, Postman, Cloud</p>
          </div>
        </div>
      </div>

      {/* Projects */}
      <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Projects</h2>

        <div className="grid md:grid-cols-2 gap-4">

          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <h3 className="font-semibold text-white">SmartQuizzer</h3>
            <p className="text-sm text-gray-400 mt-1">
              AI-powered adaptive learning platform with dynamic question generation
              and real-time difficulty adjustment.
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <h3 className="font-semibold text-white">WonderLust</h3>
            <p className="text-sm text-gray-400 mt-1">
              Travel listing platform with authentication, reviews, and map integration.
            </p>
          </div>

        </div>
      </div>

      {/* Experience */}
      <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Experience</h2>

        <div className="space-y-3 text-gray-300 text-sm">
          <div>
            <p className="text-white font-medium">IBM SkillsBuild – AI Intern</p>
            <p className="text-gray-400">Worked on AI models, NLP & cloud-based solutions.</p>
          </div>

          <div>
            <p className="text-white font-medium">Infosys – AI Intern</p>
            <p className="text-gray-400">Built ML solutions and automation workflows.</p>
          </div>
        </div>
      </div>

      {/* Contact */}
      <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Contact</h2>

        <div className="text-gray-300 text-sm space-y-1">
          <p>Email: shaikhasadimam@gmail.com</p>
          <p>GitHub: https://github.com/asadshaikh-21</p>
          <p>Linkedin: https://www.linkedin.com/in/asad-shaikh-9677522a2/</p>
        </div>
      </div>

    </div>
  );
}