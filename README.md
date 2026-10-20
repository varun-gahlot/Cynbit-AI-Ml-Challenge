# Cynbit AI/ML Challenge — Lead Intelligence & Qualification Assistant

## Selected opportunity
An AI-assisted workflow to triage inbound business enquiries, recommend a relevant Cynbit service/product area, prioritize follow-up, explain the score, and draft a human-reviewed response.

This aligns with Cynbit's public positioning around AI agents that manage leads, LLM automation, CRM automation, and its software/product ecosystem. It is a proposed opportunity, not a claim that Cynbit currently lacks such a system.

## Files
- `AI_Opportunity_Report.docx` — business/industry analysis and prioritized opportunities.
- `Technical_Approach_Report.docx` — architecture, data pipeline, model choices, prompts, evaluation, risks, and roadmap.
- `app.py` — runnable Streamlit proof of concept.
- `requirements.txt` — Python dependencies.
- `sample_leads.csv` — synthetic demo records.
- `README.md` — setup and demo instructions.

## Run locally (Windows PowerShell)
```powershell
cd path\to\cynbit_ai_challenge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown in the terminal (normally `http://localhost:8501`). Click **Load sample lead**, then **Analyze enquiry**.

## What the prototype does
1. Accepts an enquiry and optional qualification fields.
2. Uses transparent keyword matching to suggest a service area.
3. Produces a heuristic score, priority, urgency, and rationale.
4. Drafts a follow-up email for human review.
5. Allows the result to be downloaded as JSON.

## Important limitation
The prototype intentionally uses an explainable rules-based baseline rather than claiming to have trained a predictive model. It has no CRM integration, external LLM/API call, or email-sending capability. All sample records are synthetic. A production ML model requires historical, consented lead and conversion data and a measured offline evaluation.

## Suggested demo script (3–5 minutes)
1. Load the sample lead and analyze it.
2. Point out the score breakdown and service recommendation.
3. Change the budget or timeline and rerun to show how transparent rules affect priority.
4. Edit the email draft to demonstrate human oversight.
5. Explain the roadmap from rules baseline → labelled data → calibrated classifier/LLM extraction → CRM integration → monitored rollout.

## Public sources reviewed
- Cynbit homepage: https://www.cynbit.in/
- Services: https://www.cynbit.in/services
- Products: https://www.cynbit.in/products
- Contact page: https://www.cynbit.in/contact
- Microsoft Learn, Sales Qualification Agent overview: https://learn.microsoft.com/en-us/dynamics365/sales/sales-qualification-agent
- Salesforce, AI Lead Nurturing: https://www.salesforce.com/sales/engagement-platform/ai-lead-nurturing/
