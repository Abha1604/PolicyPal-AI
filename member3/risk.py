"""
Risk calculation logic with rule-based scoring.
"""

from .schemas import ClausesInput, RiskFinding


def _is_long_termination_notice(text: str) -> bool:
    """
    Check if termination notice is considered 'long' (60+ days).
    """
    if not text:
        return False
    
    # Look for day/days patterns
    import re
    match = re.search(r'(\d+)\s*days?', text.lower())
    if match:
        days = int(match.group(1))
        return days >= 60
    return False


def calculate_risk(clauses: ClausesInput) -> dict:
    """
    Calculate risk score and risk level based on clause analysis.
    
    Scoring rules:
    - +30 if renewal clause exists
    - +20 if penalty clause exists  
    - +15 if confidentiality clause is missing
    - +10 if termination notice is long (60+ days)
    
    Args:
        clauses: ClausesInput object with parsed clauses
        
    Returns:
        dict with:
        - risk_score: int (0-100)
        - risk_level: str ("Low", "Medium", "High")
        - risks: list of RiskFinding objects
    """
    
    risk_score = 0
    risk_findings: list[RiskFinding] = []
    
    # Rule 1: Renewal clause exists (+30)
    if clauses.renewal and clauses.renewal.found:
        risk_score += 30
        risk_findings.append(
            RiskFinding(
                category="Renewal",
                description="Automatic renewal clause detected. Ensure proper opt-out procedures.",
                severity="Medium"
            )
        )
    
    # Rule 2: Penalty clause exists (+20)
    if clauses.penalty and clauses.penalty.found:
        risk_score += 20
        risk_findings.append(
            RiskFinding(
                category="Penalty",
                description="Penalty clause present. Review penalty terms carefully.",
                severity="High"
            )
        )
    
    # Rule 3: Confidentiality clause is missing (+15)
    if not clauses.confidentiality or not clauses.confidentiality.found:
        risk_score += 15
        risk_findings.append(
            RiskFinding(
                category="Confidentiality",
                description="Missing confidentiality clause. No explicit data protection.",
                severity="High"
            )
        )
    
    # Rule 4: Termination notice is long (+10)
    if clauses.termination and clauses.termination.found:
        if _is_long_termination_notice(clauses.termination.text):
            risk_score += 10
            risk_findings.append(
                RiskFinding(
                    category="Termination",
                    description="Long termination notice period (60+ days). Extended exit timeline.",
                    severity="Medium"
                )
            )
    
    # Clamp score to 0-100
    risk_score = min(100, max(0, risk_score))
    
    # Determine risk level
    if risk_score <= 33:
        risk_level = "Low"
    elif risk_score <= 66:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risks": risk_findings
    }
