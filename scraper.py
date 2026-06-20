import requests
import pandas as pd

"""
Fetch live job listings from the Greenhouse Job Board API.
No HTML parsing required — the API returns structured JSON directly.
"""
BOARD_TOKEN = "stripe"
TARGET_URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD_TOKEN}/jobs"

response = requests.get(TARGET_URL)
job_elements = response.json()["jobs"]

extracted_jobs_list = []

print(f"Extracting all jobs from the Greenhouse board: '{BOARD_TOKEN}'...")

for job in job_elements:
    """
    Extract job title, location, URL, and date from the JSON response.
    The location field is a nested object, so we access job["location"]["name"].
    """
    job_dictionary = {
        "Job Title": job["title"],
        "Company Name": BOARD_TOKEN,
        "Location": job["location"]["name"],
        "Job URL": job["absolute_url"],
        "Updated At": job["updated_at"]
    }
    extracted_jobs_list.append(job_dictionary)

"""
Convert the list of extracted jobs into a Pandas DataFrame.
Save the DataFrame to a CSV file without row index labels.
"""
df = pd.DataFrame(extracted_jobs_list)
df.to_csv("job_data.csv", index=False)

print("\nPipeline execution successful!")