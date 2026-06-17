import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Fetch fake job listings from the target URL.
Parse the response using BeautifulSoup to locate job elements.
"""
TARGET_URL = "https://realpython.github.io/fake-jobs/"
response = requests.get(TARGET_URL)

soup = BeautifulSoup(response.text, "html.parser")
results_container = soup.find(id="ResultsContainer")
job_elements = results_container.find_all("div", class_="card-content")

extracted_jobs_list = []

print("Extracting all jobs from the webpage...")

for job in job_elements:
    """
    Extract job title, company, and location details from the card element.
    Clean the extracted text and append the dictionary to the main list.
    """
    title_element = job.find("h2", class_="title") 
    company_element = job.find("h3", class_="company") 
    location_element = job.find("p", class_="location") 
    
    job_dictionary = {
        "Job Title": title_element.text.strip(),
        "Company Name": company_element.text.strip(),
        "Location": location_element.text.strip()
    }

    extracted_jobs_list.append(job_dictionary)

"""
Convert the list of extracted jobs into a Pandas DataFrame.
Save the DataFrame to a CSV file without row index labels.
"""
df = pd.DataFrame(extracted_jobs_list)

df.to_csv("job_data.csv", index=False)

print("\nPipeline execution successful!")