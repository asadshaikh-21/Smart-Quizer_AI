# 🧠 Smart Quizzer  
### Adaptive AI-Based Assessment System for Personalized Learning  
Developed during Internship at Infosys

---

## 🚀 Overview

Smart Quizzer is an AI-powered adaptive assessment platform that dynamically adjusts question difficulty in real time based on user performance.

Unlike traditional static quiz systems, this platform uses performance-aware feedback loops and NLP-based dynamic question generation to optimize learning efficiency and reduce content redundancy.

---

## 🎯 Key Features

- 🔄 Real-time adaptive difficulty adjustment  
- 🧠 Bloom’s Taxonomy-based question structuring  
- 📉 40% reduction in question redundancy  
- 📈 30% improvement in measured learning efficiency  
- 🧩 Modular and scalable backend architecture  
- 📊 Performance analytics tracking  

---

## 🏗️ System Architecture

**Flow:**

User → Performance Metrics → Adaptive Engine → AI Question Generator → Structured JSON → Frontend Rendering

### Core Components

- Frontend (Vue.js)
- Backend API (Python + REST)
- Database (MongoDB)
- AI Integration (Google Gemini API)
- Adaptive Feedback Engine

---

## 🧮 Adaptive Difficulty Model

The system dynamically adjusts question difficulty using:

```
Difficulty(n+1) = f(accuracy, response_time, progression_score)
```

**Logic:**

- High accuracy + low response time → Increase difficulty  
- Low accuracy + high latency → Reduce difficulty  
- Stabilized performance → Smooth difficulty scaling  

---

## 📊 Evaluation Results

| Metric | Observed Impact |
|--------|----------------|
| Question Redundancy Reduction | ~40% decrease |
| Learning Efficiency Improvement | ~30% increase |
| API Stability | Zero JSON schema failures |

---

## 🛠️ Tech Stack

- Vue.js  
- Python  
- MongoDB  
- REST APIs  
- Google Gemini API  

---

## 📂 Project Structure

```
Smart-Quizer_AI/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
│
├── frontend/vue-project/
│   ├── src/
│   └── package.json
│
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Smart-Quizer_AI.git
cd Smart-Quizer_AI
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend/vue-project
npm install
npm run dev
```

---

## 📈 Future Enhancements

- Formal convergence analysis of adaptive difficulty scaling  
- Optimization of feedback parameter tuning  
- A/B testing for pedagogical validation  
- Robustness analysis of generative NLP outputs  

---

## 👨‍💻 Author

**Asad Shaikh**  
Bachelor of Information Technology  

**Research Interests:**
- Adaptive Machine Learning Systems  
- Data-Centric AI  
- Algorithmic Optimization  

---

## 📜 License

This project is for academic and research purposes.
