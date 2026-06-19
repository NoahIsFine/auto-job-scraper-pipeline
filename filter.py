"""
This script reads and analyzes scraped job listings from a CSV file.
It filters and displays specific roles to provide insight into job demand.
"""

import pandas as pd
import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1517334847151018106/rClODIwAtNnt7eIP-dLAs5VwwBXwCH1xXzOPe0e8OXTrl5WicfYgUM1CeBAc1nBLTjDM"

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
Filter the job dataset for Python, Java, and Manager roles.
Case-insensitive matching is used to capture all relevant job titles.
"""
python_jobs = df[df['Job Title'].str.contains('Python', case=False)]
java_jobs = df[df['Job Title'].str.contains('Java', case=False)]
manager_jobs = df[df['Job Title'].str.contains('Manager', case=False)]

"""
Builds the formatted string payload containing the statistical summary of found jobs.
Appends the top python listings to provide a preview of the available positions.
"""
report_message = (
    "📊 **TECH JOB MARKET REPORT** 📊\n"
    f"Total Job Postings Scanned: `{len(df)}`\n"
    "```text\n"
    "=========================================\n"
    f"🔹 Python Roles Found : {len(python_jobs)}\n"
    f"🔹 Java Roles Found   : {len(java_jobs)}\n"
    f"🔹 Manager Roles Found: {len(manager_jobs)}\n"
    "=========================================\n\n"
    "LATEST OPPORTUNITIES SUBSET:\n"
)

empty = (
    "Pipeline returned empty."
)

if not python_jobs.empty:
    report_message += "🐍 Top Python Positions:\n"
    for index, row in python_jobs.head(3).iterrows():
        title = row['Job Title'][:25]
        comp = row['Company Name'][:15]
        report_message += f"  - {title:<25} @ {comp:<15}\n"

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