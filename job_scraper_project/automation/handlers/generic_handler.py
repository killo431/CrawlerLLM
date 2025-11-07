"""
Generic Handler - Fallback handler for unknown platforms

Handles application submission for platforms without specific handlers.
Uses heuristic detection and best-effort submission.
"""

import time
from typing import Dict, Any, Optional
from automation.handlers.base_handler import BaseHandler
from automation.models import SubmissionResult, SubmissionStatus
from core.logger import setup_logger

logger = setup_logger("generic_handler")


class GenericHandler(BaseHandler):
    """
    Generic fallback handler for unknown application platforms.
    
    Uses intelligent form detection and heuristics to attempt submission
    on any application form.
    """
    
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit application using generic best-effort approach
        
        Process:
        1. Navigate to application page
        2. Detect all form fields
        3. Map fields to user data
        4. Upload documents
        5. Attempt submission
        """
        job_id = job.get('id', 'unknown')
        application_url = job.get('application_url', '')
        
        logger.info(f"Starting generic application for job {job_id}")
        
        try:
            # Navigate to page
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
                    platform='generic',
                    status=SubmissionStatus.CAPTCHA_DETECTED,
                    screenshot_path=screenshot_path,
                    error_message="CAPTCHA detected - manual intervention required"
                )
            
            # Attempt to fill form
            if not await self.fill_form(user_profile):
                logger.warning("Form filling had issues, continuing anyway")
            
            # Upload documents if possible
            if resume:
                await self.upload_documents(resume, cover_letter)
            
            # Handle multi-step if detected
            if self.navigator.detect_multi_step_form():
                logger.info("Multi-step form detected")
                attempt_count = 0
                max_attempts = 10  # Prevent infinite loops
                
                while not self.navigator.state.is_final_step and attempt_count < max_attempts:
                    if not self.navigator.go_next():
                        break
                    await self.fill_form(user_profile)
                    time.sleep(1)
                    attempt_count += 1
            
            # Attempt submission
            if not self._attempt_submission():
                logger.warning("Could not find submit button")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='generic',
                    status=SubmissionStatus.MANUAL_INTERVENTION_REQUIRED,
                    screenshot_path=self.capture_screenshot(job_id, "no_submit"),
                    error_message="Could not locate submit button - manual submission required"
                )
            
            # Wait for potential confirmation
            time.sleep(3)
            
            # Try to verify, but be lenient
            verified = await self.verify_submission()
            
            if verified:
                logger.info("Application appears successful")
                return SubmissionResult(
                    success=True,
                    job_id=job_id,
                    platform='generic',
                    status=SubmissionStatus.SUCCESS,
                    screenshot_path=self.capture_screenshot(job_id, "success")
                )
            else:
                # Could not verify, but may still be successful
                logger.warning("Could not verify submission - manual verification recommended")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='generic',
                    status=SubmissionStatus.MANUAL_INTERVENTION_REQUIRED,
                    screenshot_path=self.capture_screenshot(job_id, "unverified"),
                    error_message="Submission attempted but not verified - please check manually"
                )
            
        except Exception as e:
            logger.error(f"Error during generic submission: {e}", exc_info=True)
            return SubmissionResult(
                success=False,
                job_id=job_id,
                platform='generic',
                status=SubmissionStatus.FAILED,
                screenshot_path=self.capture_screenshot(job_id, "error"),
                error_message=str(e)
            )
    
    async def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """Fill form using intelligent field detection"""
        try:
            logger.info("Detecting and filling form fields")
            
            # Detect all fields
            fields = self.form_mapper.detect_all_fields()
            logger.info(f"Detected {len(fields)} fields")
            
            if not fields:
                logger.warning("No form fields detected")
                return False
            
            # Map fields to data
            field_mapping = self.form_mapper.map_fields_to_data(fields, form_data)
            logger.info(f"Mapped {len(field_mapping)} fields to user data")
            
            # Fill each field
            filled_count = 0
            for field, value in field_mapping.items():
                try:
                    if field.field_type.value in ['text', 'email', 'phone', 'url']:
                        if self.fill_text_field(field.selector, str(value)):
                            filled_count += 1
                    elif field.field_type.value == 'select':
                        if self.select_option(field.selector, str(value)):
                            filled_count += 1
                    elif field.field_type.value == 'checkbox':
                        if value and self.click_element(field.selector):
                            filled_count += 1
                    elif field.field_type.value == 'textarea':
                        if self.fill_text_field(field.selector, str(value)):
                            filled_count += 1
                    
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Could not fill field {field.selector}: {e}")
            
            logger.info(f"Successfully filled {filled_count}/{len(field_mapping)} fields")
            return filled_count > 0
            
        except Exception as e:
            logger.error(f"Error filling form: {e}")
            return False
    
    async def upload_documents(self, resume: str, cover_letter: Optional[str]) -> bool:
        """Upload documents using generic detection"""
        try:
            logger.info("Attempting document upload")
            
            success = False
            
            # Try to upload resume
            if resume:
                if self.document_uploader.upload_resume(resume):
                    logger.info("Resume uploaded successfully")
                    success = True
                else:
                    logger.warning("Resume upload failed")
            
            # Try to upload cover letter
            if cover_letter:
                if self.document_uploader.upload_cover_letter(cover_letter):
                    logger.info("Cover letter uploaded successfully")
                    success = True
                else:
                    logger.warning("Cover letter upload failed")
            
            return success
            
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return False
    
    async def verify_submission(self) -> bool:
        """Verify submission using generic indicators"""
        try:
            # Look for common success indicators
            success_patterns = [
                'thank you',
                'success',
                'submitted',
                'received',
                'confirmation',
                'application sent'
            ]
            
            page_text = self.page.text_content('body').lower()
            
            for pattern in success_patterns:
                if pattern in page_text:
                    logger.info(f"Success indicator found: {pattern}")
                    return True
            
            # Check URL for confirmation page
            url = self.page.url.lower()
            if any(word in url for word in ['confirm', 'thank', 'success']):
                logger.info("Success page detected from URL")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verifying submission: {e}")
            return False
    
    def _attempt_submission(self) -> bool:
        """Attempt to find and click submit button"""
        try:
            # Common submit button patterns
            submit_patterns = [
                'submit',
                'apply',
                'send',
                'finish',
                'complete',
                'next'
            ]
            
            # Try each pattern
            for pattern in submit_patterns:
                # Try button
                button = self.page.query_selector(f'button:has-text("{pattern}")')
                if button and button.is_visible():
                    button.click()
                    logger.info(f"Clicked submit button with text: {pattern}")
                    return True
                
                # Try input[type=submit]
                submit_input = self.page.query_selector(f'input[type="submit"][value*="{pattern}" i]')
                if submit_input and submit_input.is_visible():
                    submit_input.click()
                    logger.info(f"Clicked submit input with value: {pattern}")
                    return True
            
            # Fallback: any submit button
            any_submit = self.page.query_selector('button[type="submit"], input[type="submit"]')
            if any_submit and any_submit.is_visible():
                any_submit.click()
                logger.info("Clicked generic submit button")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error attempting submission: {e}")
            return False
