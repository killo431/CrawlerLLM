# JobCopilot - Undetectable AI Application Generator

[![CI/CD Pipeline](https://github.com/killo431/CrawlerLLM/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/killo431/CrawlerLLM/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready system for **AI-powered job application generation** with **intelligent job scraping**. Generate resumes and cover letters that are undetectable by AI detection systems like Turnitin, Originality.ai, and GPTZero.

## 🚀 JobCopilot - AI Detection Evasion System

**Based on "The Detection Arms Race" research paper**, JobCopilot creates application documents designed to bypass AI detection systems used by hiring managers and ATS.

### Core Features

- ⚙️ **Configuration Wizard**: Multi-step setup interface (NEW!)
  - Step 1: Job preferences (location, types, titles)
  - Step 2: Optional filters (experience, salary)
  - Step 3: Resume upload and selection
  - Step 4: Writing style customization
- 🎯 **Stealth Engine**: Uses Google Gemini 2.5 Pro (53% detection rate vs 99%+ for other models)
- 📊 **Application Stealth Score**: Real-time AI detection risk analysis (0-100% scale)
- 🎨 **Authenticity Polish Wizard**: 3-step guided editing (Burstiness, Perplexity, Stylometry)
- 🎤 **AI Voice Cloning**: Fine-tune personalized models on your writing style
- 🎛️ **Advanced Style Controls**: Perplexity, burstiness, tone, and imperfection sliders

**Target: <20% detection rate = Safe to submit**

[📚 Full Feature Documentation](docs/JOBCOPILOT_FEATURES.md) | [📖 Research Paper Summary](docs/DETECTION_ARMS_RACE.md)

## ✨ Features

### JobCopilot Application Generation
- **Resume Generation**: AI-generated resumes with low detectability
- **Cover Letter Generation**: Personalized cover letters matching your style
- **Stealth Scoring**: Detection risk analysis with actionable suggestions
- **Voice Cloning**: Train models on your writing samples
- **Authenticity Polish**: Fix AI markers (fingerprint words, burstiness, perplexity)

### Job Scraping & Intelligence
- **Job Extraction**: Scrape Indeed, LinkedIn, and Glassdoor
- **Export**: JSON and CSV formats
- **Benchmarking**: Performance tracking
- **AI-Powered Parsing**: Intelligent data extraction

### Infrastructure
- **Production Ready**: Docker support, CI/CD, comprehensive testing (70+ tests)
- **Interactive Dashboard**: Streamlit UI with complete workflow
- **CLI Interface**: Command-line batch processing
- **Modular Architecture**: Easy to extend and customize

## 📋 Requirements

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- Playwright browsers (installed automatically)

## 🚀 One-Click Quick Start

### Option 1: Launch Script (Easiest) ⭐

#### Linux/Mac:
```bash
./launch.sh
```

#### Windows:
```cmd
launch.bat
```

**What it does:**
- ✅ Checks system requirements
- ✅ Installs dependencies automatically
- ✅ Installs Playwright browsers
- ✅ Interactive menu to choose application
- ✅ Launches your selected app instantly

### Option 2: Make Commands (Recommended)

```bash
# One-click launch with menu
make launch

# Or launch specific app
make home          # Home page (recommended)
make wizard        # Configuration wizard
make main          # Main dashboard
make dashboard     # Job scraping
make demo          # Demo script

# Docker one-click
make docker-launch       # Launch in Docker
```

### Option 3: Docker (For Production)

```bash
# One-click Docker launch
docker-compose up -d

# Access at http://localhost:8501
```

### Option 4: Manual Launch

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Launch home page
streamlit run dashboard/home.py

# Or run the demo
python demo_jobcopilot.py
```

See [ONE_CLICK_DEPLOY.md](docs/ONE_CLICK_DEPLOY.md) for complete deployment guide.

## 📖 Using the Application

### First-Time Users
1. Run `./launch.sh` (or `launch.bat` on Windows)
2. Select option 1 (Home Page)
3. Click "Start Setup →" to begin wizard
4. Complete 4-step configuration
5. Generate your first AI application!

### Experienced Users
1. Run `make home` to launch home page
2. Click "Generate Now →" for direct access
3. Or use `make main` for main dashboard

### Available Applications
- **Home Page** (Port 8501) - Landing page with quick access
- **Configuration Wizard** (Port 8502) - 4-step guided setup
- **Main Dashboard** (Port 8503) - AI application generation
- **Job Scraping** (Port 8504) - Job board scraping

## 🧪 Testing

```bash
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

3. **Run JobCopilot:**
   ```bash
   # Interactive dashboard
   streamlit run dashboard/jobcopilot_app.py
   
   # Or demo
   python demo_jobcopilot.py
   ```

4. **Run job scraper CLI:**
   ```bash
   python main.py
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
├── ai_dev/               # AI features (JobCopilot)
│   ├── text_generator.py    # Stealth Engine
│   ├── stealth_scorer.py    # AI detection scoring
│   ├── voice_cloning.py     # Personalized models
│   ├── authenticity_polish.py # Polish wizard
│   └── feature_developer.py # Adapter generation
├── dashboard/            # Streamlit dashboards
│   ├── jobcopilot_app.py # JobCopilot UI (main)
│   └── app.py            # Legacy scraper UI
├── tests/                # Test suite (70+ tests)
│   ├── test_text_generator.py
│   ├── test_stealth_scorer.py
│   ├── test_voice_cloning.py
│   ├── test_authenticity_polish.py
│   ├── test_base_scraper.py
│   └── ...
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

### JobCopilot - Generate Undetectable Applications

**Recommended Workflow:**

```bash
# Run the JobCopilot dashboard
streamlit run dashboard/jobcopilot_app.py

# Or run the demo
python demo_jobcopilot.py
```

**Complete Process:**

1. **Setup Voice Profile** (Optional but recommended)
   - Upload 3-5 writing samples
   - Train personalized model
   - System learns your writing style

2. **Generate Application**
   - Enter your profile details
   - Enter job requirements
   - Click "Generate" → Creates resume + cover letter

3. **Check Stealth Score**
   - System automatically calculates detection risk
   - Target: <20% = Safe to submit
   - View specific issues and suggestions

4. **Polish (if needed)**
   - Use Authenticity Wizard for guided editing
   - Fix burstiness (sentence variation)
   - Fix perplexity (add personal touches)
   - Fix stylometry (remove AI-fingerprint words)

5. **Final Check & Submit**
   - Recalculate score
   - Download documents
   - Submit with confidence!

[📚 Full API Documentation](docs/JOBCOPILOT_FEATURES.md)

### Job Scraping (CLI)

```bash
# Run all scrapers
python main.py

# Results will be saved to data/output/
# - all_jobs.json
# - all_jobs.csv
```

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
