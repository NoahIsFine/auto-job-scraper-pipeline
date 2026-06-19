import pandas as pd
import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1517334847151018106/rClODIwAtNnt7eIP-dLAs5VwwBXwCH1xXzOPe0e8OXTrl5WicfYgUM1CeBAc1nBLTjDM"

try: # Monitors runtime error.
    df = pd.read_csv("job_data.csv") # Reads the csv file.
except FileNotFoundError: # If the csv file is not found.
    print("Error: Could not find 'job_data.csv'. Run scraper.py first!")
    exit()

print("--- Data Intelligence Report ---")
print(f"Total Jobs Analyzed: {len(df)}\n") # 'f' allows expressions inside brackets. len() counts the number of rows.

"""
df['Job Title'] selects the job title column.
.str.contains() checks if the string contains the keyword.
case=False means it will ignore the case.
df[...] Only takes rows that match the condition.
"""
python_jobs = df[df['Job Title'].str.contains('Python', case=False)]
java_jobs = df[df['Job Title'].str.contains('Java', case=False)]
manager_jobs = df[df['Job Title'].str.contains('Manager', case=False)]

# Holds the message that will be sent to Discord.
report_message = (
    "📊 **TECH JOB MARKET REPORT** 📊\n"
    f"Total Job Postings Scanned: `{len(df)}`\n"
    "```text\n"  # Open the monospaced code block
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

if not python_jobs.empty: #If not empty.
    report_message += "🐍 Top Python Positions:\n" # += adds this on the already existing contents of report_message.
    for index, row in python_jobs.head(3).iterrows(): # .head(3) only gets the first 3 rows of the list.
        title = row['Job Title'][:25] # [:25] only gets the first 25 characters of the string.
        comp = row['Company Name'][:15]
        report_message += f"  - {title:<25} @ {comp:<15}\n" # :<25 aligns the text to the left by adding 25 spaces after the text. 

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