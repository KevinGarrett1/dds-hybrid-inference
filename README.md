# DDS Hybrid Inference Pipelines  
### Illustrated with a Hostile Hoax Report  

---

## Purpose  
This README explains how the **DDS Hybrid Inference Pipeline** integrates Harshita’s GPT-based extraction service with the ML scoring layer using the `prov_risk` feature as an example.  
It demonstrates how the system interprets natural language, quantifies tone, and calculates a reproducible hoax probability.

---

## Overview  
The DDS Hoax Reporting System combines **LLM reasoning** and **ML precision** into a single pipeline.

- **LLM Layer** handles unstructured text, extracting entities, context, and meaning.  
- **ML Feature Layer** quantifies tone, hostility, and other measurable signals.  
- **HP v1.6 Logistic Model** aggregates all numeric features into a calibrated probability score.

This design keeps Harshita’s GPT-4o logic intact while adding deterministic, auditable ML scoring aligned with MIT Press and enterprise AI best practices.

---

## 1. Input Layer — The Raw Report  
**Role:** Collect unverified text or OCR data from users or monitoring sources.

**Example**  
> “Those filthy marsheads are back at the refinery. The three-finger freaks keep waving their antenna things like they’re casting spells. They hate humans and they said they’ll ‘quantum blow this place sky-high.’ Management ignores it, but if those creatures stay, somebody’s getting vaporized.”

**Challenge**  
Free-form language mixes fear, rumor, and bias. It must be structured and quantified before any decision logic can be applied.

---

## 2. LLM Layer — Harshita’s GPT Extraction Service  
**File:** `gpt_incident_agent.py`  
**Owner:** Harshita  
**Model:** GPT-4o (OpenAI API)

**Purpose**  
The LLM interprets and structures messy input text into standardized JSON fields that downstream ML models can process.

**Example Output**
```json
{
  "incident_id": "rpt-20251102-019",
  "incident_type": "bomb_threat",
  "location": "Refinery #12, East Lot",
  "text": "Those filthy marsheads ... vaporized.",
  "suspect_description": "group referred to as 'marsheads', three-fingered, with antennae",
  "reported_weapons": "quantum device (verbal claim)",
  "reporter_tone": "hostile / fearful"
}
```
Integration Notes

The LLM handles semantic understanding and context extraction.

It does not assign numeric scores, which prevents non-deterministic outputs.

Output is passed directly to the ML feature layer for measurable evaluation.

3. ML Feature Layer — prov_risk Module
File: prov_risk_inference.py
Owner: Kevin

Purpose
Quantify provocational and emotional tone using a deterministic ML model fine-tuned on the HateXplain dataset.

Example Output

```
json
{
  "prov_risk": 0.94,
  "breakdown": {
    "keyword_intensity": 0.91,
    "panic_level": 0.89,
    "group_targeting": 0.96
  }
}
```
Why It Matters

Converts hate-filled or panic-driven language into a measurable value.

Produces identical results for identical input, guaranteeing reproducibility.

Creates a consistent numeric foundation for the HP scoring layer.

4. Bridge Layer — Data Unification
File: bridge_prov_risk.py
Purpose: Merge LLM output and ML features into a unified schema for downstream scoring.

Example Merged Object

```
json
{
  "incident_type": "bomb_threat",
  "location": "Refinery #12, East Lot",
  "prov_risk": 0.94,
  "suspect_description": "...",
  "reported_weapons": "quantum device (verbal claim)"
}
```
Integration Logic

Acts as the interface between GPT output and ML processing.

Validates fields and enforces schema consistency.

Ensures data compatibility for the logistic scoring model.

5. HP v1.6 Logistic Model — Final Scoring
File: hp_model_v16.py
Owner: Kevin

Purpose
Compute the final Hoax Probability (HP) and assign severity.

**Core Equation**

```ini
HP = σ(θ₀ + θ_type + Σ w_g × G_g)
```

Example Output

```json
{
  "hp": 0.81,
  "severity": "high",
  "route": "SOC urgent review",
  "contributors_top3": [
    {"feature": "prov_risk", "value": 0.94},
    {"feature": "weapon_claim", "value": 1.0},
    {"feature": "lack_of_corroboration", "value": 0.8}
  ]
}
```


Interpretation

Harshita’s rules flag a high-urgency bomb threat.

The prov_risk model confirms extreme hostile tone.

The HP model aggregates these features and routes the event for human review to prevent false escalation.

6. Final Output — Interpretable and Actionable
Unified Scoring Example

```
json
{
  "incident_type": "bomb_threat",
  "prov_risk": 0.94,
  "hp": 0.81,
  "severity": "high",
  "route": "verify_and_alert",
  "summary": "High-severity bomb threat containing extreme bias language. Likely hoax but requires immediate SOC validation."
}
```

Routing Options

Verify and Alert: Analyst review within SOC.

Escalate: Notify authorities if corroborated.

Archive: Record for retraining and calibration if confirmed false.

LLM and ML Roles in the DDS Hybrid Architecture
The DDS architecture uses two intelligence layers that complement each other.
The LLM layer understands language.
The ML layer measures and scores it.
This separation keeps the system smart, stable, and accountable.

LLM Role — Interpretive Intelligence
File: gpt_incident_agent.py
Owner: Harshita
Model: GPT-4o

Purpose
The LLM interprets unstructured text and extracts structured information such as incident type, location, tone, and key entities.

Function	Description
Context Extraction	Identifies key details about the event.
Entity Detection	Finds names, objects, or places.
Tone Tagging	Detects fear, anger, or hostility.
Normalization	Produces clean, consistent JSON output.

Why It Matters
GPT models are powerful interpreters but inconsistent for scoring.
Keeping them focused on understanding rather than judgment ensures the pipeline stays reliable.

Key Idea: The LLM reads between the lines and gives structure to language.

ML Role — Quantitative Intelligence
Files: prov_risk_inference.py, hp_model_v16.py
Owner: Kevin

Purpose
The ML layer converts structured text from the LLM into numeric features. It measures emotional tone, risk, and intensity, then aggregates those signals into a probability score.

Function	Description
Feature Quantification	Converts tone and phrasing into numeric values.
Reproducible Scoring	Guarantees stable, identical results for the same input.
Calibration	Uses real datasets for accuracy and bias control.
Aggregation	Combines multiple features into a final probability.

Why It Matters
This layer grounds the system in math.
It produces scores that can be tested, audited, and recalibrated.
It provides the reproducibility that LLMs lack.

Key Idea: The ML layer measures the lines and turns words into numbers.

Combined Workflow
Step	Component	Type	Responsibility
1	LLM (GPT-4o)	Interpretive	Reads and structures text.
2	ML Features	Quantitative	Converts tone into numeric scores.
3	HP Logistic Model	Decision	Aggregates results into a final probability.

Process Summary

The LLM interprets what is said.

The ML model quantifies how it is said.

The HP model makes a decision based on data.

Why the Separation Matters
Keeping the layers distinct ensures both intelligence and consistency.
The LLM adds flexibility and understanding.
The ML layer adds stability and accountability.
Together they create a pipeline that is context-aware and scientifically grounded.

Attribute	LLM Layer	ML Layer
Strength	Handles unstructured language	Produces stable numeric outputs
Limitation	Non-deterministic	Requires structured input
Output	Structured JSON	Numeric scores and probabilities
Example Files	gpt_incident_agent.py	prov_risk_inference.py, hp_model_v16.py

In short
The LLM interprets meaning.
The ML model quantifies it.
The HP model decides what to do next.

End-to-End Summary
Layer	File	Owner	Role	Determinism
LLM Extraction	gpt_incident_agent.py	Harshita	Interpret and structure input	Controlled stochastic
ML Feature	prov_risk_inference.py	Kevin	Quantify tone and hostility	Deterministic
Bridge	bridge_prov_risk.py	Kevin	Merge JSON and features	Deterministic
HP Logistic	hp_model_v16.py	Kevin	Aggregate and route	Deterministic

Compliance and Best Practices
This architecture aligns with guidance from:

MIT Press (2024) The Inherent Instability of Large Language Models

IBM Responsible AI Framework (2023)

Google Cloud Vertex AI Hybrid Pipelines (2024)

By separating LLM interpretation from ML scoring, DDS achieves reproducible, auditable, and trustworthy inference at enterprise scale.

Author: Kevin Garrett
Machine Learning and AI Engineering Intern
Deep Defense Solutions
Last updated: November 2025

yaml
Copy code

---
