import os

from member2.contract_intelligence_agent import (
    ContractIntelligenceAgent,
    GeminiClient,
)
from member3.agent import analyze_contract
from rag.pdf_loader import extract_text_from_pdf

STANDARD_CLAUSE_CHECKS = [
    ("Payment", ["payment"]),
    ("Renewal", ["renewal"]),
    ("Termination", ["termination"]),
    ("Confidentiality", ["confidentiality"]),
    ("Penalties", ["penalt"]),
]

ANALYSIS_DEFAULT_QUESTIONS = {
    "Full Analysis": "Summarize this contract and highlight the most important terms.",
    "Risk Detection": "What are the key risks and red flags in this contract?",
    "Compliance Review": "What compliance issues, regulatory gaps, or missing standard clauses exist?",
}


def extract_text_from_document(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    if ext == ".txt":
        with open(file_path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        return {
            "filename": os.path.basename(file_path),
            "num_pages": 1,
            "text": text,
        }

    if ext == ".docx":
        try:
            from docx import Document
        except ImportError as e:
            raise ValueError(
                "DOCX support requires python-docx. Install it with: pip install python-docx"
            ) from e

        document = Document(file_path)
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        return {
            "filename": os.path.basename(file_path),
            "num_pages": None,
            "text": "\n".join(paragraphs),
        }

    raise ValueError(f"Unsupported file type: {ext or 'unknown'}")


def convert_to_member3_format(structured_contract) -> dict:
    clauses = {}

    for clause in structured_contract.clauses:
        clause_type = str(clause.clause_type).lower()

        if "payment" in clause_type:
            key = "payment"
        elif "renewal" in clause_type:
            key = "renewal"
        elif "termination" in clause_type:
            key = "termination"
        elif "confidentiality" in clause_type:
            key = "confidentiality"
        elif "penalt" in clause_type:
            key = "penalty"
        else:
            continue

        clauses[key] = {
            "found": True,
            "text": clause.original_text,
        }

    return clauses


def get_standard_clause_status(structured_contract) -> list[dict]:
    results = []

    for label, keywords in STANDARD_CLAUSE_CHECKS:
        matched = [
            clause
            for clause in structured_contract.clauses
            if any(keyword in str(clause.clause_type).lower() for keyword in keywords)
        ]
        results.append(
            {
                "label": label,
                "found": bool(matched),
                "clauses": matched,
            }
        )

    return results


def resolve_question(question: str, analysis_type: str) -> str:
    cleaned = (question or "").strip()
    if cleaned:
        return cleaned
    return ANALYSIS_DEFAULT_QUESTIONS.get(
        analysis_type,
        ANALYSIS_DEFAULT_QUESTIONS["Full Analysis"],
    )


def analyze_document(file_path: str, question: str, analysis_type: str = "Full Analysis"):
    doc_data = extract_text_from_document(file_path)
    contract_text = doc_data["text"]

    if not contract_text.strip():
        raise ValueError("No readable text found in the uploaded document.")

    agent1 = ContractIntelligenceAgent(GeminiClient())
    structured_contract = agent1.analyze(contract_text)

    member3_input = convert_to_member3_format(structured_contract)
    resolved_question = resolve_question(question, analysis_type)
    include_llm = analysis_type != "Clause Extraction"

    analysis = analyze_contract(
        clauses=member3_input,
        question=resolved_question,
        include_llm=include_llm,
    )

    metadata = {
        "filename": doc_data["filename"],
        "num_pages": doc_data.get("num_pages"),
        "analysis_type": analysis_type,
        "question": resolved_question,
    }

    return structured_contract, analysis, metadata


# Backward-compatible alias
def analyze_pdf(pdf_path, question):
    structured_contract, analysis, _metadata = analyze_document(
        pdf_path,
        question,
        analysis_type="Full Analysis",
    )
    return structured_contract, analysis
