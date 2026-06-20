"""
This script reads and analyzes scraped job listings from a CSV file.
It filters and displays specific roles to provide insight into job demand.
"""

import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

"""
Attempt to load the job data from the local CSV file.
If the file does not exist, notify the user and exit the execution.
"""
try:
    df = pd.read_csv("job_data.csv")
except FileNotFoundError:
    print("Error: Could not find 'job_data.csv'. Run scraper.py first!")
    exit()

print("--- Data Intelligence Report ---")
print(f"Total Jobs Analyzed: {len(df)}\n")

"""
Filter the job dataset for Programming-related roles.
Case-insensitive matching is used to capture all relevant job titles.
"""
prog_pattern = 'Developer|Software|Engineer|Programmer|Backend|Frontend|Full Stack'
programming_jobs = df[df['Job Title'].str.contains(prog_pattern, case=False, na=False)]

"""
Builds the formatted string payload containing the statistical summary of found jobs.
Appends the top listings to provide a preview of the available positions.
"""
report_message = (
    "📊 **TECH JOB MARKET REPORT** 📊\n"
    f"Total Job Postings Scanned: `{len(df)}`\n"
    "```text\n"
    "=========================================\n"
    f"🔹 Programming Roles Found: {len(programming_jobs)}\n"
    "=========================================\n\n"
    "LATEST OPPORTUNITIES SUBSET:\n"
)

empty = (
    "Pipeline returned empty."
)

if not programming_jobs.empty:
    report_message += "💻 Top Programming Positions:\n"
    for index, row in programming_jobs.head(10).iterrows():
        title = row['Job Title']
        url = row['Job URL'].replace("https://", "").replace("http://", "")
        report_message += f"  - {title:<40} {url}\n"

    report_message += "```\n🏁 *Pipeline execution completed successfully.*"

    payload = {"content": report_message}

else:
    payload = {"content": empty}

"""
Transmits the compiled job report payload to the designated Discord channel.
Checks the server response status to verify whether the webhook delivery succeeded.
"""
print("Sending data report to your Discord channel...")
response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

if response.status_code == 204:
    print("🚀 Success! Check your Discord app on your phone or desktop!")
else:
    print(f"❌ Failed to send alert. Error code: {response.status_code}")