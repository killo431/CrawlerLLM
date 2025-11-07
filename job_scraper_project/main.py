"""Main entry point for running scrapers via command line."""
import sys
import logging
import argparse
import asyncio
import csv
from pathlib import Path
from typing import List, Dict, Any
from adapters.indeed import IndeedScraper
from adapters.linkedin import LinkedInScraper
from adapters.glassdoor import GlassdoorScraper
from core.export_manager import export_data
from core.logger import setup_logger
from automation.application_submitter import ApplicationSubmitter
from automation.models import SubmissionConfig, ApplicationData

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


async def submit_application(args) -> int:
    """
    Submit a single job application.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code
    """
    print("=" * 60)
    print("Application Submission")
    print("=" * 60)
    
    logger.info("Starting application submission")
    
    try:
        # Create job dictionary
        job = {
            'id': args.job_id or 'cli_job',
            'application_url': args.job_url
        }
        
        # Create user profile
        user_profile = {
            'first_name': args.first_name,
            'last_name': args.last_name,
            'email': args.email,
            'phone': args.phone,
            'linkedin_url': getattr(args, 'linkedin_url', None),
            'github_url': getattr(args, 'github_url', None),
        }
        
        # Create config
        config = SubmissionConfig(
            headless=args.headless,
            screenshot_on_error=True,
            screenshot_on_success=True
        )
        
        # Submit application
        with ApplicationSubmitter(config) as submitter:
            result = await submitter.submit_application(
                job=job,
                resume=args.resume,
                cover_letter=args.cover_letter,
                user_profile=user_profile
            )
        
        # Display result
        if result.success:
            print(f"\n✅ Application submitted successfully!")
            print(f"   Job ID: {result.job_id}")
            print(f"   Platform: {result.platform}")
            if result.confirmation_number:
                print(f"   Confirmation: {result.confirmation_number}")
            if result.screenshot_path:
                print(f"   Screenshot: {result.screenshot_path}")
            logger.info("Application submitted successfully")
            return 0
        else:
            print(f"\n❌ Application failed")
            print(f"   Job ID: {result.job_id}")
            print(f"   Platform: {result.platform}")
            print(f"   Error: {result.error_message}")
            if result.screenshot_path:
                print(f"   Screenshot: {result.screenshot_path}")
            logger.error(f"Application failed: {result.error_message}")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Application submission error: {e}", exc_info=True)
        return 1


async def submit_batch(args) -> int:
    """
    Submit multiple applications from a CSV file.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code
    """
    print("=" * 60)
    print("Batch Application Submission")
    print("=" * 60)
    
    logger.info("Starting batch submission")
    
    try:
        # Load jobs from CSV
        jobs = []
        with open(args.jobs_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append({
                    'id': row.get('id', ''),
                    'application_url': row.get('url', row.get('application_url', ''))
                })
        
        print(f"\nLoaded {len(jobs)} jobs from {args.jobs_file}")
        
        # Create user profile
        user_profile = {
            'first_name': args.first_name,
            'last_name': args.last_name,
            'email': args.email,
            'phone': args.phone,
            'linkedin_url': getattr(args, 'linkedin_url', None),
            'github_url': getattr(args, 'github_url', None),
        }
        
        # Create config
        config = SubmissionConfig(
            headless=args.headless,
            screenshot_on_error=True,
            screenshot_on_success=True
        )
        
        # Submit applications
        with ApplicationSubmitter(config) as submitter:
            results = await submitter.submit_batch(
                jobs=jobs,
                resume=args.resume,
                cover_letter=args.cover_letter,
                user_profile=user_profile
            )
        
        # Display summary
        success_count = sum(1 for r in results if r.success)
        print(f"\n{'='*60}")
        print(f"Batch Complete: {success_count}/{len(jobs)} successful")
        print(f"{'='*60}")
        
        # Display details
        for result in results:
            status = "✅" if result.success else "❌"
            print(f"{status} {result.job_id} - {result.platform}")
        
        logger.info(f"Batch complete: {success_count}/{len(jobs)} successful")
        
        return 0 if success_count > 0 else 1
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Batch submission error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description='Job Scraping and Application Submission Tool'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Command to run')
        
        # Scrape command (default)
        scrape_parser = subparsers.add_parser('scrape', help='Scrape job listings')
        
        # Submit command
        submit_parser = subparsers.add_parser('submit', help='Submit a job application')
        submit_parser.add_argument('--job-url', required=True, help='URL of the job application')
        submit_parser.add_argument('--job-id', help='Job ID (optional)')
        submit_parser.add_argument('--resume', required=True, help='Path to resume file')
        submit_parser.add_argument('--cover-letter', help='Path to cover letter file')
        submit_parser.add_argument('--first-name', required=True, help='First name')
        submit_parser.add_argument('--last-name', required=True, help='Last name')
        submit_parser.add_argument('--email', required=True, help='Email address')
        submit_parser.add_argument('--phone', required=True, help='Phone number')
        submit_parser.add_argument('--linkedin-url', help='LinkedIn profile URL')
        submit_parser.add_argument('--github-url', help='GitHub profile URL')
        submit_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
        
        # Submit batch command
        batch_parser = subparsers.add_parser('submit-batch', help='Submit multiple applications')
        batch_parser.add_argument('--jobs-file', required=True, help='CSV file with job URLs')
        batch_parser.add_argument('--resume', required=True, help='Path to resume file')
        batch_parser.add_argument('--cover-letter', help='Path to cover letter file')
        batch_parser.add_argument('--first-name', required=True, help='First name')
        batch_parser.add_argument('--last-name', required=True, help='Last name')
        batch_parser.add_argument('--email', required=True, help='Email address')
        batch_parser.add_argument('--phone', required=True, help='Phone number')
        batch_parser.add_argument('--linkedin-url', help='LinkedIn profile URL')
        batch_parser.add_argument('--github-url', help='GitHub profile URL')
        batch_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
        
        args = parser.parse_args()
        
        # Execute command
        if args.command == 'submit':
            sys.exit(asyncio.run(submit_application(args)))
        elif args.command == 'submit-batch':
            sys.exit(asyncio.run(submit_batch(args)))
        else:
            # Default: run scrapers
            sys.exit(main())
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        logger.warning("Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
