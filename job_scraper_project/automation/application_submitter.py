"""
Application Submitter - Main orchestrator for automated application submission

This module coordinates the submission of job applications across different platforms.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplicationResult:
    """Result of an application submission attempt"""
    success: bool
    job_id: str
    platform: str
    submitted_at: Optional[datetime] = None
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    confirmation_number: Optional[str] = None


class ApplicationSubmitter:
    """
    Main orchestrator for automated job application submission.
    
    This class manages the submission process across multiple platforms by:
    1. Detecting the platform from the application URL
    2. Selecting the appropriate handler
    3. Executing the submission
    4. Verifying and logging the result
    
    Example:
        >>> submitter = ApplicationSubmitter()
        >>> result = await submitter.submit_application(
        ...     job=job_data,
        ...     resume=resume_doc,
        ...     cover_letter=cover_letter_doc,
        ...     user_profile=profile
        ... )
        >>> if result.success:
        ...     print(f"Applied successfully! Confirmation: {result.confirmation_number}")
    """
    
    def __init__(self):
        """Initialize the application submitter with platform handlers"""
        self.handlers = {}
        self._load_handlers()
    
    def _load_handlers(self):
        """Load all available platform handlers"""
        # Handlers will be imported and registered here
        # from automation.handlers import LinkedInHandler, IndeedHandler, etc.
        pass
    
    def detect_platform(self, application_url: str) -> str:
        """
        Detect the platform from the application URL
        
        Args:
            application_url: The URL of the job application
            
        Returns:
            Platform identifier (e.g., 'linkedin', 'indeed', 'greenhouse')
        """
        if 'linkedin.com' in application_url:
            return 'linkedin'
        elif 'indeed.com' in application_url:
            return 'indeed'
        elif 'greenhouse.io' in application_url or 'boards.greenhouse.io' in application_url:
            return 'greenhouse'
        elif 'lever.co' in application_url:
            return 'lever'
        else:
            return 'generic'
    
    async def submit_application(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> ApplicationResult:
        """
        Submit a job application
        
        Args:
            job: Job details including application_url
            resume: Path to resume file
            cover_letter: Optional path to cover letter file
            user_profile: User profile information
            
        Returns:
            ApplicationResult with submission details
        """
        try:
            # Detect platform
            platform = self.detect_platform(job.get('application_url', ''))
            
            # Get appropriate handler
            handler = self.handlers.get(platform)
            if not handler:
                return ApplicationResult(
                    success=False,
                    job_id=job.get('id', 'unknown'),
                    platform=platform,
                    error_message=f"No handler available for platform: {platform}"
                )
            
            # Execute submission
            result = await handler.submit(job, resume, cover_letter, user_profile)
            
            return result
            
        except Exception as e:
            return ApplicationResult(
                success=False,
                job_id=job.get('id', 'unknown'),
                platform='unknown',
                error_message=str(e)
            )
