"""Main entry point for running scrapers via command line."""
import sys
import logging
from typing import List, Dict, Any
from adapters.indeed import IndeedScraper
from adapters.linkedin import LinkedInScraper
from adapters.glassdoor import GlassdoorScraper
from core.export_manager import export_data
from core.logger import setup_logger

# Setup main logger
logger = setup_logger("main")


def run_scraper(name: str, scraper_class) -> List[Dict[str, Any]]:
    """
    Run a single scraper and handle errors.
    
    Args:
        name: Display name of the scraper
        scraper_class: Scraper class to instantiate
        
    Returns:
        List of scraped jobs or empty list on error
    """
    print(f"\nScraping {name.capitalize()}...")
    try:
        scraper = scraper_class()
        jobs = scraper.run()
        print(f"✅ Found {len(jobs)} jobs")
        logger.info(f"Successfully scraped {len(jobs)} jobs from {name}")
        return jobs
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Failed to scrape {name}: {e}", exc_info=True)
        return []


def main() -> int:
    """
    Run scrapers and export results.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("=" * 60)
    print("Job Scraping Agent")
    print("=" * 60)
    
    logger.info("Starting job scraping process")
    
    # Define scrapers
    scrapers = {
        'indeed': IndeedScraper,
        'linkedin': LinkedInScraper,
        'glassdoor': GlassdoorScraper
    }
    
    all_jobs: List[Dict[str, Any]] = []
    
    # Run each scraper
    for name, scraper_class in scrapers.items():
        jobs = run_scraper(name, scraper_class)
        all_jobs.extend(jobs)
    
    # Export results
    if all_jobs:
        print(f"\nTotal jobs found: {len(all_jobs)}")
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        
        # Export to both formats
        success_json = export_data(all_jobs, "all_jobs", "json")
        success_csv = export_data(all_jobs, "all_jobs", "csv")
        
        if success_json and success_csv:
            print("\nResults exported to data/output/")
            logger.info("Results exported successfully")
        else:
            print("\n⚠️ Warning: Some exports may have failed")
            logger.warning("Some exports failed")
    else:
        print("\nNo jobs found")
        logger.warning("No jobs were scraped")
    
    print("\nDone!")
    logger.info("Job scraping process completed")
    
    return 0 if all_jobs else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        logger.warning("Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
