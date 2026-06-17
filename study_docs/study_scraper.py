import requests  # For grabbing the raw HTML code
from bs4 import BeautifulSoup  # For parsing HTML code
import pandas as pd  # For creating tables/spreadsheets (Data Frame), used 'as pd' so we don't have to type 'pandas' every time.

TARGET_URL = "https://realpython.github.io/fake-jobs/" # Stores the URL string.
response = requests.get(TARGET_URL) # Sends an HTTP GET request to the URL and stores the raw response in the 'response' variable.

soup = BeautifulSoup(response.text, "html.parser") # Parses the HTML code stored in the 'response' variable and stores it in the 'soup' variable.
results_container = soup.find(id="ResultsContainer") # Finds the HTML element with the ID 'ResultsContainer' and stores it in the 'results_container' variable.
job_elements = results_container.find_all("div", class_="card-content") # Finds all HTML elements with the class 'card-content' and stores them in the 'job_elements' variable.

extracted_jobs_list = [] # Create an empty list to store all jobs

print("Extracting all jobs from the webpage...")

for job in job_elements: # Loop through every single job card on the page
    """
    Finds the class of each job (Job Title, Company Name, Location)
    and stores it in their own variable.
    """
    title_element = job.find("h2", class_="title") 
    company_element = job.find("h3", class_="company") 
    location_element = job.find("p", class_="location") 
    
    """
    Pack the data into a Dictionary.
    The .text method extracts the visible text from a HTML element.
    The .strip() method removes any leading or trailing whitespace (like spaces or newlines).
    """
    job_dictionary = {
        "Job Title": title_element.text.strip(),
        "Company Name": company_element.text.strip(),
        "Location": location_element.text.strip()
    }

    extracted_jobs_list.append(job_dictionary) # Add this individual job (now a dictionary) into our main list.
# End of loop

df = pd.DataFrame(extracted_jobs_list) # Converts the list of dictionaries into a Pandas DataFrame.

df.to_csv("job_data.csv", index=False) # Saves the DataFrame to a CSV file.

print("\nPipeline execution successful!")