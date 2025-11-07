"""
LinkedIn Easy Apply Handler

Handles automated application submission for LinkedIn Easy Apply jobs.
"""

import time
from typing import Dict, Any, Optional
from automation.handlers.base_handler import BaseHandler
from automation.models import SubmissionResult, SubmissionStatus, ApplicationData
from core.logger import setup_logger

logger = setup_logger("linkedin_handler")


class LinkedInHandler(BaseHandler):
    """
    Handler for LinkedIn Easy Apply applications.
    
    LinkedIn Easy Apply uses a multi-step form process that varies by job.
    This handler navigates through the steps and fills required fields.
    """
    
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit a LinkedIn Easy Apply application
        
        Process:
        1. Click Easy Apply button
        2. Navigate multi-step form
        3. Fill personal information
        4. Answer screening questions
        5. Upload resume (if requested)
        6. Review and submit
        """
        job_id = job.get('id', 'unknown')
        application_url = job.get('application_url', '')
        
        logger.info(f"Starting LinkedIn Easy Apply for job {job_id}")
        
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
                    platform='linkedin',
                    status=SubmissionStatus.CAPTCHA_DETECTED,
                    screenshot_path=screenshot_path,
                    error_message="CAPTCHA detected - manual intervention required"
                )
            
            # Click Easy Apply button
            if not self._click_easy_apply():
                logger.error("Could not find Easy Apply button")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='linkedin',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "no_button"),
                    error_message="Easy Apply button not found"
                )
            
            # Wait for modal to appear
            time.sleep(2)
            
            # Detect if multi-step form
            is_multi_step = self.navigator.detect_multi_step_form()
            
            if is_multi_step:
                logger.info("Multi-step form detected")
                nav_state = self.navigator.detect_steps()
                logger.info(f"Detected {nav_state.total_steps} steps")
            
            # Fill form fields
            if not await self.fill_form(user_profile):
                logger.error("Failed to fill form")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='linkedin',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "fill_error"),
                    error_message="Failed to fill form fields"
                )
            
            # Upload documents if needed
            if resume:
                if not await self.upload_documents(resume, cover_letter):
                    logger.warning("Document upload failed, continuing anyway")
            
            # Navigate through steps and fill each one
            if is_multi_step:
                while not self.navigator.state.is_final_step:
                    # Validate current step
                    is_valid, errors = self.navigator.validate_step()
                    if not is_valid:
                        logger.warning(f"Validation errors: {errors}")
                        # Try to fix errors or continue
                    
                    # Try to go to next step
                    if not self.navigator.go_next():
                        logger.error("Could not navigate to next step")
                        break
                    
                    # Fill fields on new step
                    await self.fill_form(user_profile)
                    
                    # Small delay to appear human-like
                    time.sleep(1)
            
            # Submit the application
            if not self.navigator.submit_form():
                # Try alternative submit methods
                if not self._submit_alternative():
                    logger.error("Could not submit application")
                    return SubmissionResult(
                        success=False,
                        job_id=job_id,
                        platform='linkedin',
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
                    platform='linkedin',
                    status=SubmissionStatus.SUCCESS,
                    screenshot_path=self.capture_screenshot(job_id, "success"),
                    confirmation_number=self._extract_confirmation_number()
                )
            else:
                logger.warning("Could not verify submission")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='linkedin',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "verify_error"),
                    error_message="Could not verify submission"
                )
            
        except Exception as e:
            logger.error(f"Error during LinkedIn submission: {e}", exc_info=True)
            return SubmissionResult(
                success=False,
                job_id=job_id,
                platform='linkedin',
                status=SubmissionStatus.FAILED,
                screenshot_path=self.capture_screenshot(job_id, "error"),
                error_message=str(e)
            )
    
    async def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """Fill LinkedIn Easy Apply form fields"""
        try:
            logger.info("Filling form fields")
            
            # Detect all fields on current step
            fields = self.form_mapper.detect_all_fields()
            logger.info(f"Detected {len(fields)} fields")
            
            # Map fields to data
            field_mapping = self.form_mapper.map_fields_to_data(fields, form_data)
            
            # Fill each mapped field
            for field, value in field_mapping.items():
                try:
                    if field.field_type.value in ('text', 'email', 'phone'):
                        self.fill_text_field(field.selector, str(value))
                    elif field.field_type.value == 'select':
                        self.select_option(field.selector, str(value))
                    elif field.field_type.value == 'checkbox':
                        if value:
                            self.click_element(field.selector)
                    
                    time.sleep(0.5)  # Small delay between fields
                except Exception as e:
                    logger.warning(f"Could not fill field {field.selector}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error filling form: {e}")
            return False
    
    async def upload_documents(self, resume: str, cover_letter: Optional[str]) -> bool:
        """Upload documents to LinkedIn"""
        try:
            logger.info("Attempting to upload documents")
            
            # LinkedIn usually has a resume upload section
            if resume:
                success = self.document_uploader.upload_resume(resume)
                if not success:
                    logger.warning("Resume upload failed")
                    return False
            
            # Cover letter is less common on LinkedIn Easy Apply
            if cover_letter:
                self.document_uploader.upload_cover_letter(cover_letter)
            
            return True
            
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return False
    
    async def verify_submission(self) -> bool:
        """Verify LinkedIn application submission"""
        try:
            # Look for success indicators
            success_selectors = [
                'text=Application sent',
                'text=Your application was sent',
                'text=Successfully applied',
                '.artdeco-inline-feedback--success',
                '[data-test-artdeco-toast-item-type="success"]'
            ]
            
            for selector in success_selectors:
                if self.page.locator(selector).count() > 0:
                    logger.info(f"Success indicator found: {selector}")
                    return True
            
            # Check if modal is closed (might indicate success)
            modal = self.page.query_selector('.jobs-easy-apply-modal')
            if not modal or not modal.is_visible():
                logger.info("Easy Apply modal closed - assuming success")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verifying submission: {e}")
            return False
    
    def _click_easy_apply(self) -> bool:
        """Click the Easy Apply button"""
        try:
            # Try various selectors for Easy Apply button
            selectors = [
                'button:has-text("Easy Apply")',
                '.jobs-apply-button--top-card',
                '[data-control-name="jobdetails_topcard_inapply"]'
            ]
            
            for selector in selectors:
                if self.click_element(selector, timeout=3000):
                    logger.info("Easy Apply button clicked")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error clicking Easy Apply: {e}")
            return False
    
    def _submit_alternative(self) -> bool:
        """Try alternative methods to submit"""
        try:
            # Try to find and click submit/apply button
            submit_selectors = [
                'button[aria-label*="Submit"]',
                'button:has-text("Submit application")',
                'button:has-text("Submit")',
                '.jobs-easy-apply-form-actions button[type="submit"]'
            ]
            
            for selector in submit_selectors:
                if self.click_element(selector, timeout=2000):
                    logger.info("Alternative submit clicked")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error with alternative submit: {e}")
            return False
    
    def _extract_confirmation_number(self) -> Optional[str]:
        """Extract confirmation number if available"""
        try:
            # LinkedIn doesn't typically provide confirmation numbers
            # But we can return a timestamp-based reference
            from datetime import datetime
            return f"LI_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        except:
            return None
