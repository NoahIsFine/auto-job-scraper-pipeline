import requests  # For grabbing the raw HTML code
import pandas as pd  # For creating tables/spreadsheets (Data Frame), used 'as pd' so we don't have to type 'pandas' every time.

BOARD_TOKEN = "stripe" # Identifies the company.
TARGET_URL = f"https://boards-api.greenhouse.io/v1/boards/{BOARD_TOKEN}/jobs" # The URL endpoint for the API.

response = requests.get(TARGET_URL) # Sends an HTTP GET request to the URL and stores the raw response in the 'response' variable.
job_elements = response.json()["jobs"] # Parses the JSON response and stores the list of jobs in the 'job_elements' variable.

extracted_jobs_list = [] # Create an empty list to store all jobs

print(f"Extracting all jobs from the Greenhouse board: '{BOARD_TOKEN}'...")

for job in job_elements:
    job_dictionary = {
        "Job Title": job["title"],
        "Company Name": BOARD_TOKEN,
        "Location": job["location"]["name"], # The location field is a nested object, so we access job["location"]["name"].
        "Job URL": job["absolute_url"],
        "Updated At": job["updated_at"]
    }
    extracted_jobs_list.append(job_dictionary)
# End of loop

df = pd.DataFrame(extracted_jobs_list) # Converts the list of dictionaries into a Pandas DataFrame.
df.to_csv("job_data.csv", index=False) # Saves the DataFrame to a CSV file.

print("\nPipeline execution successful!")