import streamlit as st
from agent import job_agent   # ✅ correct place

st.set_page_config(page_title="CareerPilot", layout="wide")

st.title("🚀 CareerPilot - AI Job Assistant")

query = st.text_input("🔍 Enter Job Role")
location = st.selectbox("📍 Location", ["Bangalore", "Mumbai", "Delhi"])
sort_option = st.selectbox("Sort By", ["Relevance", "Match Score"])

# --- RESUME UPLOAD ---
uploaded_file = st.file_uploader("📄 Upload Resume", type=["txt"])
resume = ""

if uploaded_file:
    resume = uploaded_file.read().decode("utf-8")
    st.subheader("🧠 Resume Analysis")

    from agent import extract_skills   # ✅ ADD THIS

    skills = extract_skills(resume)    # ✅ REAL SKILLS
    st.write("Skills:", skills)


# --- JOB SEARCH ---
if st.button("Search Jobs"):
    if not query:
        st.warning("⚠️ Please enter a job role")
    else:
        jobs = job_agent(query, resume)   # ✅ correct usage

        st.subheader("💼 Job Results")

        for job in jobs:
            st.subheader(job["title"])
            st.write(f"🏢 {job['company']}")
            st.write(f"⭐ Score: {job.get('match_score', 0)}")
            st.divider()

# --- COMPANY INFO ---
def company_info(company):
    data = {
        "NAUKRI": "Good work-life balance",
        "LINKEDIN": "Strong professional network"
    }
    return data.get(company, "No data available")

st.subheader("🏢 Company Insights")
st.write("NAUKRI:", company_info("NAUKRI"))
st.write("LINKEDIN:", company_info("LINKEDIN"))

# --- APPLICATION TRACKING ---
st.subheader("📌 Applications")

applications = [
    {"title": "Data Scientist", "company": "NAUKRI", "status": "Applied"},
    {"title": "ML Engineer", "company": "LINKEDIN", "status": "Interview"}
]

for app in applications:
    st.write(f"📄 {app['title']} at {app['company']} | Status: {app['status']}")

# --- DOWNLOAD ---
if st.button("📥 Download Job List"):
    st.download_button("Download", "Sample job data")

# --- ERROR HANDLING ---
try:
    pass
except:
    st.error("Something went wrong")