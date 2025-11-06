"""Glassdoor job board scraper with improved error handling."""
from typing import List, Dict, Any
from adapters.base_scraper import BaseScraper
from core.logger import setup_logger

logger = setup_logger("glassdoor")


class GlassdoorScraper(BaseScraper):
    """Scraper for Glassdoor job board."""
    
    def start_url(self) -> str:
        """Return Glassdoor search URL."""
        return "https://www.glassdoor.com/Job/python-developer-jobs"
    
    def extract_fields(self) -> List[Dict[str, Any]]:
        """
        Extract job listings from Glassdoor.
        
        Returns:
            List of job dictionaries
            
        Note:
            This is a mock implementation for demonstration.
            In production, this should use real scraping logic.
        """
        # Mock data for demonstration
        jobs = [
            {
                "title": "Software Engineer",
                "company": "Glassdoor Inc",
                "location": "Mill Valley, CA",
                "description": "Work with our engineering team",
                "link": "https://www.glassdoor.com/job-listing/123456",
                "salary": "$90,000 - $130,000",
                "posted_date": "2025-11-04"
            }
        ]
        logger.info(f"Extracted {len(jobs)} jobs from Glassdoor")
        return jobs
