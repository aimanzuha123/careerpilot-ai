🎯 CareerPilot AI
 Agentic Job Market Intelligence & Adaptive Career Planning System

"Continuously adapts career plans based on job market trends using Agentic AI and MLOps pipelines"

 🚀 Phase 1 — Core MVP (Complete)


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

🛠️ Setup & Run

1. Install Dependencies
pip install streamlit
 2. Run the Dashboard
cd careerpilot-ai
streamlit run dashboard/app.p
 3. Run Individual Modules
 Test data loading
python pipelines/data_loader.py
 Test skill extraction
python pipelines/skill_extractor.py
Test plan generation
python pipelines/plan_generator.py
Test full pipeline
python pipelines/core_pipeline.py



Streamlit UI         ← 3-tab dashboard
```
