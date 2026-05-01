# 🧬 PrecisionOnc RAG: Evidence-Driven Genomic Reasoning Agent

> An advisory Retrieval-Augmented Generation (RAG) framework for mapping complex, multi-gene Non-Small Cell Lung Cancer (NSCLC) profiles to curated resistance mechanisms and active clinical trial recommendations.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/Model-GPT--4o-green.svg)
![Risk](https://img.shields.io/badge/Risk%20Tier-Moderate%20Advisory-yellow.svg)
![Framework](https://img.shields.io/badge/Governance-DKITE%20Framework-blueviolet.svg)

---

## 🎯 The Clinical Problem

Precision oncology in thoracic malignancies has transformed patient outcomes — but it has created a new cognitive bottleneck. When a patient presents with a complex multi-gene resistance profile (e.g., *HER2-mutant NSCLC + SLFN11 loss + ABCC1 gain*), translating that profile into an actionable clinical trial hypothesis requires:

- Cross-referencing dozens of evolving resistance mechanism papers
- Manually mapping each alteration to current Phase II/III trial eligibility criteria
- Synthesizing findings in real-time during a Molecular Tumor Board (MTB) session

This cognitive overload delays precision trial matching, increases the risk of missed therapeutic opportunities, and places unsustainable demands on oncologists and bioinformaticians.

**PrecisionOnc RAG was built to solve this problem.**

---

## 🏗️ Architecture: Enterprise-Grade Clinical AI

This agent is designed around four core principles of responsible clinical AI deployment.

### 1. 📚 Knowledge Grounding (RAG — Not Hallucination)
Instead of relying on an LLM's internal memory — which is unverifiable, non-citable, and potentially outdated — the agent queries a **curated, structured JSON knowledge base** built from peer-reviewed oncology literature. Every output is traceable to a specific citation. No citation = no output.

### 2. 🔗 Integrations & Prompt Engineering
The system uses **OpenAI's GPT-4o** with:
- **Temperature = 0.1** — Minimizes creative generation; enforces factual, reproducible clinical reasoning
- **Structured system prompt** — Enforces output format, citation requirements, and confidence scoring rubric
- **Negative instructions** — Explicitly prohibits the model from recommending drugs, trials, or citations not present in the knowledge base

### 3. 🛡️ Guardrails & Human-in-the-Loop (HITL)
Every inference includes a mandatory regulatory disclaimer. The system is classified as a **Moderate Risk advisory tool**, meaning:
- It generates hypotheses; it does not make decisions
- All outputs require review by an attending oncologist and Molecular Tumor Board before any clinical action
- Autonomous diagnostic or treatment decisions are architecturally prohibited via prompt constraints

### 4. 📊 DKITE Clinical AI Governance Framework

| Stage | Implementation |
|-------|---------------|
| **D**efine | Moderate risk, advisory scope, human-in-the-loop required |
| **K**nowledge | Curated JSON KB from peer-reviewed thoracic oncology literature |
| **I**ntegrations | GPT-4o API + Streamlit + Secure secrets management |
| **T**est | Prompt validation across representative NSCLC resistance profiles |
| **E**volve | Modular KB design enables continuous literature updates |

---

## 🔬 Knowledge Base Coverage (v1.0)

| Pathway | Gene | Alteration | Recommendation | Trial |
|---------|------|-----------|----------------|-------|
| EGFR PACC | EGFR | P-loop & αC-helix compressing mutations | Firmonertinib | FURTHER Trial |
| HER2 ADC Resistance | HER2 | SLFN11 loss / ABCC1 gain | Sevabertinib | SOHO-02 Trial |
| MET Bypass Track | MET | High-level amplification | Osimertinib + MET inhibitor | INSIGHT-2 / ORCHARD |

---

## 🗂️ Repository Structure

```
PrecisionOnc-RAG/
│
├── app.py                  # Streamlit frontend dashboard
├── agent.py                # RAG backend — prompt engineering & OpenAI integration
├── knowledge_base.json     # Curated NSCLC resistance mechanism knowledge base
├── requirements.txt        # Python dependencies for Streamlit Cloud deployment
└── README.md               # Project documentation
```

---

## 🚀 Local Setup & Deployment

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/PrecisionOnc-RAG.git
cd PrecisionOnc-RAG

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a secrets file for local development
mkdir .streamlit
echo 'OPENAI_API_KEY = "sk-your-key-here"' > .streamlit/secrets.toml

# 4. Launch the app
streamlit run app.py
```

### Deploy to Streamlit Community Cloud

1. Push all 5 files to a **new public GitHub repository**
2. Visit [share.streamlit.io](https://share.streamlit.io) → **New App**
3. Select your repository and set `app.py` as the main file
4. Click **Advanced Settings** → **Secrets** and add:
   ```toml
   OPENAI_API_KEY = "sk-your-openai-key-here"
   ```
5. Click **Deploy** ✅

---

## 🌐 Live Demo

**[🔗 Launch PrecisionOnc Dashboard →](https://your-app-link.streamlit.app)**
*(Link will be updated after Streamlit Cloud deployment)*

---

## ⚠️ Regulatory & Ethical Statement

This tool is intended for **research and educational purposes only**. It is a **hypothesis-generation assistant** and does not constitute medical advice, a clinical diagnosis, or a treatment recommendation. All outputs must be reviewed and validated by a qualified oncologist and Molecular Tumor Board before any clinical action is taken.

This system does not store, transmit, or log any patient data. All inputs are processed transiently via the OpenAI API and are subject to [OpenAI's data usage policies](https://openai.com/policies/api-data-usage-policies).

---

## 🎓 Author

**Dana Al Rousan**  
Master's Candidate in Biomedical Informatics  
The University of Texas Health Science Center at Houston (UTHealth Houston)  
School of Biomedical Informatics (SBMI)

*Built for presentation at a healthcare AI summit and to demonstrate applied clinical AI architecture capabilities to Principal Investigators in Thoracic Oncology.*

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
