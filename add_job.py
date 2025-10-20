import sqlite3
from datetime import datetime

# connect to database
conn = sqlite3.connect('job_postings.db')
cursor = conn.cursor()

# job details 
job_title = "Data Analyst"
company_name = "Google"
location = "Bangalore"
job_description = "Looking for skilled data analyst with Python and SQL."
date_scraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
source_url = "https://example.com/job1"

# insert into table
cursor.execute('''
INSERT OR IGNORE INTO job_postings (job_title, company_name, location, job_description, date_scraped, source_url)
VALUES (?, ?, ?, ?, ?, ?)
''', (job_title, company_name, location, job_description, date_scraped, source_url))

conn.commit()
conn.close()

print("Job added successfully!")
