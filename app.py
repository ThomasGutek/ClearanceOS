import streamlit as st
import time
from ingest import simulate_vlm_extraction
from logic import adjudicate_case

st.set_page_config(layout="wide", page_title="ClearanceOS Prototype")

st.title("🛡️ ClearanceOS: Automated Adjudication")
st.markdown("### Trusted Workforce 2.0 / Continuous Vetting Demo")

# 1. Upload Section
st.sidebar.header("1. Ingest Evidence")
uploaded_file = st.sidebar.file_uploader("Upload LEA Record (PDF)", type="pdf")

if uploaded_file:
    # 2. Processing Simulation
    with st.spinner('🤖 VLM Agent scanning pixel data...'):
        time.sleep(1.5) # Fake processing time
        incident_data = simulate_vlm_extraction(uploaded_file)
    
    st.success("Extraction Complete")

    # 3. Display Extraction
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Raw Data (Extracted)")
        st.json(incident_data.dict())

    # 4. Adjudication
    with st.spinner('⚖️ Cross-referencing SEAD 4 Guidelines...'):
        time.sleep(1.0)
        decision = adjudicate_case(incident_data)

    with col2:
        st.subheader("Adjudication Recommendation")
        
        status_color = "red" if decision.recommendation != "GRANT" else "green"
        st.markdown(f"## Status: :{status_color}[{decision.recommendation}]")
        
        st.markdown("#### Statement of Reasons (Generated)")
        st.info(decision.generated_sor)
        
        st.markdown("#### Legal Citations (Audit Trail)")
        for cit in decision.citations:
            st.warning(f"**{cit.guideline}**: {cit.text} *({cit.source_paragraph})*")

    # 5. ACL Simulation
    st.divider()
    st.subheader("legacy Infrastructure Sync (ACL)")
    
    c1, c2 = st.columns(2)
    c1.metric(label="ClearanceOS Status (Real-time)", value="SUSPENDED", delta="-0s")
    c2.metric(label="NBIS Mainframe Status", value="ACTIVE", delta="Pending Batch (96h)")
    
    if st.button("Force Legacy Sync (Simulate SOAP)"):
        with st.spinner("Transmitting XML envelope to Mainframe..."):
            time.sleep(2)
        c2.metric(label="NBIS Mainframe Status", value="SUSPENDED", delta="Synced")