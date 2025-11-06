"""Setup configuration for the Job Scraper project."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="job-scraper",
    version="1.0.0",
    author="CrawlerLLM Team",
    description="A modular, production-ready job scraping system with OSINT capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/killo431/CrawlerLLM",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "playwright>=1.40.0",
        "pydantic>=2.0.0",
        "loguru>=0.7.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pyyaml>=6.0.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "job-scraper=main:main",
        ],
    },
)
