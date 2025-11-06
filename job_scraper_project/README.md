# OSINT + Job Scraping Dashboard

[![CI/CD Pipeline](https://github.com/killo431/CrawlerLLM/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/killo431/CrawlerLLM/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, modular job scraping system with OSINT capabilities. Extract job listings from multiple career sites, perform OSINT investigations, and generate new adapters using AI.

## ✨ Features

- **Job Scraping**: Extract job listings from Indeed, LinkedIn, and Glassdoor
- **OSINT Tools**: Phone lookup, digital footprint tracing, and email breach checking
- **AI-Powered**: LLM-based adapter generation for new sites
- **Stealth Capabilities**: Proxy rotation and fingerprint masking
- **Production Ready**: Docker support, CI/CD, comprehensive testing
- **Interactive Dashboard**: Streamlit UI for all features
- **CLI Interface**: Command-line tool for batch processing

## 📋 Requirements

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- Playwright browsers (installed automatically)

## 🚀 Quick Start

### Using Make (Recommended)

```bash
# Install dependencies
make install

# Run the CLI scraper
make run

# Run the dashboard
make dashboard

# Run tests
make test

# Format code
make format
```

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the CLI:**
   ```bash
   python main.py
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Run CLI version
docker-compose --profile cli up job-scraper-cli
```

## 📁 Project Structure

```
job_scraper_project/
├── adapters/              # Site-specific scrapers
│   ├── base_scraper.py   # Abstract base class
│   ├── indeed.py         # Indeed scraper
│   ├── linkedin.py       # LinkedIn scraper
│   └── glassdoor.py      # Glassdoor scraper
├── core/                  # Core functionality
│   ├── browser.py        # Playwright browser automation
│   ├── logger.py         # Centralized logging
│   ├── export_manager.py # Data export (JSON/CSV)
│   ├── config.py         # Configuration management
│   ├── environment.py    # Environment variables
│   ├── proxy.py          # Proxy rotation
│   └── utils.py          # Utility functions
├── scrapers/osint/       # OSINT tools
│   ├── phone_lookup.py   # Phone number lookup
│   ├── footprint_trace.py # Digital footprint tracing
│   └── breach_checker.py # Email breach checking
├── ai_dev/               # AI features
│   └── feature_developer.py # Adapter generation
├── dashboard/            # Streamlit dashboard
│   └── app.py
├── tests/                # Test suite
│   ├── test_base_scraper.py
│   ├── test_export_manager.py
│   ├── test_utils.py
│   └── test_config.py
├── data/output/          # Output data
├── logs/                 # Log files
├── config.yaml           # Configuration file
├── .env.example          # Environment template
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker services
├── Makefile              # Development tasks
├── setup.py              # Package setup
└── pyproject.toml        # Project metadata
```

## 🎯 Usage

### Job Scraping (CLI)

```bash
# Run all scrapers
python main.py

# Results will be saved to data/output/
# - all_jobs.json
# - all_jobs.csv
```

### Job Scraping (Dashboard)

1. Open the dashboard: `streamlit run dashboard/app.py`
2. Navigate to "Job Scraping" tab
3. Select a job board (Indeed, LinkedIn, or Glassdoor)
4. Click "Start Scraping"
5. View and export results

### OSINT Tools

Access through the dashboard:

- **Phone Lookup**: Enter a phone number to get carrier and location info
- **Footprint Trace**: Enter a name to find associated online accounts
- **Breach Checker**: Enter an email to check for known data breaches

### AI Feature Developer

Generate new scraper adapters automatically:

1. Navigate to "AI Feature Developer" tab
2. Enter target site domain
3. Specify fields to extract
4. Generate adapter code
5. Save to adapters/ directory

## ⚙️ Configuration

### Using config.yaml

Edit `config.yaml` to customize:

```yaml
global:
  output_format: json
  log_level: INFO
  max_retries: 3

indeed:
  base_url: "https://www.indeed.com/jobs?q=python"
  crawl_delay: 2
  dynamic: false
```

### Using Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Application Settings
LOG_LEVEL=INFO
OUTPUT_FORMAT=json
MAX_RETRIES=3
TIMEOUT=30

# API Keys (optional)
LINKEDIN_API_KEY=your_api_key_here
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_base_scraper.py -v
```

### Code Quality

```bash
# Format code
make format

# Check formatting
make format-check

# Run linters
make lint

# Type checking
mypy . --ignore-missing-imports
```

### Development Setup

```bash
# Install development dependencies
make install-dev

# This installs:
# - pytest (testing)
# - black (code formatting)
# - flake8 (linting)
# - mypy (type checking)
# - isort (import sorting)
```

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build image
docker build -t job-scraper:latest .

# Run dashboard
docker run -p 8501:8501 -v $(pwd)/data:/app/data job-scraper:latest

# Run CLI
docker run -v $(pwd)/data:/app/data job-scraper:latest python main.py
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# Scale CLI workers
docker-compose --profile cli up --scale job-scraper-cli=3

# View logs
docker-compose logs -f job-scraper

# Stop services
docker-compose down
```

## 🔒 Security

### Best Practices

- Store sensitive data in environment variables (`.env`)
- Never commit `.env` files to version control
- Use proxy rotation for production scraping
- Respect robots.txt and rate limits
- Implement proper error handling and logging

### Security Scanning

The project includes automated security scanning via GitHub Actions:

- Trivy vulnerability scanner
- Dependency vulnerability checks
- Code security analysis

## 📊 CI/CD

Automated pipeline includes:

- ✅ Unit testing across Python 3.11 and 3.12
- ✅ Code linting (flake8)
- ✅ Code formatting checks (black, isort)
- ✅ Type checking (mypy)
- ✅ Docker image building
- ✅ Security scanning (Trivy)

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## ⚠️ Legal & Ethics

This tool is designed for **ethical use only**. Always respect:

- ✓ robots.txt files
- ✓ Terms of service
- ✓ Rate limits
- ✓ Privacy laws (GDPR, CCPA, etc.)
- ✓ Copyright and data ownership

**Intended for:**
- Legitimate research purposes
- Authorized penetration testing
- Educational use
- Personal job search automation (with permission)

**Not intended for:**
- Unauthorized data scraping
- Terms of service violations
- Illegal activities
- Commercial data harvesting without permission

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Format code with black and isort
6. Submit a pull request

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: [https://github.com/killo431/CrawlerLLM/issues](https://github.com/killo431/CrawlerLLM/issues)
- Documentation: See inline code documentation

## 🙏 Acknowledgments

This project uses:
- [Playwright](https://playwright.dev/) for browser automation
- [Streamlit](https://streamlit.io/) for the dashboard UI
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [Loguru](https://loguru.readthedocs.io/) for logging

---

**Project Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: November 6, 2025
