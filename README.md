# 🎯 CareerPilot AI – Agentic Job Market Intelligence & Adaptive Career Planning System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

<p align="center">
<b>Empowering career growth through AI-driven job market intelligence, personalized learning paths, and adaptive career planning.</b>
</p>

---

# 📖 Overview

**CareerPilot AI** is an **Agentic AI-powered career planning platform** that continuously analyzes job market trends, extracts in-demand skills, and generates personalized career roadmaps for learners and professionals.

The platform leverages **Machine Learning, TF-IDF skill extraction, intelligent planning pipelines, and Streamlit dashboards** to help users stay aligned with rapidly changing industry demands.

---

# ✨ Key Features

- 🤖 AI-Powered Career Planning
- 📈 Job Market Trend Analysis
- 🧠 Automatic Skill Extraction (TF-IDF)
- 🎯 Personalized Learning Roadmaps
- 📊 Interactive Streamlit Dashboard
- 🔄 Modular ML Pipeline Architecture
- 📚 Role-Based Skill Taxonomy
- ⚡ Real-Time Career Recommendations
- 🔍 Job Dataset Analysis
- 🚀 Agentic AI Ready Architecture

---

# 🧠 How It Works

```text
Job Dataset
      │
      ▼
Data Loader
      │
      ▼
Skill Extraction (TF-IDF)
      │
      ▼
Role Mapping
      │
      ▼
Career Plan Generator
      │
      ▼
Interactive Dashboard
      │
      ▼
Personalized Career Roadmap
```

---

# 🏗️ Project Structure

```text
careerpilot-ai/
│
├── config/
│   └── skill_taxonomy.py
│
├── data/
│   └── jobs.json
│
├── pipelines/
│   ├── data_loader.py
│   ├── skill_extractor.py
│   ├── plan_generator.py
│   └── core_pipeline.py
│
├── dashboard/
│   └── app.py
│
├── agents/            # Future Agentic AI Modules
├── api/               # REST API (Upcoming)
├── models/            # ML Models
│
├── requirements.txt
└── README.md
```

---

# 🏛️ System Architecture

```text
               Job Market Dataset
                       │
                       ▼
              Data Loading Pipeline
                       │
                       ▼
          Skill Extraction Engine
               (TF-IDF Analysis)
                       │
                       ▼
          Career Planning Engine
                       │
                       ▼
        Personalized Career Roadmap
                       │
                       ▼
          Streamlit Dashboard UI
```

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| NLP | TF-IDF Vectorizer |
| Dataset | JSON |
| Version Control | Git & GitHub |

---

# 🚀 Getting Started

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/careerpilot-ai.git

cd careerpilot-ai
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or

```bash
pip install streamlit pandas numpy scikit-learn
```

---

## 3️⃣ Run Dashboard

```bash
streamlit run dashboard/app.py
```

Open:

```
http://localhost:8501
```

---

# 🧪 Run Individual Modules

### Test Data Loader

```bash
python pipelines/data_loader.py
```

### Test Skill Extraction

```bash
python pipelines/skill_extractor.py
```

### Test Career Plan Generator

```bash
python pipelines/plan_generator.py
```

### Test Complete Pipeline

```bash
python pipelines/core_pipeline.py
```

---

# 📊 Dashboard Features

### 📈 Job Market Analysis

- Trending Skills
- Skill Frequency
- Industry Insights

### 🎯 Career Planning

- Target Job Role
- Required Skills
- Learning Roadmap

### 📚 Personalized Recommendations

- Skills to Learn
- Suggested Learning Path
- Career Progress Tracking

---

# 📌 Project Roadmap

## ✅ Phase 1 — Core MVP (Completed)

- Data Loader
- TF-IDF Skill Extraction
- Career Plan Generator
- Streamlit Dashboard
- Modular Pipeline

---

## 🚀 Phase 2 — Enhanced Intelligence

- Resume Upload
- Skill Gap Analysis
- Learning Resource Recommendations
- Interactive Charts
- Progress Tracking

---

## 🤖 Phase 3 — API & Integration

- FastAPI REST API
- Authentication
- Database Integration
- Resume Parsing
- Job Recommendation API

---

## 🧠 Phase 4 — Agentic AI

- Career Advisor Agent
- Job Market Monitoring Agent
- Resume Optimizer Agent
- Interview Preparation Agent
- Learning Coach Agent
- Multi-Agent Collaboration

---

## ☁️ Phase 5 — MLOps & Deployment

- Docker
- CI/CD Pipeline
- Cloud Deployment
- Model Monitoring
- Automated Retraining
- Production APIs

---

# 🌟 Future Features

- 🤖 LLM-Powered Career Coach
- 📄 AI Resume Builder
- 💼 LinkedIn Profile Analyzer
- 🎯 ATS Resume Score
- 🌐 Live Job Market Integration
- 📊 Salary Prediction
- 🎤 Mock Interview Assistant
- 📚 Personalized Course Recommendations
- 📈 Career Progress Analytics

---

# 💡 Why CareerPilot AI?

✅ AI-powered personalized career planning

✅ Continuously adapts to changing job markets

✅ ML-driven skill extraction

✅ Intelligent learning roadmap generation

✅ Modular and scalable architecture

✅ Streamlit-powered interactive dashboard

---

# 👨‍💻 Author

**Aiman Zuha**

🎓 MCA Student

💻 Python & Full Stack Developer

🤖 AI • Machine Learning • MLOps • Agentic AI Enthusiast

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository

🍴 Fork it

🤝 Contribute to improve CareerPilot AI

---

# 📜 License

This project is licensed under the **MIT License**.
