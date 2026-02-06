from models import Incident, AdjudicationDecision, Citation
from rag import search_guidelines, get_guideline
from typing import List


class AdjudicationEngine:
    """
    The Deterministic Rule Engine.
    This is NOT an AI - it's pure IF/THEN logic based on SEAD 4 rules.
    """
    
    # Severity weights for risk scoring
    SEVERITY_WEIGHTS = {
        "Felony": 3.0,
        "Misdemeanor": 2.0,
        "Infraction": 1.0,
        "Unknown": 1.5
    }
    
    def __init__(self):
        self.decision_log = []
    
    def adjudicate_case(self, incident: Incident) -> AdjudicationDecision:
        """
        Main adjudication function.
        Returns a decision with legal citations.
        """
        citations = []
        recommendation = "GRANT"
        risk_score = 0.0
        reasoning_parts = []
        
        # Step 1: RAG Retrieval - Find relevant guidelines
        relevant_guidelines = self._retrieve_guidelines(incident)
        
        # Step 2: Apply Deterministic Rules
        # Rule Set A: Alcohol-Related Offenses
        if incident.alcohol_involved:
            guideline_g = get_guideline("G")
            citations.append(Citation(
                guideline="Guideline G",
                text=guideline_g["concern"][:150] + "...",
                source_paragraph=guideline_g["citation"]
            ))
            risk_score += 2.0
            reasoning_parts.append(
                f"Alcohol involvement detected in incident dated {incident.date}."
            )
        
        # Rule Set B: Criminal Charges Severity
        has_felony = any(c.severity == "Felony" for c in incident.charges)
        has_misdemeanor = any(c.severity == "Misdemeanor" for c in incident.charges)
        
        if has_felony or len(incident.charges) > 1:
            guideline_j = get_guideline("J")
            citations.append(Citation(
                guideline="Guideline J",
                text=guideline_j["concern"][:150] + "...",
                source_paragraph=guideline_j["citation"]
            ))
            risk_score += 3.0 if has_felony else 2.0
            reasoning_parts.append(
                f"Subject faces {len(incident.charges)} charge(s), "
                f"including {incident.charges[0].description}."
            )
        
        # Rule Set C: Decision Logic (The "Judge")
        if risk_score >= 4.0:
            recommendation = "REVOKE"
            reasoning_parts.append(
                "Risk threshold exceeded. Immediate revocation recommended pending investigation."
            )
        elif risk_score >= 2.0:
            recommendation = "MANUAL_REVIEW"
            reasoning_parts.append(
                "Case requires Subject Interview per SOP-101 and adjudicator review."
            )
        elif risk_score > 0:
            recommendation = "DENY"
            reasoning_parts.append(
                "Derogatory information present. Clearance application denied."
            )
        else:
            recommendation = "GRANT"
            reasoning_parts.append("No disqualifying information found.")
        
        # Step 3: Generate Statement of Reasons (SOR)
        sor = self._generate_sor(incident, reasoning_parts, citations)
        
        # Step 4: Construct Decision Object
        decision = AdjudicationDecision(
            recommendation=recommendation,
            risk_score=min(risk_score, 10.0),  # Cap at 10
            citations=citations,
            generated_sor=sor
        )
        
        # Log for audit trail
        self.decision_log.append({
            "incident_id": incident.report_id,
            "decision": recommendation,
            "timestamp": decision.timestamp
        })
        
        return decision
    
    def _retrieve_guidelines(self, incident: Incident) -> List[str]:
        """Use RAG to find relevant SEAD 4 guidelines"""
        # Build search query from incident
        query_parts = [incident.narrative_summary]
        query_parts.extend([c.description for c in incident.charges])
        
        search_query = " ".join(query_parts)
        results = search_guidelines(search_query)
        
        return [r["guideline"] for r in results]
    
    def _generate_sor(
        self, 
        incident: Incident, 
        reasoning: List[str], 
        citations: List[Citation]
    ) -> str:
        """
        Generate a formal Statement of Reasons.
        This mimics the legal language required for adjudication decisions.
        """
        header = f"STATEMENT OF REASONS\n"
        header += f"Subject: {incident.subject_name}\n"
        header += f"Incident Reference: {incident.report_id}\n"
        header += f"Date of Incident: {incident.date}\n\n"
        
        body = "FINDINGS:\n"
        for i, reason in enumerate(reasoning, 1):
            body += f"{i}. {reason}\n"
        
        if citations:
            body += "\nLEGAL BASIS:\n"
            for cit in citations:
                body += f"• {cit.guideline} ({cit.source_paragraph})\n"
        
        footer = "\nRECOMMENDATION:\n"
        footer += f"Based on the above findings, this case is classified for {reasoning[-1]}"
        
        return header + body + footer


# Convenience function for backward compatibility
def adjudicate_case(incident: Incident) -> AdjudicationDecision:
    """Legacy function - instantiates engine and runs adjudication"""
    engine = AdjudicationEngine()
    return engine.adjudicate_case(incident)


if __name__ == "__main__":
    from ingest import simulate_vlm_extraction
    
    print("Testing Adjudication Engine...")
    
    # Test with mock incident
    test_incident = simulate_vlm_extraction(b"fake", "test_dui.pdf")
    
    engine = AdjudicationEngine()
    decision = engine.adjudicate_case(test_incident)
    
    print(f"\n✓ Decision: {decision.recommendation}")
    print(f"  Risk Score: {decision.risk_score}/10")
    print(f"  Citations: {len(decision.citations)}")
    print(f"\nGenerated SOR Preview:")
    print("=" * 60)
    print(decision.generated_sor[:300] + "...")