from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime

# The "Golden Schema" - Type safety is our moat
class Charge(BaseModel):
    description: str
    severity: Literal["Felony", "Misdemeanor", "Infraction", "Unknown"]
    statute: Optional[str] = None

class Incident(BaseModel):
    report_id: str
    date: str
    subject_name: str
    narrative_summary: str
    charges: List[Charge]
    # The VLM must infer this from context
    alcohol_involved: bool = Field(..., description="True if alcohol mentioned")
    location: Optional[str] = None

class Citation(BaseModel):
    guideline: str  # e.g. "Guideline G"
    text: str
    source_paragraph: str

class AdjudicationDecision(BaseModel):
    recommendation: Literal["GRANT", "DENY", "REVOKE", "MANUAL_REVIEW"]
    risk_score: float  # Kept for backward compatibility
    citations: List[Citation]
    generated_sor: str  # Statement of Reasons
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class LegacyStatus(BaseModel):
    """Represents the dual-state of clearance status"""
    local_status: Literal["ACTIVE", "SUSPENDED", "REVOKED", "PENDING"]
    mainframe_status: Literal["ACTIVE", "SUSPENDED", "REVOKED", "PENDING", "SYNCING"]
    last_sync: Optional[str] = None
    sync_lag_hours: int = 96  # Default 4 days


if __name__ == "__main__":
    # Test the models
    print("Testing Pydantic Models...")
    
    test_incident = Incident(
        report_id="TEST-001",
        date="2024-01-15",
        subject_name="Test Subject",
        narrative_summary="Test narrative",
        charges=[
            Charge(description="Test Charge", severity="Misdemeanor", statute="TEST-123")
        ],
        alcohol_involved=False
    )
    
    print("✓ Models loaded successfully")
    print("\nSample Incident Schema:")
    print(test_incident.model_dump_json(indent=2))