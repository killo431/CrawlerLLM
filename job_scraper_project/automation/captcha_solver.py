"""
CAPTCHA detection and handling module.

Provides enhanced CAPTCHA detection and optional solving capabilities.
"""
import time
from typing import Optional, Dict, Any
from playwright.sync_api import Page
from core.logger import setup_logger

logger = setup_logger("captcha_solver")


class CaptchaSolver:
    """
    Enhanced CAPTCHA detection and solving.
    
    Provides multiple strategies for handling CAPTCHAs:
    1. Detection of various CAPTCHA types
    2. Manual intervention with user notifications
    3. Audio CAPTCHA fallback (for accessibility)
    4. Retry mechanisms
    """
    
    # Known CAPTCHA providers and their selectors
    CAPTCHA_SELECTORS = {
        'recaptcha': [
            'iframe[src*="recaptcha"]',
            '.g-recaptcha',
            '#recaptcha',
            '[data-sitekey]'
        ],
        'hcaptcha': [
            'iframe[src*="hcaptcha"]',
            '.h-captcha',
            '#hcaptcha'
        ],
        'cloudflare': [
            '#challenge-form',
            '.cf-turnstile',
            'iframe[src*="challenges.cloudflare.com"]'
        ],
        'generic': [
            '#captcha',
            '.captcha',
            '[data-captcha]',
            'img[alt*="captcha" i]'
        ]
    }
    
    def __init__(self, page: Page, wait_time: int = 300):
        """
        Initialize the CAPTCHA solver.
        
        Args:
            page: Playwright page object
            wait_time: Maximum time to wait for manual CAPTCHA solving (seconds)
        """
        self.page = page
        self.wait_time = wait_time
    
    def detect_captcha(self) -> Optional[Dict[str, Any]]:
        """
        Detect if a CAPTCHA is present on the page.
        
        Returns:
            Dictionary with CAPTCHA info if detected, None otherwise
            Format: {'type': str, 'selector': str, 'visible': bool}
        """
        try:
            for captcha_type, selectors in self.CAPTCHA_SELECTORS.items():
                for selector in selectors:
                    element = self.page.query_selector(selector)
                    if element:
                        is_visible = element.is_visible()
                        logger.info(f"CAPTCHA detected: {captcha_type} (visible: {is_visible})")
                        return {
                            'type': captcha_type,
                            'selector': selector,
                            'visible': is_visible
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting CAPTCHA: {e}")
            return None
    
    def wait_for_manual_solve(self, notification_callback=None) -> bool:
        """
        Wait for user to manually solve CAPTCHA.
        
        Args:
            notification_callback: Optional callback to notify user
            
        Returns:
            True if CAPTCHA was solved, False if timeout
        """
        try:
            logger.warning(f"CAPTCHA detected - waiting up to {self.wait_time}s for manual solving")
            
            if notification_callback:
                notification_callback("CAPTCHA detected - please solve manually")
            
            start_time = time.time()
            check_interval = 5  # Check every 5 seconds
            
            while time.time() - start_time < self.wait_time:
                # Check if CAPTCHA is still present
                captcha_info = self.detect_captcha()
                
                if not captcha_info or not captcha_info['visible']:
                    logger.info("CAPTCHA appears to be solved")
                    time.sleep(2)  # Wait a bit for page to settle
                    return True
                
                time.sleep(check_interval)
            
            logger.error(f"CAPTCHA solving timeout after {self.wait_time}s")
            return False
            
        except Exception as e:
            logger.error(f"Error waiting for CAPTCHA solve: {e}")
            return False
    
    def try_audio_captcha(self) -> bool:
        """
        Attempt to switch to audio CAPTCHA (accessibility feature).
        
        Some CAPTCHAs provide audio alternatives that may be easier to handle.
        
        Returns:
            True if switched successfully, False otherwise
        """
        try:
            # Try to find audio button for reCAPTCHA
            audio_buttons = [
                'button[aria-label*="audio" i]',
                '#recaptcha-audio-button',
                '.recaptcha-audio-button'
            ]
            
            for selector in audio_buttons:
                button = self.page.query_selector(selector)
                if button and button.is_visible():
                    logger.info("Found audio CAPTCHA button, clicking...")
                    button.click()
                    time.sleep(2)
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error trying audio CAPTCHA: {e}")
            return False
    
    def check_captcha_bypass_strategies(self) -> bool:
        """
        Try various strategies to bypass or avoid CAPTCHA.
        
        Returns:
            True if bypass successful, False otherwise
        """
        try:
            # Strategy 1: Check if we can proceed without solving
            # Some pages show CAPTCHA but don't block progression
            next_buttons = ['button:has-text("Next")', 'button:has-text("Continue")']
            for selector in next_buttons:
                button = self.page.query_selector(selector)
                if button and button.is_visible() and not button.is_disabled():
                    logger.info("Found enabled next button despite CAPTCHA, trying to proceed")
                    return True
            
            # Strategy 2: Wait for CAPTCHA to auto-resolve
            # Some CAPTCHAs have automatic verification
            logger.info("Waiting briefly for automatic CAPTCHA resolution...")
            time.sleep(5)
            
            captcha_info = self.detect_captcha()
            if not captcha_info or not captcha_info['visible']:
                logger.info("CAPTCHA resolved automatically")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking bypass strategies: {e}")
            return False
    
    def handle_captcha(
        self,
        auto_solve: bool = False,
        notification_callback=None
    ) -> bool:
        """
        Main CAPTCHA handling method.
        
        Args:
            auto_solve: Whether to attempt automatic solving (not recommended)
            notification_callback: Callback to notify user
            
        Returns:
            True if CAPTCHA handled successfully, False otherwise
        """
        try:
            captcha_info = self.detect_captcha()
            
            if not captcha_info:
                return True  # No CAPTCHA detected
            
            logger.warning(f"CAPTCHA detected: {captcha_info['type']}")
            
            # Try bypass strategies first
            if self.check_captcha_bypass_strategies():
                return True
            
            # Try audio CAPTCHA if available
            if captcha_info['type'] == 'recaptcha':
                if self.try_audio_captcha():
                    logger.info("Switched to audio CAPTCHA")
                    # Could implement audio transcription here
            
            # Fall back to manual solving
            return self.wait_for_manual_solve(notification_callback)
            
        except Exception as e:
            logger.error(f"Error handling CAPTCHA: {e}")
            return False
    
    def get_captcha_info_for_user(self) -> Optional[str]:
        """
        Get user-friendly CAPTCHA information.
        
        Returns:
            String with instructions for user, or None
        """
        captcha_info = self.detect_captcha()
        
        if not captcha_info:
            return None
        
        captcha_type = captcha_info['type']
        
        messages = {
            'recaptcha': "Google reCAPTCHA detected. Please solve the CAPTCHA in the browser window.",
            'hcaptcha': "hCaptcha detected. Please solve the CAPTCHA in the browser window.",
            'cloudflare': "Cloudflare challenge detected. Please complete the security check.",
            'generic': "CAPTCHA detected. Please solve it manually in the browser window."
        }
        
        return messages.get(captcha_type, messages['generic'])
