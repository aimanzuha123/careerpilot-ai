"""
RAG Example Retriever — Finds similar high-quality prompts
from the example dataset using TF-IDF cosine similarity.

Used by the Context Builder to inject relevant few-shot examples
into the optimization context.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ExampleRetriever:
    """
    Retrieval-Augmented Generation component that finds
    the most relevant example prompt pairs for a given query.
    """

    def __init__(self, examples_path: str = "data/example_prompts.json"):
        self.examples_path = examples_path
        self.examples: List[Dict[str, Any]] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._load_and_index()

    def _load_and_index(self) -> None:
        """Load examples from JSON and build TF-IDF index."""
        if not os.path.exists(self.examples_path):
            print(f"⚠  Example prompts not found at {self.examples_path}")
            return

        try:
            with open(self.examples_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.examples = data.get("examples", [])
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"⚠  Failed to load examples: {exc}")
            return

        if not self.examples:
            return

        # Build corpus from original + optimized + tags
        corpus = []
        for ex in self.examples:
            text_parts = [
                ex.get("original", ""),
                ex.get("optimized", ""),
                ex.get("domain", ""),
                " ".join(ex.get("tags", [])),
            ]
            corpus.append(" ".join(text_parts).lower())

        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 3,
        min_score: float = 0.05,
    ) -> List[Dict[str, Any]]:
        """
        Find the most relevant example prompts for a given query.

        Args:
            query:   The user's raw prompt text.
            domain:  Optional domain filter (e.g. "ai_ml", "coding").
            top_k:   Maximum number of examples to return.
            min_score: Minimum cosine similarity to include.

        Returns:
            List of example dicts with an added "similarity" key.
        """
        if not self.examples or self.vectorizer is None:
            return []

        # Vectorise the query
        query_clean = self._preprocess(query)
        query_vec = self.vectorizer.transform([query_clean])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Build scored candidates
        candidates = []
        for idx, sim in enumerate(similarities):
            ex = self.examples[idx]
            # Domain boost: +0.15 if domain matches
            if domain and ex.get("domain") == domain:
                sim += 0.15
            if sim >= min_score:
                candidates.append({**ex, "similarity": round(float(sim), 4)})

        # Sort by similarity descending
        candidates.sort(key=lambda x: x["similarity"], reverse=True)
        return candidates[:top_k]

    def retrieve_by_domain(self, domain: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return example prompts filtered by domain, sorted by score."""
        domain_examples = [
            ex for ex in self.examples if ex.get("domain") == domain
        ]
        domain_examples.sort(key=lambda x: x.get("score", 0), reverse=True)
        return domain_examples[:top_k]

    def get_all_domains(self) -> List[str]:
        """Return all unique domains in the example set."""
        return list(set(ex.get("domain", "general") for ex in self.examples))

    @staticmethod
    def _preprocess(text: str) -> str:
        """Basic text preprocessing for similarity matching."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text
