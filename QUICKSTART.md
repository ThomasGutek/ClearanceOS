# ClearanceOS - Quick Start Guide

## 🚀 Running the Prototype

### Option 1: Interactive Demo (No Dependencies Required)

The standalone demo works without any external packages:

```bash
cd clearanceOS
python demo.py
```

This will run an interactive command-line demonstration showing:
- VLM extraction from a simulated police report
- SEAD 4 adjudication with legal citations
- Anti-Corruption Layer sync simulation

**Press ENTER when prompted to see the legacy sync process**

---

### Option 2: Full Streamlit Dashboard (Requires Dependencies)

If you have network access and want the full web interface:

```bash
cd clearanceos
pip install -r requirements.txt
streamlit run app.py
```

This launches a web dashboard at `http://localhost:8501` with:
- File upload interface
- Visual extraction pipeline
- Side-by-side data comparison
- Interactive ACL controls

---

## 📁 Project Structure

```
clearanceos/
├── app.py                    # Streamlit web dashboard
├── demo.py                   # Standalone CLI demo (no deps)
├── models.py                 # Domain models (Pydantic schemas)
├── ingest.py                 # VLM extraction simulation
├── rag.py                    # SEAD 4 knowledge base
├── logic.py                  # Deterministic adjudication engine
├── acl.py                    # Anti-Corruption Layer
├── generate_mock_data.py     # Creates synthetic test data
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
└── data/
    └── arrest_report_scanned.pdf  # Mock police report
```

---

## 🎯 Demo Scenarios

### Scenario A: DUI Incident (Default)
- **Input**: Scanned police report with alcohol involvement
- **Triggers**: Guideline G (Alcohol), Guideline J (Criminal)
- **Output**: MANUAL_REVIEW recommendation
- **Why**: Misdemeanor + alcohol = requires subject interview

### Scenario B: Drug Possession
- Change filename to include "drug" keyword
- **Triggers**: Guideline H (Drugs)
- **Output**: MANUAL_REVIEW or DENY

---

## 🔍 Key Features to Demonstrate

### 1. VLM Intelligence
- Extracts from "dirty" documents (scanned, handwritten)
- Infers context (e.g., "alcohol involved" without explicit checkbox)
- Handles noise and document quality issues

### 2. Legal Reasoning
- RAG retrieves relevant SEAD 4 guidelines
- Deterministic rules apply consistent logic
- Auto-generates Statement of Reasons with citations

### 3. Legacy Integration
- Shows dual-status (real-time vs. batch)
- Demonstrates 96-hour sync lag
- ACL translates JSON → SOAP/XML

---

## 🧪 Testing Individual Components

Test each module independently:

```bash
# Test domain models
python models.py

# Test VLM extraction
python ingest.py

# Test RAG knowledge base
python rag.py

# Test adjudication engine
python logic.py

# Test ACL
python acl.py
```

Each module has built-in test cases in its `if __name__ == "__main__"` block.

---

## 📊 Expected Output

When running `demo.py`, you should see:

```
======================================================================
  ClearanceOS Prototype v0.1 - Automated Adjudication
======================================================================

Demonstrating VLM-Driven Ingestion + SEAD 4 Adjudication
Trusted Workforce 2.0 / Continuous Vetting Demo

======================================================================
  PHASE 1: VLM Ingestion
======================================================================

🤖 VLM Agent processing: arrest_report_scanned.pdf
   - Reading pixel data...
   - Detecting text regions...
   - Extracting structured data...
✅ Extraction complete!

📊 Extracted Data:
   Report ID: LEA-2024-8892
   Subject: John Doe
   ...

[continues through all phases]
```

---

## 🎥 Demo Presentation Flow

**Time: 4-5 minutes**

1. **Introduction (30s)**
   - Problem: 40% of adjudicator time spent on manual data entry
   - Solution: Automate with VLM + RAG

2. **VLM Ingestion (1m)**
   - Show messy PDF
   - Run extraction
   - Highlight inferred fields (alcohol detection)

3. **Legal Reasoning (1.5m)**
   - Show SEAD 4 citations
   - Explain deterministic rules
   - Display Statement of Reasons

4. **Legacy Integration (1m)**
   - Point out dual status
   - Explain sync lag problem
   - Force sync to demonstrate ACL

5. **Q&A (1m)**
   - Technical architecture
   - Production roadmap
   - ROI metrics

---

## ⚠️ Important Notes

- **Synthetic Data Only**: All incidents, names, dates are fake
- **Not Production Ready**: Missing auth, encryption, real APIs
- **Demo Purpose**: Proves technical feasibility only
- **SEAD 4 Accuracy**: Guidelines are simplified excerpts

---

## 🔧 Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: Use `demo.py` instead of `app.py`, or install dependencies

**Problem**: "Network connection error"
**Solution**: Demo works offline. Use standalone `demo.py`

**Problem**: No PDF generated
**Solution**: Run `python generate_mock_data.py` first

---

## 📞 Support

For questions about the prototype:
- Review `README.md` for full technical details
- Check code comments in each module
- Run individual component tests

---

**ClearanceOS v0.1** - Proof of Concept
*Automating Security Clearance Adjudication*