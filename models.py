from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# The "Golden Schema" - Type safety is our moat
class Charge(BaseModel):
    description: str
    severity: Literal["Felony", "Misdemeanor", "Infraction", "Unknown"]
    statute: Optional[str]

class Incident(BaseModel):
    report_id: str
    date: str
    subject_name: str
    narrative_summary: str
    charges: List[Charge]
    # The VLM must infer this from context
    alcohol_involved: bool = Field(..., description="True if alcohol mentioned")

class Citation(BaseModel):
    guideline: str  # e.g. "Guideline G"
    text: str
    source_paragraph: str

class AdjudicationDecision(BaseModel):
    recommendation: Literal["GRANT", "DENY", "REVOKE", "MANUAL_REVIEW"]
    risk_score: float # Kept for backward compatibility
    citations: List[Citation]
    generated_sor: str # Statement of Reasons