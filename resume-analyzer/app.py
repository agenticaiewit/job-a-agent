import streamlit as st
import PyPDF2
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import os

# -------------------------------
# Load spaCy model safely
# -------------------------------
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except:
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_nlp()

# -------------------------------
# Extract text from PDF safely
# -------------------------------
def extract_text(file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# -------------------------------
# Clean text
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -------------------------------
# Calculate ATS Score
# -------------------------------
def calculate_score(resume, job_desc):
    if not resume or not job_desc:
        return 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        vectors = vectorizer.fit_transform([resume, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return round(similarity[0][0] * 100, 2)
    except:
        return 0.0

# -------------------------------
# Extract keywords
# -------------------------------
def extract_keywords(text):
    if not text:
        return []
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"] and len(token.text) > 2:
            keywords.add(token.text.lower())

    return list(keywords)

# -------------------------------
# Find missing keywords
# -------------------------------
def find_missing_keywords(resume, keywords):
    missing = []
    for word in keywords:
        pattern = r'\b' + re.escape(word) + r'\b'
        if not re.search(pattern, resume):
            missing.append(word)
    return missing

# -------------------------------
# Generate PDF Report safely
# -------------------------------
def create_pdf_report(score, missing_keywords):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ATS Resume Analysis Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"ATS Score: {score}%", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, "Missing Keywords:", ln=True)

    pdf.set_font("Arial", "", 11)
    for word in missing_keywords[:20]:
        try:
            pdf.cell(0, 8, f"- {word}", ln=True)
        except:
            pass  # avoid encoding crash

    return pdf.output(dest="S").encode("latin-1", errors="ignore")

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📄")

st.title("📄 AI ATS Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Job Description", height=200)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("Analyze Resume"):
    if resume_file is None:
        st.warning("Please upload a resume.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing..."):

            # Extract & clean
            resume_text = extract_text(resume_file)
            if not resume_text:
                st.error("Could not extract text from resume.")
                st.stop()

            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_description)

            # Score
            score = calculate_score(resume_clean, job_clean)

            # Keywords
            keywords = extract_keywords(job_description)
            missing = find_missing_keywords(resume_clean, keywords)

            # -------------------------------
            # OUTPUT
            # -------------------------------
            st.divider()
            st.subheader(f"📊 ATS Score: {score}%")

            if score >= 75:
                st.success("Excellent match! Resume is well optimized.")
            elif score >= 50:
                st.warning("Decent match. Add more keywords.")
            else:
                st.error("Low match. Improve your resume.")

            st.subheader("🔑 Missing Keywords (Top 15)")
            if missing:
                st.write(", ".join(missing[:15]))
            else:
                st.success("No major keywords missing!")

            # PDF download
            report = create_pdf_report(score, missing)

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )