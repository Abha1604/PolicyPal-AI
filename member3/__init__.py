"""
Member 3: Explanation & Risk Agent
AI Contract Review Project

Powered by Google Gemini Free API (no credit card required)

Public API:
- analyze_contract(clauses, question) → ContractAnalysisOutput
- calculate_risk(clauses) → dict
"""

from agent import analyze_contract
from risk import calculate_risk
from schemas import (
    ClauseInfo,
    ClausesInput,
    ContractAnalysisInput,
    ContractAnalysisOutput,
    RiskFinding
)

__version__ = "2.0.0"
__all__ = [
    "analyze_contract",
    "calculate_risk",
    "ClauseInfo",
    "ClausesInput",
    "ContractAnalysisInput",
    "ContractAnalysisOutput",
    "RiskFinding",
]
