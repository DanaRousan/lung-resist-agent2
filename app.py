import streamlit as st
from agent import generate_inference

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PrecisionOnc | Genomic Reasoning Agent",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Clinical Aesthetics ────────────────────────────────────────
st.markdown("""
<style>
    /* Main background and font */
    .main { background-color: #f0f4f8; }
    
    /* Title styling */
    h1 { color: #003366 !important; font-weight: 800; }
    h2, h3 { color: #0056b3 !important; }

    /* Report output box */
    .report-box {
        background-color: #ffffff;
        padding: 24px 28px;
        border-radius: 12px;
        border-left: 6px solid #0056b3;
        box-shadow: 0 2px 12px rgba(0, 86, 179, 0.1);
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background-color: #fff8e1;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        font-size: 0.85rem;
        color: #555;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #003366;
        color: white;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Button */
    .stButton > button {
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #003d80;
    }

    /* Divider */
    hr { border: 1px solid #dce6f0; margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 PrecisionOnc")
    st.markdown("**Evidence-Driven Genomic Reasoning Agent**")
    st.markdown("---")
    st.markdown("### 🏗️ System Architecture")
    st.markdown("""
    - **Framework:** RAG (Retrieval-Augmented Generation)  
    - **Model:** OpenAI GPT-4o  
    - **Temperature:** 0.1 (Clinical Safety Mode)  
    - **Knowledge Source:** Curated JSON — Peer-Reviewed Literature  
    """)
    st.markdown("---")
    st.markdown("### 🛡️ Governance: DKITE Framework")
    st.markdown("""
    | Stage | Status |
    |-------|--------|
    | **D**efine | ✅ Moderate Risk Advisory |
    | **K**nowledge | ✅ Structured JSON KB |
    | **I**ntegrations | ✅ GPT-4o + Guardrails |
    | **T**est | ✅ Validated Prompts |
    | **E**volve | 🔄 Active Development |
    """)
    st.markdown("---")
    st.markdown("### 📚 Knowledge Base Coverage")
    st.markdown("""
    - EGFR PACC Mutations  
    - HER2 ADC Payload Resistance  
    - MET Amplification (Bypass Track)  
    """)
    st.markdown("---")
    st.caption("v1.0 | UTHealth Houston | Biomedical Informatics")

# ── Main Header ───────────────────────────────────────────────────────────────
st.title("🧬 PrecisionOnc: Genomic Reasoning Agent")
st.markdown("**NSCLC Resistance Inference Engine** — EGFR · HER2 · MET")
st.markdown(
    "This advisory tool maps complex multi-gene NSCLC profiles to curated resistance mechanisms "
    "and active clinical trial recommendations. All outputs require Molecular Tumor Board validation."
)
st.markdown("---")

# ── Two-Column Layout ─────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1.6], gap="large")

# ── LEFT COLUMN: Input + Governance ──────────────────────────────────────────
with col1:
    st.markdown("### 📋 Patient Genomic Profile Input")

    patient_text = st.text_area(
        label="Enter clinical and genomic data below:",
        height=200,
        placeholder=(
            "Examples:\n"
            "• 65yo female, HER2-mutant NSCLC progressing on T-DXd. NGS shows SLFN11 loss.\n"
            "• 58yo male, EGFR PACC mutation, failed osimertinib. Seeking trial options.\n"
            "• 70yo, EGFR exon 19 del, acquired MET amplification (MET/CEP7 ratio = 6.2)."
        )
    )

    analyze_button = st.button("🔍 Generate Resistance Inference", type="primary")

    st.markdown("---")
    st.markdown("### 🛡️ Clinical Safety Guardrails")
    st.info("""
**Risk Classification:** Moderate (Advisory Only)  
**Oversight Model:** Human-in-the-Loop (MTB Required)  
**Governance Framework:** DKITE Clinical AI Standard  
**Hallucination Prevention:** All outputs grounded exclusively in curated peer-reviewed JSON knowledge base.  
**Autonomous Decision Making:** ❌ Prohibited — this tool generates hypotheses only.
    """)

    st.markdown("---")
    st.markdown("### 💡 Sample Inputs to Try")
    with st.expander("Click to view example patient profiles"):
        st.markdown("""
**Example 1 — HER2 ADC Resistance:**  
`65yo female, HER2-mutant NSCLC progressing on T-DXd. NGS shows SLFN11 loss.`

**Example 2 — EGFR PACC:**  
`58yo male, EGFR PACC mutation (G719A), failed erlotinib and osimertinib. Seeking next-line trial.`

**Example 3 — MET Bypass:**  
`70yo never-smoker, EGFR exon 19 del, progressing on osimertinib. ctDNA shows MET amplification, copy number 12.`

**Example 4 — Multi-gene:**  
`62yo female, HER2-amplified NSCLC, ABCC1 gain detected on NGS. Also SLFN11-low by IHC.`
        """)

# ── RIGHT COLUMN: Report Output ───────────────────────────────────────────────
with col2:
    st.markdown("### 📊 Ranked Resistance Report")

    if analyze_button:
        if not patient_text.strip():
            st.warning("⚠️ Please enter a patient genomic profile before generating a report.")
        else:
            with st.spinner("🔄 Querying knowledge base and synthesizing evidence... Please wait."):
                try:
                    report = generate_inference(patient_text)

                    st.success("✅ Inference Complete — Evidence Grounded in Curated Knowledge Base")

                    # Render the report in a styled clinical box
                    st.markdown(
                        f'<div class="report-box">{report}</div>',
                        unsafe_allow_html=True
                    )

                    # Download button for the report
                    st.download_button(
                        label="⬇️ Download Report as .txt",
                        data=report,
                        file_name="PrecisionOnc_Resistance_Report.txt",
                        mime="text/plain"
                    )

                    # Static safety disclaimer
                    st.markdown("""
                    <div class="disclaimer-box">
                    ⚠️ <strong>Regulatory Notice:</strong> This output is generated by an AI advisory system 
                    and does not constitute a medical diagnosis or treatment order. Review by a qualified 
                    oncologist and Molecular Tumor Board is mandatory before any clinical action is taken.
                    </div>
                    """, unsafe_allow_html=True)

                except KeyError:
                    st.error(
                        "🔑 **Configuration Error:** OpenAI API Key not found in Streamlit Secrets. "
                        "Please add `OPENAI_API_KEY` in the Streamlit Cloud Advanced Settings → Secrets section."
                    )
                except Exception as e:
                    st.error(f"❌ **Unexpected System Error:** The inference engine encountered an issue. Details: `{e}`")
    else:
        # Placeholder state
        st.markdown("""
        <div style="
            background-color: #eef4fb;
            border: 2px dashed #aac8e8;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            color: #5580aa;
        ">
            <h3 style="color: #0056b3;">Awaiting Patient Input</h3>
            <p>Enter a genomic profile in the left panel and click<br>
            <strong>"Generate Resistance Inference"</strong> to begin analysis.</p>
            <p style="font-size:0.85rem; margin-top: 16px;">
                Supported pathways: EGFR PACC · HER2 ADC Resistance · MET Amplification
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.82rem;'>"
    "PrecisionOnc RAG Agent v1.0 · Built by Dana Al Rousan · Master's Candidate, Biomedical Informatics, UTHealth Houston · "
    "Compliant with DKITE Clinical AI Framework"
    "</div>",
    unsafe_allow_html=True
)
