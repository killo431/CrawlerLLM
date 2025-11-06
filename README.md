# AI Job Scraping Agent

This project implements a scalable, modular job board scraper to extract job listings from multiple sites. It respects robots.txt, handles dynamic content, and ensures compliance with site policies.

## Project Structure

```
job-scraper/
├── adapters/                  # Site-specific scrapers
│   ├── __init__.py
│   ├── indeed.py
│   ├── linkedin.py
│   └── ...
├── core/
│   ├── __init__.py
│   ├── base_scraper.py       # Abstract base class
│   ├── browser.py            # Headless browser setup
│   ├── storage.py            # Data storage logic
│   ├── logger.py             # Logging setup
│   └── utils.py              # Shared helpers
├── data/
│   └── output/               # Scraped data (CSV/JSON)
├── tests/
│   ├── test_scrapers.py
│   └── test_utils.py
├── .env                      # Environment variables
├── config.yaml               # Site configs, crawl delays, etc.
├── requirements.txt          # Python dependencies
├── main.py                   # Entry point
└── README.md                 # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/killo431/CrawlerLLM.git
   cd CrawlerLLM/job-scraper
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browser binaries for Playwright
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env` and fill in secrets (proxies, API keys if needed).

5. **Edit config.yaml**:
   - Add site-specific settings like URLs, crawl delays, etc.

## Usage

Run the scraper with:
```bash
python main.py
```

This will start scraping based on the configured sites in `config.yaml`.

## Configuration

Edit `config.yaml` to add or modify site adapters:

```yaml
indeed:
  base_url: "https://www.indeed.com/jobs?q=python"
  crawl_delay: 2
  dynamic: true
  max_pages: 10

linkedin:
  base_url: "https://www.linkedin.com/jobs/search/?keywords=python"
  crawl_delay: 5
  dynamic: true
  max_pages: 5
```

## Adding New Sites

1. Create a new file in `adapters/` (e.g., `new_site.py`) inheriting from `BaseScraper`.
2. Implement `extract_fields()` and `handle_pagination()` methods.
3. Add configuration to `config.yaml`.
4. Update `main.py` to load the new adapter.

Example adapter stub:

```python
from core.base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    def extract_fields(self, soup):
        # Extract job data
        pass

    def handle_pagination(self):
        # Handle pagination logic
        pass
```

## Testing

Run tests with:
```bash
pytest tests/
```

## Troubleshooting

- **CAPTCHA/Bot Detection**: Use proxies or rotate user agents. Check `browser.py` for stealth options.
- **403 Errors**: Respect robots.txt and increase crawl delays.
- **Dynamic Content Issues**: Ensure Playwright is installed and configured.
- **Data Validation Errors**: Check pydantic schemas in `storage.py`.

## Compliance & Ethics

- Always respect `robots.txt` and terms of service.
- Use polite headers with contact info.
- Limit request rates to avoid overloading servers.

## Documentation

- [Architecture Diagram](./docs/architecture.png)
- [Site Compliance Matrix](./docs/site_compliance_matrix.csv)
- [Robots and TOS Summary](./docs/robots_and_tos_summary.md)

## Contributing

1. Fork the repo.
2. Create a feature branch.
3. Add tests for new features.
4. Submit a pull request.

## License

MIT License.