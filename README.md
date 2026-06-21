# 🔍 Auto Job Scraper Pipeline

An automated Python pipeline that scrapes live job postings from the [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html), filters for tech/programming roles, and delivers a formatted report directly to a Discord channel via webhook.

## Features

- **Live API Scraping** — Fetches real-time job listings from any Greenhouse-hosted job board (no HTML parsing required)
- **Data Processing** — Extracts and structures job title, company, location, URL, and update date into a clean CSV
- **Configurable Filtering** — Filters for programming-related roles via a customizable keyword pattern, set via `.env` (falls back to a built-in default if not set)
- **Discord Reporting** — Sends a formatted job market report with top matches to a Discord channel via webhook
- **Pipeline Architecture** — Orchestrated via a single entry point (`main.py`) for easy execution

## How It Works

```
main.py (orchestrator)
  ├── scraper.py    → Fetches jobs from Greenhouse API → Saves to job_data.csv
  └── job_filter.py → Reads CSV → Filters tech roles → Sends Discord report
```

1. **Scrape** — `scraper.py` calls the Greenhouse Job Board API, extracts job data from the JSON response, and saves it to `job_data.csv`
2. **Filter & Report** — `job_filter.py` reads the CSV, filters for matching job titles using a configurable keyword pattern, and posts a summary report to Discord

## Tech Stack

| Tool             | Purpose                                        |
| ---------------- | ---------------------------------------------- |
| Python 3         | Core language                                  |
| Requests         | HTTP client for API calls and webhook delivery |
| Pandas           | Data manipulation and CSV I/O                  |
| python-dotenv    | Secure environment variable loading            |
| Greenhouse API   | Job listing data source                        |
| Discord Webhooks | Report delivery                                |

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/NoahIsFine/auto-job-scraper-pipeline.git
cd auto-job-scraper-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GREENHOUSE_BOARD_TOKEN=your_company_board_token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
JOB_FILTER_PATTERN=Developer|Software|Engineer|Programmer|Backend|Frontend|Full Stack
```

| Variable                 | Required | Description                                                                                                                      |
| ------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `GREENHOUSE_BOARD_TOKEN` | ✅       | The company identifier from Greenhouse (e.g., `reddit`, `stripe`). Find it in the URL: `boards.greenhouse.io/{BOARD_TOKEN}/jobs` |
| `DISCORD_WEBHOOK_URL`    | ✅       | Create one in your Discord server under Server Settings → Integrations → Webhooks                                                |
| `JOB_FILTER_PATTERN`     | ❌       | Pipe-separated keywords to match against job titles. Falls back to a built-in default if not set                                 |

### 4. Run the pipeline

```bash
python main.py
```

## Sample Output (Discord)

```
📊 TECH JOB MARKET REPORT 📊
Total Job Postings Scanned: 159

=========================================
🔹 Programming Roles Found: 28
=========================================

LATEST OPPORTUNITIES SUBSET:
💻 Top Programming Positions:

Senior Software Engineer, Ads
https://job-boards.greenhouse.io/reddit/jobs/6909091

Software Engineer, Ads
https://job-boards.greenhouse.io/reddit/jobs/6469397

🏁 Pipeline execution completed successfully.
```

## Project Structure

```
auto-job-scraper-pipeline/
├── main.py          # Pipeline orchestrator
├── scraper.py       # Greenhouse API scraper
├── job_filter.py    # Job filter + Discord reporter
├── study_docs/      # Learning notes and early drafts (not production code)
├── .env             # API tokens + config (not tracked)
├── .gitignore       # Ignored files
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## License

This project is open source and available under the [MIT License](LICENSE).
