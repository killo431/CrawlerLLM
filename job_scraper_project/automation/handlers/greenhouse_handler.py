"""
Greenhouse ATS Handler

Handles automated application submission for Greenhouse ATS.
"""

import time
from typing import Dict, Any, Optional
from automation.handlers.base_handler import BaseHandler
from automation.models import SubmissionResult, SubmissionStatus
from core.logger import setup_logger

logger = setup_logger("greenhouse_handler")


class GreenhouseHandler(BaseHandler):
    """
    Handler for Greenhouse ATS applications.
    
    Greenhouse has a standardized form structure making it more predictable
    than platform-specific handlers.
    """
    
    async def submit(
        self,
        job: Dict[str, Any],
        resume: str,
        cover_letter: Optional[str],
        user_profile: Dict[str, Any]
    ) -> SubmissionResult:
        """
        Submit a Greenhouse ATS application
        
        Process:
        1. Navigate to application page
        2. Fill personal information fields
        3. Upload resume
        4. Upload cover letter (if applicable)
        5. Answer custom questions
        6. Accept privacy policy
        7. Submit
        """
        job_id = job.get('id', 'unknown')
        application_url = job.get('application_url', '')
        
        logger.info(f"Starting Greenhouse application for job {job_id}")
        
        try:
            # Navigate to application page
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
                    platform='greenhouse',
                    status=SubmissionStatus.CAPTCHA_DETECTED,
                    screenshot_path=screenshot_path,
                    error_message="CAPTCHA detected - manual intervention required"
                )
            
            # Fill basic form fields
            if not await self.fill_form(user_profile):
                logger.error("Failed to fill form")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='greenhouse',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "fill_error"),
                    error_message="Failed to fill form fields"
                )
            
            # Upload documents
            if resume:
                if not await self.upload_documents(resume, cover_letter):
                    logger.error("Failed to upload documents")
                    return SubmissionResult(
                        success=False,
                        job_id=job_id,
                        platform='greenhouse',
                        status=SubmissionStatus.FAILED,
                        screenshot_path=self.capture_screenshot(job_id, "upload_error"),
                        error_message="Failed to upload documents"
                    )
            
            # Handle custom questions if present
            await self._answer_custom_questions(user_profile)
            
            # Accept privacy policy if required
            self._accept_privacy_policy()
            
            # Submit application
            if not self._submit_application():
                logger.error("Could not submit application")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='greenhouse',
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
                    platform='greenhouse',
                    status=SubmissionStatus.SUCCESS,
                    screenshot_path=self.capture_screenshot(job_id, "success")
                )
            else:
                logger.warning("Could not verify submission")
                return SubmissionResult(
                    success=False,
                    job_id=job_id,
                    platform='greenhouse',
                    status=SubmissionStatus.FAILED,
                    screenshot_path=self.capture_screenshot(job_id, "verify_error"),
                    error_message="Could not verify submission"
                )
            
        except Exception as e:
            logger.error(f"Error during Greenhouse submission: {e}", exc_info=True)
            return SubmissionResult(
                success=False,
                job_id=job_id,
                platform='greenhouse',
                status=SubmissionStatus.FAILED,
                screenshot_path=self.capture_screenshot(job_id, "error"),
                error_message=str(e)
            )
    
    async def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """Fill Greenhouse application form"""
        try:
            logger.info("Filling Greenhouse form fields")
            
            # Greenhouse typically has standard field IDs
            standard_fields = {
                'first_name': '#first_name',
                'last_name': '#last_name',
                'email': '#email',
                'phone': '#phone'
            }
            
            # Try standard field selectors first
            for field_name, selector in standard_fields.items():
                if field_name in form_data and form_data[field_name]:
                    try:
                        self.fill_text_field(selector, str(form_data[field_name]))
                        time.sleep(0.3)
                    except:
                        logger.debug(f"Could not fill {field_name} using standard selector")
            
            # Detect and fill remaining fields
            fields = self.form_mapper.detect_all_fields()
            field_mapping = self.form_mapper.map_fields_to_data(fields, form_data)
            
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
        """Upload documents to Greenhouse"""
        try:
            logger.info("Uploading documents to Greenhouse")
            
            # Greenhouse typically has specific selectors for resume
            resume_selectors = [
                '#resume',
                'input[name="resume"]',
                'input[type="file"][id*="resume"]'
            ]
            
            # Try to upload resume
            if resume:
                uploaded = False
                for selector in resume_selectors:
                    try:
                        success = self.document_uploader.upload_file(resume, selector)
                        if success:
                            uploaded = True
                            break
                    except:
                        continue
                
                if not uploaded:
                    # Fallback to generic file input
                    uploaded = self.document_uploader.upload_resume(resume)
                
                if not uploaded:
                    logger.error("Could not upload resume")
                    return False
            
            # Upload cover letter if available
            if cover_letter:
                cover_letter_selectors = [
                    '#cover_letter',
                    'input[name="cover_letter"]',
                    'input[type="file"][id*="cover"]'
                ]
                
                for selector in cover_letter_selectors:
                    try:
                        self.document_uploader.upload_file(cover_letter, selector)
                        break
                    except:
                        continue
            
            return True
            
        except Exception as e:
            logger.error(f"Error uploading documents: {e}")
            return False
    
    async def verify_submission(self) -> bool:
        """Verify Greenhouse application submission"""
        try:
            # Look for success indicators
            success_selectors = [
                'text=Application submitted',
                'text=Thank you for applying',
                'text=Your application has been submitted',
                '.application-confirmation',
                '#application_confirmation'
            ]
            
            for selector in success_selectors:
                if self.page.locator(selector).count() > 0:
                    logger.info(f"Success indicator found: {selector}")
                    return True
            
            # Check URL for confirmation page
            if 'confirmation' in self.page.url.lower() or 'thank' in self.page.url.lower():
                logger.info("Confirmation page detected")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verifying submission: {e}")
            return False
    
    async def _answer_custom_questions(self, user_profile: Dict[str, Any]) -> bool:
        """Answer custom screening questions"""
        try:
            # Look for custom question fields
            custom_questions = self.page.query_selector_all('[data-question-type]')
            
            if not custom_questions:
                logger.info("No custom questions found")
                return True
            
            logger.info(f"Found {len(custom_questions)} custom questions")
            
            # Try to answer based on user profile's screening_responses
            screening_responses = user_profile.get('screening_responses', {})
            
            for question_elem in custom_questions:
                try:
                    # Get question text
                    question_text = question_elem.text_content().strip()
                    logger.debug(f"Question: {question_text}")
                    
                    # Check if we have a response
                    if question_text in screening_responses:
                        response = screening_responses[question_text]
                        
                        # Find input field within question
                        input_field = question_elem.query_selector('input, select, textarea')
                        if input_field:
                            tag_name = input_field.evaluate('el => el.tagName.toLowerCase()')
                            if tag_name == 'select':
                                input_field.select_option(response)
                            else:
                                input_field.fill(response)
                except Exception as e:
                    logger.warning(f"Could not answer custom question: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error answering custom questions: {e}")
            return False
    
    def _accept_privacy_policy(self) -> bool:
        """Accept privacy policy checkbox if present"""
        try:
            # Look for privacy policy checkboxes
            privacy_selectors = [
                'input[type="checkbox"][id*="privacy"]',
                'input[type="checkbox"][name*="privacy"]',
                'input[type="checkbox"][id*="terms"]'
            ]
            
            for selector in privacy_selectors:
                checkbox = self.page.query_selector(selector)
                if checkbox and not checkbox.is_checked():
                    checkbox.click()
                    logger.info("Accepted privacy policy")
                    return True
            
            return True  # No privacy checkbox found, continue
            
        except Exception as e:
            logger.warning(f"Error accepting privacy policy: {e}")
            return True  # Continue even if this fails
    
    def _submit_application(self) -> bool:
        """Submit the Greenhouse application"""
        try:
            submit_selectors = [
                '#submit_app',
                'input[type="submit"][value*="Submit"]',
                'button[type="submit"]',
                'button:has-text("Submit Application")'
            ]
            
            for selector in submit_selectors:
                if self.click_element(selector, timeout=2000):
                    logger.info("Submit button clicked")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return False
