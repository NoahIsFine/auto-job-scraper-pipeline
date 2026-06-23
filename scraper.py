"""
Greenhouse API Scraper Module

Fetches live job listings from the Greenhouse Job Board API.
Extracts structured job data and saves it to a local CSV file.
"""

import requests
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

CSV_PATH = Path(__file__).parent / "job_data.csv"

def main():
    """
    Main entry point for the scraper pipeline.
    
    1. Loads environment configurations.
    2. Fetches the latest job postings from the configured Greenhouse board.
    3. Parses the JSON response to extract relevant job attributes.
    4. Serializes the structured data to a CSV file.
    """
    load_dotenv()
    BOARD_TOKEN = os.getenv("GREENHOUSE_BOARD_TOKEN")

    if not BOARD_TOKEN:
        raise RuntimeError("GREENHOUSE_BOARD_TOKEN not set in .env")

    TARGET_URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD_TOKEN}/jobs"

    response = requests.get(TARGET_URL)
    response.raise_for_status()
    job_elements = response.json()["jobs"]

    extracted_jobs_list = []

    print(f"Extracting all jobs from the Greenhouse board: '{BOARD_TOKEN}'...")

    for job in job_elements:
        job_dictionary = {
            "Job Title": job.get("title", "Unknown Title"),
            "Company Name": BOARD_TOKEN,
            "Location": job.get("location", {}).get("name", "Unknown Location"),
            "Job URL": job.get("absolute_url", ""),
            "Updated At": job.get("updated_at", "")
        }
        extracted_jobs_list.append(job_dictionary)

    df = pd.DataFrame(extracted_jobs_list)
    df.to_csv(CSV_PATH, index=False)

    print("\nPipeline execution successful!")

if __name__ == "__main__":
    main()