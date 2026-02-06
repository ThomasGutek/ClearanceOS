"""
This module generates a mock "scanned" police report PDF for demo purposes.
Uses reportlab to create a realistic-looking document.
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import io
    
    def generate_mock_police_report(output_path: str = "data/arrest_report_scanned.pdf"):
        """
        Creates a fake police report PDF that looks like a scanned document.
        """
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Simulate "scanned" effect with slight rotation
        c.rotate(0.5)
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 80, "METROPOLITAN POLICE DEPARTMENT")
        c.setFont("Helvetica", 10)
        c.drawString(100, height - 100, "Incident Report - Confidential")
        
        # Report Details
        y = height - 140
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y, "Report ID: LEA-2024-8892")
        
        y -= 25
        c.setFont("Helvetica", 11)
        c.drawString(80, y, "Date of Incident: May 12, 2024")
        c.drawString(350, y, "Time: 01:45 Hours")
        
        y -= 20
        c.drawString(80, y, "Location: Interstate 95, Exit 42")
        
        y -= 20
        c.drawString(80, y, "Subject Name: JOHN DOE")
        c.drawString(350, y, "DOB: 03/15/1985")
        
        # Narrative Section
        y -= 40
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y, "NARRATIVE:")
        
        y -= 25
        c.setFont("Helvetica", 10)
        narrative = [
            "At approximately 0145 hours, I observed a vehicle (2018 Honda Accord, License",
            "Plate: ABC-1234) weaving across lanes on Interstate 95 northbound near Exit 42.",
            "",
            "I initiated a traffic stop. Upon approach, I detected a strong odor of alcoholic",
            "beverage emanating from the vehicle. Subject's eyes appeared bloodshot and watery.",
            "",
            "Field Sobriety Tests administered:",
            "  - Horizontal Gaze Nystagmus: FAILED",
            "  - Walk and Turn: FAILED (subject unable to maintain balance)",
            "  - One Leg Stand: FAILED",
            "",
            "Subject refused preliminary breathalyzer test. During questioning, subject stated",
            "\"I only had two beers at dinner.\" Subject arrested for suspicion of DUI.",
        ]
        
        for line in narrative:
            c.drawString(100, y, line)
            y -= 15
        
        # Charges Section
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y, "CHARGES:")
        
        y -= 25
        c.setFont("Helvetica", 10)
        c.drawString(100, y, "1. Driving Under Influence of Alcohol (VC 23152(a)) - Misdemeanor")
        y -= 18
        c.drawString(100, y, "2. Reckless Driving (VC 23103) - Misdemeanor")
        
        # Officer signature area (simulated handwriting)
        y -= 60
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(80, y, "Officer: J. Martinez #4521")
        c.drawString(350, y, "Badge: 4521")
        
        y -= 20
        c.drawString(80, y, "Signature: ____[scribbled signature]____")
        
        # Footer
        c.setFont("Helvetica", 8)
        c.drawString(80, 50, "This is a synthetic document created for demonstration purposes.")
        c.drawString(80, 38, "CONFIDENTIAL - Law Enforcement Sensitive")
        
        c.save()
        print(f"✓ Generated mock police report: {output_path}")

except ImportError:
    def generate_mock_police_report(output_path: str = "data/arrest_report_scanned.pdf"):
        """Fallback: Create a simple text file if reportlab not available"""
        content = """
METROPOLITAN POLICE DEPARTMENT
Incident Report - Confidential

Report ID: LEA-2024-8892
Date of Incident: May 12, 2024          Time: 01:45 Hours
Location: Interstate 95, Exit 42
Subject Name: JOHN DOE                  DOB: 03/15/1985

NARRATIVE:
At approximately 0145 hours, I observed a vehicle (2018 Honda Accord, License
Plate: ABC-1234) weaving across lanes on Interstate 95 northbound near Exit 42.

I initiated a traffic stop. Upon approach, I detected a strong odor of alcoholic
beverage emanating from the vehicle. Subject's eyes appeared bloodshot and watery.

Field Sobriety Tests administered:
  - Horizontal Gaze Nystagmus: FAILED
  - Walk and Turn: FAILED (subject unable to maintain balance)
  - One Leg Stand: FAILED

Subject refused preliminary breathalyzer test. During questioning, subject stated
"I only had two beers at dinner." Subject arrested for suspicion of DUI.

CHARGES:
1. Driving Under Influence of Alcohol (VC 23152(a)) - Misdemeanor
2. Reckless Driving (VC 23103) - Misdemeanor

Officer: J. Martinez #4521
Badge: 4521
Signature: ____[scribbled signature]____

CONFIDENTIAL - Law Enforcement Sensitive
"""
        
        with open(output_path.replace('.pdf', '.txt'), 'w') as f:
            f.write(content)
        print(f"✓ Generated mock police report: {output_path.replace('.pdf', '.txt')}")


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_mock_police_report()