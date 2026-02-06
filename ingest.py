import json
from models import Incident, Charge
from typing import Optional

# SEAD 4 Guideline Keywords (for VLM context awareness)
GUIDELINE_INDICATORS = {
    "G": ["alcohol", "drinking", "dui", "dwi", "intoxicated", "bar", "tavern"],
    "H": ["drug", "marijuana", "cocaine", "substance", "narcotic", "prescription abuse"],
    "D": ["sexual", "harassment", "misconduct", "inappropriate"],
    "J": ["assault", "battery", "violence", "fight", "threatening"],
}


def simulate_vlm_extraction(file_bytes: bytes, filename: str = "") -> Incident:
    """
    Simulates the extraction of a messy law enforcement report.
    
    In production, this would:
    1. Send image to GPT-4o-Vision API
    2. Use a structured prompt with the Incident schema
    3. Handle retries with reflexion if validation fails
    
    For the demo, we return pre-validated synthetic data.
    """
    
    # Mock Response 1: DUI Case (High severity)
    mock_dui_case = {
        "report_id": "LEA-2024-8892",
        "date": "2024-05-12",
        "subject_name": "John Doe",
        "location": "Interstate 95, Exit 42",
        "narrative_summary": (
            "Subject observed weaving across lanes at 0145 hours. "
            "Vehicle pulled over. Strong odor of alcoholic beverage detected. "
            "Field sobriety tests administered - subject failed horizontal gaze nystagmus, "
            "walk-and-turn, and one-leg stand. Refused breathalyzer. "
            "Subject stated 'I only had two beers' during questioning."
        ),
        "charges": [
            {
                "description": "Driving Under Influence of Alcohol",
                "severity": "Misdemeanor",
                "statute": "VC 23152(a)"
            },
            {
                "description": "Reckless Driving",
                "severity": "Misdemeanor", 
                "statute": "VC 23103"
            }
        ],
        "alcohol_involved": True
    }
    
    # Mock Response 2: Drug Possession (for variety)
    mock_drug_case = {
        "report_id": "LEA-2024-9103",
        "date": "2024-06-03",
        "subject_name": "Jane Smith",
        "location": "123 Main St, Apartment 4B",
        "narrative_summary": (
            "Officers executed search warrant at subject's residence. "
            "Discovered 15 grams controlled substance (marijuana) in bedroom closet. "
            "Subject admitted to personal use. No intent to distribute found. "
            "Subject cooperative during arrest."
        ),
        "charges": [
            {
                "description": "Possession of Controlled Substance",
                "severity": "Misdemeanor",
                "statute": "HS 11357"
            }
        ],
        "alcohol_involved": False
    }
    
    # Select based on filename hint, default to DUI
    if "drug" in filename.lower():
        selected_case = mock_drug_case
    else:
        selected_case = mock_dui_case
    
    return Incident(**selected_case)


def extract_guideline_flags(narrative: str) -> list[str]:
    """
    Helper function that a real VLM would use to identify
    which SEAD 4 guidelines might be relevant based on keywords.
    """
    narrative_lower = narrative.lower()
    flagged = []
    
    for guideline, keywords in GUIDELINE_INDICATORS.items():
        if any(keyword in narrative_lower for keyword in keywords):
            flagged.append(guideline)
    
    return flagged


# The actual VLM prompt (for demonstration/documentation)
VLM_SYSTEM_PROMPT = """
You are a forensic document analyst specializing in law enforcement records.
Your task is to extract structured data from scanned police reports, arrest records, 
and incident narratives - even when handwritten, crooked, or partially illegible.

CRITICAL INSTRUCTIONS:
1. Extract ALL visible charges, even if handwritten in margins
2. Infer alcohol involvement from context clues (odor, FST, breathalyzer, statements)
3. Preserve verbatim quotes from officers when present
4. If a field is unclear, mark as "Unknown" rather than guessing
5. Return ONLY valid JSON matching the Incident schema

OUTPUT FORMAT:
{
  "report_id": "string",
  "date": "YYYY-MM-DD",
  "subject_name": "string",
  "narrative_summary": "string",
  "charges": [...],
  "alcohol_involved": boolean
}

FAIL SAFE: If you cannot extract enough data, return:
{"error": "INSUFFICIENT_DATA", "reason": "..."}
"""


if __name__ == "__main__":
    # Test extraction
    print("Testing VLM Extraction...")
    
    test_data = simulate_vlm_extraction(b"fake_bytes", "test_dui_report.pdf")
    print(f"\n✓ Extracted Incident: {test_data.report_id}")
    print(f"  Subject: {test_data.subject_name}")
    print(f"  Charges: {len(test_data.charges)}")
    print(f"  Alcohol: {test_data.alcohol_involved}")
    
    flags = extract_guideline_flags(test_data.narrative_summary)
    print(f"  Flagged Guidelines: {flags}")