# OSINT + Job Scraping Dashboard

This project was automatically extracted and reconstructed from conversation data.

## Overview

This is a modular, stealth-capable scraping agent designed to extract job listings from multiple career sites. The system includes:

- **Scraping Adapters**: Indeed, LinkedIn, Glassdoor
- **OSINT Tools**: Phone lookup, digital footprint trace, breach checker
- **Dashboard**: Streamlit-based UI for all tools
- **AI Features**: LLM-powered adapter generation
- **Stealth Capabilities**: Proxy rotation, fingerprint masking

## Project Structure


```
Proxy/Anti-bot	Smartproxy or ScraperAPI	Rotate IPs, handle captchas
Login/API requirements
🛠️ Phase 2: Technology Selection
Guidelines
Use Python 3.11+
Choose:
Scrapy for structured crawling
Playwright for JS-heavy pages
loguru for logging
pydantic for schema validation
httpx or aiohttp for async requests
Proxy support: Smartproxy, ScraperAPI, or rotating user agents
core/browser.py	Launch Playwright with stealth patches
core/proxy.py	Rotate residential proxies
core/session.py	Persist cookies and session state
core/behavior.py	Simulate human-like interaction
core/llm_brain.py	Use LLM to adapt to DOM changes
adapters/*.py	Site-specific scrapers (e.g., indeed.py)
main.py	Orchestrate scraping flow
🛠️ Implementation Phases
Phase 1: Environment Setup
docs/adding_new_site.md: Adapter template and guide
docs/troubleshooting.md: Common errors and fixes
config.yaml: Crawl delay, dynamic flags, proxy rules
👥 Team Roles & Handoff
Role	Responsibility
Research Analyst	Site compliance, robots.txt, TOS review
QA/Tester	Validation, unit testing
docs/adding_new_site.md – Adapter template
docs/troubleshooting.md – Common issues
🧠 LLM Brain
Uses OpenAI or local LLMs to adapt to DOM changes and suggest selectors.
core/browser.py
core/proxy.py
core/session.py
core/behavior.py
core/llm_brain.py
🧩 Scraper Adapters
adapters/base_scraper.py
adapters/indeed.py
adapters/linkedin.py
adapters/glassdoor.py
🧠 AI Feature Developer
ai_dev/feature_developer.py
📞 OSINT Modules
scrapers/osint/phone_lookup.py
scrapers/osint/footprint_trace.py
📊 Dashboard
dashboard/app.py
🐳 Deployment
```


## Requirements

```
streamlit
playwright
pydantic
loguru
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. Run the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## Features

### Job Scraping
- Modular adapter system for multiple job boards
- Retry logic with LLM fallback for broken selectors
- Export to JSON/CSV

### OSINT Tools
- Phone number lookup
- Digital footprint tracing
- Email breach checking

### Stealth Features
- Proxy rotation
- Custom headers
- Fingerprint masking
- Human behavior simulation

## Documentation

See the `docs/` directory for detailed documentation on:
- Adding new scraping adapters
- Configuration options
- Troubleshooting guide

## License

MIT License
