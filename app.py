import streamlit as st
import requests
import json
import fitz
import re
import pandas as pd
from groq import Groq

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==============================
# HELPER FUNCTIONS
# ==============================

def safe_display(value):

    if isinstance(value, dict):
        return ", ".join(value.keys())

    if isinstance(value, list):
        return ", ".join(str(v) for v in value)

    return str(value)


def extract_text_from_pdf(file):

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return text


def safe_json_extract(text):

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group(0))

    except:
        return None


# ==============================
# LOAD SECRETS
# ==============================

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]

client = Groq(api_key=GROQ_API_KEY)

# ==============================
# HEADER
# ==============================

st.title("📄 AI Resume Analyzer")
st.caption("Resume Parsing • Candidate Insights • Automation")

st.divider()

# ==============================
# INPUTS
# ==============================

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

criteria = st.text_area(
    "Enter Hiring Criteria",
    placeholder="Example: Looking for a Business Analyst with SQL and Python with 2+ years experience."
)

# ==============================
# ANALYZE BUTTON
# ==============================

if st.button("🚀 Analyze Resume"):

    if not resume_file or not criteria:

        st.warning("Please upload resume and enter hiring criteria.")

    else:

        resume_text = extract_text_from_pdf(resume_file)

        if len(resume_text) > 12000:
            resume_text = resume_text[:12000]

        with st.spinner("Analyzing candidate..."):

            prompt = f"""
You are an AI recruitment assistant.

Analyze the resume against the hiring criteria.

Return ONLY valid JSON.

Structure:

{{
"candidate_name":"",
"email":"",
"location":"",
"current_role":"",
"years_of_experience":"",
"skills":[],
"education":"",
"match_score":0,
"hiring_recommendation":"",
"candidate_summary":""
}}

Rules:

match_score must be between 0 and 100

Hiring recommendation rules:

score >= 80 → Hire
60-79 → Maybe
<60 → Reject

candidate_summary must summarize:
- experience
- skills
- education
- achievements

HIRING CRITERIA:
{criteria}

RESUME TEXT:
{resume_text}
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Return JSON only"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content

            extracted_data = safe_json_extract(raw_output)

            if not extracted_data:

                st.error("AI failed to extract resume data.")
                st.write(raw_output)
                st.stop()

            st.session_state["resume_text"] = resume_text
            st.session_state["criteria"] = criteria
            st.session_state["data"] = extracted_data


# ==============================
# DASHBOARD
# ==============================

if "data" in st.session_state:

    data = st.session_state["data"]

    st.subheader("📊 Candidate Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Candidate Name",
        safe_display(data.get("candidate_name", "Unknown"))
    )

    col2.metric(
        "Years of Experience",
        safe_display(data.get("years_of_experience", "Unknown"))
    )

    col3.metric(
        "Current Role",
        safe_display(data.get("current_role", "Unknown"))
    )

    col4.metric(
        "Location",
        safe_display(data.get("location", "Unknown"))
    )

    st.divider()

# ==============================
# CONTACT INFO
# ==============================

    st.subheader("📧 Contact Information")

    st.write("Email:", safe_display(data.get("email", "Not found")))

    st.divider()

# ==============================
# SUMMARY
# ==============================

    st.subheader("🧠 Candidate Summary")

    st.info(
        safe_display(data.get("candidate_summary", "No summary available"))
    )

# ==============================
# SKILLS
# ==============================

    st.subheader("🛠 Skills Detected")

    skills = data.get("skills", [])

    if isinstance(skills, str):
        skills = [skills]

    if isinstance(skills, dict):
        skills = list(skills.keys())

    if skills:

        cols = st.columns(3)

        for i, skill in enumerate(skills):
            cols[i % 3].markdown(f"✔ {skill}")

    else:
        st.write("No skills detected")

    st.divider()

# ==============================
# EDUCATION
# ==============================

    st.subheader("🎓 Education")

    st.write(safe_display(data.get("education", "Unknown")))

    st.divider()

# ==============================
# STRUCTURED DATA TABLE
# ==============================

    st.subheader("📋 Structured Resume Data")

    df = pd.DataFrame({
        "Field": list(data.keys()),
        "Value": [safe_display(v) for v in data.values()]
    })

    st.dataframe(df, use_container_width=True, hide_index=True)

# ==============================
# RAW JSON OUTPUT (REQUIREMENT)
# ==============================

    with st.expander("🔎 Structured Data Extracted (JSON)"):
        st.json(data)

    st.divider()

# ==============================
# AUTOMATION WORKFLOW
# ==============================

    st.subheader("📡 Automation Workflow")

    recipient_email = st.text_input(
        "Recipient Email",
        placeholder="recruiter@company.com"
    )

    if st.button("📡 Send to Automation (n8n)"):

        if not recipient_email:

            st.warning("Please enter recipient email")

        else:

            score = data.get("match_score", 0)
            decision = data.get("hiring_recommendation", "None")

            payload = {

                "candidate_name": data.get("candidate_name"),
                "match_score": score,
                "hiring_decision": decision,
                "recipient_email": recipient_email,
                "criteria": st.session_state["criteria"]
            }

            response = requests.post(N8N_WEBHOOK_URL, json=payload)

            if response.status_code == 200:

                result = response.json()

# ==============================
# FINAL ANALYTICAL ANSWER
# ==============================

                st.subheader("🧠 Final Analytical Answer")

                st.write(
                    result.get(
                        "final_answer",
                        "Candidate analysis completed and automation workflow executed."
                    )
                )

# ==============================
# GENERATED EMAIL BODY
# ==============================

                st.subheader("📧 Generated Email Body")

                st.text_area(
                    "Email Content",
                    result.get("email_body", "Email was generated and sent."),
                    height=200
                )

# ==============================
# EMAIL AUTOMATION STATUS
# ==============================

                st.subheader("📨 Email Automation Status")

                status = result.get("status", "")

                if status == "SENT":
                    st.success("Alert Email Status: SENT")

                elif status == "NOT_SENT":
                    st.error("Status: Condition Not Met")

                else:
                    st.warning("Unknown automation status")
