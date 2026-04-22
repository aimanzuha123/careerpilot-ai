"""
Domain-specific prompt templates for the Context Builder Agent.

Each template provides:
  - role: the expert persona to assume
  - structure: recommended output format
  - constraints: quality guardrails
  - example_phrases: few-shot fragments
"""

from typing import Dict, List, Any


# ── Role Assignments ─────────────────────────────────────────────────────────
DOMAIN_ROLES: Dict[str, str] = {
    "ai_ml":        "You are an expert AI/ML engineer and researcher with deep knowledge of modern deep learning, NLP, and MLOps.",
    "coding":       "You are a senior software engineer specializing in clean architecture, design patterns, and production-grade code.",
    "devops":       "You are a senior DevOps/SRE engineer with expertise in CI/CD, containerization, cloud infrastructure, and monitoring.",
    "data_science": "You are a senior data scientist skilled in statistical analysis, data visualization, and communicating insights to stakeholders.",
    "business":     "You are a seasoned business strategist and startup advisor with 15+ years of experience in market analysis and growth.",
    "education":    "You are an experienced educator and curriculum designer who makes complex topics accessible through practical examples.",
    "resume":       "You are a professional resume writer and career coach specializing in tech industry hiring and ATS optimization.",
    "general":      "You are a knowledgeable assistant that provides clear, well-structured, and actionable responses.",
}


# ── Structural Templates ─────────────────────────────────────────────────────
INTENT_STRUCTURES: Dict[str, Dict[str, Any]] = {
    "instruction": {
        "format": "step_by_step",
        "sections": [
            "Requirements / Specifications",
            "Implementation Steps",
            "Expected Output",
            "Testing / Validation",
        ],
        "constraints": [
            "Provide complete, runnable code — no pseudo-code or placeholders",
            "Include proper error handling",
            "Add comments explaining non-obvious logic",
            "Follow language-specific best practices and conventions",
        ],
    },
    "question": {
        "format": "structured_explanation",
        "sections": [
            "Core Concept",
            "How It Works",
            "Practical Example",
            "Common Misconceptions",
            "Further Reading",
        ],
        "constraints": [
            "Start with a concise 1–2 sentence answer",
            "Use analogies for complex concepts",
            "Include concrete examples",
            "Cite sources or authoritative references where applicable",
        ],
    },
    "creative": {
        "format": "open_creative",
        "sections": [
            "Context / Background",
            "Main Content",
            "Summary / Key Takeaways",
        ],
        "constraints": [
            "Be original and engaging",
            "Maintain a consistent tone throughout",
            "Include actionable takeaways where appropriate",
        ],
    },
    "analysis": {
        "format": "analytical_report",
        "sections": [
            "Overview / Executive Summary",
            "Methodology",
            "Findings",
            "Recommendations",
            "Limitations",
        ],
        "constraints": [
            "Support claims with data or evidence",
            "Present multiple perspectives",
            "Clearly separate facts from opinions",
            "Include quantified results where possible",
        ],
    },
    "debug": {
        "format": "diagnostic",
        "sections": [
            "Problem Description",
            "Root Cause Analysis",
            "Solution",
            "Prevention",
        ],
        "constraints": [
            "Reproduce the issue first",
            "Explain WHY the bug occurs, not just how to fix it",
            "Provide before/after code comparison",
            "Suggest preventive measures",
        ],
    },
}


# ── Domain-Specific Constraints ──────────────────────────────────────────────
DOMAIN_CONSTRAINTS: Dict[str, List[str]] = {
    "ai_ml": [
        "Specify the ML framework (PyTorch, TensorFlow, scikit-learn, etc.)",
        "Include data preprocessing and feature engineering steps",
        "Report evaluation metrics appropriate to the task",
        "Discuss model limitations and potential biases",
    ],
    "coding": [
        "Follow SOLID principles and clean code practices",
        "Include type hints and docstrings",
        "Provide unit tests for core functionality",
        "Consider edge cases and input validation",
    ],
    "devops": [
        "Consider security best practices (secrets management, least privilege)",
        "Include monitoring and logging configuration",
        "Document required environment variables and prerequisites",
        "Provide rollback procedures for deployments",
    ],
    "data_science": [
        "Document data sources and assumptions",
        "Handle missing values and outliers explicitly",
        "Use appropriate statistical tests for conclusions",
        "Create reproducible analyses (random seeds, environment specs)",
    ],
    "business": [
        "Include market data or research to support claims",
        "Define target audience / Ideal Customer Profile clearly",
        "Provide realistic financial projections with stated assumptions",
        "Address competitive landscape and differentiation",
    ],
    "education": [
        "Progress from simple to complex concepts",
        "Include hands-on exercises for each concept",
        "Anticipate common beginner mistakes",
        "Provide multiple learning pathways for different styles",
    ],
    "resume": [
        "Optimize for ATS keyword scanning",
        "Use the STAR method (Situation, Task, Action, Result) for achievements",
        "Quantify impact with numbers (%, $, time saved)",
        "Tailor content to the specific target role",
    ],
    "general": [
        "Be concise and to the point",
        "Use examples to illustrate abstract concepts",
        "Structure the response for easy scanning (headers, bullets)",
    ],
}


# ── Tone Guidelines ──────────────────────────────────────────────────────────
TONE_MAP: Dict[str, str] = {
    "instruction":  "Clear, precise, and professional. Prioritize completeness.",
    "question":     "Informative and approachable. Use a teacher's tone.",
    "creative":     "Engaging and thoughtful. Balance creativity with clarity.",
    "analysis":     "Objective and data-driven. Use formal academic tone.",
    "debug":        "Systematic and solution-oriented. Be direct.",
}


def get_template(domain: str, intent: str) -> Dict[str, Any]:
    """
    Assemble a complete template for a given domain + intent combination.

    Returns a dict with keys: role, structure, constraints, tone.
    """
    role = DOMAIN_ROLES.get(domain, DOMAIN_ROLES["general"])
    structure = INTENT_STRUCTURES.get(intent, INTENT_STRUCTURES["instruction"])
    domain_cons = DOMAIN_CONSTRAINTS.get(domain, DOMAIN_CONSTRAINTS["general"])
    intent_cons = structure.get("constraints", [])
    tone = TONE_MAP.get(intent, TONE_MAP["instruction"])

    return {
        "role": role,
        "structure": {
            "format": structure["format"],
            "sections": structure["sections"],
        },
        "constraints": intent_cons + domain_cons,
        "tone": tone,
    }
