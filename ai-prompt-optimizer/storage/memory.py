"""
Feedback Storage & Memory System.

Persists optimization results to a JSON file and provides
retrieval / analytics capabilities for the self-improving loop.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from collections import defaultdict


class FeedbackMemory:
    """
    JSON-backed storage for prompt optimization history.

    Each record stores:
      - original prompt
      - optimized prompt
      - analysis metadata (domain, intent, missing details)
      - evaluation scores
      - user feedback (optional)
      - timestamp
    """

    def __init__(self, db_path: str = "storage/feedback_db.json"):
        self.db_path = db_path
        self._ensure_file()

    # ── Persistence ──────────────────────────────────────────────────────

    def _ensure_file(self) -> None:
        """Create the DB file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        if not os.path.exists(self.db_path):
            self._write({"records": [], "patterns": {}, "stats": {}})

    def _read(self) -> Dict[str, Any]:
        """Read the entire DB."""
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"records": [], "patterns": {}, "stats": {}}

    def _write(self, data: Dict[str, Any]) -> None:
        """Write the entire DB."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── CRUD ─────────────────────────────────────────────────────────────

    def store(
        self,
        original: str,
        optimized: str,
        analysis: Dict[str, Any],
        scores: Dict[str, Any],
        user_feedback: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store a completed optimization record.

        Returns the unique record ID.
        """
        record_id = str(uuid.uuid4())[:8]
        record = {
            "id": record_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_prompt": original,
            "optimized_prompt": optimized,
            "analysis": analysis,
            "scores": scores,
            "user_feedback": user_feedback,
            "overall_score": scores.get("overall", 0),
        }

        db = self._read()
        db["records"].append(record)
        self._write(db)
        return record_id

    def get_all_records(self) -> List[Dict[str, Any]]:
        """Return all stored records, newest first."""
        db = self._read()
        return sorted(db["records"], key=lambda r: r["timestamp"], reverse=True)

    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific record by ID."""
        for rec in self._read()["records"]:
            if rec["id"] == record_id:
                return rec
        return None

    def update_user_feedback(
        self, record_id: str, feedback: Dict[str, Any]
    ) -> bool:
        """
        Attach user feedback (rating, comment) to an existing record.

        Returns True if the record was found and updated.
        """
        db = self._read()
        for rec in db["records"]:
            if rec["id"] == record_id:
                rec["user_feedback"] = feedback
                self._write(db)
                return True
        return False

    def delete_record(self, record_id: str) -> bool:
        """Delete a record by ID."""
        db = self._read()
        original_len = len(db["records"])
        db["records"] = [r for r in db["records"] if r["id"] != record_id]
        if len(db["records"]) < original_len:
            self._write(db)
            return True
        return False

    def clear_all(self) -> None:
        """Delete all records (keeps structure)."""
        self._write({"records": [], "patterns": {}, "stats": {}})

    # ── Analytics ────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Compute aggregate statistics across all records."""
        records = self._read()["records"]
        if not records:
            return {
                "total_optimizations": 0,
                "avg_score": 0.0,
                "domain_breakdown": {},
                "intent_breakdown": {},
                "score_trend": [],
            }

        # Domain & intent counts
        domain_counts: Dict[str, int] = defaultdict(int)
        intent_counts: Dict[str, int] = defaultdict(int)
        scores: List[float] = []
        score_trend: List[Dict[str, Any]] = []

        for rec in records:
            domain = rec.get("analysis", {}).get("domain", "general")
            intent = rec.get("analysis", {}).get("intent", "instruction")
            overall = rec.get("overall_score", 0)

            domain_counts[domain] += 1
            intent_counts[intent] += 1
            scores.append(overall)

            score_trend.append({
                "id": rec["id"],
                "timestamp": rec["timestamp"],
                "score": overall,
                "domain": domain,
            })

        return {
            "total_optimizations": len(records),
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "max_score": round(max(scores), 2) if scores else 0.0,
            "min_score": round(min(scores), 2) if scores else 0.0,
            "domain_breakdown": dict(domain_counts),
            "intent_breakdown": dict(intent_counts),
            "score_trend": score_trend[-50:],  # last 50
        }

    def get_top_patterns(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Return the top-scoring optimization records.

        Used by the Feedback Agent to learn what makes a good prompt.
        """
        records = self._read()["records"]
        scored = [r for r in records if r.get("overall_score", 0) > 0]
        scored.sort(key=lambda r: r["overall_score"], reverse=True)
        return scored[:n]

    def get_domain_patterns(self, domain: str) -> List[Dict[str, Any]]:
        """Return past optimizations for a specific domain."""
        records = self._read()["records"]
        return [
            r for r in records
            if r.get("analysis", {}).get("domain") == domain
        ]

    def get_recent(self, n: int = 5) -> List[Dict[str, Any]]:
        """Return the N most recent records."""
        return self.get_all_records()[:n]
