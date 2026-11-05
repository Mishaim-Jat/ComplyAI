# ComplyAI — AI-Powered Cybersecurity Compliance Analysis

**Completed: March 2026** · **Team Project: Trojan Hex** · **CSIT321**

ComplyAI is an AI-powered cybersecurity compliance platform that uses Retrieval-Augmented Generation (RAG) to analyse organisational policy documents against the **NIST Cybersecurity Framework (NIST CSF 2.0)**.

The platform combines semantic and keyword-based retrieval with locally hosted large language models to identify potential compliance gaps, map findings to relevant framework controls, recommend remediation actions and generate structured compliance reports.

## Overview

Reviewing cybersecurity policies against regulatory frameworks is a time-consuming process that requires identifying relevant controls, evaluating policy statements and documenting areas of non-compliance.

ComplyAI was developed to assist this process through an AI-driven analysis workflow. It retrieves relevant NIST controls, evaluates policy content against those controls and produces evidence-based findings for compliance officers to review.

The system also incorporates risk assessment, compliance questionnaires, reporting and real-time collaboration into a single web application.

## Key Features

- **AI-Powered Compliance Gap Detection:** Analyse uploaded policy documents and identify potential gaps against NIST CSF 2.0 controls.
- **Hybrid Retrieval-Augmented Generation:** Combine FAISS semantic search and BM25 keyword retrieval, with Reciprocal Rank Fusion (RRF) to consolidate relevant results.
- **Local LLM Integration:** Use Ollama-hosted models for document analysis, embedding generation and compliance-related AI workflows.
- **Evidence-Based Findings:** Ground generated findings in retrieved controls and source-document evidence, with confidence scoring and false-positive filtering.
- **AI Remediation Recommendations:** Generate recommendations to address identified compliance gaps.
- **Risk Assessment and Heatmaps:** Evaluate findings using likelihood and impact scores and visualise risk exposure through a 5×5 risk heatmap.
- **NIST CSF Questionnaire:** Collect structured compliance information across Govern, Identify, Protect, Detect, Respond and Recover.
- **Compliance Reporting:** Generate structured reports with PDF and DOCX export support.
- **Real-Time Collaboration:** Support shared assessment workflows, messaging, presence indicators and collaborative review.
- **Framework Management:** Support framework ingestion, version management and dynamic retrieval-index activation.

## Technical Architecture

ComplyAI uses a Python and Flask-based application architecture, with separate presentation, service, AI processing and persistence responsibilities.

| Layer | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | Jinja2, HTML, CSS, JavaScript |
| AI and LLM | Ollama, Qwen2.5 3B, CybersecurityRiskAnalyst |
| Embeddings | Qwen3 Embedding |
| RAG and Retrieval | LangChain, FAISS, Rank-BM25, Reciprocal Rank Fusion |
| Document Processing | LangChain PDF Loader, RecursiveCharacterTextSplitter, PySBD |
| Data Storage | SQLite, FAISS indexes, local filesystem |
| Real-Time Communication | Flask-SocketIO, WebSockets |
| Data Validation | Pydantic |
| Reporting and Visualisation | ReportLab, python-docx, Matplotlib |
| Testing | PyTest |

## How It Works

1. **Document Ingestion:** Users upload PDF policy documents through the web interface.
2. **Text Extraction and Processing:** The application extracts document text, segments it into sentences and prepares content for batch analysis.
3. **Hybrid Retrieval:** FAISS retrieves semantically relevant NIST controls, while BM25 identifies keyword-based matches.
4. **Rank Fusion:** Reciprocal Rank Fusion combines the retrieval results to prioritise relevant controls.
5. **LLM Analysis:** The locally hosted language model evaluates policy statements against retrieved control requirements.
6. **Gap Detection:** Potential compliance gaps are extracted with supporting evidence, control references, severity levels, confidence scores and recommendations.
7. **Risk Assessment:** Findings are consolidated and evaluated using likelihood and impact scores.
8. **Reporting:** Results feed into compliance dashboards, risk heatmaps and downloadable reports.

## My Contribution

**AI System Engineer — RAG Architecture and Framework Mapping**

As a member of Team Trojan Hex, my primary responsibility was the design of the RAG architecture and implementation of the RAG-based compliance gap detection system.

My contribution focused on:

- Designing the RAG architecture for retrieving relevant NIST CSF controls during policy analysis.
- Implementing the retrieval-based compliance gap detection workflow.
- Developing the framework mapping logic connecting policy content to relevant cybersecurity control requirements.
- Working with semantic and keyword-based retrieval to improve the relevance of control selection.
- Supporting the integration of retrieved framework context into the AI-assisted compliance analysis process.

This work strengthened my practical experience in **Retrieval-Augmented Generation, information retrieval, semantic search, NLP, framework mapping and AI system design**.

## Application and Screenshots


## Screenshots

### 1. Dashboard & Navigation

![Main Dashboard](screenshots/Main_Dashboard_page.png)

![Documents Page](screenshots/Documents_Page.png)

![Calendar Page](screenshots/Calendar_Page.png)

### 2. Document Management

![Upload Documents](screenshots/Upload_Documents_page.png)

![Upload and Analysis](screenshots/Upload_and_Analysis_Page.png)

![Download Report](screenshots/download_report.png)

### 3. AI-Powered Compliance Analysis

![Compliance Gap Analysis](screenshots/Compliance_Gap_Analysis_Page.png)

![Compliance Gap Analysis Details](screenshots/Compliance_gap_analysis.png)

![High Priority Gap](screenshots/high_priority_gap.png)

![NIST Compliance Questionnaire](screenshots/NIST_compliance_questionaire.png)

### 4. Risk Assessment & Management

![Risk Overview](screenshots/Risk_overview_page.png)

![Risk Heatmap](screenshots/Risj_Heatmap_page.png)

![Risk Heatmap Items](screenshots/Risk_Heatmap_items.png)

![Risk Assessment](screenshots/risk_assessment.png)

![Risk Appetite Assessment](screenshots/Risk_Appetite_assesment.png)

![Risk Recommendations](screenshots/Risk_Reccomendations.png)

### 5. Framework Management

![Framework Management](screenshots/Framework_management.png)

![Framework Management Page](screenshots/Framework_managememt_page.png)

### 6. AI Chatbot & Collaboration

![AI Chatbot](screenshots/Chat_Bot.png)

![Calendar Notes](screenshots/Notes_on_Calendar.png)

![Share Link](screenshots/Add_Viewer_and_share_link.png)

![Share Link Expiry](screenshots/share_link_expiry.png)

### 7. Administration & User Management

![User Management](screenshots/Admin_user_management.png)

![Admin Status Change](screenshots/Admin_Status_change.png)

![Account Settings](screenshots/Account_settings_Page.png)

![Organisation Information](screenshots/Add_organisation_information.png)

### 8. Authentication

![Sign In](screenshots/Signin_Page.png)

![Sign Up](screenshots/signup_Page.png)

### 9. Additional Screenshots

![Compliance Assessment](screenshots/Compliance_assesment.png)

![Edited Compliance Report](screenshots/edit_complaince_report_gap_analysis.png)

![Report](screenshots/Report.png)

![Picture 1](screenshots/Picture1.png)


The application includes a compliance dashboard, document analysis workflow, risk assessment visualisations, questionnaire interface, collaboration features and report-generation functionality.

> Add screenshots of the actual application here. Recommended images: dashboard, document upload, compliance findings, risk heatmap and generated report.

## Running Locally

ComplyAI was developed as a locally hosted application. It was not released as a publicly hosted production service.

### Prerequisites

- Python
- Ollama
- Git
- At least 16 GB RAM (32 GB recommended by the project report)
- The project repository and its `requirements.txt` file

### Installation

Clone the repository:

```bash
git clone <https://github.com/Mishaim-Jat/ComplyAI>
cd <repository-folder>
```

Create and activate a virtual environment:

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Ollama Models

Install Ollama and make the required models available locally. The project report identifies the following models:

- `qwen2.5:3b` — report generation and compliance gap analysis
- `qwen3-embedding` — document embeddings
- `saki007ster/CybersecurityRiskAnalyst` — specialised cybersecurity risk assessment

Pull the models using the corresponding Ollama model identifiers:

```bash
ollama pull qwen2.5:3b
ollama pull qwen3-embedding
ollama pull saki007ster/CybersecurityRiskAnalyst
```

### Start the Application

The project report identifies `run.py` as the application launcher and documents local Flask-SocketIO hosting on port `5005`.

```bash
python run.py
```

Open the local application in your browser:

```text
http://localhost:5005
```

*Note: Environment variables and any additional configuration required by the repository must be set before launching. Confirm the current repository configuration and model identifiers before running the application.*

## Testing and Limitations

The project included a testing plan covering authentication, document uploads, RAG processing, compliance analysis, database operations, reporting and application workflows.

The documented MVP scope and known limitations include:

- PDF document ingestion was the supported policy-document format for the MVP.
- Local LLM inference depends on available hardware and Ollama model availability.
- FAISS index persistence across server restarts was identified as a limitation in the testing documentation.
- Large-scale performance testing, advanced penetration testing and production infrastructure hardening were outside the MVP scope.
- AI-generated compliance findings require human review before being treated as final compliance decisions.

## Project Status

**Completed academic software engineering and AI team project — March 2026.**

ComplyAI demonstrates the application of RAG, hybrid information retrieval and locally hosted LLMs to a practical cybersecurity compliance use case.

## Team

**Team Trojan Hex** — CSIT321

Developed collaboratively, with responsibilities spanning AI engineering, RAG architecture, backend development, frontend engineering, database integration and security engineering.
