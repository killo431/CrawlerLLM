"""LinkedIn job board scraper."""
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
