# Member 3: Explanation & Risk Agent

Simple, modular Python implementation of the Explanation & Risk Agent for the AI Contract Review project.

**Now using Google Gemini Free API** (no cost, no credit card required)

## Overview

This module receives parsed contract clauses and generates:
- **Risk Score**: Rule-based calculation (0-100)
- **Risk Level**: Low/Medium/High classification
- **Risk Findings**: Structured list of identified risks
- **Executive Summary**: LLM-generated contract overview (via Gemini)
- **Answer**: LLM response to user's contract question (via Gemini)

## Architecture

```
Input (from Member 2)
    ↓
[schemas.py] → Validation & type safety
    ↓
[risk.py] → Rule-based scoring (Python only)
    ↓
[agent.py] → Gemini-powered analysis
    ↓
Output → JSON to Member 4
```

## Files

### `schemas.py`
Pydantic models for type validation:
- `ClauseInfo`: Single clause (found: bool, text: str)
- `ClausesInput`: All parsed clauses (payment, renewal, termination, confidentiality, penalty)
- `ContractAnalysisInput`: Input wrapper (clauses + user question)
- `ContractAnalysisOutput`: Standardized output format
- `RiskFinding`: Individual risk with category, description, severity

### `risk.py`
Rule-based risk calculation:
- `calculate_risk(clauses)`: Scoring engine
  - +30 if renewal clause exists
  - +20 if penalty clause exists
  - +15 if confidentiality clause is missing
  - +10 if termination notice is long (60+ days)
  - Score clamped to 0-100
  - Returns: risk_score, risk_level, risks list

### `agent.py`
Main analysis function using Google Gemini:
- `analyze_contract(clauses, question)`: Orchestrator
  1. Calls `calculate_risk()` for Python-based scoring
  2. Formats clauses for LLM context
  3. Sends to Gemini API with risk context
  4. Parses Gemini response (summary + answer)
  5. Returns `ContractAnalysisOutput`

## Setup

### 1. Get Free Gemini API Key
No credit card required. Limited free tier is generous for testing.

```bash
# Go to https://aistudio.google.com/apikey
# Click "Create API Key"
# Copy the key
```

### 2. Install & Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="your-key-from-aistudio"

# Test it works
python example_usage.py
```

## Usage

### Basic Usage
```python
from agent import analyze_contract

clauses_data = {
    "payment": {"found": True, "text": "Payment within 30 days."},
    "renewal": {"found": True, "text": "Automatically renews yearly."},
    "termination": {"found": True, "text": "60 day notice."},
    "confidentiality": {"found": False, "text": ""},
    "penalty": {"found": False, "text": ""}
}

question = "Is this contract risky?"

result = analyze_contract(clauses_data, question)
print(result.model_dump_json(indent=2))
```

### Output Format
```json
{
  "summary": "This is a standard service agreement with automatic renewal...",
  "risk_score": 55,
  "risk_level": "Medium",
  "risks": [
    {
      "category": "Renewal",
      "description": "Automatic renewal clause detected. Ensure proper opt-out procedures.",
      "severity": "Medium"
    }
  ],
  "answer": "Yes, this contract carries medium risk, primarily due to the automatic renewal clause..."
}
```

## Integration with Other Members

### Input from Member 1.2 (Clause Extraction)
```python
clauses = ClausesInput(
    payment=ClauseInfo(found=True, text="..."),
    renewal=ClauseInfo(found=True, text="..."),
    # ... etc
)
```

### Output to Member 4 (Streamlit UI)
```python
result = analyze_contract(clauses, question)
output_json = result.model_dump()  # Dict-ready for JSON serialization
```

## Risk Scoring Logic

### Examples

**Example 1: Minimal Risk**
- No renewal, no penalty, confidentiality present, short termination
- Score: 0 → Low

**Example 2: Medium Risk** (given input)
- Renewal (+30), no penalty, no confidentiality (+15), 60-day termination (+10)
- Score: 55 → Medium

**Example 3: High Risk**
- Renewal (+30), penalty (+20), no confidentiality (+15), long termination (+10)
- Score: 75 → High

## Dependencies

- **google-generativeai**: Google Gemini API client
- **pydantic**: Data validation & schemas

## Environment

Requires `GEMINI_API_KEY` environment variable.

## API Costs

- **Gemini 1.5 Flash**: Free tier with generous limits
- No credit card required
- Perfect for development and testing
- See pricing: https://ai.google.dev/pricing

## Troubleshooting

### Missing API Key
```
Error: "GEMINI_API_KEY environment variable not set"
Solution: 
1. Get free key at https://aistudio.google.com/apikey
2. Run: export GEMINI_API_KEY='your-key-here'
```

### Invalid JSON Response
```
Error: "json.JSONDecodeError"
Solution: The module handles this gracefully. Summary will be truncated response.
```

### Invalid Clause Format
```
Error: "validation error in ClausesInput"
Solution: Ensure clauses match schema:
{
  "clause_name": {"found": bool, "text": str}
}
```

## Performance Notes

- **Risk calculation**: ~1ms (pure Python)
- **Gemini API call**: ~1-3 seconds (depends on API latency)
- **Total**: ~2-4 seconds per contract

## Notes

- Risk scores are calculated deterministically by Python rules
- Summary and answer are generated by Google Gemini
- LLM context includes identified risks to inform its analysis
- JSON parsing is robust (handles markdown code blocks)
- Module is stateless and thread-safe
