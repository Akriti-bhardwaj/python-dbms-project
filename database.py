import sqlite3
import pandas as pd

DB_PATH = "job_postings.db"

# ----------------------------------
# Database Connection
# ----------------------------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ----------------------------------
# Create the table
# ----------------------------------
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS job_postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            job_description TEXT
        )
    """)
    conn.commit()
    conn.close()

# ----------------------------------
# Add job to database
# ----------------------------------
def add_job_to_db(title, company, location, description):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO job_postings (title, company, location, job_description)
        VALUES (?, ?, ?, ?)
    """, (title, company, location, description))
    conn.commit()
    conn.close()

# ----------------------------------
# Read jobs as a DataFrame
# ----------------------------------
def read_jobs_df():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM job_postings", conn)
    conn.close()
    return df

# ----------------------------------
# Count skills in job descriptions
# ----------------------------------
def count_skills(df, skills_to_check):
    counts = {}
    
    if df.empty or not skills_to_check:
        return pd.DataFrame({"Skill": [], "Count": []})

    text_series = df["job_description"].fillna("").str.lower()

    for skill in skills_to_check:
        patt = r"\b" + skill.lower() + r"\b"
        count = text_series.str.contains(patt, regex=True, case=False).sum()
        counts[skill] = int(count)

    result_df = pd.DataFrame(list(counts.items()), columns=["Skill", "Count"])
    return result_df.sort_values(by="Count", ascending=False)
