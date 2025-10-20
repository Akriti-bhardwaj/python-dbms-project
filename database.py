import sqlite3

# create database connection
conn = sqlite3.connect('job_postings.db')
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS job_postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company_name TEXT,
    location TEXT,
    job_description TEXT,
    date_scraped TEXT,
    source_url TEXT UNIQUE
)
''')

print("Database and table created successfully!")

conn.commit()
conn.close()
