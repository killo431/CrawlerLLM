"""
Multi-step form navigation module.

Handles navigation through multi-step application forms.
"""
import time
from typing import Optional, List, Tuple
from playwright.sync_api import Page
from automation.models import NavigationState
from core.logger import setup_logger

logger = setup_logger("navigation")


class FormNavigator:
    """
    Handles navigation through multi-step application forms.
    
    Detects progress indicators, next/back buttons, and manages state transitions.
    """
    
    # Common button text patterns
    NEXT_BUTTON_PATTERNS = [
        'next',
        'continue',
        'proceed',
        'forward',
        'submit',
        'save and continue'
    ]
    
    BACK_BUTTON_PATTERNS = [
        'back',
        'previous',
        'prev',
        'return'
    ]
    
    SUBMIT_BUTTON_PATTERNS = [
        'submit',
        'apply',
        'send application',
        'complete application',
        'finish',
        'done'
    ]
    
    def __init__(self, page: Page):
        """
        Initialize the form navigator.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.state = NavigationState()
    
    def detect_multi_step_form(self) -> bool:
        """
        Detect if the current form is multi-step.
        
        Returns:
            True if multi-step form detected
        """
        try:
            # Look for progress indicators
            progress_indicators = [
                '.progress-bar',
                '.stepper',
                '.wizard',
                '[role="progressbar"]',
                '.steps',
                '.step-indicator'
            ]
            
            for selector in progress_indicators:
                if self.page.query_selector(selector):
                    logger.info(f"Multi-step form detected: {selector}")
                    return True
            
            # Look for "next" button (indicator of multi-step)
            if self._find_next_button():
                logger.info("Multi-step form detected: next button found")
                return True
            
            # Look for step numbers in text
            if self.page.locator('text=/step [0-9]/i').count() > 0:
                logger.info("Multi-step form detected: step text found")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error detecting multi-step form: {e}")
            return False
    
    def detect_steps(self) -> NavigationState:
        """
        Detect the number of steps and current position.
        
        Returns:
            NavigationState with step information
        """
        try:
            # Try to find step indicators
            step_elements = self.page.query_selector_all(
                '.step, .wizard-step, [data-step], .stepper-item'
            )
            
            if step_elements:
                total_steps = len(step_elements)
                
                # Try to determine current step
                current_step = 0
                for i, elem in enumerate(step_elements):
                    classes = elem.get_attribute('class') or ''
                    if 'active' in classes or 'current' in classes:
                        current_step = i
                        break
                
                self.state.total_steps = total_steps
                self.state.current_step = current_step
                
                # Extract step titles if available
                for elem in step_elements:
                    title = elem.text_content()
                    if title:
                        self.state.step_titles.append(title.strip())
                
                logger.info(f"Detected {total_steps} steps, currently on step {current_step + 1}")
            
            # Update navigation capabilities
            self.state.can_go_next = self._find_next_button() is not None
            self.state.can_go_back = self._find_back_button() is not None
            self.state.is_final_step = self._is_final_step()
            
            return self.state
            
        except Exception as e:
            logger.error(f"Error detecting steps: {e}")
            return self.state
    
    def go_next(self, wait_time: float = 2.0) -> bool:
        """
        Navigate to the next step.
        
        Args:
            wait_time: Time to wait after clicking (seconds)
            
        Returns:
            True if navigation successful
        """
        try:
            next_button = self._find_next_button()
            
            if not next_button:
                logger.warning("No next button found")
                return False
            
            # Click the button
            logger.info("Clicking next button")
            next_button.click()
            
            # Wait for navigation
            time.sleep(wait_time)
            
            # Update state
            self.state.advance_step()
            
            # Re-detect capabilities
            self.state.can_go_next = self._find_next_button() is not None
            self.state.can_go_back = self._find_back_button() is not None
            self.state.is_final_step = self._is_final_step()
            
            logger.info(f"Navigated to step {self.state.current_step + 1}")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to next step: {e}")
            return False
    
    def go_back(self, wait_time: float = 2.0) -> bool:
        """
        Navigate to the previous step.
        
        Args:
            wait_time: Time to wait after clicking (seconds)
            
        Returns:
            True if navigation successful
        """
        try:
            back_button = self._find_back_button()
            
            if not back_button:
                logger.warning("No back button found")
                return False
            
            # Click the button
            logger.info("Clicking back button")
            back_button.click()
            
            # Wait for navigation
            time.sleep(wait_time)
            
            # Update state
            self.state.go_back()
            
            # Re-detect capabilities
            self.state.can_go_next = self._find_next_button() is not None
            self.state.can_go_back = self._find_back_button() is not None
            self.state.is_final_step = self._is_final_step()
            
            logger.info(f"Navigated back to step {self.state.current_step + 1}")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to previous step: {e}")
            return False
    
    def submit_form(self, wait_time: float = 3.0) -> bool:
        """
        Submit the final form.
        
        Args:
            wait_time: Time to wait after submission (seconds)
            
        Returns:
            True if submission successful
        """
        try:
            submit_button = self._find_submit_button()
            
            if not submit_button:
                logger.warning("No submit button found")
                return False
            
            # Click submit
            logger.info("Clicking submit button")
            submit_button.click()
            
            # Wait for submission to process
            time.sleep(wait_time)
            
            logger.info("Form submitted")
            return True
            
        except Exception as e:
            logger.error(f"Error submitting form: {e}")
            return False
    
    def _find_next_button(self):
        """Find the next/continue button."""
        return self._find_button_by_patterns(self.NEXT_BUTTON_PATTERNS)
    
    def _find_back_button(self):
        """Find the back/previous button."""
        return self._find_button_by_patterns(self.BACK_BUTTON_PATTERNS)
    
    def _find_submit_button(self):
        """Find the submit/apply button."""
        return self._find_button_by_patterns(self.SUBMIT_BUTTON_PATTERNS)
    
    def _find_button_by_patterns(self, patterns: List[str]):
        """
        Find a button matching any of the given text patterns.
        
        Args:
            patterns: List of text patterns to match
            
        Returns:
            ElementHandle for button or None
        """
        try:
            # Try to find button or input[type=submit] with matching text
            for pattern in patterns:
                # Case-insensitive search
                button = self.page.query_selector(
                    f'button:has-text("{pattern}"), '
                    f'input[type="submit"][value*="{pattern}" i], '
                    f'a:has-text("{pattern}")'
                )
                
                if button and button.is_visible():
                    return button
            
            # Try aria-label
            for pattern in patterns:
                button = self.page.query_selector(f'button[aria-label*="{pattern}" i]')
                if button and button.is_visible():
                    return button
            
            return None
            
        except Exception as e:
            logger.debug(f"Error finding button: {e}")
            return None
    
    def _is_final_step(self) -> bool:
        """
        Check if we're on the final step.
        
        Returns:
            True if on final step
        """
        try:
            # Check if submit button is visible
            if self._find_submit_button():
                return True
            
            # Check if "next" button says something like "submit" or "finish"
            next_button = self._find_next_button()
            if next_button:
                button_text = next_button.text_content().lower()
                if any(pattern in button_text for pattern in self.SUBMIT_BUTTON_PATTERNS):
                    return True
            
            # Check step indicators
            if self.state.total_steps > 1:
                return self.state.current_step >= self.state.total_steps - 1
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking if final step: {e}")
            return False
    
    def wait_for_navigation(self, timeout: float = 10.0) -> bool:
        """
        Wait for page navigation to complete.
        
        Args:
            timeout: Maximum time to wait (seconds)
            
        Returns:
            True if navigation completed
        """
        try:
            self.page.wait_for_load_state('networkidle', timeout=timeout * 1000)
            return True
        except Exception as e:
            logger.warning(f"Navigation wait timed out: {e}")
            return False
    
    def validate_step(self) -> Tuple[bool, List[str]]:
        """
        Validate current step for errors.
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        try:
            errors = []
            
            # Look for error messages
            error_selectors = [
                '.error',
                '.error-message',
                '[role="alert"]',
                '.alert-danger',
                '.validation-error',
                '.field-error'
            ]
            
            for selector in error_selectors:
                error_elements = self.page.query_selector_all(selector)
                for elem in error_elements:
                    if elem.is_visible():
                        error_text = elem.text_content().strip()
                        if error_text:
                            errors.append(error_text)
            
            is_valid = len(errors) == 0
            
            if not is_valid:
                logger.warning(f"Validation errors found: {errors}")
            else:
                logger.info("Step validation passed")
            
            return is_valid, errors
            
        except Exception as e:
            logger.error(f"Error validating step: {e}")
            return False, [str(e)]
    
    def get_current_step_title(self) -> Optional[str]:
        """
        Get the title of the current step.
        
        Returns:
            Step title or None
        """
        if self.state.step_titles and self.state.current_step < len(self.state.step_titles):
            return self.state.step_titles[self.state.current_step]
        return None
    
    def reset_state(self):
        """Reset navigation state."""
        self.state = NavigationState()
        logger.info("Navigation state reset")
