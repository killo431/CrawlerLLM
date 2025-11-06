"""Glassdoor job board scraper."""
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
