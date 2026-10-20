import re
import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cynbit Lead Intelligence", page_icon="🎯", layout="wide")

SERVICES = {
    "AI Automation & Agents": ["ai agent", "automation", "llm", "chatbot", "voice agent", "workflow", "document processing", "generative ai"],
    "Custom Software Development": ["web app", "mobile app", "software", "platform", "dashboard", "backend", "api", "saas", "application"],
    "Cloud & Infrastructure": ["cloud", "aws", "azure", "migration", "devops", "docker", "kubernetes", "infrastructure", "deployment"],
    "Digital Marketing & SEO": ["seo", "digital marketing", "google ads", "meta ads", "marketing", "organic traffic", "campaign", "lead generation"],
    "CRM & Sales Automation": ["crm", "sales pipeline", "lead management", "follow-up", "customer relationship", "sales automation"],
    "AI Career / EdTech": ["coding assessment", "mock interview", "career", "learning platform", "adaptive learning", "student", "training", "education"],
    "Property Management (TenantEase)": ["property", "tenant", "rent", "occupancy", "property management", "lease"],
    "Review Intelligence (Revio)": ["review", "reputation", "sentiment", "customer feedback", "google reviews", "ratings"]
}
HIGH_INTENT = ["need a quote", "proposal", "budget approved", "ready to start", "urgent", "asap", "this month", "within 2 weeks", "within two weeks", "looking to hire", "schedule a call", "book a demo"]
MEDIUM_INTENT = ["exploring", "considering", "planning", "next quarter", "learn more", "requirements", "evaluate"]
LOW_INTENT = ["just curious", "student project", "free", "no budget", "research only"]

def analyze_lead(name, company, email, industry, message, budget, timeline):
    text = " ".join([name or "", company or "", email or "", industry or "", message or "", budget or "", timeline or ""]).lower()
    service_scores = {}
    for service, keywords in SERVICES.items():
        service_scores[service] = sum(1 for kw in keywords if kw in text)
    best_service = max(service_scores, key=service_scores.get)
    if service_scores[best_service] == 0:
        best_service = "Needs human review"

    score = 20
    reasons = ["Base score: 20"]
    if company.strip():
        score += 10; reasons.append("+10: company provided")
    if email.strip() and re.search(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        score += 10; reasons.append("+10: valid-looking email supplied")
    if len(message.strip()) >= 80:
        score += 15; reasons.append("+15: detailed project description")
    elif len(message.strip()) >= 30:
        score += 8; reasons.append("+8: some project detail")
    if budget in ["₹1L–₹5L", "₹5L–₹15L", "₹15L+"]:
        score += {"₹1L–₹5L": 10, "₹5L–₹15L": 15, "₹15L+": 20}[budget]
        reasons.append(f"+{ {'₹1L–₹₹5L':10}.get(budget, {'₹1L–₹5L':10,'₹5L–₹15L':15,'₹15L+':20}[budget]) }: budget range selected")
    if timeline in ["Within 2 weeks", "Within 1 month"]:
        score += 15; reasons.append("+15: near-term timeline")
    elif timeline == "1–3 months":
        score += 8; reasons.append("+8: planned timeline")
    if any(k in text for k in HIGH_INTENT):
        score += 15; reasons.append("+15: high-intent language")
    elif any(k in text for k in MEDIUM_INTENT):
        score += 7; reasons.append("+7: evaluation/planning language")
    if any(k in text for k in LOW_INTENT):
        score -= 15; reasons.append("-15: low buying intent / early research")
    score = max(0, min(100, score))
    if score >= 70:
        priority = "High"
        action = "Respond promptly; confirm scope, decision process, timeline, and schedule a discovery call."
    elif score >= 45:
        priority = "Medium"
        action = "Send a tailored follow-up and ask 1–2 questions to clarify scope, budget, and timeline."
    else:
        priority = "Low / nurture"
        action = "Share a relevant overview or case study and request missing qualification details."
    urgency = "Urgent" if any(k in text for k in ["urgent", "asap", "today", "tomorrow"]) or timeline == "Within 2 weeks" else "Normal"
    if best_service == "Needs human review":
        action = "Human review required: clarify the requested service before routing."
    return {
        "lead_score": score, "priority": priority, "service": best_service,
        "urgency": urgency, "recommended_action": action,
        "score_explanation": reasons,
        "follow_up": make_follow_up(name, company, best_service, message, timeline)
    }

def make_follow_up(name, company, service, message, timeline):
    first = (name or "").strip().split(" ")[0] if name.strip() else "there"
    company_line = f" at {company.strip()}" if company.strip() else ""
    summary = message.strip()
    if len(summary) > 240:
        summary = summary[:237].rsplit(" ", 1)[0] + "..."
    return (
        f"Subject: Next steps for your {service} enquiry\\n\\n"
        f"Hi {first},\\n\\n"
        f"Thank you for reaching out to Cynbit Technologies{company_line}. "
        f"From your note, it sounds like you are exploring {service.lower()}. "
        f"We would be happy to understand your goals and suggest a practical approach.\\n\\n"
        f"To prepare for a useful discussion, could you share any key requirements, "
        f"success criteria, or constraints we should consider? "
        f"We have noted your stated timeline as {timeline.lower() if timeline else 'not yet specified'}.\\n\\n"
        f"If convenient, we can arrange a short discovery call. This draft is for review by the Cynbit team before sending.\\n\\n"
        f"Regards,\\nCynbit Technologies"
    )

st.title("🎯 Cynbit Lead Intelligence & Qualification Assistant")
st.caption("Challenge prototype • Transparent baseline scoring • Human approval required")
st.info("This is a demonstration using explainable rules and keyword matching, not a trained predictive model. Do not enter sensitive personal data.")

with st.sidebar:
    st.header("Demo controls")
    st.write("Enter a sample business enquiry or use the example below.")
    if st.button("Load sample lead", use_container_width=True):
        st.session_state["sample"] = True
    st.markdown("---")
    st.caption("Prototype v1.0 | Local demo | No data is sent to an external service")

sample = st.session_state.get("sample", False)
default_name = "Aarav Sharma" if sample else ""
default_company = "Northstar Retail" if sample else ""
default_email = "aarav@example.com" if sample else ""
default_industry = "Retail / E-commerce" if sample else ""
default_message = ("We need an AI workflow to classify incoming customer enquiries, route qualified leads to our sales team, and connect with our CRM. We want to start within two weeks and would like a proposal."
                   if sample else "")
default_budget = "₹5L–₹15L" if sample else "Not specified"
default_timeline = "Within 2 weeks" if sample else "Not specified"

left, right = st.columns([1, 1])
with left:
    st.subheader("1. Incoming enquiry")
    with st.form("lead_form"):
        name = st.text_input("Contact name", value=default_name)
        company = st.text_input("Company", value=default_company)
        email = st.text_input("Business email", value=default_email)
        industry = st.text_input("Industry", value=default_industry)
        message = st.text_area("Enquiry / project description", value=default_message, height=180)
        budget = st.selectbox("Indicative budget", ["Not specified", "Under ₹1L", "₹1L–₹5L", "₹5L–₹15L", "₹15L+"],
                              index=["Not specified", "Under ₹1L", "₹1L–₹5L", "₹5L–₹15L", "₹15L+"].index(default_budget))
        timeline = st.selectbox("Desired timeline", ["Not specified", "Within 2 weeks", "Within 1 month", "1–3 months", "3+ months"],
                                index=["Not specified", "Within 2 weeks", "Within 1 month", "1–3 months", "3+ months"].index(default_timeline))
        submitted = st.form_submit_button("Analyze enquiry", type="primary", use_container_width=True)

with right:
    st.subheader("2. Qualification results")
    if submitted:
        result = analyze_lead(name, company, email, industry, message, budget, timeline)
        st.session_state["last_result"] = result
        st.session_state["last_lead"] = {"name":name,"company":company,"email":email,"industry":industry,"message":message,"budget":budget,"timeline":timeline}
    result = st.session_state.get("last_result")
    if result:
        m1, m2, m3 = st.columns(3)
        m1.metric("Lead score", f"{result['lead_score']}/100")
        m2.metric("Priority", result["priority"])
        m3.metric("Urgency", result["urgency"])
        st.markdown(f"**Recommended service:** {result['service']}")
        st.markdown("**Recommended next action**")
        st.write(result["recommended_action"])
        with st.expander("Why this score? (explainability)", expanded=True):
            for reason in result["score_explanation"]:
                st.write("• " + reason)
        st.markdown("**Follow-up draft — review before sending**")
        st.text_area("Editable email draft", value=result["follow_up"], height=260, key="draft_output")
        st.download_button("Download analysis as JSON", data=pd.Series({
            "lead_score":result["lead_score"],"priority":result["priority"],"urgency":result["urgency"],
            "service":result["service"],"recommended_action":result["recommended_action"],
            "score_explanation":result["score_explanation"],"follow_up":result["follow_up"]
        }).to_json(indent=2), file_name="lead_analysis.json", mime="application/json")
    else:
        st.write("Submit an enquiry to see its score, recommended service, urgency, rationale, and follow-up draft.")
        st.markdown("- **Lead score:** transparent heuristic score (0–100)")
        st.markdown("- **Service match:** keyword-based routing across Cynbit's public service/product areas")
        st.markdown("- **Human-in-the-loop:** no emails sent and no CRM changes made")

st.markdown("---")
st.subheader("3. Prototype limitations and next step")
st.write("This proof of concept uses a deterministic baseline so reviewers can inspect every scoring rule. It does not learn from historical conversions, verify company information, connect to a CRM, or use an LLM. A production version should be validated on consented historical data, calibrated with sales staff, monitored for drift, and integrated only after access controls and approval workflows are in place.")
