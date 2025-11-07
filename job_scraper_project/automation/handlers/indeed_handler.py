"""
Indeed Application Handler

Handles automated application submission for Indeed job postings.
"""

import time
from typing import Dict, Any, Optional
from automation.handlers.base_handler import BaseHandler
from automation.models import SubmissionResult, SubmissionStatus
from core.logger import setup_logger

logger = setup_logger("indeed_handler")


class IndeedHandler(BaseHandler):
    """
    Handler for Indeed job applications.
    
    Indeed applications can be either Indeed-hosted or redirect to company sites.
    This handler detects and handles both scenarios.
    """
    
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit an Indeed application
        
        Process:
        1. Navigate to job page
        2. Click Apply button
        3. Detect if Indeed-hosted or external
        4. Fill application form
        5. Upload resume
        6. Submit
        """
        job_id = job.get('id', 'unknown')
        application_url = job.get('application_url', '')
        
        logger.info(f"Starting Indeed application for job {job_id}")
        
        try:
            # Navigate to job page
            self.page.goto(application_url)
            self.wait_for_page_load()
            
            # Capture initial screenshot
            screenshot_path = self.capture_screenshot(job_id, "start")
            
            # Check for CAPTCHA
            if self.detect_captcha():
                logger.warning("CAPTCHA detected")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.CAPTCHA_DETECTED,
                    screenshot_path=screenshot_path,
                    error_message="CAPTCHA detected - manual intervention required"
                )
            
            # Click Apply button
            if not self._click_apply_button():
                logger.error("Could not find Apply button")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "no_button"),
                    error_message="Apply button not found"
                )
            
            # Wait for form to load
            time.sleep(2)
            
            # Detect if Indeed-hosted or external redirect
            is_indeed_hosted = self._is_indeed_hosted_application()
            
            if not is_indeed_hosted:
                logger.warning("External application detected - may not be fully supported")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.MANUAL_INTERVENTION_REQUIRED,
                    screenshot_path=self.capture_screenshot(job_id, "external"),
                    error_message="External company application - manual application required"
                )
            
            # Upload resume first if available
            if resume:
                if not await self.upload_documents(resume, cover_letter):
                    logger.warning("Document upload failed")
            
            # Fill form fields
            if not await self.fill_form(user_profile):
                logger.error("Failed to fill form")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "fill_error"),
                    error_message="Failed to fill form fields"
                )
            
            # Handle multi-step if needed
            if self.navigator.detect_multi_step_form():
                logger.info("Multi-step form detected")
                while not self.navigator.state.is_final_step:
                    if not self.navigator.go_next():
                        break
                    await self.fill_form(user_profile)
                    time.sleep(1)
            
            # Submit application
            if not self._submit_application():
                logger.error("Could not submit application")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "submit_error"),
                    error_message="Could not submit application"
                )
            
            # Wait for confirmation
            time.sleep(3)
            
            # Verify submission
            if await self.verify_submission():
                logger.info("Application submitted successfully")
                return SubmissionResult(
                    success=True,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.SUCCESS,
                    screenshot_path=self.capture_screenshot(job_id, "success")
                )
            else:
                logger.warning("Could not verify submission")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='indeed',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "verify_error"),
                    error_message="Could not verify submission"
                )
            
        except Exception as e:
            logger.error(f"Error during Indeed submission: {e}", exc_info=True)
            return SubmissionResult(
                success=False,
                job_id=job_id,
                platform='indeed',
                status=SubmissionStatus.FAILED,
                screenshot_path=self.capture_screenshot(job_id, "error"),
                error_message=str(e)
            )
    
    async def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """Fill Indeed application form"""
        try:
            logger.info("Filling form fields")
            
            # Detect all fields
            fields = self.form_mapper.detect_all_fields()
            logger.info(f"Detected {len(fields)} fields")
            
            # Map fields to data
            field_mapping = self.form_mapper.map_fields_to_data(fields, form_data)
            
            # Fill each field
            for field, value in field_mapping.items():
                try:
                    if field.field_type.value in ['text', 'email', 'phone']:
                        self.fill_text_field(field.selector, str(value))
                    elif field.field_type.value == 'select':
                        self.select_option(field.selector, str(value))
                    elif field.field_type.value == 'checkbox':
                        if value:
                            self.click_element(field.selector)
                    
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Could not fill field {field.selector}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error filling form: {e}")
            return False
    
    async def upload_documents(self, resume: str, cover_letter: Optional[str]) -> bool:
        """Upload documents to Indeed"""
        try:
            logger.info("Uploading documents")
            
            if resume:
                success = self.document_uploader.upload_resume(resume)
                if not success:
                    logger.warning("Resume upload failed")
                    return False
            
            if cover_letter:
                self.document_uploader.upload_cover_letter(cover_letter)
            
            return True
            
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return False
    
    async def verify_submission(self) -> bool:
        """Verify Indeed application submission"""
        try:
            # Look for success indicators
            success_selectors = [
                'text=Application submitted',
                'text=Your application has been submitted',
                'text=Successfully applied',
                '.ia-BasePage-heading:has-text("Application submitted")',
                '[data-testid="application-confirmation"]'
            ]
            
            for selector in success_selectors:
                if self.page.locator(selector).count() > 0:
                    logger.info(f"Success indicator found: {selector}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verifying submission: {e}")
            return False
    
    def _click_apply_button(self) -> bool:
        """Click the Apply button"""
        try:
            selectors = [
                'button:has-text("Apply now")',
                'button:has-text("Apply")',
                '.ia-container .ia-IndeedApplyButton',
                '[data-testid="apply-button"]'
            ]
            
            for selector in selectors:
                if self.click_element(selector, timeout=3000):
                    logger.info("Apply button clicked")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error clicking Apply button: {e}")
            return False
    
    def _is_indeed_hosted_application(self) -> bool:
        """Check if application is Indeed-hosted"""
        try:
            from urllib.parse import urlparse
            
            # Check URL using proper domain parsing
            parsed = urlparse(self.page.url)
            hostname = parsed.hostname
            
            if hostname and (hostname == 'indeed.com' or hostname.endswith('.indeed.com')):
                if 'apply' in self.page.url.lower():
                    return True
            
            # Check for Indeed application elements
            indeed_indicators = [
                '.ia-container',
                '[data-testid="indeed-apply"]',
                '.indeed-apply-widget'
            ]
            
            for selector in indeed_indicators:
                if self.page.query_selector(selector):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking application type: {e}")
            return False
    
    def _submit_application(self) -> bool:
        """Submit the application"""
        try:
            submit_selectors = [
                'button:has-text("Submit application")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                '[data-testid="submit-application"]'
            ]
            
            for selector in submit_selectors:
                if self.click_element(selector, timeout=2000):
                    logger.info("Submit button clicked")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return False
