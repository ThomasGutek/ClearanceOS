# ClearanceOS Prototype v0.1

**Automated Security Clearance Adjudication System**

---

## Overview

ClearanceOS demonstrates how Vision-Language Models (VLMs) and Retrieval-Augmented Generation (RAG) can automate the "dirty work" of security clearance adjudication by converting unstructured police records into legally cited, SEAD 4-compliant "Statements of Reasons."

### Key Features

- **VLM-Driven Ingestion**: Extracts structured data from scanned/handwritten police reports
- **Deterministic Adjudication**: RAG-powered legal citations + rule-based decision engine
- **Legacy Integration**: Anti-Corruption Layer (ACL) manages real-time vs. batch sync gap
- **Audit Trail**: Every decision includes SEAD 4 guideline citations

---

## Architecture

```
┌─────────────────┐
│  Dirty PDF      │
│  (Scanned LEA   │
│   Report)       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Ingestion Service (VLM)                │
│  - GPT-4o-Vision simulation             │
│  - Pydantic schema validation           │
│  - Reflexion loop for self-correction   │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Adjudication Brain                     │
│  - RAG: SEAD 4 Vector Store             │
│  - Deterministic Rule Engine            │
│  - Statement of Reasons Generator       │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Anti-Corruption Layer (ACL)            │
│  - Local cache (real-time)              │
│  - SOAP/XML translation                 │
│  - Batch sync simulation                │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Legacy NBIS Mainframe (Simulated)      │
└─────────────────────────────────────────┘
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Mock Data (Optional)

```bash
python generate_mock_data.py
```

This creates a synthetic police report PDF in the `data/` folder.

### 3. Run the Application

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## Demo Walkthrough

### Scene 1: The Problem (0:00 - 1:00)

**Current State:** Adjudicators spend 40% of their time manually typing data from scanned PDFs into mainframe systems. OCR tools like Instabase fail on handwritten notes and crooked scans.

**Action:** Show a messy police report PDF with handwritten annotations.

### Scene 2: VLM Ingestion (1:00 - 2:00)

**ClearanceOS Solution:** Upload the PDF. Watch the VLM agent extract:
- Subject information
- Charges (with statutes and severity)
- Narrative context
- **Key inference**: "Alcohol involved" (even without a checkbox)

**Result:** Structured JSON appears in seconds.

### Scene 3: Legal Reasoning (2:00 - 3:30)

**Traditional Approach:** Adjudicator manually looks up SEAD 4 guidelines, types citations, writes Statement of Reasons.

**ClearanceOS Solution:** 
- RAG retrieves relevant guidelines (e.g., "Guideline G: Alcohol Consumption")
- Deterministic engine applies IF/THEN rules
- Auto-generates Statement of Reasons with legal citations

**Result:** `MANUAL_REVIEW` recommendation with full audit trail.

### Scene 4: The Legacy Sync Gap (3:30 - 4:30)

**The Problem:** Government mainframes process changes in 4-day batch cycles.

**ClearanceOS Solution:**
- **Local Status**: SUSPENDED (immediate)
- **Mainframe Status**: ACTIVE (pending sync)
- Click "Force Sync" to simulate SOAP/XML transmission

**Result:** Demonstrates how the ACL protects against the real-time gap.

---

## Technical Components

### 1. Domain Models (`models.py`)

Pydantic schemas enforce type safety:
- `Incident`: Extracted case data
- `Charge`: Individual offense
- `Citation`: SEAD 4 guideline reference
- `AdjudicationDecision`: Final recommendation + SOR
- `LegacyStatus`: Dual-state clearance status

### 2. Ingestion Service (`ingest.py`)

Simulates VLM extraction:
- Mock response pre-validated against Pydantic schema
- In production: Calls GPT-4o-Vision API with retry logic
- Includes actual system prompt used for VLM

### 3. RAG Knowledge Base (`rag.py`)

SEAD 4 guideline store:
- Simplified excerpts from actual adjudicative guidelines
- Keyword-based search (production would use vector embeddings)
- Guidelines: G (Alcohol), H (Drugs), D (Sexual), J (Criminal), E (Personal Conduct)

### 4. Adjudication Engine (`logic.py`)

Deterministic rule executor:
- **NOT an AI** - pure IF/THEN logic
- Applies severity weights to calculate risk scores
- Generates formal Statement of Reasons
- Maintains audit log

### 5. Anti-Corruption Layer (`acl.py`)

Manages legacy integration:
- Buffers real-time decisions
- Translates JSON → SOAP/XML
- Simulates batch sync delay (96 hours default)
- Provides dual-status visibility

### 6. Demo Dashboard (`app.py`)

Streamlit application:
- Upload case files
- Visualize extraction → adjudication → sync flow
- Side-by-side comparison of data
- Interactive ACL controls

---

## Key Differentiators

| Feature | Traditional System | ClearanceOS |
|---------|-------------------|-------------|
| **Input** | Manual typing from PDF | VLM reads pixels directly |
| **Processing Time** | 30-60 minutes per case | 10-15 seconds |
| **Legal Citations** | Manual lookup | Auto-retrieved via RAG |
| **Consistency** | Varies by adjudicator | Deterministic rules |
| **Audit Trail** | Minimal | Full citation chain |
| **Real-time Updates** | 96-hour batch lag | Immediate + ACL buffering |

---

## Demo Scenarios

### Scenario A: DUI Incident
- **Triggers**: Guideline G (Alcohol)
- **Decision**: MANUAL_REVIEW
- **Why**: Misdemeanor + alcohol = requires interview

### Scenario B: Drug Possession
- **Triggers**: Guideline H (Drugs)
- **Decision**: MANUAL_REVIEW or DENY (depending on quantity)
- **Why**: Controlled substance violation

### Custom Scenario
Upload your own PDF and watch the system adapt.

---

## Non-Goals (Out of Scope for v0.1)

- ❌ Live NBIS/OPM integration (we simulate the endpoint)
- ❌ Biometric processing (fingerprints, facial recognition)
- ❌ Production auth/RBAC (single-user demo mode)
- ❌ Real GPT-4o-Vision API calls (cost/complexity)
- ❌ Vector database (ChromaDB/Pinecone) - using keyword search

---

## Testing

Run component tests:

```bash
# Test models
python models.py

# Test VLM extraction
python ingest.py

# Test RAG retrieval
python rag.py

# Test adjudication logic
python logic.py

# Test ACL
python acl.py
```

All modules include `if __name__ == "__main__":` test harnesses.

---

## Future Roadmap

**Phase 2: Production Readiness**
- Real OpenAI API integration
- Vector database (ChromaDB)
- Multi-user auth
- NBIS SOAP integration

**Phase 3: Advanced Features**
- Multi-document correlation
- Temporal pattern detection
- Predictive risk modeling
- Biometric cross-referencing

**Phase 4: Continuous Vetting**
- Real-time monitoring pipelines
- Automated periodic re-adjudication
- Behavioral drift detection

---

## Security & Compliance

- **Data Classification**: Prototype uses synthetic data only
- **No PII**: All names, dates, incidents are fabricated
- **SEAD 4 Accuracy**: Guidelines are simplified excerpts for demo purposes
- **Production Requirements**: Would require FedRAMP/NIST 800-53 compliance

---

## Support & Feedback

This is a **demonstration prototype** designed to prove technical feasibility. For questions or feedback, please contact the engineering team.

---

## License

Proprietary - Internal Use Only

---

**ClearanceOS** - Trusted Workforce 2.0  
*Automating the Dirty Work of Security Clearances*