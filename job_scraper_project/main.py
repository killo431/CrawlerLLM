"""Main entry point for running scrapers via command line."""
import sys
from adapters.indeed import IndeedScraper
from adapters.linkedin import LinkedInScraper
from adapters.glassdoor import GlassdoorScraper
from core.export_manager import export_data

def main():
    """Run scrapers and export results."""
    print("=" * 60)
    print("Job Scraping Agent")
    print("=" * 60)
    
    scrapers = {
        'indeed': IndeedScraper(),
        'linkedin': LinkedInScraper(),
        'glassdoor': GlassdoorScraper()
    }
    
    all_jobs = []
    
    for name, scraper in scrapers.items():
        print(f"\nScraping {name.capitalize()}...")
        try:
            jobs = scraper.run()
            all_jobs.extend(jobs)
            print(f"✅ Found {len(jobs)} jobs")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    if all_jobs:
        print(f"\nTotal jobs found: {len(all_jobs)}")
        export_data(all_jobs, "all_jobs", "json")
        export_data(all_jobs, "all_jobs", "csv")
        print("\nResults exported to data/output/")
    else:
        print("\nNo jobs found")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
