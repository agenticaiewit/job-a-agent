import streamlit as st
from agent import job_agent, extract_skills

st.set_page_config(page_title="CareerPilot", layout="wide")

st.title("🚀 CareerPilot - AI Job Assistant")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Jobs", "📄 Resume", "🤖 Interview"])

jobs = []  # ✅ initialize
skills = []

# --- TAB 1: JOB SEARCH ---
with tab1:
    st.header("🔍 Job Search")

    query = st.text_input("Enter Job Role")
    location = st.selectbox("Location", ["Bangalore", "Mumbai", "Delhi"])
    sort_option = st.selectbox("Sort By", ["Relevance", "Match Score"])

    if st.button("Search Jobs"):
        if not query:
            st.warning("⚠️ Please enter a job role")
        else:
            try:
                jobs = job_agent(query, "")
                st.subheader("💼 Job Results")

                for job in jobs:
                    st.write(f"📄 {job['title']} at {job['company']}")
                    st.write(f"⭐ Score: {job.get('match_score', 0)}")
                    st.divider()

            except Exception as e:
                st.error("Something went wrong while fetching jobs")

    # Analytics
    if jobs:
        st.subheader("📊 Analytics")
        st.metric("Jobs Found", len(jobs))


# --- TAB 2: RESUME ---
with tab2:
    st.header("📄 Resume Analysis")

    uploaded_file = st.file_uploader("Upload Resume", type=["txt"])

    if uploaded_file:
        resume = uploaded_file.read().decode("utf-8")

        if len(resume.strip()) < 20:
            st.warning("⚠️ Resume content too short")
        else:
            skills = extract_skills(resume)
            st.success("✅ Resume uploaded successfully")
            st.write("Skills:", skills)


# --- TAB 3: INTERVIEW ---
with tab3:
    st.header("🤖 Mock Interview")

    st.info("Sample Questions:")
    st.write([
        "What is overfitting?",
        "Explain bias vs variance",
        "What is a confusion matrix?"
    ])


# --- COMPANY INFO ---
st.subheader("🏢 Company Insights")

def company_info(company):
    data = {
        "NAUKRI": "Good work-life balance",
        "LINKEDIN": "Strong professional network"
    }
    return data.get(company, "No data available")

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
if jobs:
    st.download_button(
        "📥 Download Job List",
        data=str(jobs),
        file_name="jobs.txt"
    )