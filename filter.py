"""
This script reads and analyzes scraped job listings from a CSV file.
It filters and displays specific roles to provide insight into job demand.
"""
import pandas as pd

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
Print the demand statistics and display a detailed preview of the Python roles.
If no Python roles are found, display a fallback notification message.
"""
print("Skill/Role Demand Breakdown:\n")
print(f"Python-related Roles: {len(python_jobs)}\n")
print(f"Java-related Roles: {len(java_jobs)}\n")
print(f"Managerial Roles: {len(manager_jobs)}\n")
print("-" * 32)

print("\nPreviewing Python Opportunities Found:")

if not python_jobs.empty:
    for index, row in python_jobs.iterrows():
        print(f"-> {row['Job Title']} at {row['Company Name']} ({row['Location']})")
else:
    print("No Python jobs found in this batch.")