# Quick Start Guide - Member 3 with Google Gemini

## ✨ What Changed

✅ **Now uses Google Gemini Free API**
- No cost (free tier with generous limits)
- No credit card required
- Simple setup (3 steps)

## 🚀 Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Free Gemini API Key
```bash
# Visit: https://aistudio.google.com/apikey
# Click "Create API Key"
# Copy the key and run:
export GEMINI_API_KEY="your-key-here"
```

### Step 3: Test It Works
```bash
python example_usage.py
```

Done! ✓

## 📚 Usage

### Simple Import
```python
from member3 import analyze_contract

result = analyze_contract(clauses_dict, question)
print(result.model_dump_json(indent=2))
```

### For Streamlit (Member 4)
```python
import streamlit as st
from member3 import analyze_contract

clauses = st.session_state.clauses
question = st.text_input("Your question:")

if st.button("Analyze"):
    result = analyze_contract(clauses, question)
    st.write(f"Risk: {result.risk_level}")
    st.metric("Score", f"{result.risk_score}/100")
    st.write(result.answer)
```

## 🔑 Gemini API Key

### Get It
1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy and set: `export GEMINI_API_KEY="..."`

### Pricing
- **Free tier**: Generous limits for development
- See details: https://ai.google.dev/pricing

### Why Gemini?
- ✅ Free (no credit card)
- ✅ No API key management required
- ✅ Perfect for MVP/testing
- ✅ Easy to swap to Claude/OpenAI later

## 📋 Input/Output

### Input
```python
{
    "clauses": {
        "payment": {"found": True, "text": "..."},
        "renewal": {"found": True, "text": "..."},
        "termination": {"found": True, "text": "..."},
        "confidentiality": {"found": False, "text": ""},
        "penalty": {"found": False, "text": ""}
    },
    "question": "Is this contract risky?"
}
```

### Output
```json
{
    "summary": "...",
    "risk_score": 55,
    "risk_level": "Medium",
    "risks": [...],
    "answer": "..."
}
```

## ❓ Troubleshooting

### "GEMINI_API_KEY not set"
```bash
# Get key from https://aistudio.google.com/apikey
export GEMINI_API_KEY="your-key"
```

### "Invalid JSON response"
The module handles this automatically. No action needed.

### "Validation error"
Ensure clauses follow the schema (found: bool, text: str)

## 📊 How It Works

```
Your Data
    ↓
[Risk Scoring] ← Python (fast, deterministic)
    ↓
[Gemini LLM] ← For summary & answer
    ↓
Structured JSON Output
    ↓
Your App
```

## ✅ Testing

Run tests anytime:
```bash
python test_validation.py
```

All test cases pass ✓

## 📂 Files

| File | Purpose |
|------|---------|
| `agent.py` | Main orchestrator (Gemini) |
| `risk.py` | Rule-based scoring (Python) |
| `schemas.py` | Data validation (Pydantic) |
| `__init__.py` | Package exports |
| `requirements.txt` | Dependencies |
| `README.md` | Full documentation |
| `INTEGRATION.md` | Architecture guide |
| `example_usage.py` | Demo script |
| `test_validation.py` | Test suite |

## 🎯 For Each Member

**Member 4 (Streamlit):**
```python
from member3 import analyze_contract
result = analyze_contract(clauses, question)
```

**Member 2 (LangGraph):**
```python
# As a node in your workflow
result = analyze_contract(state["clauses"], state["question"])
state["analysis"] = result.model_dump()
```

## 💡 Pro Tips

1. **Set API key once**: `export GEMINI_API_KEY="..."`
2. **Use dict or object**: Works with both dicts and ClausesInput
3. **Error handling**: Module gracefully handles API errors
4. **Free tier limits**: ~60 requests/minute (plenty for testing)

## 🔄 Can I Switch APIs Later?

Yes! Member 3 is designed to be LLM-agnostic:
- Currently: Google Gemini
- Easy to swap: Claude, OpenAI, etc.
- Just update `agent.py`

## 📞 Questions?

See `README.md` for detailed documentation.
See `INTEGRATION.md` for architecture details.
