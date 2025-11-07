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
from automation.rate_limiter import AdaptiveRateLimiter
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
        
        # Use adaptive rate limiter
        self.rate_limiter = AdaptiveRateLimiter(
            default_rate=10,
            min_delay=self.config.delay_between_submissions,
            max_delay=300
        )
    
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
        from urllib.parse import urlparse
        
        try:
            parsed = urlparse(application_url)
            hostname = parsed.hostname
            
            if not hostname:
                return 'generic'
            
            hostname_lower = hostname.lower()
            
            # Check for exact domain matches or subdomain matches
            if hostname_lower == 'linkedin.com' or hostname_lower.endswith('.linkedin.com'):
                return 'linkedin'
            elif hostname_lower == 'indeed.com' or hostname_lower.endswith('.indeed.com'):
                return 'indeed'
            elif hostname_lower == 'greenhouse.io' or hostname_lower.endswith('.greenhouse.io'):
                return 'greenhouse'
            elif hostname_lower == 'lever.co' or hostname_lower.endswith('.lever.co'):
                return 'lever'
            elif hostname_lower == 'workday.com' or hostname_lower.endswith('.workday.com'):
                return 'workday'
            else:
                return 'generic'
        except Exception as e:
            logger.warning(f"Error parsing URL {application_url}: {e}")
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
            # Detect platform
            platform = self.detect_platform(application_url)
            logger.info(f"Detected platform: {platform}")
            
            # Check rate limiting for this platform
            if not self.rate_limiter.check_rate_limit(platform):
                stats = self.rate_limiter.get_platform_stats(platform)
                logger.warning(f"Rate limit exceeded for {platform}: {stats}")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform=platform,
                    status=SubmissionStatus.RATE_LIMITED,
                    error_message=self.rate_limiter.suggest_optimal_timing(platform)
                )
            
            # Wait if needed based on adaptive rate limiting
            self.rate_limiter.wait_if_needed(platform)
            
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
            
            # Record submission for rate limiting
            error_type = None
            if not result.success:
                if result.status == SubmissionStatus.RATE_LIMITED:
                    error_type = 'rate_limited'
                elif result.status == SubmissionStatus.CAPTCHA_DETECTED:
                    error_type = 'captcha'
            
            self.rate_limiter.record_submission(platform, result.success, error_type)
            
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
    
    def get_rate_limiter_stats(self) -> Dict[str, Dict]:
        """
        Get rate limiter statistics for all platforms.
        
        Returns:
            Dictionary mapping platform to stats
        """
        return self.rate_limiter.get_all_stats()
    
    def reset_rate_limiter(self, platform: Optional[str] = None):
        """
        Reset rate limiter for a specific platform or all platforms.
        
        Args:
            platform: Platform to reset, or None to reset all
        """
        if platform:
            self.rate_limiter.reset_platform(platform)
        else:
            # Reset all platforms
            for plat in self.rate_limiter.platform_history.keys():
                self.rate_limiter.reset_platform(plat)
    
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
