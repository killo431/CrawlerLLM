"""Base scraper class for all adapters with improved error handling."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ScraperError(Exception):
    """Base exception for scraper errors."""
    pass


class ScraperConnectionError(ScraperError):
    """Exception for connection-related errors."""
    pass


class ScraperParseError(ScraperError):
    """Exception for parsing-related errors."""
    pass


class BaseScraper(ABC):
    """Base class for all scraper adapters."""
    
    def __init__(self, max_pages: int = 1):
        """
        Initialize base scraper.
        
        Args:
            max_pages: Maximum number of pages to scrape
        """
        self.page: Optional[Any] = None
        self.max_pages = max_pages
        self.current_page = 0
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def run(self) -> List[Dict[str, Any]]:
        """
        Main execution method.
        
        Returns:
            List of scraped job dictionaries
            
        Raises:
            ScraperError: If scraping fails
        """
        try:
            self.logger.info(f"Starting scraper for {self.__class__.__name__}")
            results = self.extract_fields()
            self.logger.info(f"Successfully scraped {len(results)} items")
            return results
        except Exception as e:
            self.logger.error(f"Scraper failed: {e}")
            raise ScraperError(f"Failed to scrape: {e}") from e
    
    @abstractmethod
    def start_url(self) -> str:
        """
        Return the starting URL for scraping.
        
        Returns:
            Starting URL as string
        """
        pass
    
    @abstractmethod
    def extract_fields(self) -> List[Dict[str, Any]]:
        """
        Extract job fields from the page.
        
        Returns:
            List of job dictionaries with extracted fields
        """
        pass
    
    def handle_pagination(self) -> bool:
        """
        Handle pagination if supported.
        
        Returns:
            True if more pages exist, False otherwise
        """
        return False
    
    def validate_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate a single result.
        
        Args:
            result: Dictionary containing scraped data
            
        Returns:
            True if result is valid, False otherwise
        """
        required_fields = ['title', 'company']
        return all(field in result and result[field] for field in required_fields)
