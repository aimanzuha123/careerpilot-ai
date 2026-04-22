# pipelines/core_pipeline.py
"""
CorePipeline -- Phase 1 + Phase 2 Upgrade

Orchestrates the full CareerPilot AI pipeline:
  Phase 1: DataLoader -> SkillExtractor -> PlanGenerator
  Phase 2: + RoleManager + ResumeAnalyzer -> Gap-driven PlanGenerator

Usage:
    # Generic plan (no resume)
    pipeline = CorePipeline(role_type="MLOps", skill_level="intermediate")
    result = pipeline.run()

    # Personalized plan (with resume bytes from Streamlit)
    pipeline = CorePipeline(role_type="MLOps")
    result = pipeline.run(resume_bytes=pdf_bytes, resume_filename="cv.pdf")

Phase 4+: Will be replaced by OrchestratorAgent.
"""

from typing import Dict, Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import DataLoader
from skill_extractor import SkillExtractor
from plan_generator import PlanGenerator
from role_manager import RoleManager
from resume_analyzer import ResumeAnalyzer


class CorePipeline:
    """
    Single entry point for the full CareerPilot AI pipeline.

    Result dict keys:
        pipeline_status   : "success" | "error"
        config            : run parameters
        data_stats        : job dataset summary
        role_context      : active role metadata
        skill_summary     : top skills + categories
        top_skills        : list of {skill, score, frequency}
        skills_by_category: grouped skills
        resume_analysis   : ResumeAnalysisResult dict (None if no resume)
        plan              : 4-week learning plan dict
    """

    def __init__(
        self,
        role_type: str = "AI/ML",
        skill_level: str = "intermediate",
        hours_per_week: float = 10.0,
        data_path: Optional[str] = None,
        top_n_skills: int = 20
    ):
        self.role_type = role_type
        self.skill_level = skill_level
        self.hours_per_week = hours_per_week
        self.data_path = data_path
        self.top_n_skills = top_n_skills
        self._result: Optional[Dict] = None

    def run(
        self,
        resume_bytes: Optional[bytes] = None,
        resume_filename: str = "resume.pdf",
        resume_text: Optional[str] = None
    ) -> Dict:
        """
        Execute the full pipeline.

        Args:
            resume_bytes:    Raw PDF bytes (from Streamlit uploader)
            resume_filename: Original filename for display
            resume_text:     Plain text resume (alternative to PDF)

        Returns:
            Full result dict.
        """
        # ── 1. Role Manager ────────────────────────────────────────
        role_mgr = RoleManager()
        
        # Adapt to RoleManager's actual methods since activate() does not exist
        if hasattr(role_mgr, "get_role_info"):
            role_info = role_mgr.get_role_info(self.role_type)
        else:
            role_info = {}

        # ── 2. Load Data ───────────────────────────────────────────
        loader = DataLoader(data_path=self.data_path)
        loader.load()
        data_stats = loader.get_stats()

        # ── 3. Extract & Rank Skills (role-boosted) ────────────────
        descriptions = loader.get_descriptions(role_type=self.role_type)
        if not descriptions:
            descriptions = loader.get_descriptions()

        extractor = SkillExtractor(role_type=self.role_type)
        extractor.extract(descriptions)

        raw_top = extractor.get_top_skills(self.top_n_skills)
        
        # Apply role boost if methods exist, otherwise fallback
        if hasattr(role_mgr, "filter_skills_for_role"):
            top_skills = role_mgr.filter_skills_for_role(raw_top)
        else:
            top_skills = raw_top

        skill_summary = extractor.get_summary()
        skills_by_category = extractor.get_by_category()

        # ── 4. Resume Analysis (Phase 2) ───────────────────────────
        resume_result = None
        gap_skills = []
        known_skills = []

        has_resume = resume_bytes is not None or resume_text is not None

        if has_resume:
            analyzer = ResumeAnalyzer(role_type=self.role_type)
            if resume_bytes is not None:
                resume_result = analyzer.analyze_bytes(
                    resume_bytes, top_skills, filename=resume_filename
                )
            else:
                resume_result = analyzer.analyze_text(
                    resume_text, top_skills, source_name="pasted_text"
                )
            gap_skills = resume_result.gap_skills
            known_skills = resume_result.matched_skills

        # ── 5. Generate Plan ───────────────────────────────────────
        generator = PlanGenerator(
            role_type=self.role_type,
            skill_level=self.skill_level,
            top_skills=top_skills,
            hours_per_week=self.hours_per_week,
            gap_skills=gap_skills if has_resume else [],
            known_skills=known_skills if has_resume else []
        )
        generator.generate()
        plan = generator.get_plan_dict()

        # ── 6. Assemble Result ────────────────────────────────────
        self._result = {
            "pipeline_status": "success",
            "has_resume": has_resume,
            "config": {
                "role_type": self.role_type,
                "skill_level": self.skill_level,
                "hours_per_week": self.hours_per_week
            },
            "data_stats": data_stats,
            "role_context": role_info,
            "skill_summary": skill_summary,
            "top_skills": [
                {"skill": s, "score": round(sc, 3), "frequency": f}
                for s, sc, f in top_skills
            ],
            "skills_by_category": {
                cat: [{"skill": s, "frequency": fr} for s, fr in items]
                for cat, items in skills_by_category.items()
            },
            "resume_analysis": resume_result.to_dict() if resume_result else None,
            "plan": plan
        }
        return self._result

    def get_result(self) -> Optional[Dict]:
        return self._result


# -- Quick test ----------------------------------------------------------------
if __name__ == "__main__":
    import json

    # Test 1: no resume
    print("=== Test 1: Generic pipeline (no resume) ===")
    p = CorePipeline(role_type="MLOps", skill_level="intermediate", hours_per_week=10.0)
    r = p.run()
    print(f"Status:  {r['pipeline_status']}")
    print(f"Role:    {r['role_context']['label']}")
    print(f"Jobs:    {r['data_stats']['total_jobs']}")
    print(f"Skills:  {r['skill_summary']['total_unique_skills']}")

    # Test 2: with sample resume text
    print("\n=== Test 2: Resume-driven pipeline ===")
    RESUME = """
    Jane Smith | ML Engineer
    Skills: Python, TensorFlow, Docker, FastAPI, PostgreSQL, AWS
    Built ML pipelines with TensorFlow and deployed via Docker on AWS.
    Used FastAPI for serving, PostgreSQL for storage.
    """
    p2 = CorePipeline(role_type="MLOps", skill_level="intermediate")
    r2 = p2.run(resume_text=RESUME)
    ra = r2["resume_analysis"]
    print(f"Match Score:    {ra['match_score']}%")
    print(f"Resume Skills:  {ra['total_resume_skills']}")
    print(f"Matched:        {ra['matched_skills']}")
    print(f"Top 5 Gaps:")
    for g in ra["gap_skills"][:5]:
        print(f"  [{g['demand_level']}] {g['skill']}")
    print(f"\nPlan mode: {'Gap-Driven' if r2['plan']['gap_driven'] else 'Market-Driven'}")
