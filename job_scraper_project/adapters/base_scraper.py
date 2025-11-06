"""Base scraper class for all adapters."""
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
