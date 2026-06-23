"""
Job Filter and Reporter Module

Analyzes scraped job listings from a CSV dataset.
Filters positions based on configurable regex patterns, tracks previously
seen roles using a SQLite database to prevent duplicate alerts, and
transmits batch reports to Discord via webhooks.
"""

import pandas as pd
import requests
import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

CSV_PATH = Path(__file__).parent / "job_data.csv"
DB_PATH = Path(__file__).parent / "jobs.db"

def main():
    """
    Main entry point for the filtering and reporting pipeline.
    
    1. Loads environment configurations.
    2. Reads scraped job data from the CSV file.
    3. Initializes the SQLite database for duplicate tracking.
    4. Filters jobs based on the target pattern.
    5. Checks the database for unseen jobs and updates records.
    6. Formats and sends a batched Discord report payload.
    """
    load_dotenv()
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    DEFAULT_PATTERN = 'Developer|Software|Engineer|Programmer|Backend|Frontend|Full Stack'
    JOB_FILTER_PATTERN = os.getenv("JOB_FILTER_PATTERN", DEFAULT_PATTERN)

    if not DISCORD_WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL not set in .env")

    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        raise RuntimeError("Could not find 'job_data.csv'. Run scraper.py first!")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seen_jobs (
                job_url TEXT UNIQUE
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database initialization failed: {e}")

    print("--- Data Intelligence Report ---")
    print(f"Total Jobs Analyzed: {len(df)}\n")

    programming_jobs = df[df['Job Title'].str.contains(JOB_FILTER_PATTERN, case=False, na=False)]

    new_jobs = []
    try:
        for index, row in programming_jobs.iterrows():
            title = row['Job Title']
            url = row['Job URL']
            try:
                cursor.execute('INSERT OR IGNORE INTO seen_jobs (job_url) VALUES (?)', (url,))
                if cursor.rowcount > 0:
                    new_jobs.append((title, url))
            except sqlite3.Error as e:
                print(f"Error inserting {url} into database: {e}")
        
        conn.commit()
    finally:
        if conn:
            conn.close()

    payloads = []
    if new_jobs:
        batch_size = 15
        for i in range(0, len(new_jobs), batch_size):
            batch = new_jobs[i:i + batch_size]
            
            if i == 0:
                report_message = (
                    "📊 **TECH JOB MARKET REPORT** 📊\n"
                    f"Total Job Postings Scanned: `{len(df)}`\n"
                    "```text\n"
                    "=========================================\n"
                    f"🔹 New Programming Roles Found: {len(new_jobs)}\n"
                    "=========================================\n\n"
                    "💻 New Programming Positions:\n\n"
                )
            else:
                report_message = f"```text\n💻 New Programming Positions (Part {i//batch_size + 1}):\n\n"
                
            for title, url in batch:
                report_message += f"{title}\n{url}\n\n"

            report_message += "```"
            if i + batch_size >= len(new_jobs):
                report_message += "\n🏁 *Pipeline execution completed successfully.*"
            
            payloads.append({"content": report_message})

    else:
        payloads.append({"content": "No new programming jobs found today.\n🏁 *Pipeline execution completed successfully.*"})

    print("Sending data report to your Discord channel...")

    try:
        for payload in payloads:
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                print("Success! Check your Discord!")
            else:
                print(f"Failed. Error code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

if __name__ == "__main__":
    main()
