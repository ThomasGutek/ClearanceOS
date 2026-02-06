from models import Incident, AdjudicationDecision, Citation

def adjudicate_case(incident: Incident) -> AdjudicationDecision:
    citations = []
    recommendation = "GRANT"
    sor_text = "No derogatory information found."

    # 1. RAG Step (Simulated Retrieval)
    if incident.alcohol_involved:
        citations.append(Citation(
            guideline="Guideline G",
            text="Alcohol consumption creates doubt about a person's judgment...",
            source_paragraph="SEAD 4, Para 21"
        ))
    
    # 2. Deterministic Logic Step (The "Code", not the AI)
    # Rule: If Alcohol + Misdemeanor -> Manual Review
    if incident.alcohol_involved and any(c.severity == "Misdemeanor" for c in incident.charges):
        recommendation = "MANUAL_REVIEW"
        sor_text = (
            f"Subject {incident.subject_name} flagged for Guideline G (Alcohol). "
            f"Incident on {incident.date} involves {len(incident.charges)} charges. "
            "Requires Subject Interview per SOP-101."
        )

    return AdjudicationDecision(
        recommendation=recommendation,
        risk_score=0.75, # Arbitrary, we don't rely on it
        citations=citations,
        generated_sor=sor_text
    )