import requests
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

CSV_PATH = Path(__file__).parent / "job_data.csv"

def main():
    # Fetch live job listings from the Greenhouse Job Board API.
    # No HTML parsing required — the API returns structured JSON directly.

    load_dotenv()
    BOARD_TOKEN = os.getenv("GREENHOUSE_BOARD_TOKEN")
    TARGET_URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD_TOKEN}/jobs"

    response = requests.get(TARGET_URL)
    response.raise_for_status()  # Raises an HTTPError if status is 4xx/5xx
    job_elements = response.json()["jobs"]

    extracted_jobs_list = []

    print(f"Extracting all jobs from the Greenhouse board: '{BOARD_TOKEN}'...")

    for job in job_elements:
        # Extract job title, location, URL, and date from the JSON response.
        # Use .get() to safely access keys, including nested objects like location.
        job_dictionary = {
            "Job Title": job.get("title", "Unknown Title"),
            "Company Name": BOARD_TOKEN,
            "Location": job.get("location", {}).get("name", "Unknown Location"),
            "Job URL": job.get("absolute_url", ""),
            "Updated At": job.get("updated_at", "")
        }
        extracted_jobs_list.append(job_dictionary)

    # Convert the list of extracted jobs into a Pandas DataFrame.
    # Save the DataFrame to a CSV file without row index labels.
    df = pd.DataFrame(extracted_jobs_list)
    df.to_csv(CSV_PATH, index=False)

    print("\nPipeline execution successful!")

if __name__ == "__main__":
    main()