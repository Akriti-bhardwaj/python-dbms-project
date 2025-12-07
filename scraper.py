import requests
from bs4 import BeautifulSoup
import re
from database import add_job_to_db

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def scrape_naukri(keyword="Data Analyst", location="India"):
    url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: Could not fetch data (status {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("article", {"class": "jobTuple"})

    scraped_count = 0

    for job in jobs:
        title = clean_text(job.find("a", {"class": "title"}).text)
        company = clean_text(job.find("a", {"class": "subTitle"}).text)
        location = clean_text(job.find("li", {"class": "location"}).text if job.find("li", {"class": "location"}) else "Not specified")
        desc = clean_text(job.find("div", {"class": "job-description"}).text if job.find("div", {"class": "job-description"}) else "No description")

        add_job_to_db(title, company, location, desc)
        scraped_count += 1

    return f"Successfully scraped {scraped_count} job postings!"
