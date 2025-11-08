# DDS Hybrid Inference System  
### Fine-Tuned ML + GPT Integration for Incident Credibility Scoring  

**Author:** Kevin Garrett — Machine Learning & AI Engineering  
**Last Updated:** November 2025  

---

## Purpose  

The **DDS Hybrid Inference System** is a modular AI pipeline that combines language understanding with measurable inference.  
It was designed to evaluate the credibility of incident reports by blending **LLM-based interpretation** and **deterministic ML scoring** into one reproducible workflow.

Where most systems choose between generative reasoning or classical models, this architecture integrates both:

- **LLM Extraction Layer** — interprets and structures free text into standardized JSON.  
- **ML Feature Layer** — converts tone and phrasing into numeric features that can be tested, audited, and recalibrated.  

The outcome is a **Hoax Probability (HP)** score — a quantitative measure of whether an incident is exaggerated, hostile, or fabricated.

---

## System Context  

This repository represents one **Hybrid Inference module** inside the **DDS Enterprise Incident Platform**.

| Platform Layer | Description |
|----------------|--------------|
| Client / Orchestration | Handles report intake and routes data to model endpoints. |
| Hybrid Inference (this repo) | Extracts and scores linguistic, emotional, and contextual signals. |
| Adjudication | Aggregates model outputs into calibrated probabilities. |
| Audit & Human Review | Provides explainability and bias tracking. |

Each module in this layer follows the same design pattern:  
**Interpret → Quantify → Validate → Aggregate.**

---

## Architecture Overview  
Input Report → LLM Extraction → ML Feature Scoring → HP Logistic Model → Human Review


### Layers  

1. **Input Layer** – Collects unstructured text or OCR input.  
2. **LLM Extraction Layer** – Parses and structures the narrative (incident type, entities, tone).  
3. **ML Feature Layer** – Scores measurable attributes such as provocation, panic, and keyword intensity.  
4. **Bridge Layer** – Validates schema and merges all numeric features.  
5. **HP Model (v1.6)** – Aggregates weighted scores into a single probability.  
6. **Audit Layer** – Logs results for retraining and compliance review.  

---

## Current Implementation  

### Completed Features (Built & Trained)  

| Feature | Purpose | Model Type | Dataset |
|----------|----------|-------------|----------|
| **prov_risk** | Detects provocational or hate-driven tone | Fine-tuned BERT / Logistic Regression | HateXplain |
| **panic_level** | Detects fear or panic intensity in language | Fine-tuned RoBERTa | GoEmotions + HateXplain |

These models form the **Linguistic Pattern Group** of the DDS G-Pattern family — the emotional and tonal foundation of the HP scoring pipeline.

---

## Training Summary (Colab Build)

The **panic_level** model was trained and validated in Google Colab using the following workflow:

1. **Dataset Integration** – Loaded and merged GoEmotions + HateXplain datasets, unified labels into a binary `panic_label`.  
2. **Fine-Tuning** – Trained `roberta-base` for three epochs using AdamW (`2e-5` LR, batch size `16`).  
3. **Exported Model Assets** – `config.json`, `tokenizer.json`, `vocab.json`, `merges.txt`, `model.safetensors`.  
4. **Batched Inference** – Generated `panic_level_features.csv` using GPU batching for speed.  
5. **Schema Validation** – Confirmed feature compliance with DDS incident schema v1.  
6. **Drive Storage** – Saved model under `/MyDrive/DDS_Models/panic_level_model/` for orchestration integration.  

This process now serves as the standard pattern for future DDS text-based feature builds.

---

## Repository Structure  

dds/
├── features/
│ ├── prov_risk/
│ │ ├── prov_risk_model.py
│ │ ├── prov_risk_inference.py
│ │ └── prov_risk_bridge.py
│ ├── panic_level/
│ │ ├── config.json
│ │ ├── merges.txt
│ │ ├── vocab.json
│ │ ├── tokenizer.json
│ │ ├── tokenizer_config.json
│ │ ├── special_tokens_map.json
│ │ └── model.safetensors ← stored in Drive (not GitHub)
│ └── keyword_intensity/ ← planned for HP v1.7
├── validation_log.txt
├── venv/
└── README.md


---

## Model Details — Panic Level (RoBERTa Fine-Tune)

| Setting | Value |
|----------|--------|
| Base model | roberta-base |
| Architecture | RobertaForSequenceClassification (binary) |
| Epochs | 3 |
| Batch size | 16 |
| Learning rate | 2 × 10⁻⁵ |
| Optimizer | AdamW |
| Dropout | 0.1 |
| Hidden size | 768 |
| Final loss | Train ≈ 0.08 / Val ≈ 0.16 |

---

## Integration Summary  

| Layer | Input | Output | Responsibility |
|--------|--------|--------|----------------|
| LLM Extraction | Raw report text | Structured JSON | Parsing / context understanding |
| prov_risk Model | Structured text | `prov_risk ∈ [0, 1]` | Hostility quantification |
| panic_level Model | Structured text | `panic_level ∈ [0, 1]` | Emotional intensity quantification |
| Bridge | Feature merge | Unified schema | Validation / standardization |
| HP Model | Numeric features | Hoax Probability ∈ [0, 1] | Aggregation & routing logic |

---

## Next Phase — Integration & Expansion  

| Goal | Description |
|------|--------------|
| **Feature Expansion (HP v1.7)** | Add `keyword_intensity` (TF-IDF baseline) and `pattern_burst` (n-gram similarity). |
| **Service Deployment** | Expose `panic_level` and `prov_risk` as REST microservices callable by the orchestration layer. |
| **Model Registry Alignment** | Register model metadata (version, bias metrics, latency) in the DDS Model Registry. |
| **Schema Automation** | Implement pre-export JSON schema validation hooks. |
| **Hybrid Aggregation** | Combine panic and prov_risk scores as a composite G-Pattern signal. |
| **Recalibration Pipeline** | Add periodic retraining and drift monitoring. |

---

## Compliance & Best Practices  

This module aligns with enterprise AI reliability frameworks:  

- *MIT Press (2024)* — *The Inherent Instability of LLMs*  
- *IBM Responsible AI Framework (2023)*  
- *Google Vertex AI Hybrid Pipelines (2024)*  

Separating language understanding from numeric scoring ensures **interpretability, reproducibility, and traceable AI decision-making.**

---



