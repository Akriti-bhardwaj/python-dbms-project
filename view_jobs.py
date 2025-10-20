import sqlite3

conn = sqlite3.connect('job_postings.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM job_postings")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
