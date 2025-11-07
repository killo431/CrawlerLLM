"""
External redirect detection and handling module.

Handles cases where job applications redirect to external company sites.
"""
import time
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from playwright.sync_api import Page
from core.logger import setup_logger

logger = setup_logger("redirect_handler")


class RedirectHandler:
    """
    Handles external redirects during application submission.
    
    Many job boards redirect to company career sites. This handler:
    1. Detects redirects
    2. Identifies the target platform
    3. Attempts to continue with appropriate handler
    """
    
    def __init__(self, page: Page):
        """
        Initialize the redirect handler.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.redirect_history = []
    
    def detect_redirect(self, original_url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Detect if a redirect has occurred.
        
        Args:
            original_url: The original URL we navigated to
            timeout: Time to wait for redirect detection
            
        Returns:
            Dictionary with redirect info or None
        """
        try:
            start_time = time.time()
            original_domain = urlparse(original_url).netloc
            
            # Wait a bit for potential redirects
            time.sleep(2)
            
            while time.time() - start_time < timeout:
                current_url = self.page.url
                current_domain = urlparse(current_url).netloc
                
                if current_domain != original_domain:
                    redirect_info = {
                        'original_url': original_url,
                        'redirected_url': current_url,
                        'original_domain': original_domain,
                        'redirected_domain': current_domain,
                        'redirect_time': time.time() - start_time
                    }
                    
                    logger.info(f"Redirect detected: {original_domain} -> {current_domain}")
                    self.redirect_history.append(redirect_info)
                    
                    return redirect_info
                
                time.sleep(0.5)
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting redirect: {e}")
            return None
    
    def identify_redirected_platform(self, url: str) -> str:
        """
        Identify the platform after redirect.
        
        Args:
            url: The redirected URL
            
        Returns:
            Platform identifier
        """
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if not hostname:
                return 'unknown'
            
            hostname_lower = hostname.lower()
            
            # Check for known ATS platforms using exact domain matching
            if hostname_lower == 'greenhouse.io' or hostname_lower.endswith('.greenhouse.io'):
                return 'greenhouse'
            elif hostname_lower == 'lever.co' or hostname_lower.endswith('.lever.co'):
                return 'lever'
            elif hostname_lower == 'workday.com' or hostname_lower.endswith('.workday.com'):
                return 'workday'
            elif hostname_lower == 'taleo.net' or hostname_lower.endswith('.taleo.net'):
                return 'taleo'
            elif hostname_lower == 'brassring.com' or hostname_lower.endswith('.brassring.com'):
                return 'brassring'
            elif hostname_lower == 'myworkdayjobs.com' or hostname_lower.endswith('.myworkdayjobs.com'):
                return 'workday'
            elif hostname_lower == 'applytojob.com' or hostname_lower.endswith('.applytojob.com'):
                return 'applytojob'
            else:
                # Check for company career sites
                if any(word in hostname_lower for word in ['career', 'jobs', 'hiring', 'talent']):
                    return 'company_careers'
                return 'unknown'
            
        except Exception as e:
            logger.error(f"Error identifying platform: {e}")
            return 'unknown'
    
    def check_for_external_apply_button(self) -> Optional[str]:
        """
        Check if there's an external apply button/link.
        
        Returns:
            External URL if found, None otherwise
        """
        try:
            # Common patterns for external apply buttons
            selectors = [
                'a:has-text("Apply on company site")',
                'a:has-text("Apply on Company Website")',
                'a:has-text("Apply externally")',
                'a:has-text("Visit site to apply")',
                'button:has-text("Apply on company site")',
                '[data-testid*="external-apply"]',
                '.external-apply-button'
            ]
            
            for selector in selectors:
                element = self.page.query_selector(selector)
                if element:
                    href = element.get_attribute('href')
                    if href:
                        logger.info(f"Found external apply link: {href}")
                        return href
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking for external apply: {e}")
            return None
    
    def handle_external_redirect(
        self,
        original_platform: str,
        follow_redirect: bool = True
    ) -> Dict[str, Any]:
        """
        Handle an external redirect.
        
        Args:
            original_platform: The platform we started on
            follow_redirect: Whether to follow the redirect
            
        Returns:
            Dictionary with handling result
        """
        try:
            # Check for external apply button first
            external_url = self.check_for_external_apply_button()
            
            if external_url:
                logger.info(f"External application detected from {original_platform}")
                
                if follow_redirect:
                    logger.info("Following external redirect...")
                    self.page.goto(external_url)
                    time.sleep(2)
                    
                    # Identify new platform
                    new_platform = self.identify_redirected_platform(self.page.url)
                    
                    return {
                        'redirected': True,
                        'external_url': external_url,
                        'new_platform': new_platform,
                        'can_continue': new_platform != 'unknown',
                        'message': f"Redirected to {new_platform} platform"
                    }
                else:
                    return {
                        'redirected': True,
                        'external_url': external_url,
                        'can_continue': False,
                        'message': "External redirect detected but not followed"
                    }
            
            return {
                'redirected': False,
                'can_continue': True,
                'message': "No external redirect detected"
            }
            
        except Exception as e:
            logger.error(f"Error handling redirect: {e}")
            return {
                'redirected': False,
                'can_continue': False,
                'error': str(e)
            }
    
    def get_redirect_chain(self) -> list:
        """
        Get the full redirect chain.
        
        Returns:
            List of redirect info dictionaries
        """
        return self.redirect_history.copy()
    
    def detect_iframe_application(self) -> Optional[str]:
        """
        Detect if application is in an iframe.
        
        Some platforms embed external applications in iframes.
        
        Returns:
            iframe source URL if detected, None otherwise
        """
        try:
            iframes = self.page.query_selector_all('iframe')
            
            for iframe in iframes:
                src = iframe.get_attribute('src')
                if src and any(keyword in src.lower() for keyword in ['apply', 'job', 'application', 'career']):
                    logger.info(f"Detected application iframe: {src}")
                    return src
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting iframe: {e}")
            return None
    
    def should_follow_redirect(
        self,
        redirect_info: Dict[str, Any],
        allowed_domains: Optional[list] = None
    ) -> bool:
        """
        Determine if we should follow a redirect.
        
        Args:
            redirect_info: Information about the redirect
            allowed_domains: Optional list of allowed domains
            
        Returns:
            True if redirect should be followed
        """
        try:
            if not redirect_info:
                return True
            
            redirected_domain = redirect_info['redirected_domain']
            
            # If we have allowed domains, check against them
            if allowed_domains:
                for domain in allowed_domains:
                    if domain in redirected_domain:
                        return True
                return False
            
            # Check if it's a known ATS platform
            platform = self.identify_redirected_platform(redirect_info['redirected_url'])
            
            # Follow redirects to known platforms
            known_platforms = ['greenhouse', 'lever', 'workday', 'taleo']
            
            return platform in known_platforms
            
        except Exception as e:
            logger.error(f"Error checking if should follow redirect: {e}")
            return False
