import requests
from bs4 import BeautifulSoup

# The sandbox job board
TARGET_URL = "https://realpython.github.io/fake-jobs/"
response = requests.get(TARGET_URL)

soup = BeautifulSoup(response.text, "html.parser")
results_container = soup.find(id="ResultsContainer")
job_elements = results_container.find_all("div", class_="card-content")

print(f"Successfully found {len(job_elements)} job postings!\n")

# Print the first 5 jobs just to verify it works
for job in job_elements[:5]:
    title_element = job.find("h2", class_="title")
    company_element = job.find("h3", class_="company")
    
    print(f"Job: {title_element.text.strip()} | Company: {company_element.text.strip()}")