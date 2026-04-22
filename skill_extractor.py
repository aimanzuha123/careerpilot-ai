# pipelines/skill_extractor.py
"""
SkillExtractor — Phase 1 Core Module

Extracts skills from job descriptions using:
  - Taxonomy-based keyword matching (Phase 1)
  - TF-IDF frequency scoring
  - Category-weighted ranking

Phase 4+: Will be replaced by an NLP Agent with spaCy NER + LLM-assisted extraction.
"""

import re
import math
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_taxonomy import SKILL_TAXONOMY, ROLE_FOCUS


class SkillExtractor:
    """
    Extracts and ranks skills from job description text.

    Attributes:
        role_type: Target role for weighted extraction (AI/ML, MLOps, DevOps, Data)
        
    Methods:
        extract(descriptions)  -> Dict of skill → frequency
        get_top_skills(n)     -> List of (skill, score) tuples
        get_by_category()     -> Dict of category → [skills]
    """

    def __init__(self, role_type: Optional[str] = None):
        self.role_type = role_type
        self._skill_counts: Counter = Counter()
        self._skill_categories: Dict[str, str] = {}
        self._total_docs: int = 0
        self._doc_freq: Counter = Counter()  # How many docs contain each skill

        # Build flat skill → category lookup
        self._skill_to_category: Dict[str, str] = {}
        for category, data in SKILL_TAXONOMY.items():
            for skill in data["skills"]:
                self._skill_to_category[skill.lower()] = category

    def _clean_text(self, text: str) -> str:
        """Normalize text for matching."""
        text = text.lower()
        text = re.sub(r'[^\w\s\-/+#.]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_from_single(self, description: str) -> Dict[str, int]:
        """Extract skill mentions from a single job description."""
        cleaned = self._clean_text(description)
        found: Dict[str, int] = {}

        for category, data in SKILL_TAXONOMY.items():
            for skill in data["skills"]:
                skill_lower = skill.lower()
                # Match whole word/phrase occurrences
                pattern = r'\b' + re.escape(skill_lower) + r'\b'
                matches = re.findall(pattern, cleaned)
                if matches:
                    found[skill_lower] = len(matches)

        return found

    def _get_category_weight(self, category: str) -> float:
        """Get role-adjusted weight for a category."""
        base_weight = SKILL_TAXONOMY.get(category, {}).get("weight", 1.0)

        if self.role_type and self.role_type in ROLE_FOCUS:
            role_cfg = ROLE_FOCUS[self.role_type]
            if category in role_cfg["primary"]:
                return base_weight * 1.5
            elif category in role_cfg["secondary"]:
                return base_weight * 1.1
            else:
                return base_weight * 0.7

        return base_weight

    def extract(self, descriptions: List[str]) -> "SkillExtractor":
        """
        Process a list of job descriptions and extract skills.
        Returns self for method chaining.
        """
        self._skill_counts = Counter()
        self._doc_freq = Counter()
        self._total_docs = len(descriptions)

        for desc in descriptions:
            doc_skills = self._extract_from_single(desc)
            for skill, count in doc_skills.items():
                self._skill_counts[skill] += count
            # Document frequency (how many jobs mention this skill)
            for skill in doc_skills:
                self._doc_freq[skill] += 1

        return self

    def _compute_tfidf_score(self, skill: str, raw_count: int) -> float:
        """
        Compute a TF-IDF inspired score:
        - TF: normalized count within corpus
        - IDF: log(N / df) where df = number of docs containing skill
        - Weighted by role-specific category importance
        """
        if self._total_docs == 0:
            return 0.0

        tf = raw_count / max(sum(self._skill_counts.values()), 1)
        df = self._doc_freq.get(skill, 1)
        idf = math.log((self._total_docs + 1) / (df + 1)) + 1.0

        category = self._skill_to_category.get(skill, "general")
        cat_weight = self._get_category_weight(category)

        return round(tf * idf * cat_weight * 100, 4)

    def get_top_skills(self, n: int = 20) -> List[Tuple[str, float, int]]:
        """
        Return top N skills as (skill_name, tfidf_score, raw_frequency).
        Sorted by TF-IDF score descending.
        """
        scored = []
        for skill, count in self._skill_counts.items():
            score = self._compute_tfidf_score(skill, count)
            scored.append((skill, score, count))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:n]

    def get_by_category(self) -> Dict[str, List[Tuple[str, int]]]:
        """Return skills grouped by category with their raw frequency."""
        categorized: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        for skill, count in self._skill_counts.items():
            category = self._skill_to_category.get(skill, "other")
            categorized[category].append((skill, count))

        # Sort each category by frequency
        for cat in categorized:
            categorized[cat].sort(key=lambda x: x[1], reverse=True)

        return dict(categorized)

    def get_skill_frequency(self) -> Dict[str, int]:
        """Return raw skill → frequency mapping."""
        return dict(self._skill_counts)

    def get_summary(self) -> Dict:
        """Return a summary of extraction results."""
        top = self.get_top_skills(10)
        return {
            "total_unique_skills": len(self._skill_counts),
            "total_docs_processed": self._total_docs,
            "role_filter": self.role_type or "All",
            "top_10_skills": [{"skill": s, "score": sc, "freq": f} for s, sc, f in top],
            "categories_found": list(self.get_by_category().keys())
        }


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample_descriptions = [
        "We need Python, PyTorch, LangChain, Docker, Kubernetes, and MLflow experience.",
        "Must know Python, TensorFlow, FastAPI, Docker, and Kubernetes. LangChain a plus.",
        "Required: Python, Kubeflow, MLflow, Airflow, Docker, GitHub Actions, Terraform."
    ]

    extractor = SkillExtractor(role_type="MLOps")
    extractor.extract(sample_descriptions)

    print("=== SkillExtractor Test ===")
    summary = extractor.get_summary()
    print(f"Unique skills found: {summary['total_unique_skills']}")
    print("\nTop 10 skills:")
    for item in summary["top_10_skills"]:
        print(f"  {item['skill']:<25} score={item['score']:.4f}  freq={item['freq']}")
