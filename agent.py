import json
import streamlit as st
import requests


def load_knowledge() -> dict:
    """Loads the structured JSON knowledge base."""
    with open("knowledge_base.json", "r") as f:
        return json.load(f)


def generate_inference(patient_input: str) -> str:
    """
    Core reasoning function using Hugging Face Inference API (free tier).
    Uses Mistral-7B-Instruct-v0.3.
    """

    api_key = st.secrets["HF_API_KEY"]
    kb = load_knowledge()

    system_prompt = """You are PrecisionOnc, an evidence-driven genomic reasoning assistant for thoracic oncology, operating under strict clinical AI governance protocols.

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

[Add Rank 2, Rank 3 entries only if additional knowledge base matches are found. If no match exists, state: "No knowledge base entry found for [alteration]."]

---

#### ⚠️ Clinical Safety Disclaimer
This report is a **hypothesis-generation tool only**. It does not constitute a diagnosis, treatment decision, or medical order. All recommendations require review and validation by the attending physician and Molecular Tumor Board before any clinical action is taken. This system operates as a **Moderate Risk, Human-in-the-Loop advisory tool** in compliance with the DKITE Clinical AI Framework.

## CONFIDENCE SCORING RUBRIC
- **90-100%:** Direct unambiguous match (gene + alteration both present).
- **70-89%:** Strong match using synonymous terminology.
- **50-69%:** Partial or indirect match.
- **< 50%:** Do not report. State no reliable match was found.

## CRITICAL GUARDRAILS
1. Do NOT recommend any drug not listed in the knowledge base.
2. Do NOT generate citations not present in the knowledge base.
3. Do NOT make autonomous diagnostic or treatment decisions.
4. Always include the full Clinical Safety Disclaimer.
5. If no match: state "No knowledge base match identified. Recommend manual literature review and MTB consultation."
"""

    user_prompt = f"""## Patient Genomic Profile:
{patient_input}

## Curated Knowledge Base (Your ONLY source of truth):
{json.dumps(kb, indent=2)}

Please generate the Ranked Resistance Report now."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # New HF Inference API format (v2) — works with all current models
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.1
    }

    response = requests.post(
        "https://api-inference.huggingface.co/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"HuggingFace API error {response.status_code}: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
