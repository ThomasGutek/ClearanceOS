import streamlit as st
import time
from datetime import datetime
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from ingest import simulate_vlm_extraction, VLM_SYSTEM_PROMPT
from logic import AdjudicationEngine
from acl import AntiCorruptionLayer
from models import LegacyStatus

# Page configuration
st.set_page_config(
    layout="wide", 
    page_title="ClearanceOS Prototype v0.1",
    page_icon="🛡️"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-suspended {
        color: #dc3545;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    .citation-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'acl' not in st.session_state:
    st.session_state.acl = AntiCorruptionLayer(sync_interval_hours=96)
if 'engine' not in st.session_state:
    st.session_state.engine = AdjudicationEngine()
if 'current_incident' not in st.session_state:
    st.session_state.current_incident = None
if 'current_decision' not in st.session_state:
    st.session_state.current_decision = None
if 'current_subject_id' not in st.session_state:
    st.session_state.current_subject_id = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ ClearanceOS: Automated Adjudication</h1>
    <p style="font-size: 1.2em; margin-top: 0.5rem;">
        Trusted Workforce 2.0 / Continuous Vetting Prototype
    </p>
    <p style="font-size: 0.9em; opacity: 0.9; margin-top: 0.5rem;">
        Prototype v0.1 | VLM-Driven Ingestion + Deterministic SEAD 4 Adjudication
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Ingestion Section
st.sidebar.header("📄 1. Ingest Evidence")
st.sidebar.markdown("Upload law enforcement records (PDF format)")

uploaded_file = st.sidebar.file_uploader(
    "Select Case File", 
    type=["pdf", "txt"],
    help="Upload a police report, arrest record, or incident narrative"
)

# Demo mode selection
demo_mode = st.sidebar.radio(
    "Demo Scenario:",
    ["DUI Incident (Alcohol)", "Drug Possession", "Custom Upload"],
    help="Select a pre-configured scenario or upload your own"
)

process_button = st.sidebar.button("🚀 Process Case File", type="primary")

# Main content area
if process_button or uploaded_file:
    
    # Determine which scenario to use
    if demo_mode == "DUI Incident (Alcohol)":
        filename = "dui_report.pdf"
    elif demo_mode == "Drug Possession":
        filename = "drug_report.pdf"
    else:
        filename = uploaded_file.name if uploaded_file else "custom.pdf"
    
    # Generate a subject ID
    subject_id = f"SUBJ-{hash(filename) % 100000:05d}"
    st.session_state.current_subject_id = subject_id
    
    # Phase 1: VLM Extraction
    with st.spinner('🤖 VLM Agent scanning document...'):
        progress_bar = st.progress(0)
        time.sleep(0.5)
        progress_bar.progress(33)
        
        # Simulate extraction
        file_bytes = uploaded_file.read() if uploaded_file else b"fake_bytes"
        incident_data = simulate_vlm_extraction(file_bytes, filename)
        st.session_state.current_incident = incident_data
        
        time.sleep(0.5)
        progress_bar.progress(100)
    
    st.success("✅ Extraction Complete - Structured Data Generated")
    
    # Display Results in Columns
    col1, col2 = st.columns([1, 1])
    
    # Column 1: Extracted Data
    with col1:
        st.markdown("### 📊 Extracted Intelligence")
        st.markdown(f"**Subject:** {incident_data.subject_name}")
        st.markdown(f"**Report ID:** {incident_data.report_id}")
        st.markdown(f"**Date:** {incident_data.date}")
        st.markdown(f"**Location:** {incident_data.location or 'N/A'}")
        
        st.markdown("#### 📝 Narrative Summary")
        st.info(incident_data.narrative_summary)
        
        st.markdown("#### ⚖️ Charges Filed")
        for i, charge in enumerate(incident_data.charges, 1):
            severity_color = "🔴" if charge.severity == "Felony" else "🟡" if charge.severity == "Misdemeanor" else "🟢"
            st.markdown(f"{severity_color} **{i}.** {charge.description}")
            st.caption(f"   Statute: {charge.statute} | Severity: {charge.severity}")
        
        # Key indicators
        st.markdown("#### 🔍 Key Indicators")
        alcohol_badge = "🍺 Alcohol Involved" if incident_data.alcohol_involved else "✅ No Alcohol"
        st.markdown(f"- {alcohol_badge}")
        st.markdown(f"- Total Charges: {len(incident_data.charges)}")
    
    # Phase 2: Adjudication
    with st.spinner('⚖️ Cross-referencing SEAD 4 Guidelines...'):
        time.sleep(1.0)
        decision = st.session_state.engine.adjudicate_case(incident_data)
        st.session_state.current_decision = decision
    
    # Column 2: Adjudication Decision
    with col2:
        st.markdown("### 🎯 Adjudication Decision")
        
        # Status badge with color coding
        status_emoji = {
            "GRANT": "✅",
            "DENY": "❌",
            "REVOKE": "🚫",
            "MANUAL_REVIEW": "⚠️"
        }
        
        status_class = {
            "GRANT": "status-active",
            "DENY": "status-suspended",
            "REVOKE": "status-suspended",
            "MANUAL_REVIEW": "status-pending"
        }
        
        emoji = status_emoji.get(decision.recommendation, "❓")
        css_class = status_class.get(decision.recommendation, "")
        
        st.markdown(f"## {emoji} Recommendation: {decision.recommendation}")
        st.markdown(f"**Risk Score:** {decision.risk_score:.1f}/10.0")
        st.caption(f"Generated: {decision.timestamp}")
        
        # Statement of Reasons
        st.markdown("#### 📋 Statement of Reasons (Auto-Generated)")
        st.text_area(
            "SOR Preview:",
            value=decision.generated_sor,
            height=250,
            disabled=True
        )
        
        # Legal Citations
        st.markdown("#### 📚 Legal Citations (Audit Trail)")
        if decision.citations:
            for cit in decision.citations:
                st.markdown(f"""
                <div class="citation-box">
                    <strong>{cit.guideline}</strong><br/>
                    {cit.text}<br/>
                    <em style="font-size: 0.9em; color: #666;">Source: {cit.source_paragraph}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific guidelines flagged.")
    
    # Phase 3: Legacy Integration (ACL)
    st.divider()
    st.markdown("### 🔄 Legacy Infrastructure Synchronization")
    st.caption("Demonstrating the Anti-Corruption Layer (ACL) pattern")
    
    # Publish decision to ACL
    if st.session_state.current_decision and st.session_state.current_subject_id:
        status = st.session_state.acl.publish_decision(
            st.session_state.current_subject_id,
            st.session_state.current_decision
        )
        
        # Display dual-status metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                label="🚀 ClearanceOS Status",
                value=status.local_status,
                delta="Real-time (0s latency)",
                help="Immediate decision based on rules engine"
            )
        
        with metric_col2:
            st.metric(
                label="🏛️ NBIS Mainframe Status",
                value=status.mainframe_status,
                delta=f"Sync lag: {status.sync_lag_hours}h" if status.sync_lag_hours > 0 else "Synced",
                delta_color="inverse",
                help="Legacy system updated via batch processing"
            )
        
        with metric_col3:
            queue_size = st.session_state.acl.get_sync_queue_size()
            st.metric(
                label="📋 Pending Sync Queue",
                value=queue_size,
                help="Number of decisions awaiting batch sync"
            )
        
        # Force sync button
        st.markdown("---")
        col_a, col_b = st.columns([1, 3])
        
        with col_a:
            if st.button("🔧 Force Legacy Sync (Simulate SOAP)", key="force_sync"):
                with st.spinner("📡 Transmitting XML envelope to Mainframe..."):
                    time.sleep(1.5)
                    synced_status = st.session_state.acl.force_sync(
                        st.session_state.current_subject_id
                    )
                
                st.success("✅ Mainframe synchronized!")
                st.rerun()
        
        with col_b:
            st.info(
                "**Note:** In production, the mainframe sync happens via nightly batch jobs. "
                "This creates a 'real-time gap' where ClearanceOS knows about issues "
                "before legacy systems. The ACL manages this impedance mismatch."
            )

# Sidebar - System Information
st.sidebar.divider()
st.sidebar.markdown("### 🔧 System Information")
st.sidebar.markdown(f"**Decisions Logged:** {len(st.session_state.engine.decision_log)}")
st.sidebar.markdown(f"**ACL Queue:** {st.session_state.acl.get_sync_queue_size()} pending")

# Sidebar - Technical Deep Dive
with st.sidebar.expander("🧠 View VLM System Prompt"):
    st.code(VLM_SYSTEM_PROMPT, language="text")

with st.sidebar.expander("📐 Architecture Overview"):
    st.markdown("""
    **Components:**
    - **Ingestion Service:** VLM-based extraction
    - **Adjudication Brain:** RAG + Deterministic rules
    - **Legacy ACL:** SOAP/XML buffer layer
    - **Demo Dashboard:** This Streamlit UI
    
    **Tech Stack:**
    - Pydantic (Schema validation)
    - Simulated GPT-4o-Vision
    - SEAD 4 Vector Store (RAG)
    - Python Rule Engine
    """)

# Footer
st.divider()
st.caption("ClearanceOS Prototype v0.1 | For Demonstration Purposes Only")
st.caption("⚠️ This system uses simulated data and is not connected to live government systems.")