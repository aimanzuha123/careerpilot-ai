"""
LLM Client — Unified abstraction for AI generation.

Supports:
  - OpenAI API (when OPENAI_API_KEY is set)
  - Graceful fallback to rule-based mode (agents handle their own logic)

The client provides a clean interface so agents don't need to care
about which backend is active.
"""

from typing import Optional
from core.config import Config


class LLMClient:
    """Unified LLM interface."""

    def __init__(self, config: Config):
        self.config = config
        self._openai_client = None

        # Attempt to initialise OpenAI if configured
        if config.mode == "llm" and config.openai_api_key:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=config.openai_api_key)
            except ImportError:
                print("⚠  openai package not installed — falling back to rule-based mode.")
                self.config.mode = "rule_based"
            except Exception as exc:
                print(f"⚠  Failed to initialise OpenAI client: {exc}")
                self.config.mode = "rule_based"

    # ── Public API ───────────────────────────────────────────────────────

    @property
    def is_llm_available(self) -> bool:
        """Return True when the OpenAI client is ready."""
        return self._openai_client is not None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[str] = None,
    ) -> str:
        """
        Generate a response using the active backend.

        In rule-based mode this returns an empty string — each agent
        checks ``is_llm_available`` and falls back to its own heuristics.
        """
        if self._openai_client:
            return self._call_openai(
                system_prompt, user_prompt, temperature, max_tokens, response_format
            )
        return ""

    # ── Private ──────────────────────────────────────────────────────────

    def _call_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[str] = None,
    ) -> str:
        """Call the OpenAI Chat Completions API."""
        try:
            kwargs: dict = {
                "model": self.config.llm_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature or self.config.llm_temperature,
                "max_tokens": max_tokens or self.config.llm_max_tokens,
            }
            if response_format == "json":
                kwargs["response_format"] = {"type": "json_object"}

            response = self._openai_client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()
        except Exception as exc:
            print(f"⚠  OpenAI API error: {exc}")
            return ""
