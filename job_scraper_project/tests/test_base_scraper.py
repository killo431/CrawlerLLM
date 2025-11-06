"""Unit tests for base scraper functionality."""
import pytest
from adapters.base_scraper import BaseScraper, ScraperError


class MockScraper(BaseScraper):
    """Mock scraper for testing."""
    
    def start_url(self) -> str:
        return "https://example.com"
    
    def extract_fields(self):
        return [
            {"title": "Test Job", "company": "Test Corp", "location": "Test City"}
        ]


class FailingScraper(BaseScraper):
    """Scraper that fails for testing error handling."""
    
    def start_url(self) -> str:
        return "https://example.com"
    
    def extract_fields(self):
        raise Exception("Mock failure")


def test_scraper_initialization():
    """Test scraper can be initialized."""
    scraper = MockScraper()
    assert scraper.max_pages == 1
    assert scraper.current_page == 0


def test_scraper_run():
    """Test scraper run method."""
    scraper = MockScraper()
    results = scraper.run()
    assert len(results) == 1
    assert results[0]["title"] == "Test Job"


def test_scraper_start_url():
    """Test start_url method."""
    scraper = MockScraper()
    assert scraper.start_url() == "https://example.com"


def test_scraper_validation():
    """Test result validation."""
    scraper = MockScraper()
    valid_result = {"title": "Job", "company": "Company", "location": "City"}
    invalid_result = {"title": "Job"}
    
    assert scraper.validate_result(valid_result) is True
    assert scraper.validate_result(invalid_result) is False


def test_scraper_error_handling():
    """Test error handling in scraper."""
    scraper = FailingScraper()
    with pytest.raises(ScraperError):
        scraper.run()


def test_scraper_pagination():
    """Test pagination handling."""
    scraper = MockScraper()
    assert scraper.handle_pagination() is False
