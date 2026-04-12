# -*- coding: utf-8 -*-
"""agent.ipynb (cleaned for Python execution)"""

def search_jobs(query, source="default"):
    return [
        {
            "title": f"{query} Engineer",
            "company": source.upper(),
            "skills": ["python", "machine learning", "sql"]
        }
    ]


def unified_job_search(query):
    results = []
    results.extend(search_jobs(query, "naukri"))
    results.extend(search_jobs(query, "linkedin"))
    results.extend(search_jobs(query, "indeed"))
    return results


# ---------------- TOOLS ----------------

def extract_skills(text):
    text = text.lower()
    skills = []

    if "python" in text:
        skills.append("python")

    if "machine learning" in text or "ml" in text:
        skills.append("machine learning")   # ✅ FIXED

    if "sql" in text:
        skills.append("sql")

    if "data science" in text:
        skills.append("data science")

    return skills

def match_jobs(user_skills, jobs):
    matched = []

    for job in jobs:
        score = len(set(user_skills) & set(job["skills"]))

        if score > 0:
            job["match_score"] = score
            matched.append(job)

    return sorted(matched, key=lambda x: x["match_score"], reverse=True)


# ---------------- MAIN AGENT ----------------


def job_agent(query, resume_text=""):
    skills = extract_skills(resume_text)
    print("USER SKILLS:", skills)   # 👈 ADD THIS

    jobs = unified_job_search(query)
    print("JOB SKILLS:", jobs)      # 👈 ADD THIS

    matched_jobs = match_jobs(skills, jobs)
    return matched_jobs


# ---------------- EXTRA FEATURES ----------------

def interview_prep(role):
    questions = {
        "data scientist": [
            "What is overfitting?",
            "Explain bias vs variance",
            "What is a confusion matrix?"
        ]
    }
    return questions.get(role.lower(), ["Tell me about yourself"])


def salary_estimator(role):
    salary_data = {
        "data scientist": "₹6 LPA – ₹20 LPA",
        "software engineer": "₹4 LPA – ₹15 LPA"
    }
    return salary_data.get(role.lower(), "Not available")


def career_recommendation(skills):
    if "ml" in skills:
        return "Recommended Role: Data Scientist"
    elif "java" in skills:
        return "Recommended Role: Backend Developer"
    else:
        return "Recommended Role: Software Engineer"


def networking_tips():
    return [
        "Build LinkedIn profile",
        "Attend tech meetups",
        "Connect with professionals",
        "Participate in hackathons"
    ]


# ---------------- LINKEDIN OPTIMIZER ----------------

def linkedin_optimizer(skills, role):
    suggestions = []

    suggestions.append(f"Update headline to: '{role} | {', '.join(skills[:3])}'")
    suggestions.append("Write a strong 'About' section highlighting your skills and projects")
    suggestions.append("Add relevant skills like: " + ", ".join(skills))
    suggestions.append("Add projects related to your domain")
    suggestions.append("Connect with professionals in your domain")

    return suggestions


# ---------------- JOB ALERT ----------------

def job_alert(query):
    jobs = unified_job_search(query)

    print("🔔 New Job Alerts:")
    for job in jobs:
        print(f"{job['title']} at {job['company']}")


# ---------------- DATABASE ----------------

import sqlite3

conn = sqlite3.connect("career.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skills TEXT,
    goals TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    company TEXT,
    status TEXT,
    match_score INTEGER
)
""")

conn.commit()


# ---------------- APPLICATION TRACKING ----------------

applications = []

def apply_job(job):
    job["status"] = "Applied"
    applications.append(job)
    return "Application submitted"


def view_applications():
    return applications


# ---------------- SALARY ----------------

salary_data = {
    "Data Scientist": (6, 20),
    "Software Engineer": (4, 15),
}

def salary_benchmark(role):
    if role in salary_data:
        low, high = salary_data[role]
        avg = (low + high) // 2
        return {"min": low, "max": high, "average": avg}
    return {"min": 5, "max": 15, "average": 10}


def compare_salary(role, user_salary):
    market = salary_benchmark(role)

    if user_salary < market["min"]:
        return "Below market value ❌"
    elif user_salary > market["max"]:
        return "Above market value 🚀"
    else:
        return "Within market range ✅"


def negotiation_tips(role, user_salary):
    market = salary_benchmark(role)
    tips = []

    if user_salary < market["average"]:
        tips.append("Negotiate for higher salary based on market average.")
    else:
        tips.append("Offer is competitive.")

    tips.append("Highlight your key skills.")
    tips.append("Research company salary standards.")
    tips.append("Be confident.")

    return tips