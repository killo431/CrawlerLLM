"""Indeed job board scraper."""
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
