import pandas as pd

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

print("Skill/Role Demand Breakdown:\n")
print(f"Python-related Roles: {len(python_jobs)}\n")
print(f"Java-related Roles: {len(java_jobs)}\n")
print(f"Managerial Roles: {len(manager_jobs)}\n")
print("-" * 32) # "-" * 32 multiply the string by 32, printing out 32 hyphens.

print("\nPreviewing Python Opportunities Found:")

if not python_jobs.empty:
    """
    iterrows() loops for every rows in the dataframe. 
    We access the columns using row['Column Name'].
    """
    for index, row in python_jobs.iterrows(): 
        print(f"-> {row['Job Title']} at {row['Company Name']} ({row['Location']})")
else:
    print("No Python jobs found in this batch.")