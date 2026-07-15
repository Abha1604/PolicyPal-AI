"""
Explanation & Risk Agent - main module.
Combines rule-based risk scoring with LLM-generated insights using Google Gemini.
"""

import json
import os
import google.generativeai as genai

from schemas import ClausesInput, ContractAnalysisInput, ContractAnalysisOutput, RiskFinding
from risk import calculate_risk


def analyze_contract(clauses: ClausesInput | dict, question: str) -> ContractAnalysisOutput:
    """
    Analyze a contract for risks and generate explanations using Google Gemini.
    
    Args:
        clauses: ClausesInput object or dict with parsed clauses
        question: User's question about the contract
        
    Returns:
        ContractAnalysisOutput with summary, risk_score, risk_level, risks, and answer
    """
    
    # Convert dict to ClausesInput if needed
    if isinstance(clauses, dict):
        clauses = ClausesInput(**clauses)
    
    # Step 1: Calculate risk using rule-based engine
    risk_result = calculate_risk(clauses)
    risk_score = risk_result["risk_score"]
    risk_level = risk_result["risk_level"]
    risks = risk_result["risks"]
    
    # Step 2: Prepare context for LLM
    clauses_context = _format_clauses_for_llm(clauses)
    
    # Step 3: Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set.\n"
            "Get your free API key at: https://aistudio.google.com/apikey\n"
            "Then run: export GEMINI_API_KEY='your-key-here'"
        )
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")
    
    system_prompt = """You are an expert contract analyst. You will be provided with:
1. Parsed contract clauses
2. A risk assessment
3. A user question about the contract

Your task is to:
1. Write a concise executive summary (2-3 sentences) of the contract's key terms and implications
2. Answer the user's question directly and professionally

Be factual, clear, and practical. Focus on business implications.

IMPORTANT: Always respond with ONLY valid JSON (no markdown, no explanation). Format:
{
  "summary": "...",
  "answer": "..."
}"""

    user_message = f"""{system_prompt}

Contract Clauses:
{clauses_context}

Risk Assessment (calculated by rules):
- Risk Score: {risk_score}/100
- Risk Level: {risk_level}
- Identified Risks: {json.dumps([r.model_dump() for r in risks], indent=2)}

User Question: {question}

Respond ONLY as valid JSON with keys "summary" and "answer". No markdown, no code blocks, no other text."""

    response = model.generate_content(user_message)
    
    # Step 4: Parse LLM response
    response_text = response.text
    
    try:
        # Try to extract JSON from response
        # Handle case where LLM might wrap response in markdown code blocks
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text
        
        llm_output = json.loads(json_str)
        summary = llm_output.get("summary", "")
        answer = llm_output.get("answer", "")
    except (json.JSONDecodeError, IndexError, KeyError, ValueError):
        # Fallback if JSON parsing fails
        summary = response_text[:200] if len(response_text) > 200 else response_text
        answer = response_text
    
    # Step 5: Construct and return output
    return ContractAnalysisOutput(
        summary=summary,
        risk_score=risk_score,
        risk_level=risk_level,
        risks=risks,
        answer=answer
    )


def _format_clauses_for_llm(clauses: ClausesInput) -> str:
    """
    Format clauses into readable text for LLM context.
    """
    output = []
    
    for clause_name in ["payment", "renewal", "termination", "confidentiality", "penalty"]:
        clause = getattr(clauses, clause_name, None)
        if clause:
            status = "✓ FOUND" if clause.found else "✗ MISSING"
            text = clause.text if clause.text else "(empty)"
            output.append(f"{clause_name.upper()}: {status}\n  {text}")
    
    return "\n".join(output) if output else "No clauses found"
