import json
from models import Incident

# SIMULATION: In a real app, this calls GPT-4o-Vision
def simulate_vlm_extraction(file_bytes):
    """
    Simulates the extraction of a messy DUI report.
    Returns a valid Incident object.
    """
    # This represents the "Cleaned" data from a "Dirty" source
    mock_response = {
        "report_id": "LEA-2024-8892",
        "date": "2024-05-12",
        "subject_name": "John Doe",
        "narrative_summary": "Subject observed weaving across lanes. FST administered. Failed.",
        "charges": [
            {"description": "Driving Under Influence", "severity": "Misdemeanor", "statute": "VC 23152(a)"},
            {"description": "Reckless Driving", "severity": "Misdemeanor", "statute": "VC 23103"}
        ],
        "alcohol_involved": True
    }
    return Incident(**mock_response)