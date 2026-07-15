"""
contract_intelligence_agent.py
-------------------------------
Agent 1: Contract Intelligence Agent.

Takes raw contract text (already extracted from PDF — see Member 1's
document_processor.py) and returns a validated StructuredContract.

LLM client note:
The project plan specifies Gemini, but the calling logic below is
written against a minimal `LLMClient` interface so it's a one-file
swap between providers. A ready-to-use Anthropic implementation is
included; swapping to Gemini means writing a GeminiClient with the
same `.complete()` signature.
"""

from __future__ import annotations
import json
import re
from typing import Optional, Protocol

from pydantic import ValidationError

from member2.schemas import StructuredContract
from member2.prompts import SYSTEM_PROMPT, build_extraction_messages


# ---------------------------------------------------------------------------
# LLM client abstraction — swap providers without touching agent logic
# ---------------------------------------------------------------------------

class LLMClient(Protocol):
    def complete(self, system: str, messages: list[dict]) -> str:
        """Return the raw text response from the model."""
        ...


class AnthropicClient:
    """Reference implementation using the Anthropic API."""

    def __init__(self, model: str = "claude-sonnet-5", max_tokens: int = 4000):
        import anthropic  # imported lazily so the module loads without the dep
        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, system: str, messages: list[dict]) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=messages,
        )
        return "".join(
            block.text for block in response.content if block.type == "text"
        )


class GeminiClient:
    """
    Reference implementation using Gemini, per the original tech stack.

    Uses the current `google-genai` SDK (NOT the deprecated
    `google-generativeai` package, which Google shut off on 2025-11-30
    and which is what caused the "model no longer available" errors).

    Requires:
        pip install google-genai
        export GEMINI_API_KEY="your-key-here"   # from aistudio.google.com

    Free-tier-friendly models (as of mid-2026): "gemini-3.1-flash-lite" or
    "gemini-flash-lite-latest". Avoid "gemini-2.5-pro" on the free tier —
    it's capped very low (a handful of requests/day).

    Note: "gemini-2.5-flash" and "gemini-flash-latest" (resolves to
    gemini-3.5-flash) may hit strict free-tier quotas for new API keys.
    """

    def __init__(self, model: str = "gemini-3.1-flash-lite"):
        from google import genai
        import os

        api_key = (
            os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )

        if not api_key:
            raise RuntimeError("Google API key not found.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model

    @staticmethod
    def _extract_text(response) -> str:
        if response.text:
            return response.text
        if response.candidates:
            parts = []
            for part in response.candidates[0].content.parts or []:
                if part.text:
                    parts.append(part.text)
            return "".join(parts)
        return ""

    def complete(self, system: str, messages: list[dict]) -> str:
        from google.genai import types, errors
        import time

        contents = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=m["content"])])
            )

        for attempt in range(5):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0,
                        max_output_tokens=8192,
                        response_mime_type="application/json",
                    ),
                )

                text = self._extract_text(response)
                if text.strip():
                    return text

                print(f"Gemini returned empty response... retry {attempt + 1}/5")
                time.sleep(3)

            except errors.ServerError:
                print(f"Gemini is busy... retry {attempt + 1}/5")
                time.sleep(5)
            except errors.ClientError as e:
                if getattr(e, "code", None) == 429:
                    print(f"Gemini rate limited... retry {attempt + 1}/5")
                    time.sleep(15)
                else:
                    raise

        raise RuntimeError("Gemini service unavailable after 5 retries.")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class ContractIntelligenceAgentError(Exception):
    """Raised when extraction fails after all retries."""


class ContractIntelligenceAgent:
    """
    Agent 1. Converts unstructured contract text into a validated
    StructuredContract instance.
    """

    def __init__(self, llm_client: LLMClient, max_retries: int = 2):
        self.llm_client = llm_client
        self.max_retries = max_retries

    def analyze(self, contract_text: str) -> StructuredContract:
        """
        Runs extraction with validation and a bounded self-repair loop:
        if the model's output doesn't parse/validate, we feed the error
        back to the model and ask it to correct itself.
        """
        messages = build_extraction_messages(contract_text)
        last_error: Optional[str] = None

        for attempt in range(self.max_retries + 1):
            if last_error:
                messages = messages + [
                    {
                        "role": "user",
                        "content": (
                            "Your previous response was invalid JSON or did not "
                            f"match the required schema. Error:\n{last_error}\n\n"
                            "Please respond again with ONLY the corrected JSON object."
                        ),
                    }
                ]

            raw_output = self.llm_client.complete(SYSTEM_PROMPT, messages)
            if not raw_output or not raw_output.strip():
                last_error = "Model returned an empty response"
                continue

            cleaned = self._strip_code_fences(raw_output)

            try:
                data = json.loads(cleaned)
                structured = StructuredContract.model_validate(data)
                return structured
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = str(e)
                continue

        raise ContractIntelligenceAgentError(
            f"Failed to produce a valid structured contract after "
            f"{self.max_retries + 1} attempts. Last error: {last_error}"
        )

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        """Defensive cleanup in case the model wraps JSON in ```json ... ``` anyway."""
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()