"""
Configuration management for AI Prompt Optimizer.

Loads settings from environment variables with sensible defaults.
Supports two modes:
  - "llm"        → uses OpenAI API (requires OPENAI_API_KEY)
  - "rule_based" → uses heuristic NLP pipeline (no API key needed)
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Central configuration for the entire system."""

    # ── LLM Settings ──────────────────────────────────────────────────────
    openai_api_key: Optional[str] = None
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048

    # ── Mode ──────────────────────────────────────────────────────────────
    # Automatically set to "llm" if an API key is found, else "rule_based"
    mode: str = "rule_based"

    # ── Storage Paths ─────────────────────────────────────────────────────
    feedback_db_path: str = "storage/feedback_db.json"
    example_prompts_path: str = "data/example_prompts.json"

    # ── RAG Settings ──────────────────────────────────────────────────────
    rag_top_k: int = 3
    similarity_threshold: float = 0.25

    # ── Evaluation Thresholds ─────────────────────────────────────────────
    score_excellent: float = 8.0
    score_good: float = 6.0
    score_needs_work: float = 4.0

    # ── Self-Improvement ──────────────────────────────────────────────────
    learning_rate: float = 0.1          # how fast patterns are weighted
    min_feedback_for_learning: int = 5  # minimum samples before adapting

    @classmethod
    def from_env(cls) -> "Config":
        """Create a Config instance from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        mode = "llm" if api_key else "rule_based"

        return cls(
            openai_api_key=api_key,
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
            mode=mode,
            feedback_db_path=os.getenv("FEEDBACK_DB_PATH", "storage/feedback_db.json"),
            example_prompts_path=os.getenv("EXAMPLE_PROMPTS_PATH", "data/example_prompts.json"),
            rag_top_k=int(os.getenv("RAG_TOP_K", "3")),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.25")),
            learning_rate=float(os.getenv("LEARNING_RATE", "0.1")),
            min_feedback_for_learning=int(os.getenv("MIN_FEEDBACK_FOR_LEARNING", "5")),
        )

    def summary(self) -> dict:
        """Return a serializable summary of current config (no secrets)."""
        return {
            "mode": self.mode,
            "llm_model": self.llm_model if self.mode == "llm" else "N/A",
            "rag_top_k": self.rag_top_k,
            "learning_rate": self.learning_rate,
        }
