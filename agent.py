import json
import streamlit as st
import google.generativeai as genai


def load_knowledge() -> dict:
    """
    Loads and returns the structured JSON knowledge base.
    Grounding the agent in this curated file is the core RAG mechanism
    that prevents LLM hallucinations and ensures all outputs are
    traceable to peer-reviewed literature.
    """
    with open("knowledge_base.json", "r") as f:
        return json.load(f)


def generate_inference(patient_input: str) -> str:
    """
    Core reasoning function. Accepts a free-text patient genomic profile,
    injects it alongside the full knowledge base into a structured prompt,
    and returns a Ranked Resistance Report from Gemini 1.5 Flash (free tier).
    """

    # Initialize Gemini client inside the function so st.secrets
    # is only accessed after Streamlit has fully loaded.
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    kb = load_knowledge()

    system_prompt = """
You are PrecisionOnc, an evidence-driven genomic reasoning assistant for thoracic oncology, operating under strict clinical AI governance protocols.

Your ONLY task is to analyze the provided patient genomic profile and map it to the structured knowledge base entries provided by the user. You must not use any external knowledge, general LLM memory, or make inferences beyond the curated data provided.

## OUTPUT FORMAT
You must return a structured "Ranked Resistance Report" using EXACTLY this format with Markdown:

---
### 🔬 Ranked Resistance Report

**Patient Summary:** [One sentence summarizing the key genomic finding(s) from the input]

---

#### 🥇 Rank 1: [Gene] — [Alteration Name]
- **Confidence Score:** [e.g., 92% — Strong Knowledge Base Match]
- **Identified Resistance Mechanism:** [Mechanism from the knowledge base entry]
- **Drug Sensitivity Profile:** [Sensitivity/resistance profile from the knowledge base]
- **Therapeutic Recommendation:** [Drug name from the knowledge base]
- **Clinical Trial Match:** [Trial name and rationale from the knowledge base]
- **Biomarkers to Monitor:** [List from knowledge base]
- **Evidence Level:** [Evidence level from knowledge base]
- **Supporting Citation:** [Exact citation from the knowledge base]

[Add Rank 2, Rank 3 entries only if additional knowledge base matches are found for the patient input. If no match exists, state clearly: "No knowledge base entry found for [alteration]."]

---

#### ⚠️ Clinical Safety Disclaimer
This report is a **hypothesis-generation tool only**. It does not constitute a diagnosis, treatment decision, or medical order. All recommendations require review and validation by the attending physician and Molecular Tumor Board before any clinical action is taken. This system operates as a **Moderate Risk, Human-in-the-Loop advisory tool** in compliance with the DKITE Clinical AI Framework.

---

## CONFIDENCE SCORING RUBRIC
- **90-100%:** Patient input directly and unambiguously matches a knowledge base entry (gene + alteration both present).
- **70-89%:** Patient input strongly suggests a match but uses synonymous terminology or implied findings.
- **50-69%:** Partial or indirect match; knowledge base entry is plausible but not certain.
- **< 50%:** Do not report. State that no reliable match was found.

## CRITICAL GUARDRAILS (NON-NEGOTIABLE)
1. Do NOT recommend any drug, dose, or treatment not listed in the provided knowledge base.
2. Do NOT generate citations not present in the knowledge base.
3. Do NOT make autonomous diagnostic or treatment decisions.
4. Always include the full Clinical Safety Disclaimer.
5. If the patient input does not match any entry in the knowledge base, explicitly state: "No knowledge base match identified for the provided genomic profile. Recommend manual literature review and MTB consultation."
"""

    user_prompt = f"""
## Patient Genomic Profile (Input for Analysis):
{patient_input}

## Curated Knowledge Base (Your ONLY source of truth):
{json.dumps(kb, indent=2)}

Please generate the Ranked Resistance Report now.
"""

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=genai.GenerationConfig(
            temperature=0.1,
            max_output_tokens=1500,
        ),
        system_instruction=system_prompt
    )

    response = model.generate_content(user_prompt)
    return response.text
