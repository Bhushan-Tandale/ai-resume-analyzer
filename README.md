# 📄 AI Resume Analyzer

An AI-powered Resume Analysis and Recruitment Automation system built
using **Streamlit, Groq AI, and n8n**.

This application allows recruiters to upload resumes, extract structured
candidate data using AI, evaluate candidates against hiring criteria,
and automate email notifications through workflow automation.

------------------------------------------------------------------------

## 🚀 Features

-   Upload and analyze **PDF resumes**
-   AI-powered **resume parsing**
-   Extract structured candidate data:
    -   Name
    -   Email
    -   Location
    -   Skills
    -   Experience
    -   Education
-   Generate **AI candidate summary**
-   Calculate **candidate match score**
-   Provide **hiring recommendation**
-   Trigger **n8n automation workflow**
-   Send **automated email notifications**
-   Display **automation status in the dashboard**

------------------------------------------------------------------------

## 🧠 AI Capabilities

The system uses **Groq LLM (Llama 3.1)** to:

-   Understand resume content
-   Extract structured information
-   Evaluate candidates against hiring criteria
-   Generate candidate insights

------------------------------------------------------------------------

## 🏗 System Architecture

User → Streamlit App → Groq AI\
↓\
Structured Resume Data\
↓\
n8n Webhook Automation\
↓\
Decision Engine\
↓\
Email Notification\
↓\
Results Returned to Streamlit

------------------------------------------------------------------------

## 📊 Application Workflow

1.  Upload Resume (PDF)
2.  Enter Hiring Criteria
3.  AI analyzes resume
4.  Structured candidate data extracted
5.  Candidate evaluated against criteria
6.  Automation workflow triggered via n8n
7.  Email sent if conditions are met
8.  Results displayed in dashboard

------------------------------------------------------------------------

## 🛠 Tech Stack

  Technology   Purpose
  ------------ ---------------------
  Python       Backend logic
  Streamlit    Web interface
  Groq AI      Resume analysis
  PyMuPDF      PDF text extraction
  Pandas       Data visualization
  n8n          Workflow automation

------------------------------------------------------------------------

## ⚙️ Installation (Local)

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
    cd ai-resume-analyzer

Install dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

------------------------------------------------------------------------

## ☁️ Deployment (Streamlit Cloud)

1.  Push the repository to GitHub
2.  Go to https://share.streamlit.io
3.  Click **New App**
4.  Select your repository
5.  Choose **app.py** as the main file
6.  Deploy the application

------------------------------------------------------------------------

## 🔑 Environment Secrets

Add the following secrets in **Streamlit Cloud → App Settings →
Secrets**

    GROQ_API_KEY="your_groq_api_key"

    N8N_WEBHOOK_URL="your_n8n_webhook_url"

These keys are required for:

-   AI resume analysis
-   Automation workflow trigger

------------------------------------------------------------------------

## 📧 Email Automation

The system integrates with **n8n workflow automation**.

Workflow steps:

1.  Receives candidate data via webhook
2.  Evaluates match score
3.  Sends email if criteria are met
4.  Returns automation status to Streamlit

------------------------------------------------------------------------

## 📌 Example Hiring Criteria

    Looking for a data analyst with SQL, Python and 2+ years of experience

------------------------------------------------------------------------

## 👨‍💻 Author

AI Resume Analyzer Project\
Built using **Streamlit + Groq AI + n8n**
