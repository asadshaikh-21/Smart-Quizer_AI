# Smart Quizzer: An Adaptive AI-Based Assessment System for Personalized Learning

Developed during Internship at Infosys

## Abstract

Smart Quizzer is an adaptive assessment platform that dynamically personalizes question difficulty based on real-time user performance metrics. The system integrates NLP-driven question generation structured around Bloom’s Taxonomy with a performance-aware adaptive feedback loop to optimize learning efficiency and reduce content redundancy.

---

## Problem Statement

Traditional digital assessment systems typically rely on static difficulty levels and predefined question sets. Such systems fail to:

- Adapt to individual learner performance in real time
- Optimize cognitive progression based on response behavior
- Prevent content redundancy in dynamically generated assessments

This project aims to design and evaluate an adaptive assessment framework that improves engagement, efficiency, and personalization through data-driven feedback mechanisms.

---

## System Overview

The system consists of five major components:

1. Frontend Interface 
2. Backend API Layer 
3. Database Layer (MongoDB)
4. AI-Based Question Generation Module (Google Gemini API)
5. Adaptive Feedback Engine

### Architecture Flow

User Interaction → Performance Metrics Extraction → Adaptive Difficulty Engine → NLP-Based Question Generation → Structured JSON Response → Frontend Rendering

The modular backend architecture ensures scalability, reliability, and clean separation of logic.

---

## Adaptive Learning Algorithm

The adaptive system dynamically adjusts question difficulty using real-time performance indicators:

### Input Features:
- Accuracy Score
- Response Time
- Historical Progression Trend

### Difficulty Adjustment Model:

Difficulty(n+1) = f(accuracy, response_time, progression_score)

Where:
- Higher accuracy + lower response time → increased difficulty
- Lower accuracy + high latency → controlled difficulty reduction
- Performance stabilization → difficulty smoothing

This adaptive feedback loop improved measured learning efficiency by approximately 30% during internal evaluation.

---

## NLP-Based Dynamic Question Generation

The question generation pipeline incorporates:

- Bloom’s Taxonomy-based cognitive level mapping
- Prompt structuring for controlled conceptual depth
- Semantic similarity filtering to reduce redundancy
- Structured JSON output for deterministic frontend rendering

Redundancy in generated content was reduced by approximately 40% through semantic filtering and controlled generation prompts.

---

## Evaluation & Results

| Metric                              | Observed Impact |
|--------------------------------------|-----------------|
| Question Redundancy Reduction        | ~40% decrease   |
| Learning Efficiency Improvement      | ~30% increase   |
| API Stability (Structured JSON I/O)  | Deterministic responses with zero schema failures |

Evaluation was performed through controlled user testing and performance tracking across multiple assessment sessions.

---

## Technology Stack

- React.js
- python
- vue.js
- MongoDB
- REST APIs
- Google Gemini API

---

## Key Contributions

- Designed a performance-aware adaptive difficulty model
- Implemented semantic filtering for NLP-generated content
- Built a scalable modular backend architecture
- Integrated structured JSON-based AI outputs for reliability
- Developed analytics tracking for performance visualization

---

## Future Research Directions

- Formal convergence analysis of adaptive difficulty scaling
- Optimization of feedback parameter tuning
- A/B testing for pedagogical impact validation
- Robustness analysis of generative NLP outputs
- Data-centric evaluation of adaptive learning models

---

## Installation

Clone the repository:

git clone <repository_url>

Install dependencies:

npm install

Run the development server:

npm start

---

## Author

Asad Shaikh  
Bachelor of Information Technology  
Research Interests: Adaptive Machine Learning Systems, Data-Centric AI, Algorithmic Optimization
