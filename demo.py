#!/usr/bin/env python3
"""
ClearanceOS Prototype - Standalone Demo
Runs without external dependencies (no Streamlit, Pydantic, etc.)
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Literal


# ============================================================================
# DOMAIN MODELS (Pure Python - No Pydantic)
# ============================================================================

class Charge:
    def __init__(self, description: str, severity: str, statute: Optional[str] = None):
        self.description = description
        self.severity = severity  # Felony, Misdemeanor, Infraction, Unknown
        self.statute = statute
    
    def to_dict(self):
        return {
            "description": self.description,
            "severity": self.severity,
            "statute": self.statute
        }


class Incident:
    def __init__(self, report_id: str, date: str, subject_name: str,
                 narrative_summary: str, charges: List[Charge], 
                 alcohol_involved: bool, location: Optional[str] = None):
        self.report_id = report_id
        self.date = date
        self.subject_name = subject_name
        self.narrative_summary = narrative_summary
        self.charges = charges
        self.alcohol_involved = alcohol_involved
        self.location = location
    
    def to_dict(self):
        return {
            "report_id": self.report_id,
            "date": self.date,
            "subject_name": self.subject_name,
            "narrative_summary": self.narrative_summary,
            "charges": [c.to_dict() for c in self.charges],
            "alcohol_involved": self.alcohol_involved,
            "location": self.location
        }


class Citation:
    def __init__(self, guideline: str, text: str, source_paragraph: str):
        self.guideline = guideline
        self.text = text
        self.source_paragraph = source_paragraph
    
    def to_dict(self):
        return {
            "guideline": self.guideline,
            "text": self.text,
            "source_paragraph": self.source_paragraph
        }


class AdjudicationDecision:
    def __init__(self, recommendation: str, risk_score: float, 
                 citations: List[Citation], generated_sor: str):
        self.recommendation = recommendation
        self.risk_score = risk_score
        self.citations = citations
        self.generated_sor = generated_sor
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "recommendation": self.recommendation,
            "risk_score": self.risk_score,
            "citations": [c.to_dict() for c in self.citations],
            "generated_sor": self.generated_sor,
            "timestamp": self.timestamp
        }


# ============================================================================
# VLM INGESTION SIMULATION
# ============================================================================

def simulate_vlm_extraction(filename: str = "dui_report.pdf") -> Incident:
    """Simulates VLM extraction from a scanned police report"""
    
    print(f"🤖 VLM Agent processing: {filename}")
    print("   - Reading pixel data...")
    time.sleep(0.5)
    print("   - Detecting text regions...")
    time.sleep(0.5)
    print("   - Extracting structured data...")
    time.sleep(0.5)
    
    # Mock DUI case
    charges = [
        Charge("Driving Under Influence of Alcohol", "Misdemeanor", "VC 23152(a)"),
        Charge("Reckless Driving", "Misdemeanor", "VC 23103")
    ]
    
    incident = Incident(
        report_id="LEA-2024-8892",
        date="2024-05-12",
        subject_name="John Doe",
        location="Interstate 95, Exit 42",
        narrative_summary=(
            "Subject observed weaving across lanes at 0145 hours. "
            "Vehicle pulled over. Strong odor of alcoholic beverage detected. "
            "Field sobriety tests administered - subject failed horizontal gaze nystagmus, "
            "walk-and-turn, and one-leg stand. Refused breathalyzer. "
            "Subject stated 'I only had two beers' during questioning."
        ),
        charges=charges,
        alcohol_involved=True
    )
    
    print("✅ Extraction complete!\n")
    return incident


# ============================================================================
# RAG KNOWLEDGE BASE
# ============================================================================

SEAD4_GUIDELINES = {
    "G": {
        "title": "Guideline G: Alcohol Consumption",
        "concern": (
            "Excessive alcohol consumption often leads to the exercise of questionable judgment "
            "or the failure to control impulses, and can raise questions about an individual's "
            "reliability and trustworthiness."
        ),
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 21"
    },
    "J": {
        "title": "Guideline J: Criminal Conduct",
        "concern": (
            "Criminal activity creates doubt about a person's judgment, reliability, and "
            "trustworthiness. By its very nature, it calls into question a person's ability "
            "or willingness to comply with laws, rules, and regulations."
        ),
        "citation": "SEAD 4, Adjudicative Guidelines, Paragraph 30"
    }
}


# ============================================================================
# ADJUDICATION ENGINE
# ============================================================================

class AdjudicationEngine:
    """Deterministic rule engine for clearance decisions"""
    
    def adjudicate_case(self, incident: Incident) -> AdjudicationDecision:
        print("⚖️  Adjudication Engine processing...")
        time.sleep(0.5)
        
        citations = []
        risk_score = 0.0
        reasoning_parts = []
        
        # Rule Set A: Alcohol Detection
        if incident.alcohol_involved:
            print("   - Flagged: Guideline G (Alcohol Consumption)")
            citations.append(Citation(
                guideline="Guideline G",
                text=SEAD4_GUIDELINES["G"]["concern"][:150] + "...",
                source_paragraph=SEAD4_GUIDELINES["G"]["citation"]
            ))
            risk_score += 2.0
            reasoning_parts.append(
                f"Alcohol involvement detected in incident dated {incident.date}."
            )
        
        # Rule Set B: Criminal Charges
        has_felony = any(c.severity == "Felony" for c in incident.charges)
        has_misdemeanor = any(c.severity == "Misdemeanor" for c in incident.charges)
        
        if has_felony or len(incident.charges) > 1:
            print("   - Flagged: Guideline J (Criminal Conduct)")
            citations.append(Citation(
                guideline="Guideline J",
                text=SEAD4_GUIDELINES["J"]["concern"][:150] + "...",
                source_paragraph=SEAD4_GUIDELINES["J"]["citation"]
            ))
            risk_score += 3.0 if has_felony else 2.0
            reasoning_parts.append(
                f"Subject faces {len(incident.charges)} charge(s), "
                f"including {incident.charges[0].description}."
            )
        
        # Decision Logic
        if risk_score >= 4.0:
            recommendation = "REVOKE"
            reasoning_parts.append(
                "Risk threshold exceeded. Immediate revocation recommended."
            )
        elif risk_score >= 2.0:
            recommendation = "MANUAL_REVIEW"
            reasoning_parts.append(
                "Case requires Subject Interview per SOP-101 and adjudicator review."
            )
        else:
            recommendation = "GRANT"
            reasoning_parts.append("No disqualifying information found.")
        
        # Generate Statement of Reasons
        sor = self._generate_sor(incident, reasoning_parts, citations)
        
        print(f"✅ Decision: {recommendation}\n")
        
        return AdjudicationDecision(
            recommendation=recommendation,
            risk_score=min(risk_score, 10.0),
            citations=citations,
            generated_sor=sor
        )
    
    def _generate_sor(self, incident: Incident, reasoning: List[str], 
                      citations: List[Citation]) -> str:
        """Generate formal Statement of Reasons"""
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
        footer += reasoning[-1]
        
        return header + body + footer


# ============================================================================
# ANTI-CORRUPTION LAYER
# ============================================================================

class AntiCorruptionLayer:
    """Manages dual-state sync between modern and legacy systems"""
    
    def __init__(self):
        self.pending_queue = []
        self.sync_lag_hours = 96  # 4 days
    
    def publish_decision(self, subject_id: str, decision: AdjudicationDecision):
        """Publish to local cache and queue for legacy sync"""
        status_map = {
            "GRANT": "ACTIVE",
            "DENY": "PENDING",
            "REVOKE": "REVOKED",
            "MANUAL_REVIEW": "SUSPENDED"
        }
        
        local_status = status_map.get(decision.recommendation, "PENDING")
        
        print("🔄 Anti-Corruption Layer:")
        print(f"   - Local Status: {local_status} (Immediate)")
        print(f"   - Mainframe Status: ACTIVE (Pending batch sync)")
        print(f"   - Sync Lag: {self.sync_lag_hours} hours")
        
        self.pending_queue.append({
            "subject_id": subject_id,
            "local_status": local_status,
            "queued_at": datetime.now().isoformat()
        })
        
        return local_status
    
    def force_sync(self, subject_id: str):
        """Simulate forced SOAP sync to legacy mainframe"""
        print("\n📡 Forcing legacy sync...")
        print("   - Generating SOAP/XML envelope...")
        time.sleep(0.5)
        print("   - Transmitting to NBIS mainframe...")
        time.sleep(1.0)
        print("   - Waiting for acknowledgment...")
        time.sleep(0.5)
        print("✅ Mainframe synchronized!\n")


# ============================================================================
# MAIN DEMO
# ============================================================================

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def run_demo():
    print_separator("ClearanceOS Prototype v0.1 - Automated Adjudication")
    print("Demonstrating VLM-Driven Ingestion + SEAD 4 Adjudication")
    print("Trusted Workforce 2.0 / Continuous Vetting Demo\n")
    
    # Phase 1: Ingestion
    print_separator("PHASE 1: VLM Ingestion")
    incident = simulate_vlm_extraction("arrest_report_scanned.pdf")
    
    print("📊 Extracted Data:")
    print(f"   Report ID: {incident.report_id}")
    print(f"   Subject: {incident.subject_name}")
    print(f"   Date: {incident.date}")
    print(f"   Location: {incident.location}")
    print(f"   Alcohol Involved: {'Yes' if incident.alcohol_involved else 'No'}")
    print(f"\n   Charges ({len(incident.charges)}):")
    for i, charge in enumerate(incident.charges, 1):
        print(f"     {i}. [{charge.severity}] {charge.description}")
        print(f"        Statute: {charge.statute}")
    print(f"\n   Narrative:")
    print(f"   {incident.narrative_summary[:200]}...")
    
    # Phase 2: Adjudication
    print_separator("PHASE 2: Adjudication & Legal Analysis")
    engine = AdjudicationEngine()
    decision = engine.adjudicate_case(incident)
    
    print("🎯 Decision Summary:")
    print(f"   Recommendation: {decision.recommendation}")
    print(f"   Risk Score: {decision.risk_score}/10.0")
    print(f"   Timestamp: {decision.timestamp}")
    
    print(f"\n📚 Legal Citations ({len(decision.citations)}):")
    for cit in decision.citations:
        print(f"   • {cit.guideline}")
        print(f"     {cit.text}")
        print(f"     Source: {cit.source_paragraph}\n")
    
    print("📋 Statement of Reasons:")
    print("-" * 70)
    print(decision.generated_sor)
    print("-" * 70)
    
    # Phase 3: Legacy Integration
    print_separator("PHASE 3: Legacy System Integration (ACL)")
    acl = AntiCorruptionLayer()
    subject_id = "SUBJ-12345"
    acl.publish_decision(subject_id, decision)
    
    print("\n⏳ Simulating batch processing delay...")
    print("   (In production, this would be a 96-hour nightly batch job)")
    
    input("\nPress ENTER to force immediate sync (simulate emergency update)...")
    acl.force_sync(subject_id)
    
    # Summary
    print_separator("DEMO COMPLETE")
    print("Key Takeaways:")
    print("✓ VLM extracts structured data from unstructured documents")
    print("✓ RAG provides legal citations from SEAD 4 guidelines")
    print("✓ Deterministic engine ensures consistent decisions")
    print("✓ ACL manages the real-time vs. legacy batch gap")
    print("\nThis prototype demonstrates technical feasibility.")
    print("Production deployment would require:")
    print("  - Real OpenAI API integration")
    print("  - Vector database (ChromaDB/Pinecone)")
    print("  - NBIS SOAP endpoint integration")
    print("  - FedRAMP compliance\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()