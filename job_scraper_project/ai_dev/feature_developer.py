"""AI-powered feature and adapter generation."""

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
