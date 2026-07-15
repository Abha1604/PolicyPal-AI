# Integration Guide: Member 3 in AI Contract Review

**Member 3 now uses Google Gemini Free API** - No cost, no credit card required!

## Project Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ Member 4: Streamlit UI                                  │
│ (Input form, Display results, User interaction)         │
└────────────┬────────────────────────────────────────────┘
             │
             │ JSON Input
             ▼
┌─────────────────────────────────────────────────────────┐
│ Member 2: LangGraph Orchestrator                        │
│ (Coordinates workflow, passes data between stages)      │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────┐    ┌──────────────┐
│ Member 1 │    │ Member 2.1   │
│ PDF      │    │ RAG          │
│ Parsing  │    │              │
└────┬─────┘    └────┬─────────┘
     │               │
     └───────┬───────┘
             │
             ▼
    ┌─────────────────┐
    │ Member 1.2      │
    │ Clause          │
    │ Extraction      │
    └────────┬────────┘
             │
             │ ClausesInput (JSON)
             │
             ▼
    ┌─────────────────────────────┐
    │ ★ Member 3: Risk Agent ★   │
    │ (THIS MODULE)               │
    │ - Gemini API for LLM        │
    │ - Python rule-based scoring │
    └────────┬────────────────────┘
             │
             │ ContractAnalysisOutput (JSON)
             │
             ▼
    ┌─────────────────────────────┐
    │ ★ Member 4: Streamlit UI ★ │
    │ (Display results)           │
    └─────────────────────────────┘
```

## Data Flow: Step-by-Step

### Step 1: PDF Processing (Members 1 + 2)
```
PDF File
  ↓
[Member 1: PDF Parsing]
  ↓ (text extraction)
Document Text
  ↓
[Member 2.1: RAG - Semantic Search]
  ↓ (relevant sections)
Relevant Sections
  ↓
[Member 1.2: Clause Extraction]
  ↓ (identifies clauses)
ClausesInput (JSON)
```

### Step 2: Risk Analysis (Member 3 - THIS MODULE)
```
ClausesInput + Question
  ↓
analyze_contract(clauses, question)
  │
  ├─→ calculate_risk(clauses)
  │   └─→ Rule-based scoring (Python only)
  │       ├─ Check renewal
  │       ├─ Check penalty
  │       ├─ Check confidentiality
  │       └─ Check termination length
  │       → risk_score, risk_level, risks[]
  │
  ├─→ Format for LLM
  │
  ├─→ Call Gemini API
  │   └─→ Generate summary
  │   └─→ Answer question
  │
  └─→ Return ContractAnalysisOutput (JSON)
```

### Step 3: UI Rendering (Member 4)
```
ContractAnalysisOutput
  ↓
[Streamlit Dashboard]
  ├─ Display Summary
  ├─ Show Risk Score (visual)
  ├─ List Risks
  └─ Display Answer
```

## Input/Output Contract

### Input to Member 3 (from Member 1.2)
```json
{
  "clauses": {
    "payment": {"found": true, "text": "Payment within 30 days."},
    "renewal": {"found": true, "text": "Automatically renews yearly."},
    "termination": {"found": true, "text": "60 day notice."},
    "confidentiality": {"found": false, "text": ""},
    "penalty": {"found": false, "text": ""}
  },
  "question": "Is this contract risky?"
}
```

### Output from Member 3 (to Member 4)
```json
{
  "summary": "This is a standard service agreement with automatic renewal and immediate payment terms...",
  "risk_score": 55,
  "risk_level": "Medium",
  "risks": [
    {
      "category": "Renewal",
      "description": "Automatic renewal clause detected. Ensure proper opt-out procedures.",
      "severity": "Medium"
    },
    {
      "category": "Confidentiality",
      "description": "Missing confidentiality clause. No explicit data protection.",
      "severity": "High"
    },
    {
      "category": "Termination",
      "description": "Long termination notice period (60+ days). Extended exit timeline.",
      "severity": "Medium"
    }
  ],
  "answer": "Yes, this contract carries medium risk. The automatic renewal clause and missing confidentiality provisions are the main concerns. The 60-day termination notice is also restrictive."
}
```

## Responsibilities by Member

| Member | Component | Responsibility | Output |
|--------|-----------|-----------------|--------|
| 1 | PDF Parsing | Extract text from PDF | Raw text |
| 2.1 | RAG | Find relevant sections | Ranked sections |
| 1.2 | Extraction | Identify specific clauses | ClausesInput |
| **3** | **Risk Agent** | **Score risk + explain (Gemini)** | **ContractAnalysisOutput** |
| 4 | Streamlit | Display results | Web UI |

## How to Integrate Member 3

### Option A: Direct Import (Simple)
```python
# Member 4's Streamlit app
from member3 import analyze_contract

result = analyze_contract(clauses_dict, user_question)
st.write(f"Risk Level: {result.risk_level}")
st.write(f"Score: {result.risk_score}/100")
```

### Option B: Via LangGraph (Member 2's Orchestrator)
```python
# Member 2's LangGraph workflow
from member3 import analyze_contract

# In your state machine:
def risk_analysis_node(state):
    clauses = state["clauses"]  # From extraction node
    question = state["question"]
    result = analyze_contract(clauses, question)
    state["analysis"] = result.model_dump()
    return state
```

### Option C: Via REST API (Future Enhancement)
```python
# If Member 4 runs Member 3 as a microservice
response = requests.post(
    "http://risk-agent:8000/analyze",
    json={"clauses": clauses_dict, "question": question}
)
result = response.json()
```

## Setup for Gemini API

### Get Free API Key (No Credit Card Required)

1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key
4. Run: `export GEMINI_API_KEY='your-key-here'`

### Pricing

- **Gemini 1.5 Flash**: Free tier with generous limits
- Perfect for development and testing
- See: https://ai.google.dev/pricing

## Testing Member 3 Standalone

```bash
# Install dependencies
pip install -r requirements.txt

# Get free Gemini API key (no credit card)
# Visit: https://aistudio.google.com/apikey
# Click "Create API Key"
export GEMINI_API_KEY="your-key-here"

# Run example
python example_usage.py

# Or import in your own test
from member3 import analyze_contract
result = analyze_contract(test_clauses, test_question)
assert result.risk_score >= 0 and result.risk_score <= 100
```

## Troubleshooting

### Missing API Key
```
Error: "GEMINI_API_KEY not set"
Solution: 
1. Visit https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Run: export GEMINI_API_KEY='your-key-here'
```

### JSON Parsing Error
```
Error: "json.JSONDecodeError"
The LLM response wasn't valid JSON.
Solution: This is caught and handled gracefully - summary will be truncated response.
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
- **Gemini API call**: ~1-3 seconds (depends on Google's API latency)
- **Total**: ~2-4 seconds per contract

For batch processing, consider async calls or parallel processing in Member 4.

## Next Steps for Integration

1. **Member 1.2** exports ClausesInput objects
2. **Member 3** (THIS) accepts those objects + calls Gemini
3. **Member 4** receives ContractAnalysisOutput for display
4. **Member 2** coordinates the pipeline with LangGraph
