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
├── .env
├── config.yaml               # Site configs, crawl delays, etc.
├── requirements.txt
├── README.md
└── main.py                   # Entry point
