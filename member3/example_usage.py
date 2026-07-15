"""
Example usage of the Explanation & Risk Agent.
This shows how Member 4 (Streamlit) would integrate Member 3's module.
"""

from agent import analyze_contract

# Ezzxample input (from Member 2's PDF parsing + Member 1's clause extraction)
contract_data = {
    "clauses": {
        "payment": {
            "found": True,
            "text": "Payment within 30 days."
        },
        "renewal": {
            "found": True,
            "text": "Automatically renews yearly."
        },
        "termination": {
            "found": True,
            "text": "60 day notice."
        },
        "confidentiality": {
            "found": False,
            "text": ""
        },
        "penalty": {
            "found": False,
            "text": ""
        }
    },
    "question": "Is this contract risky?"
}

# Analyze the contract
result = analyze_contract(
    clauses=contract_data["clauses"],
    question=contract_data["question"]
)

# Output is structured and ready for Streamlit
print("=" * 60)
print("CONTRACT ANALYSIS RESULT")
print("=" * 60)
print(f"\nSummary:\n{result.summary}")
print(f"\nRisk Score: {result.risk_score}/100")
print(f"Risk Level: {result.risk_level}")
print(f"\nIdentified Risks:")
for risk in result.risks:
    print(f"  • {risk.category} ({risk.severity}): {risk.description}")
print(f"\nAnswer to Question:\n{result.answer}")
print("\n" + "=" * 60)

# For JSON serialization (to pass to Streamlit or other services)
import json
output_json = result.model_dump()
print("\nJSON Output (for Streamlit):")
print(json.dumps(output_json, indent=2))
