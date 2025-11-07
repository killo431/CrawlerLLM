"""
Base Handler - Abstract base class for all platform handlers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseHandler(ABC):
    """
    Abstract base class for platform-specific application handlers.
    
    Each platform handler must implement the submit method to handle
    the specific application flow for that platform.
    """
    
    def __init__(self, browser_manager=None):
        """
        Initialize the handler
        
        Args:
            browser_manager: Browser automation manager (e.g., Playwright)
        """
        self.browser = browser_manager
    
    @abstractmethod
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> Any:
        """
        Submit an application for the given job
        
        Args:
            job: Job details including application URL
            resume: Path to resume file
            cover_letter: Optional path to cover letter
            user_profile: User profile data
            
        Returns:
            ApplicationResult object with submission details
        """
        pass
    
    @abstractmethod
    async def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """
        Fill out the application form
        
        Args:
            form_data: Dictionary mapping form fields to values
            
        Returns:
            True if form filled successfully, False otherwise
        """
        pass
    
    @abstractmethod
    async def upload_documents(self, resume: str, cover_letter: Optional[str]) -> bool:
        """
        Upload resume and cover letter
        
        Args:
            resume: Path to resume file
            cover_letter: Optional path to cover letter
            
        Returns:
            True if uploaded successfully, False otherwise
        """
        pass
    
    @abstractmethod
    async def verify_submission(self) -> bool:
        """
        Verify that the application was submitted successfully
        
        Returns:
            True if submission confirmed, False otherwise
        """
        pass
