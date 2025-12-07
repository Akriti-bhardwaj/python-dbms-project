# Job Skill Analyzer 💼

A modern Streamlit web application that analyzes job descriptions, extracts high-demand skills, and visualizes trends using interactive charts.

This project uses:
- Python
- Streamlit
- SQLite (Local Database)
- Pandas
- Plotly

---

## 🔍 Overview

Job Skill Analyzer helps users:
- Add job postings manually
- Store job data in a local SQLite database
- Analyze skill frequency from job descriptions
- Visualize skill trends with interactive bar charts
- Search and filter job postings easily

It is an upgraded and redesigned version with a modern UI, custom CSS, and improved backend structure.

---

## 🚀 Features

### ✅ Add Job Postings
- Enter title, company, location, and full job description.
- Jobs are stored in a local SQLite database.
- Clean UI with validation and improved form experience.

### 📊 Analyze Skills
- Input any list of skills (comma-separated).
- System scans all job descriptions and counts occurrences.
- Displays:
  - Top skill
  - Total jobs analyzed
  - Average skills/job
- Interactive Plotly chart of skill frequencies.
- Ability to view full skill table.

### 📋 View Jobs
- Search jobs by title, company, or keywords.
- Clean card-style display of each posting.
- Shows job metadata and short description preview.

---

## 🗂 Project Structure

job_skill_analyser/
│── app.py # Main Streamlit application
│── database.py # SQLite database functions
│── seed_jobs.py # Adds sample job entries
│── job_postings.db # SQLite database file
│── README.md # Project documentation
└── requirements.txt # Dependencies

yaml
Copy code

---

## 🛠 Installation

### 1. Clone the repository
git clone https://github.com/Akriti-bhardwaj/job_skill_analyser.git
cd job_skill_analyser

shell
Copy code

### 2. Create a virtual environment
python -m venv .venv

makefile
Copy code

### 3. Activate it  
**Windows:**
.venv\Scripts\activate

makefile
Copy code

**Mac/Linux:**
source .venv/bin/activate

shell
Copy code

### 4. Install dependencies
pip install -r requirements.txt

shell
Copy code

### 5. Initialize database
python -c "from database import init_db; init_db()"

bash
Copy code

(Optional) Add sample jobs:
python seed_jobs.py

shell
Copy code

### 6. Run the app
streamlit run app.py

yaml
Copy code

---

## 📦 Technologies Used

- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**
- **Plotly**
- **Custom CSS (UI styling)**

---

## 📘 Future Enhancements

- Web scraping from Naukri/LinkedIn
- Export skill reports to PDF
- Resume vs job skill matching
- Cloud database support (PostgreSQL)

---

## 👩‍💻 Author

**Akriti Bhardwaj**  
Made with 💜 using Python & Streamlit

---

## 📄 License

This project is open-source and free to use.
