import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect('job_postings.db')

# read data into pandas DataFrame
df = pd.read_sql_query("SELECT job_title, job_description FROM job_postings", conn)

# define the skills to search for
skills = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Machine Learning", "HTML", "JavaScript"]

# count how many descriptions mention each skill
counts = {}

for skill in skills:
    counts[skill] = df['job_description'].str.contains(skill, case=False, na=False).sum()

# show results
print("\nSkill Frequency in Job Descriptions:\n")
for skill, count in counts.items():
    print(f"{skill}: {count}")

conn.close()
