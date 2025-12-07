from database import get_connection

def seed_sample_jobs():
    """Insert sample job postings only if the table is empty."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM job_postings")
    count = c.fetchone()[0]

    if count == 0:
        sample_jobs = [
            ("Data Analyst", "TCS", "Bangalore", "Python, SQL, Excel, Power BI"),
            ("Machine Learning Engineer", "Google", "Hyderabad", "TensorFlow, Python, AWS, ML"),
            ("Frontend Developer", "Infosys", "Pune", "HTML, CSS, JavaScript, React"),
            ("Backend Developer", "Wipro", "Chennai", "Python, Django, SQL, REST APIs"),
            ("Cloud Engineer", "Amazon Web Services", "Gurugram", "AWS, Azure, Docker, Cloud Deployment"),
            ("Business Analyst", "Accenture", "Mumbai", "Excel, Tableau, SQL, Communication Skills"),
            ("Full Stack Developer", "Tech Mahindra", "Noida", "React, Node.js, MongoDB, JavaScript"),
            ("AI Research Intern", "IBM Research", "Delhi", "Python, pandas, Machine Learning, Data Cleaning")
        ]

        c.executemany(
            "INSERT INTO job_postings (title, company, location, job_description) VALUES (?, ?, ?, ?)",
            sample_jobs
        )

        conn.commit()
        print("Sample jobs added successfully.")
    else:
        print("Sample jobs already exist.")

    conn.close()

if __name__ == "__main__":
    seed_sample_jobs()
