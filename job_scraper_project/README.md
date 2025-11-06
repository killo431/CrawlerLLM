# OSINT + Job Scraping Dashboard

This project is a modular, stealth-capable scraping agent designed to extract job listings from multiple career sites.

## Features

- **Job Scraping**: Extract job listings from Indeed, LinkedIn, and Glassdoor
- **OSINT Tools**: Phone lookup, digital footprint tracing, and email breach checking
- **AI-Powered**: LLM-based adapter generation for new sites
- **Stealth Capabilities**: Proxy rotation and fingerprint masking
- **Dashboard**: Interactive Streamlit UI for all features

## Project Structure

```
job_scraper_project/
├── adapters/           # Site-specific scrapers
│   ├── base_scraper.py
│   ├── indeed.py
│   ├── linkedin.py
│   └── glassdoor.py
├── core/               # Core functionality
│   ├── browser.py
│   ├── logger.py
│   ├── export_manager.py
│   ├── proxy.py
│   └── utils.py
├── scrapers/osint/     # OSINT tools
│   ├── phone_lookup.py
│   ├── footprint_trace.py
│   └── breach_checker.py
├── ai_dev/             # AI features
│   └── feature_developer.py
├── dashboard/          # Streamlit dashboard
│   └── app.py
├── data/output/        # Output data
├── logs/               # Log files
└── config.yaml         # Configuration
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install
   ```

3. Run the dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

## Usage

### Job Scraping
1. Open the dashboard
2. Select a job board (Indeed, LinkedIn, or Glassdoor)
3. Click "Start Scraping"
4. View and export results

### OSINT Tools
- **Phone Lookup**: Enter a phone number to get carrier and location info
- **Footprint Trace**: Enter a name to find associated online accounts
- **Breach Checker**: Enter an email to check for known data breaches

### AI Feature Developer
Generate new scraper adapters automatically:
1. Enter target site domain
2. Specify fields to extract
3. Generate adapter code
4. Save to adapters/ directory

## Configuration

Edit `config.yaml` to customize:
- Output formats
- Crawl delays
- Site-specific settings
- Proxy configuration

## License

MIT License

## Security Note

This tool is designed for ethical use only. Always respect:
- robots.txt files
- Terms of service
- Rate limits
- Privacy laws

Use responsibly for legitimate research and automation purposes.
