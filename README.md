# ComplyAI: AI-Powered Cybersecurity Compliance Analysis

**Completed: March 2026**
**Team Project | Team Trojan Hex**

ComplyAI is an AI-powered cybersecurity compliance platform designed to support gap analysis against the NIST Cybersecurity Framework (NIST CSF). It combines document processing, hybrid information retrieval, and locally hosted large language models to help analyse cybersecurity documentation against relevant compliance controls.

## Project Overview

Cybersecurity compliance assessments can involve reviewing large volumes of documentation and mapping evidence to relevant framework controls. ComplyAI aims to streamline this process through an AI-assisted workflow that retrieves relevant controls and generates analysis to support compliance reviews.

## Key Features

* **Document Upload:** Upload documents for compliance analysis.
* **AI-Assisted Gap Analysis:** Analyse documentation against relevant NIST CSF controls.
* **Hybrid Retrieval:** Combine semantic search and keyword-based retrieval to find relevant information.
* **Local LLM Integration:** Use Ollama to run a language model locally.
* **Source-Aware Analysis:** Retrieve supporting information to help ground generated results.
* **Role-Based Access:** Support Admin, ComplianceOfficer, and Viewer roles.
* **Web Interface:** Interact with the application through a Flask-powered interface.

## Technical Stack

| Component             | Technologies                 |
| --------------------- | ---------------------------- |
| Backend               | Python, Flask                |
| Language Model        | Ollama, Qwen3 Embeddings     |
| Information Retrieval | FAISS, BM25                  |
| Document Processing   | PySBD                        |
| Frontend              | HTML, CSS, JavaScript        |
| Framework             | NIST Cybersecurity Framework |

## How It Works

1. **Upload:** A user submits a document for analysis.
2. **Process:** The application processes the document and prepares its content for retrieval.
3. **Retrieve:** Hybrid retrieval combines semantic similarity with keyword matching to identify relevant controls and supporting information.
4. **Analyse:** The local language model uses retrieved context to support the compliance analysis.
5. **Review:** Users access the resulting analysis through the web interface.

## Application Endpoints

| Endpoint    | Purpose                                |
| ----------- | -------------------------------------- |
| `/upload`   | Handles document uploads               |
| `/analyze`  | Runs the compliance analysis           |
| `/progress` | Provides analysis progress information |

## My Contribution

As part of Team Trojan Hex, I worked on the core backend and AI-powered analysis workflow. My work focused on connecting the application logic with document processing, hybrid retrieval, and language-model-assisted compliance analysis.

This project strengthened my practical experience with Python backend development, retrieval-augmented generation (RAG), information retrieval, and integrating AI components into a web application.

## Screenshots

Screenshots of the application interface and analysis workflow will be added here.

<!-- Add screenshots to a folder such as screenshots/ and embed them below.
Example:
![ComplyAI Dashboard](screenshots/dashboard.png)
-->

## Running Locally

ComplyAI was developed as a local application and has not been deployed as a publicly hosted service.

To explore the project locally:

1. Clone this repository.
2. Install the required Python dependencies from the project's dependency file, if provided.
3. Ensure the required Ollama model is installed and available.
4. Configure the application using your local environment.
5. Start the Flask application using the appropriate entry point and instructions for the project.

Exact dependency installation and startup commands should be documented after verifying the project's configuration.

## Project Status

**Completed academic team project.** This repository presents the project as a software engineering and AI portfolio piece. A public live demo is not currently available.

## Acknowledgements

Developed collaboratively by **Team Trojan Hex**.
