# app.py - Streamlit frontend for Job Skills Analyzer
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "job_postings.db"  # change if your DB file name/location differs

# ---------- Database helpers ----------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS job_postings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    job_description TEXT
                 )""")
    conn.commit()
    conn.close()

def add_job_to_db(title, company, location, description):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO job_postings (title, company, location, job_description) VALUES (?, ?, ?, ?)",
              (title, company, location, description))
    conn.commit()
    conn.close()

def read_jobs_df():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM job_postings", conn)
    conn.close()
    return df

# ---------- Skill analyzer ----------
DEFAULT_SKILLS = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Machine Learning", "HTML", "JavaScript", "pandas"]

def count_skills(df, skills=DEFAULT_SKILLS):
    counts = {}
    if df.empty:
        return pd.DataFrame({"Skill": [], "Count": []})
    text_series = df['job_description'].fillna("").str.lower()
    for s in skills:
        counts[s] = int(text_series.str.contains(s.lower()).sum())
    skill_df = pd.DataFrame(list(counts.items()), columns=["Skill", "Count"]).sort_values("Count", ascending=False)
    return skill_df

# ---------- Streamlit App ----------
st.set_page_config(page_title="Job Skills Analyzer", layout="wide")
st.title("🧠 Job Skills Analyzer")
init_db()

menu = st.sidebar.selectbox("Choose action", ["Add job", "View jobs", "Analyze & Visualize"])

if menu == "Add job":
    st.header("Add a Job Posting")
    with st.form("add_job_form"):
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        location = st.text_input("Location")
        description = st.text_area("Job Description")
        submitted = st.form_submit_button("Add Job")
        if submitted:
            if not description.strip():
                st.warning("Please enter a job description.")
            else:
                add_job_to_db(title, company, location, description)
                st.success("✅ Job added successfully!")

elif menu == "View jobs":
    st.header("All Job Postings")
    df = read_jobs_df()
    st.write(f"Total jobs: {len(df)}")
    st.dataframe(df)

elif menu == "Analyze & Visualize":
    st.header("Skill Frequency")
    df = read_jobs_df()
    skill_df = count_skills(df)
    st.subheader("Skill Counts")
    st.table(skill_df)

    if not skill_df.empty and skill_df['Count'].sum() > 0:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(skill_df['Skill'], skill_df['Count'])
        ax.set_title("Skill Frequency in Job Descriptions")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No skills found yet — add some jobs first!")

