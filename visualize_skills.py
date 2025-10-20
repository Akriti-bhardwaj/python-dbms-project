import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# connect to the database
conn = sqlite3.connect('job_postings.db')
df = pd.read_sql_query("SELECT job_description FROM job_postings", conn)
conn.close()

# define the skills to search for
skills = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Machine Learning", "HTML", "JavaScript"]

# count how many times each skill appears
counts = {}
for skill in skills:
    counts[skill] = df['job_description'].str.contains(skill, case=False, na=False).sum()

# make a DataFrame for plotting
skill_df = pd.DataFrame(list(counts.items()), columns=["Skill", "Count"])

# plot a bar chart
plt.bar(skill_df["Skill"], skill_df["Count"])
plt.title("Skill Frequency in Job Descriptions")
plt.xlabel("Skills")
plt.ylabel("Count")
plt.xticks(rotation=30)
plt.show()
