# compliance.py


import os
import re
import fitz
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai


SIMILARITY_THRESHOLD = 0.45
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY environment variable")


client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-2.5-flash"


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


SECURITY_KEYWORDS = [
    "data", "encryption", "password", "backup", "access",
    "authentication", "authorization", "confidentiality",
    "integrity", "availability", "logging", "audit",
    "monitoring", "risk", "controls", "incident", "security",
    "privacy", "compliance", "policy", "standard",
    "network", "system", "firewall", "mfa",
    "disaster recovery", "business continuity", "incident response",
    "vulnerability",
]


# ---------------- Helper functions ----------------


def extract_pdf_pages_lines(pdf_path):
    doc = fitz.open(pdf_path)
    pages_lines = []
    for page_num, page in enumerate(doc, start=1):
        lines = page.get_text("text").splitlines()
        for line_num, line in enumerate(lines, start=1):
            clean_line = re.sub(r"\s+", " ", line).strip()
            if clean_line:
                pages_lines.append({
                    "page": page_num,
                    "line": line_num,
                    "text": clean_line
                })
    return pages_lines


def filter_security_lines(lines):
    return [l for l in lines if any(k in l["text"].lower() for k in SECURITY_KEYWORDS)]


# ---------------- Main analyze function ----------------


def analyze(policy_path):
    NIST_PDF = "C:/Users/LENOVO/OneDrive/Desktop/Adalia_complyAI/NIST.CSWP.29.pdf"
    nist_lines = extract_pdf_pages_lines(NIST_PDF)
    policy_lines_all = extract_pdf_pages_lines(policy_path)
    policy_lines = filter_security_lines(policy_lines_all)


    nist_texts = [l["text"] for l in nist_lines]
    policy_texts = [l["text"] for l in policy_lines]


    nist_embeddings = embedding_model.encode(nist_texts, convert_to_numpy=True)
    policy_embeddings = embedding_model.encode(policy_texts, convert_to_numpy=True)


    # Find gaps
    gaps = []
    for i, p_emb in enumerate(policy_embeddings):
        similarities = cosine_similarity([p_emb], nist_embeddings)[0]
        best_score = float(np.max(similarities))
        best_idx = int(np.argmax(similarities))


        if best_score < SIMILARITY_THRESHOLD:
            gaps.append({
                "policy_text": policy_lines[i]["text"],
                "policy_page": policy_lines[i]["page"],
                "policy_line": policy_lines[i]["line"],
                "nist_text": nist_lines[best_idx]["text"]
            })


    if not gaps:
        return ["✅ All policy lines appear compliant with NIST standards."]


    # Prepare LLM prompt
    findings = ""
    for gap in gaps:
        findings += f"Policy (Page {gap['policy_page']}, Line {gap['policy_line']}): \"{gap['policy_text']}\"\nNIST: \"{gap['nist_text']}\"\n\n"


    prompt = f"""
You are a NIST cybersecurity auditor.
For each policy line below, return EXACTLY 3 lines in this format:


❌ Policy gap (Page X, Line Y): "<quote the non-compliant policy text>"
📘 Violation: "<which NIST control it violates>"
✅ Required fix: "<concrete, actionable fix>"


Policy Findings:
{findings}
"""


    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)


    output_lines = [block.strip() for block in response.text.split("\n\n") if block.strip()]
    return output_lines