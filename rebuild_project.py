#!/usr/bin/env python3
"""
Enhanced script to rebuild the complete project from page_text (1).txt
This creates a working job scraping dashboard with all components properly organized.
"""

import os
import re
from pathlib import Path

def create_complete_project():
    """Create the complete project structure with all necessary files."""
    
    base_dir = 'job_scraper_project'
    
    # Define all files and their content
    files = {
        # Core modules
        'core/__init__.py': '',
        
        'core/browser.py': '''"""Browser automation with stealth capabilities."""
from playwright.sync_api import sync_playwright

def launch_stealth_browser():
    """Launch a browser with stealth patches to avoid detection."""
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        # Create new context
        context = browser.new_context()
        
        # Create new page
        page = context.new_page()
        
        # Apply stealth patches (navigator.webdriver masking, etc.)
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        return page
''',
        
        'core/logger.py': '''"""Centralized logging module."""
import logging
import os

def setup_logger(name="scraper", level=logging.INFO, log_dir="logs"):
    """Set up a logger with file and console handlers."""
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    fh = logging.FileHandler(f"{log_dir}/{name}.log")
    fh.setLevel(level)
    
    # Console handler (only errors)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
''',
        
        'core/export_manager.py': '''"""Unified export manager for all data formats."""
import json
import csv
import os

def export_data(data, name, format="json", folder="data/output"):
    """Export data to specified format."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.{format}")
    
    if format == "json":
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        if not data:
            print(f"[Warning] No data to export to {path}")
            return
        keys = data[0].keys()
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    
    print(f"[Exported] {len(data) if isinstance(data, list) else 1} records to {path}")
''',
        
        'core/proxy.py': '''"""Proxy rotation and stealth headers."""
import random

PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080"
]

STEALTH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}

def get_random_proxy():
    """Get a random proxy from the pool."""
    return random.choice(PROXIES)

def apply_stealth_headers(context):
    """Apply stealth headers to browser context."""
    context.set_extra_http_headers(STEALTH_HEADERS)
''',
        
        'core/benchmark.py': '''"""Adapter benchmarking and performance metrics."""
import time
from core.logger import setup_logger

logger = setup_logger("benchmark")

def benchmark_adapter(adapter_class):
    """Benchmark a scraper adapter."""
    scraper = adapter_class()
    start = time.time()
    try:
        scraper.run()
        duration = time.time() - start
        logger.info(f"{adapter_class.__name__} completed in {duration:.2f}s")
        return {"adapter": adapter_class.__name__, "duration": duration}
    except Exception as e:
        logger.error(f"{adapter_class.__name__} failed: {e}")
        return {"adapter": adapter_class.__name__, "error": str(e)}
''',
        
        'core/utils.py': '''"""Utility functions including retry logic."""
import time
import functools

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"[Retry] {func.__name__} failed: {e}")
                    time.sleep(delay * (backoff ** attempts))
                    attempts += 1
            print(f"[Retry] {func.__name__} failed after {max_attempts} attempts.")
            return None
        return wrapper
    return decorator
''',
        
        # Adapters
        'adapters/__init__.py': '',
        
        'adapters/base_scraper.py': '''"""Base scraper class for all adapters."""
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """Base class for all scraper adapters."""
    
    def __init__(self):
        self.page = None
    
    def run(self):
        """Main execution method."""
        return self.extract_fields()
    
    @abstractmethod
    def start_url(self) -> str:
        """Return the starting URL for scraping."""
        pass
    
    @abstractmethod
    def extract_fields(self) -> list:
        """Extract job fields from the page."""
        pass
    
    def handle_pagination(self) -> bool:
        """Handle pagination if supported. Return True if more pages exist."""
        return False
''',
        
        'adapters/indeed.py': '''"""Indeed job board scraper."""
from adapters.base_scraper import BaseScraper
from core.logger import setup_logger

logger = setup_logger("indeed")

class IndeedScraper(BaseScraper):
    """Scraper for Indeed job board."""
    
    def start_url(self) -> str:
        return "https://www.indeed.com/jobs?q=python+developer"
    
    def extract_fields(self) -> list:
        """Extract job listings from Indeed."""
        # Mock data for demonstration
        jobs = [
            {
                "title": "Python Developer",
                "company": "Indeed Corp",
                "location": "Austin, TX",
                "description": "Looking for experienced Python developer",
                "link": "https://www.indeed.com/viewjob?jk=123456"
            }
        ]
        logger.info(f"Extracted {len(jobs)} jobs from Indeed")
        return jobs
''',
        
        'adapters/linkedin.py': '''"""LinkedIn job board scraper."""
from adapters.base_scraper import BaseScraper
from core.logger import setup_logger

logger = setup_logger("linkedin")

class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job board."""
    
    def start_url(self) -> str:
        return "https://www.linkedin.com/jobs/search/?keywords=python+developer"
    
    def extract_fields(self) -> list:
        """Extract job listings from LinkedIn."""
        # Mock data for demonstration
        jobs = [
            {
                "title": "Backend Engineer",
                "company": "LinkedIn",
                "location": "San Francisco, CA",
                "description": "Join our backend team",
                "link": "https://www.linkedin.com/jobs/view/123456"
            }
        ]
        logger.info(f"Extracted {len(jobs)} jobs from LinkedIn")
        return jobs
''',
        
        'adapters/glassdoor.py': '''"""Glassdoor job board scraper."""
from adapters.base_scraper import BaseScraper
from core.logger import setup_logger

logger = setup_logger("glassdoor")

class GlassdoorScraper(BaseScraper):
    """Scraper for Glassdoor job board."""
    
    def start_url(self) -> str:
        return "https://www.glassdoor.com/Job/python-developer-jobs"
    
    def extract_fields(self) -> list:
        """Extract job listings from Glassdoor."""
        # Mock data for demonstration
        jobs = [
            {
                "title": "Software Engineer",
                "company": "Glassdoor Inc",
                "location": "Mill Valley, CA",
                "description": "Work with our engineering team",
                "link": "https://www.glassdoor.com/job-listing/123456"
            }
        ]
        logger.info(f"Extracted {len(jobs)} jobs from Glassdoor")
        return jobs
''',
        
        # OSINT tools
        'scrapers/__init__.py': '',
        'scrapers/osint/__init__.py': '',
        
        'scrapers/osint/phone_lookup.py': '''"""Phone number lookup functionality."""
from core.export_manager import export_data

def lookup_phone(phone):
    """Look up phone number information."""
    # Mock implementation
    return {
        "phone": phone,
        "carrier": "Verizon",
        "location": "Austin, TX",
        "type": "Mobile"
    }

def export_phone_result(result, phone):
    """Export phone lookup results."""
    export_data([result], f"phone_{phone}", "json")
''',
        
        'scrapers/osint/footprint_trace.py': '''"""Digital footprint tracing."""
from core.export_manager import export_data

def trace_footprint(name):
    """Trace digital footprint for a name."""
    # Mock implementation
    return {
        "name": name,
        "accounts": ["LinkedIn", "GitHub", "Twitter"],
        "location": "Austin, TX"
    }

def export_footprint_result(result, name):
    """Export footprint trace results."""
    export_data([result], f"footprint_{name.replace(' ', '_')}", "json")
''',
        
        'scrapers/osint/breach_checker.py': '''"""Email breach checking."""
from core.export_manager import export_data

def check_email_breach(email):
    """Check if email appears in known breaches."""
    # Mock implementation
    return {
        "email": email,
        "breaches": ["LinkedIn 2012", "Adobe 2013"],
        "count": 2
    }

def export_breach_result(result, email):
    """Export breach check results."""
    export_data([result], f"breach_{email.replace('@', '_at_')}", "json")
''',
        
        # AI development tools
        'ai_dev/__init__.py': '',
        
        'ai_dev/feature_developer.py': '''"""AI-powered feature and adapter generation."""

def generate_adapter(site: str, field: str) -> str:
    """Generate a new scraper adapter using LLM."""
    class_name = f"{site.capitalize()}Scraper"
    selector = f".{field}_selector"
    
    template = f"""from adapters.base_scraper import BaseScraper
from core.logger import setup_logger

logger = setup_logger("{site}")

class {class_name}(BaseScraper):
    def start_url(self) -> str:
        return "https://{site}.com/jobs?q=python+developer"
    
    def extract_fields(self) -> list:
        job_cards = self.page.locator(".job_card_selector")
        jobs = []
        for i in range(job_cards.count()):
            card = job_cards.nth(i)
            job = {{
                "{field}": card.locator("{selector}").inner_text()
            }}
            jobs.append(job)
        logger.info(f"Extracted {{len(jobs)}} jobs from {site}")
        return jobs
"""
    return template
''',
        
        # Dashboard
        'dashboard/app.py': '''"""Streamlit dashboard for OSINT and job scraping."""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.export_manager import export_data

st.set_page_config(layout="wide", page_title="OSINT + Job Scraping Dashboard")
st.title("🧠 OSINT + Job Scraping Dashboard")

tabs = st.tabs([
    "Job Scraping", 
    "Phone Lookup", 
    "Footprint Trace", 
    "Breach Checker",
    "AI Feature Developer", 
    "About"
])

# Tab 1: Job Scraping
with tabs[0]:
    st.header("🧳 Job Scraper")
    
    site = st.selectbox("Select Job Board", ["Indeed", "LinkedIn", "Glassdoor"])
    
    if st.button("Start Scraping"):
        with st.spinner(f"Scraping {site}..."):
            if site == "Indeed":
                from adapters.indeed import IndeedScraper
                scraper = IndeedScraper()
            elif site == "LinkedIn":
                from adapters.linkedin import LinkedInScraper
                scraper = LinkedInScraper()
            else:
                from adapters.glassdoor import GlassdoorScraper
                scraper = GlassdoorScraper()
            
            jobs = scraper.run()
            
            if jobs:
                export_data(jobs, f"{site.lower()}_jobs", "json")
                export_data(jobs, f"{site.lower()}_jobs", "csv")
                st.success(f"✅ Scraped {len(jobs)} jobs from {site}")
                st.dataframe(jobs)
            else:
                st.warning("No jobs found")

# Tab 2: Phone Lookup
with tabs[1]:
    st.header("📞 Phone Lookup")
    from scrapers.osint.phone_lookup import lookup_phone, export_phone_result
    
    phone = st.text_input("Enter phone number")
    if st.button("Lookup Phone"):
        if phone:
            result = lookup_phone(phone)
            export_phone_result(result, phone)
            st.json(result)
        else:
            st.warning("Please enter a phone number")

# Tab 3: Digital Footprint
with tabs[2]:
    st.header("🕵️ Digital Footprint Trace")
    from scrapers.osint.footprint_trace import trace_footprint, export_footprint_result
    
    name = st.text_input("Enter full name")
    if st.button("Trace Footprint"):
        if name:
            result = trace_footprint(name)
            export_footprint_result(result, name)
            st.json(result)
        else:
            st.warning("Please enter a name")

# Tab 4: Breach Checker
with tabs[3]:
    st.header("🛡️ Email Breach Checker")
    from scrapers.osint.breach_checker import check_email_breach, export_breach_result
    
    email = st.text_input("Enter email address")
    if st.button("Check Breaches"):
        if email:
            result = check_email_breach(email)
            export_breach_result(result, email)
            st.json(result)
        else:
            st.warning("Please enter an email address")

# Tab 5: AI Feature Developer
with tabs[4]:
    st.header("🧠 AI Feature Developer")
    from ai_dev.feature_developer import generate_adapter
    
    site = st.text_input("Target site/domain (e.g., monster, ziprecruiter)")
    field = st.text_input("Field to extract (e.g., salary, benefits)")
    
    if st.button("Generate Adapter"):
        if site and field:
            code = generate_adapter(site, field)
            st.code(code, language="python")
            
            # Option to save
            save_path = f"adapters/{site}.py"
            if st.button("Save Adapter"):
                with open(save_path, "w") as f:
                    f.write(code)
                st.success(f"Adapter saved to {save_path}")
        else:
            st.warning("Please fill in all fields")

# Tab 6: About
with tabs[5]:
    st.header("📚 About")
    st.markdown("""
    ## OSINT + Job Scraping Dashboard
    
    This is a modular, stealth-capable scraping agent designed to extract job listings 
    from multiple career sites. The system includes:
    
    - **Scraping Adapters**: Indeed, LinkedIn, Glassdoor
    - **OSINT Tools**: Phone lookup, digital footprint trace, breach checker
    - **AI Features**: LLM-powered adapter generation
    - **Stealth Capabilities**: Proxy rotation, fingerprint masking
    
    ### Features
    - Modular adapter system
    - Retry logic with fallback
    - Export to JSON/CSV
    - Centralized logging
    - Benchmark tracking
    
    ### Tech Stack
    - Python 3.11+
    - Streamlit
    - Playwright (for browser automation)
    - Pydantic (for data validation)
    
    Built for cybersecurity research and OSINT automation.
    """)
''',
        
        # Configuration and docs
        'config.yaml': '''# Global configuration
global:
  output_format: json
  log_level: INFO
  
# Site-specific configurations
indeed:
  base_url: "https://www.indeed.com/jobs?q=python"
  crawl_delay: 2
  dynamic: false

linkedin:
  base_url: "https://www.linkedin.com/jobs/search/?keywords=python"
  crawl_delay: 3
  dynamic: true

glassdoor:
  base_url: "https://www.glassdoor.com/Job/python-jobs"
  crawl_delay: 2
  dynamic: true
''',
        
        'requirements.txt': '''streamlit>=1.28.0
playwright>=1.40.0
pydantic>=2.0.0
loguru>=0.7.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pyyaml>=6.0.0
''',
        
        'README.md': '''# OSINT + Job Scraping Dashboard

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
''',
        
        '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Data and logs
data/output/
logs/
*.log

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
''',
        
        'main.py': '''"""Main entry point for running scrapers via command line."""
import sys
from adapters.indeed import IndeedScraper
from adapters.linkedin import LinkedInScraper
from adapters.glassdoor import GlassdoorScraper
from core.export_manager import export_data

def main():
    """Run scrapers and export results."""
    print("=" * 60)
    print("Job Scraping Agent")
    print("=" * 60)
    
    scrapers = {
        'indeed': IndeedScraper(),
        'linkedin': LinkedInScraper(),
        'glassdoor': GlassdoorScraper()
    }
    
    all_jobs = []
    
    for name, scraper in scrapers.items():
        print(f"\\nScraping {name.capitalize()}...")
        try:
            jobs = scraper.run()
            all_jobs.extend(jobs)
            print(f"✅ Found {len(jobs)} jobs")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    if all_jobs:
        print(f"\\nTotal jobs found: {len(all_jobs)}")
        export_data(all_jobs, "all_jobs", "json")
        export_data(all_jobs, "all_jobs", "csv")
        print("\\nResults exported to data/output/")
    else:
        print("\\nNo jobs found")
    
    print("\\nDone!")

if __name__ == '__main__':
    main()
'''
    }
    
    # Create all files
    created_files = []
    for filepath, content in files.items():
        full_path = os.path.join(base_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(full_path)
        print(f"[Created] {full_path}")
    
    # Create empty directories
    dirs = [
        'data/output',
        'logs',
        'docs'
    ]
    
    for dir_path in dirs:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        # Create .gitkeep to preserve empty directories
        gitkeep = os.path.join(full_path, '.gitkeep')
        with open(gitkeep, 'w') as f:
            pass
        print(f"[Created] {full_path}/ (empty directory)")
    
    return base_dir, created_files

def main():
    """Main execution function."""
    print("=" * 70)
    print("Rebuilding Complete Job Scraping Project")
    print("=" * 70)
    
    base_dir, files = create_complete_project()
    
    print("\\n" + "=" * 70)
    print(f"✅ Successfully created {len(files)} files")
    print("=" * 70)
    print(f"\\nProject location: {base_dir}/")
    print("\\nNext steps:")
    print("1. cd job_scraper_project")
    print("2. pip install -r requirements.txt")
    print("3. playwright install")
    print("4. streamlit run dashboard/app.py")
    print("\\nOr run CLI version:")
    print("5. python main.py")
    print("=" * 70)

if __name__ == '__main__':
    main()
