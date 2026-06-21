import scraper
import job_filter

def main():
    print("Starting the Job Scraper Pipeline...")

    print("\n--- Running scraper ---")
    try:
        scraper.main()
    except Exception as e:
        print(f"Error: scraper.py failed to execute. Details: {e}")
        return

    print("\n--- Running filter ---")
    try:
        job_filter.main()
    except Exception as e:
        print(f"Error: job_filter.py failed to execute. Details: {e}")
        return

    print("\nPipeline finished successfully!")

if __name__ == "__main__":
    main()
