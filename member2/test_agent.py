"""
test_agent.py
--------------
Validates that the schema + agent parsing/validation/retry logic works
correctly end-to-end, using a MockLLMClient instead of a real API call.

Run this with: python3 test_agent.py

To test against a REAL model instead of the mock:
    from contract_intelligence_agent import AnthropicClient  # or GeminiClient
    agent = ContractIntelligenceAgent(llm_client=AnthropicClient())
(Requires `pip install anthropic` / `pip install google-generativeai`
and the relevant API key set as an environment variable.)
"""

import json
from member2.contract_intelligence_agent import ContractIntelligenceAgent, LLMClient
from member2.schemas import StructuredContract


# ---------------------------------------------------------------------------
# Mock client — simulates a well-behaved model response for the sample
# employment contract, so we can test parsing/validation without network
# access. Also includes a "broken first attempt" test to prove the
# self-repair retry loop actually works.
# ---------------------------------------------------------------------------

GOOD_RESPONSE = json.dumps({
    "contract_type": "Employment Contract",
    "parties": [
        {"name": "Bright Tech Solutions Pvt. Ltd.", "role": "Employer"},
        {"name": "Employee (Schedule A)", "role": "Employee"},
    ],
    "important_dates": [
        {"type": "start_date", "value": "1 January 2026", "source_section": "Section 3"},
    ],
    "financial_obligations": [
        {"type": "salary", "amount": "₹80,000/month", "responsible_party": "Employer", "source_section": "Section 6"},
        {"type": "training_cost_recovery", "amount": "₹80,000", "responsible_party": "Employee", "source_section": "Section 18"},
    ],
    "party_obligations": [
        {"party": "Employee", "obligation": "Keep proprietary information confidential during and after employment.", "source_section": "Section 21"},
        {"party": "Employee", "obligation": "Not accept employment with a competing company for 12 months after termination.", "source_section": "Section 24"},
    ],
    "clauses": [
        {"clause_type": "Termination", "original_text": "Either party may terminate this agreement by providing 90 days' written notice. The Employer may terminate immediately for cause as defined in Schedule B.", "source_section": "Section 14"},
        {"clause_type": "Non-Compete", "original_text": "For a period of 12 months following termination of employment for any reason, the Employee shall not accept employment with, or provide services to, any company that directly competes with the Employer's business.", "source_section": "Section 24"},
    ],
})

MALFORMED_RESPONSE = "Sure! Here is the contract analysis: " + GOOD_RESPONSE[:50]  # deliberately broken/truncated


class MockLLMClient(LLMClient):
    """First call returns malformed output; subsequent calls return valid output.
    This proves the retry/self-repair loop in the agent actually works."""

    def __init__(self):
        self.call_count = 0

    def complete(self, system: str, messages: list[dict]) -> str:
        self.call_count += 1
        if self.call_count == 1:
            return MALFORMED_RESPONSE
        return GOOD_RESPONSE


def main():
    with open("sample_contracts/employment_agreement.txt") as f:
        contract_text = f.read()

    mock_client = MockLLMClient()
    agent = ContractIntelligenceAgent(llm_client=mock_client, max_retries=2)

    print("Running extraction (mock client, simulates 1 failed + 1 successful attempt)...\n")
    result: StructuredContract = agent.analyze(contract_text)

    print(f"LLM calls made: {mock_client.call_count} (should be 2 — proves retry logic works)\n")
    print("=" * 70)
    print("VALIDATED STRUCTURED CONTRACT")
    print("=" * 70)
    print(result.model_dump_json(indent=2))

    # Sanity assertions
    assert mock_client.call_count == 2, "Retry logic did not trigger as expected"
    assert result.contract_type == "Employment Contract"
    assert len(result.clauses) == 2
    assert any(fo.type == "training_cost_recovery" for fo in result.financial_obligations)
    print("\nAll assertions passed. Schema validation and retry logic confirmed working.")


if __name__ == "__main__":
    main()