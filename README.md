# 🎯 CareerPilot AI
### Agentic Job Market Intelligence & Adaptive Career Planning System

> **"Continuously adapts career plans based on job market trends using Agentic AI and MLOps pipelines"**

---

## 🚀 Phase 1 — Core MVP (Complete)

### What's Built

| Module | File | Description |
|---|---|---|
| Data Loader | `pipelines/data_loader.py` | Loads & validates job dataset |
| Skill Extractor | `pipelines/skill_extractor.py` | NLP-based TF-IDF skill extraction |
| Plan Generator | `pipelines/plan_generator.py` | 4-week adaptive learning plan |
| Core Pipeline | `pipelines/core_pipeline.py` | Orchestrates all modules |
| Dashboard | `dashboard/app.py` | Streamlit UI |
| Skill Taxonomy | `config/skill_taxonomy.py` | 100+ skills across 12 categories |
| Dataset | `data/jobs.json` | 15 curated AI/ML job listings |

### Project Structure

```
careerpilot-ai/
├── config/
│   └── skill_taxonomy.py      # Master skill list + role weights
├── data/
│   └── jobs.json              # Sample job market dataset
├── pipelines/
│   ├── data_loader.py         # DataLoader class
│   ├── skill_extractor.py     # SkillExtractor class (TF-IDF)
│   ├── plan_generator.py      # PlanGenerator class
│   └── core_pipeline.py       # CorePipeline orchestrator
├── dashboard/
│   └── app.py                 # Streamlit UI
├── agents/                    # (Phase 4)
├── api/                       # (Phase 3)
├── models/                    # (Phase 4)
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup & Run

### 1. Install Dependencies
```bash
pip install streamlit
```

### 2. Run the Dashboard
```bash
cd careerpilot-ai
streamlit run dashboard/app.py
```

### 3. Run Individual Modules
```bash
# Test data loading
python pipelines/data_loader.py

# Test skill extraction
python pipelines/skill_extractor.py

# Test plan generation
python pipelines/plan_generator.py

# Test full pipeline
python pipelines/core_pipeline.py
```

---

## ⚙️ Tech Stack — Phase 1

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| NLP | Regex + TF-IDF (custom) |
| UI | Streamlit |
| Data | JSON dataset |

---

## 🗺️ Roadmap

| Phase | Status | Features |
|---|---|---|
| **Phase 1** | ✅ Done | Core MVP: data + NLP + plan + UI |
| Phase 2 | ⏳ Next | Resume PDF analyzer + skill gap + role switching |
| Phase 3 | 🔜 | FastAPI layer + dashboard charts |
| Phase 4 | 🔜 | Agentic AI (7 agents) + forecasting |
| Phase 5 | 🔜 | Docker + CI/CD + monitoring |

---

## 🧠 Architecture (Phase 1)

```
Job Dataset (JSON)
      ↓
 DataLoader          ← validates & structures job records
      ↓
SkillExtractor       ← TF-IDF + role-weighted scoring
      ↓
PlanGenerator        ← 4-week adaptive plan
      ↓
CorePipeline         ← orchestrator (→ OrchestratorAgent in Phase 4)
      ↓
Streamlit UI         ← 3-tab dashboard
```
