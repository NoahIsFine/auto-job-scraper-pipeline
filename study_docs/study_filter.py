import pandas as pd
import requests
import os
from dotenv import load_dotenv
# Used .env file instead to secure webhook url.
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

try: # Monitors runtime error.
    df = pd.read_csv("job_data.csv") # Reads the csv file.
except FileNotFoundError: # If the csv file is not found.
    print("Error: Could not find 'job_data.csv'. Run scraper.py first!")
    exit()

print("--- Data Intelligence Report ---")
print(f"Total Jobs Analyzed: {len(df)}\n") # 'f' allows expressions inside brackets. len() counts the number of rows.

prog_pattern = 'Developer|Software|Engineer|Programmer|Backend|Frontend|Full Stack' # | acts as an OR operator.
programming_jobs = df[df['Job Title'].str.contains(prog_pattern, case=False, na=False)]

# Holds the message that will be sent to Discord.
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
        url = row['Job URL'].replace("https://", "").replace("http://", "") # Removes the http:// at the start of the url.
        report_message += f"  - {title:<40} {url}\n"

    report_message += "```\n🏁 *Pipeline execution completed successfully.*"

    payload = {"content": report_message}

else:
    payload = {"content": empty}

print("Sending data report to your Discord channel...")
response = requests.post(DISCORD_WEBHOOK_URL, json=payload) # Sends the payload to the Discord API.

if response.status_code == 204: # Checks if the response status code is 204.
    print("🚀 Success! Check your Discord app on your phone or desktop!")
else:
    print(f"❌ Failed to send alert. Error code: {response.status_code}")