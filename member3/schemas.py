"""
Pydantic schemas for contract risk analysis.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class ClauseInfo(BaseModel):
    """Individual clause information."""
    found: bool
    text: str = ""


class ClausesInput(BaseModel):
    """Input clauses from previous stages (PDF parsing, extraction)."""
    payment: Optional[ClauseInfo] = None
    renewal: Optional[ClauseInfo] = None
    termination: Optional[ClauseInfo] = None
    confidentiality: Optional[ClauseInfo] = None
    penalty: Optional[ClauseInfo] = None
    
    class Config:
        extra = "allow"  # Allow additional clauses


class ContractAnalysisInput(BaseModel):
    """Input to the analysis agent."""
    clauses: ClausesInput
    question: str


class RiskFinding(BaseModel):
    """A single risk finding."""
    category: str
    description: str
    severity: str  # "Low", "Medium", "High"


class ContractAnalysisOutput(BaseModel):
    """Output from the analysis agent."""
    summary: str = Field(..., description="Executive summary of the contract")
    risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100")
    risk_level: str = Field(..., description="Risk level: Low/Medium/High")
    risks: List[RiskFinding] = Field(default_factory=list, description="List of identified risks")
    answer: str = Field(..., description="Answer to the user's question")
