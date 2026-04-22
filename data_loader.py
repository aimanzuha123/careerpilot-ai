# pipelines/data_loader.py
"""
DataLoader — Phase 1 Core Module
Responsible for loading and validating job market data from JSON datasets.
In later phases this will be extended to support live APIs (LinkedIn, etc.)
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JobRecord:
    """Structured job record with validated fields."""
    id: int
    title: str
    company: str
    role_type: str
    description: str
    location: str
    salary: str
    posted_days_ago: int
    loaded_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "role_type": self.role_type,
            "description": self.description,
            "location": self.location,
            "salary": self.salary,
            "posted_days_ago": self.posted_days_ago,
            "loaded_at": self.loaded_at
        }


class DataLoader:
    """
    Loads and validates job market data.
    
    Supports:
        - Local JSON file loading
        - Basic validation and schema enforcement
        - Role-based filtering
    
    Phase 4+: Will support live API sources (LinkedIn, Indeed)
    """

    VALID_ROLE_TYPES = {"AI/ML", "MLOps", "DevOps", "Data"}

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            # Default to jobs.json relative to project root
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, "jobs.json")
        self.data_path = data_path
        self._jobs: List[JobRecord] = []
        self._load_errors: List[str] = []

    def load(self) -> "DataLoader":
        """Load job data from the configured source. Returns self for chaining."""
        self._jobs = []
        self._load_errors = []

        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        for idx, raw in enumerate(raw_data):
            try:
                job = self._parse_record(raw)
                self._jobs.append(job)
            except (KeyError, ValueError) as e:
                self._load_errors.append(f"Record {idx}: {str(e)}")

        return self

    def _parse_record(self, raw: Dict) -> JobRecord:
        """Parse and validate a raw dict into a JobRecord."""
        required = ["id", "title", "company", "role_type", "description"]
        for field in required:
            if field not in raw:
                raise KeyError(f"Missing required field: '{field}'")

        return JobRecord(
            id=int(raw["id"]),
            title=str(raw["title"]),
            company=str(raw["company"]),
            role_type=str(raw.get("role_type", "General")),
            description=str(raw["description"]),
            location=str(raw.get("location", "Unknown")),
            salary=str(raw.get("salary", "Not disclosed")),
            posted_days_ago=int(raw.get("posted_days_ago", 0))
        )

    def get_all(self) -> List[JobRecord]:
        """Return all loaded job records."""
        return self._jobs

    def get_by_role(self, role_type: str) -> List[JobRecord]:
        """Filter jobs by role type (AI/ML, MLOps, DevOps, Data)."""
        return [j for j in self._jobs if j.role_type == role_type]

    def get_stats(self) -> Dict:
        """Return summary statistics about the loaded dataset."""
        role_counts = {}
        for job in self._jobs:
            role_counts[job.role_type] = role_counts.get(job.role_type, 0) + 1

        return {
            "total_jobs": len(self._jobs),
            "role_breakdown": role_counts,
            "load_errors": len(self._load_errors),
            "error_details": self._load_errors,
            "data_source": self.data_path
        }

    def get_descriptions(self, role_type: Optional[str] = None) -> List[str]:
        """Extract raw descriptions for NLP processing."""
        jobs = self.get_by_role(role_type) if role_type else self.get_all()
        return [j.description for j in jobs]


# ── Quick test when run directly ──────────────────────────────────────────────
if __name__ == "__main__":
    loader = DataLoader()
    loader.load()
    stats = loader.get_stats()
    print("=== DataLoader Test ===")
    print(f"Loaded {stats['total_jobs']} jobs")
    print(f"Role breakdown: {stats['role_breakdown']}")
    print(f"Errors: {stats['load_errors']}")
    for job in loader.get_by_role("AI/ML")[:2]:
        print(f"\n  → [{job.role_type}] {job.title} @ {job.company}")
