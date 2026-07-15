"""
run_real_extraction.py
------------------------
Runs Agent 1 against a REAL LLM (not the mock) and prints the
validated structured contract.

Setup:
    1. Choose a provider (Anthropic or Gemini) and install its package:
         pip install pydantic anthropic
       or
         pip install pydantic google-genai

       NOTE: Gemini support uses the current `google-genai` SDK. The
       older `google-generativeai` package is deprecated (Google turned
       it off on 2025-11-30) and will fail with errors like
       "model ... is no longer available to new users" even for models
       that still work fine — the SDK itself is the problem, not the
       model name.

    2. Set your API key as an environment variable:

       macOS/Linux (terminal):
           export ANTHROPIC_API_KEY="your-key-here"
       Windows (PowerShell):
           $env:ANTHROPIC_API_KEY="your-key-here"

       (Use GEMINI_API_KEY instead if using Gemini — get a free key,
       no credit card required, at https://aistudio.google.com/apikey)

    3. Run:
           python3 run_real_extraction.py

    4. To test a different contract, change CONTRACT_PATH below, or
       run: python3 run_real_extraction.py path/to/your_contract.txt
"""

import sys
import os

try:
    from dotenv import load_dotenv
    load_dotenv()  # reads .env in the current directory, if present
except ImportError:
    pass  # dotenv is optional — falls back to manually-set env vars

from member2.contract_intelligence_agent import (
    ContractIntelligenceAgent,
    ContractIntelligenceAgentError,
    AnthropicClient,
    GeminiClient,
)

CONTRACT_PATH = "sample_contracts/employment_agreement.txt"

# "gemini" is the free option (Google AI Studio free tier, no credit card needed).
# Change to "anthropic" if you'd rather use Claude (paid, small cost per call).
PROVIDER = "gemini"


def build_client():
    if PROVIDER == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit(
                "ERROR: ANTHROPIC_API_KEY is not set.\n"
                "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
            )
        return AnthropicClient(model="claude-sonnet-5")

    elif PROVIDER == "gemini":
        if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            sys.exit(
                "ERROR: GEMINI_API_KEY is not set.\n"
                "Get a free key at https://aistudio.google.com/apikey\n"
                "Set it with: export GEMINI_API_KEY='your-key-here'\n"
                "(or put GEMINI_API_KEY=your-key-here in your .env file)"
            )
        # Uses the new `google-genai` SDK — install with: pip install google-genai
        # (the old `google-generativeai` package is deprecated and no longer works)
        return GeminiClient(model="gemini-2.0-flash")

    else:
        sys.exit(f"Unknown PROVIDER: {PROVIDER}")


def main():
    contract_path = sys.argv[1] if len(sys.argv) > 1 else CONTRACT_PATH

    if not os.path.exists(contract_path):
        sys.exit(f"ERROR: Contract file not found: {contract_path}")

    with open(contract_path, "r", encoding="utf-8") as f:
        contract_text = f.read()

    print(f"Reading contract: {contract_path}")
    print(f"Using provider: {PROVIDER}")
    print("Calling the LLM... (this may take a few seconds)\n")

    client = build_client()
    agent = ContractIntelligenceAgent(llm_client=client, max_retries=2)

    try:
        result = agent.analyze(contract_text)
    except ContractIntelligenceAgentError as e:
        sys.exit(f"Extraction failed: {e}")

    print("=" * 70)
    print("STRUCTURED CONTRACT (real LLM output)")
    print("=" * 70)
    print(result.model_dump_json(indent=2))

    # Save to a file too, so you can inspect / hand it to Member 3
    output_path = "last_extraction_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))
    print(f"\nSaved output to {output_path}")


if __name__ == "__main__":
    main()