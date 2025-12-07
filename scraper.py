import requests
from bs4 import BeautifulSoup

def scrape_naukri(keyword, location):
    try:
        url = f"https://www.naukri.com/{keyword}-jobs-in-{location}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        titles = soup.find_all("a", class_="title fw500 ellipsis")
        companies = soup.find_all("a", class_="subTitle ellipsis fleft")

        for t, c in zip(titles, companies):
            results.append({
                "title": t.text.strip(),
                "company": c.text.strip()
            })

        if not results:
            return {"error": "No jobs found. Try different keyword/location."}

        return results

    except Exception as e:
        return {"error": str(e)}
