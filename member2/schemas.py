"""
schemas.py
----------
Pydantic models defining the Structured Contract Model produced by
Agent 1 (Contract Intelligence Agent).

This schema is the "contract" (pun intended) between Agent 1 and the
rest of the system — Agent 2 (Risk & Explanation), the RAG pipeline,
and the UI all consume this exact shape. Keep it stable; if it must
change, coordinate with the whole team since Members 3, 4, and 5 all
depend on it.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums — constrain the model to a known, finite vocabulary wherever possible.
# This makes downstream logic (e.g. Agent 2's risk rules, UI badges) reliable
# instead of having to string-match freeform LLM text.
# ---------------------------------------------------------------------------

class ContractType(str, Enum):
    RENTAL_AGREEMENT = "Rental Agreement"
    EMPLOYMENT_CONTRACT = "Employment Contract"
    LOAN_AGREEMENT = "Loan Agreement"
    SERVICE_AGREEMENT = "Service Agreement"
    INSURANCE_POLICY = "Insurance Policy"
    VENDOR_CONTRACT = "Vendor Contract"
    SUBSCRIPTION_CONTRACT = "Subscription Contract"
    TERMS_AND_CONDITIONS = "Terms & Conditions"
    OTHER = "Other"


class ClauseType(str, Enum):
    PAYMENT_TERMS = "Payment Terms"
    TERMINATION = "Termination"
    RENEWAL = "Renewal"
    PENALTIES = "Penalties"
    CONFIDENTIALITY = "Confidentiality"
    LIABILITY = "Liability"
    INDEMNIFICATION = "Indemnification"
    REFUNDS = "Refunds"
    WARRANTIES = "Warranties"
    INTELLECTUAL_PROPERTY = "Intellectual Property"
    NON_COMPETE = "Non-Compete"
    DISPUTE_RESOLUTION = "Dispute Resolution"
    GOVERNING_LAW = "Governing Law"
    ARBITRATION = "Arbitration"
    DATA_PRIVACY = "Data Privacy"
    OTHER = "Other"


class DateType(str, Enum):
    START_DATE = "start_date"
    EXPIRATION_DATE = "expiration_date"
    PAYMENT_DUE_DATE = "payment_due_date"
    RENEWAL_DEADLINE = "renewal_deadline"
    NOTICE_PERIOD = "notice_period"
    TERMINATION_DEADLINE = "termination_deadline"
    OTHER = "other"


class FinancialObligationType(str, Enum):
    MONTHLY_RENT = "monthly_rent"
    SECURITY_DEPOSIT = "security_deposit"
    LATE_PAYMENT_PENALTY = "late_payment_penalty"
    EARLY_TERMINATION_FEE = "early_termination_fee"
    SALARY = "salary"
    TRAINING_COST_RECOVERY = "training_cost_recovery"
    PREMIUM = "premium"
    LOAN_AMOUNT = "loan_amount"
    INTEREST_RATE = "interest_rate"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Core structural pieces
# ---------------------------------------------------------------------------

class Party(BaseModel):
    name: str = Field(..., description="Name of the party as it appears in the contract, e.g. 'Party A' or the actual named entity if given.")
    role: str = Field(..., description="Role of the party, e.g. 'Landlord', 'Tenant', 'Employer', 'Employee'.")


class ImportantDate(BaseModel):
    type: DateType

    value: str = Field(
        ...,
        description="Date exactly as written in the contract."
    )

    normalized_value: Optional[str] = Field(
        default=None,
        description="ISO format date (YYYY-MM-DD) if it can be determined."
    )

    source_section: str = Field(
        ...,
        description="Section where the date was found."
    )

class FinancialObligation(BaseModel):
    type: FinancialObligationType

    amount: str = Field(
        ...,
        description="Amount exactly as written in the contract."
    )

    currency: Optional[str] = Field(
        default=None,
        description="Currency code if identifiable, e.g. INR, USD."
    )

    frequency: Optional[str] = Field(
        default=None,
        description="monthly, yearly, one-time, weekly etc."
    )

    responsible_party: str = Field(
        ...,
        description="Party responsible for the payment."
    )

    source_section: str


class Clause(BaseModel):
    clause_type: ClauseType

    original_text: str = Field(
        ...,
        description="Exact wording from the contract."
    )

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Model confidence between 0 and 1."
    )

    source_section: str


class PartyObligation(BaseModel):
    party: str

    obligation: str

    mandatory: bool = Field(
        default=True,
        description="Whether the obligation is mandatory."
    )

    source_section: str


class StructuredContract(BaseModel):
    """
    Top-level output of Agent 1. This is what gets handed to Agent 2,
    stored for the report, and referenced by the RAG pipeline for
    cross-checking answers against structured facts.
    """
    contract_type: ContractType
    parties: List[Party]
    important_dates: List[ImportantDate] = Field(default_factory=list)
    financial_obligations: List[FinancialObligation] = Field(default_factory=list)
    party_obligations: List[PartyObligation] = Field(default_factory=list)
    clauses: List[Clause] = Field(default_factory=list)
    document_language: Optional[str] = "English"
    schema_version: str = "1.1"
    summary: Optional[str] = Field(
     default=None,
     description="Short summary of the agreement."
)
    class Config:
        use_enum_values = True