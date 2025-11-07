"""
Application Submitter - Main orchestrator for automated application submission

This module coordinates the submission of job applications across different platforms.
"""

import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser
from automation.models import SubmissionResult, SubmissionStatus, SubmissionConfig, ApplicationData
from automation.handlers import (
    LinkedInHandler,
    IndeedHandler,
    GreenhouseHandler,
    GenericHandler
)
from core.logger import setup_logger

logger = setup_logger("application_submitter")


class ApplicationSubmitter:
    """
    Main orchestrator for automated job application submission.
    
    This class manages the submission process across multiple platforms by:
    1. Detecting the platform from the application URL
    2. Selecting the appropriate handler
    3. Executing the submission
    4. Verifying and logging the result
    
    Example:
        >>> submitter = ApplicationSubmitter(config)
        >>> result = await submitter.submit_application(
        ...     job=job_data,
        ...     resume=resume_doc,
        ...     cover_letter=cover_letter_doc,
        ...     user_profile=profile
        ... )
        >>> if result.success:
        ...     print(f"Applied successfully! Confirmation: {result.confirmation_number}")
    """
    
    def __init__(self, config: Optional[SubmissionConfig] = None):
        """
        Initialize the application submitter with platform handlers
        
        Args:
            config: Configuration for submission behavior
        """
        self.config = config or SubmissionConfig()
        self.handlers = {}
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        # Track submissions for rate limiting
        self.submission_history: List[float] = []
    
    def __enter__(self):
        """Context manager entry"""
        self._setup_browser()
        self._load_handlers()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self._cleanup()
    
    def _setup_browser(self):
        """Initialize Playwright browser"""
        try:
            logger.info("Setting up browser")
            self.playwright = sync_playwright().start()
            
            self.browser = self.playwright.chromium.launch(
                headless=self.config.headless,
                slow_mo=self.config.slow_mo
            )
            
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Apply stealth patches
            self.page = self.context.new_page()
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            logger.info("Browser setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up browser: {e}")
            raise
    
    def _load_handlers(self):
        """Load all available platform handlers"""
        try:
            logger.info("Loading platform handlers")
            
            # Create screenshot directory
            Path(self.config.screenshot_dir).mkdir(parents=True, exist_ok=True)
            
            # Initialize handlers with the page
            self.handlers = {
                'linkedin': LinkedInHandler(self.page, self.config.screenshot_dir),
                'indeed': IndeedHandler(self.page, self.config.screenshot_dir),
                'greenhouse': GreenhouseHandler(self.page, self.config.screenshot_dir),
                'generic': GenericHandler(self.page, self.config.screenshot_dir)
            }
            
            logger.info(f"Loaded {len(self.handlers)} platform handlers")
            
        except Exception as e:
            logger.error(f"Error loading handlers: {e}")
            raise
    
    def _cleanup(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Browser cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def detect_platform(self, application_url: str) -> str:
        """
        Detect the platform from the application URL
        
        Args:
            application_url: The URL of the job application
            
        Returns:
            Platform identifier (e.g., 'linkedin', 'indeed', 'greenhouse')
        """
        url_lower = application_url.lower()
        
        if 'linkedin.com' in url_lower:
            return 'linkedin'
        elif 'indeed.com' in url_lower:
            return 'indeed'
        elif 'greenhouse.io' in url_lower or 'boards.greenhouse.io' in url_lower:
            return 'greenhouse'
        elif 'lever.co' in url_lower:
            return 'lever'
        elif 'workday.com' in url_lower:
            return 'workday'
        else:
            return 'generic'
    
    async def submit_application(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit a job application
        
        Args:
            job: Job details including application_url
            resume: Path to resume file
            cover_letter: Optional path to cover letter file
            user_profile: User profile information
            
        Returns:
            SubmissionResult with submission details
        """
        job_id = job.get('id', 'unknown')
        application_url = job.get('application_url', '')
        
        logger.info(f"Starting application submission for job {job_id}")
        
        try:
            # Check rate limiting
            if not self._check_rate_limit():
                logger.warning("Rate limit exceeded, waiting...")
                time.sleep(self.config.delay_between_submissions)
            
            # Detect platform
            platform = self.detect_platform(application_url)
            logger.info(f"Detected platform: {platform}")
            
            # Get appropriate handler
            handler = self.handlers.get(platform)
            if not handler:
                # Use generic handler as fallback
                logger.warning(f"No specific handler for {platform}, using generic")
                handler = self.handlers['generic']
            
            # Validate files exist
            if resume and not Path(resume).exists():
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform=platform,
                    status=SubmissionStatus.FAILED,
                    error_message=f"Resume file not found: {resume}"
                )
            
            # Execute submission with retries
            result = None
            for attempt in range(self.config.max_retries):
                try:
                    logger.info(f"Submission attempt {attempt + 1}/{self.config.max_retries}")
                    result = await handler.submit(job, resume, cover_letter, user_profile)
                    
                    # If successful or CAPTCHA/manual intervention needed, don't retry
                    if result.success or result.status in [
                        SubmissionStatus.CAPTCHA_DETECTED,
                        SubmissionStatus.MANUAL_INTERVENTION_REQUIRED
                    ]:
                        break
                    
                    # Wait before retry
                    if attempt < self.config.max_retries - 1:
                        logger.info(f"Waiting {self.config.retry_delay}s before retry")
                        time.sleep(self.config.retry_delay)
                        
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == self.config.max_retries - 1:
                        raise
            
            # Track submission time for rate limiting
            self._record_submission()
            
            # Log result
            if result.success:
                logger.info(f"Application submitted successfully: {job_id}")
            else:
                logger.error(f"Application failed: {job_id} - {result.error_message}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error during submission: {e}", exc_info=True)
            return SubmissionResult(
                success=False,
                job_id=job_id,
                platform=platform if 'platform' in locals() else 'unknown',
                status=SubmissionStatus.FAILED,
                error_message=str(e)
            )
    
    def _check_rate_limit(self) -> bool:
        """
        Check if we're within rate limits
        
        Returns:
            True if within limits, False if rate limited
        """
        current_time = time.time()
        
        # Remove submissions older than 1 hour
        cutoff_time = current_time - 3600
        self.submission_history = [
            t for t in self.submission_history if t > cutoff_time
        ]
        
        # Check if we've exceeded the hourly limit
        # TODO: Add applications_per_hour to SubmissionConfig
        max_per_hour = 10  # Default rate limit
        
        if len(self.submission_history) >= max_per_hour:
            return False
        
        return True
    
    def _record_submission(self):
        """Record a submission for rate limiting"""
        self.submission_history.append(time.time())
    
    async def submit_batch(
        self,
        jobs: List[Dict[str, Any]],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> List[SubmissionResult]:
        """
        Submit multiple applications in batch
        
        Args:
            jobs: List of job dictionaries
            resume: Path to resume file
            cover_letter: Optional path to cover letter
            user_profile: User profile data
            
        Returns:
            List of SubmissionResult objects
        """
        results = []
        
        logger.info(f"Starting batch submission for {len(jobs)} jobs")
        
        for i, job in enumerate(jobs):
            logger.info(f"Processing job {i + 1}/{len(jobs)}")
            
            result = await self.submit_application(
                job, resume, cover_letter, user_profile
            )
            results.append(result)
            
            # Delay between submissions
            if i < len(jobs) - 1:
                logger.info(f"Waiting {self.config.delay_between_submissions}s before next submission")
                time.sleep(self.config.delay_between_submissions)
        
        # Summary
        success_count = sum(1 for r in results if r.success)
        logger.info(f"Batch complete: {success_count}/{len(jobs)} successful")
        
        return results
