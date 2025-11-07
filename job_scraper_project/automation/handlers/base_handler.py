"""
Base Handler - Abstract base class for all platform handlers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from automation.models import SubmissionResult, SubmissionStatus, ApplicationData
from automation.form_mapper import FormMapper
from automation.document_uploader import DocumentUploader
from automation.navigation import FormNavigator
from core.logger import setup_logger

logger = setup_logger("base_handler")


class BaseHandler(ABC):
    """
    Abstract base class for platform-specific application handlers.
    
    Each platform handler must implement the submit method to handle
    the specific application flow for that platform.
    
    Provides common utilities for:
    - Form field detection and filling
    - Document uploads
    - Screenshot capture
    - Multi-step navigation
    """
    
    def __init__(self, page: Page, screenshot_dir: str = "data/screenshots"):
        """
        Initialize the handler
        
        Args:
            page: Playwright page object
            screenshot_dir: Directory to save screenshots
        """
        self.page = page
        self.screenshot_dir = screenshot_dir
        
        # Initialize helper modules
        self.form_mapper = FormMapper(page)
        self.document_uploader = DocumentUploader(page)
        self.navigator = FormNavigator(page)
        
        # Ensure screenshot directory exists
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit an application for the given job
        
        Args:
            job: Job details including application URL
            resume: Path to resume file
            cover_letter: Optional path to cover letter
            user_profile: User profile data
            
        Returns:
            SubmissionResult object with submission details
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
    
    def capture_screenshot(self, job_id: str, step: str = "final") -> Optional[str]:
        """
        Capture a screenshot of the current page.
        
        Args:
            job_id: Unique identifier for the job
            step: Description of the current step
            
        Returns:
            Path to saved screenshot or None
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{job_id}_{step}_{timestamp}.png"
            filepath = Path(self.screenshot_dir) / filename
            
            self.page.screenshot(path=str(filepath), full_page=True)
            logger.info(f"Screenshot saved: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None
    
    def detect_captcha(self) -> bool:
        """
        Detect if a CAPTCHA is present on the page.
        
        Returns:
            True if CAPTCHA detected
        """
        try:
            # Common CAPTCHA selectors
            captcha_selectors = [
                'iframe[src*="recaptcha"]',
                'iframe[src*="hcaptcha"]',
                '.g-recaptcha',
                '.h-captcha',
                '#captcha',
                '[data-captcha]'
            ]
            
            for selector in captcha_selectors:
                if self.page.query_selector(selector):
                    logger.warning(f"CAPTCHA detected: {selector}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting CAPTCHA: {e}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30):
        """
        Wait for page to fully load.
        
        Args:
            timeout: Timeout in seconds
        """
        try:
            self.page.wait_for_load_state('networkidle', timeout=timeout * 1000)
        except Exception as e:
            logger.warning(f"Page load timeout: {e}")
    
    def fill_text_field(self, selector: str, value: str, delay: int = 100) -> bool:
        """
        Fill a text field with the given value.
        
        Args:
            selector: CSS selector for the field
            value: Value to fill
            delay: Delay between keystrokes in milliseconds
            
        Returns:
            True if successful
        """
        try:
            element = self.page.wait_for_selector(selector, timeout=5000)
            if element:
                element.fill(value, timeout=5000)
                logger.debug(f"Filled field {selector} with value")
                return True
            return False
        except Exception as e:
            logger.error(f"Error filling field {selector}: {e}")
            return False
    
    def click_element(self, selector: str, timeout: int = 5000) -> bool:
        """
        Click an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Timeout in milliseconds
            
        Returns:
            True if successful
        """
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)
            if element and element.is_visible():
                element.click()
                logger.debug(f"Clicked element: {selector}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clicking element {selector}: {e}")
            return False
    
    def select_option(self, selector: str, value: str) -> bool:
        """
        Select an option from a dropdown.
        
        Args:
            selector: CSS selector for the select element
            value: Value or label to select
            
        Returns:
            True if successful
        """
        try:
            element = self.page.wait_for_selector(selector, timeout=5000)
            if element:
                element.select_option(value)
                logger.debug(f"Selected option {value} in {selector}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error selecting option in {selector}: {e}")
            return False
