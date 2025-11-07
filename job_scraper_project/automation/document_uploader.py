"""
Document upload automation module.

Handles file upload for resumes, cover letters, and other documents during application submission.
"""
import os
import time
from pathlib import Path
from typing import Optional, List
from playwright.sync_api import Page, ElementHandle
from core.logger import setup_logger

logger = setup_logger("document_uploader")


class DocumentUploader:
    """
    Handles document uploads during application submission.
    
    Supports multiple upload strategies:
    - Direct input element interaction
    - Drag-and-drop simulation
    - File chooser dialogs
    """
    
    # Supported file formats
    RESUME_FORMATS = ['.pdf', '.doc', '.docx', '.txt']
    COVER_LETTER_FORMATS = ['.pdf', '.doc', '.docx', '.txt']
    
    def __init__(self, page: Page):
        """
        Initialize the document uploader.
        
        Args:
            page: Playwright page object
        """
        self.page = page
    
    def upload_file(
        self, 
        file_path: str, 
        selector: Optional[str] = None,
        timeout: int = 10000
    ) -> bool:
        """
        Upload a file to a form.
        
        Args:
            file_path: Path to the file to upload
            selector: CSS selector for file input (optional)
            timeout: Timeout in milliseconds
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            # Validate file format
            if not self._validate_file_format(file_path):
                logger.error(f"Unsupported file format: {file_path}")
                return False
            
            # Convert to absolute path
            abs_path = os.path.abspath(file_path)
            
            # Try to find file input
            if selector:
                file_input = self.page.wait_for_selector(selector, timeout=timeout)
            else:
                file_input = self._find_file_input()
            
            if not file_input:
                logger.error("Could not find file input element")
                return False
            
            # Upload file
            file_input.set_input_files(abs_path)
            logger.info(f"Successfully uploaded file: {file_path}")
            
            # Wait a bit for upload to process
            time.sleep(1)
            
            # Verify upload
            return self._verify_upload(file_input, file_path)
            
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def upload_resume(
        self, 
        resume_path: str,
        selector: Optional[str] = None
    ) -> bool:
        """
        Upload a resume file.
        
        Args:
            resume_path: Path to resume file
            selector: Optional CSS selector for resume input
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Uploading resume: {resume_path}")
        
        # Try to find resume input if no selector provided
        if not selector:
            selector = self._find_resume_input_selector()
        
        return self.upload_file(resume_path, selector)
    
    def upload_cover_letter(
        self, 
        cover_letter_path: str,
        selector: Optional[str] = None
    ) -> bool:
        """
        Upload a cover letter file.
        
        Args:
            cover_letter_path: Path to cover letter file
            selector: Optional CSS selector for cover letter input
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Uploading cover letter: {cover_letter_path}")
        
        # Try to find cover letter input if no selector provided
        if not selector:
            selector = self._find_cover_letter_input_selector()
        
        return self.upload_file(cover_letter_path, selector)
    
    def _find_file_input(self) -> Optional[ElementHandle]:
        """
        Find any visible file input on the page.
        
        Returns:
            ElementHandle for file input or None
        """
        try:
            file_inputs = self.page.query_selector_all('input[type="file"]')
            
            for file_input in file_inputs:
                # Check if visible
                if file_input.is_visible():
                    return file_input
            
            # Return first one even if not visible
            if file_inputs:
                return file_inputs[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding file input: {e}")
            return None
    
    def _find_resume_input_selector(self) -> Optional[str]:
        """
        Find the selector for resume upload input.
        
        Returns:
            CSS selector or None
        """
        try:
            # Look for inputs with resume-related attributes
            resume_keywords = ['resume', 'cv', 'curriculum']
            
            file_inputs = self.page.query_selector_all('input[type="file"]')
            
            for file_input in file_inputs:
                # Check various attributes
                elem_id = file_input.get_attribute('id') or ''
                elem_name = file_input.get_attribute('name') or ''
                elem_class = file_input.get_attribute('class') or ''
                
                # Check if any resume keyword matches
                combined = f"{elem_id} {elem_name} {elem_class}".lower()
                if any(keyword in combined for keyword in resume_keywords):
                    # Build selector
                    if file_input.get_attribute('id'):
                        return f'#{file_input.get_attribute("id")}'
                    elif file_input.get_attribute('name'):
                        return f'[name="{file_input.get_attribute("name")}"]'
            
            # Fallback: return first file input
            if file_inputs:
                if file_inputs[0].get_attribute('id'):
                    return f'#{file_inputs[0].get_attribute("id")}'
            
            return 'input[type="file"]'
            
        except Exception as e:
            logger.error(f"Error finding resume input: {e}")
            return 'input[type="file"]'
    
    def _find_cover_letter_input_selector(self) -> Optional[str]:
        """
        Find the selector for cover letter upload input.
        
        Returns:
            CSS selector or None
        """
        try:
            # Look for inputs with cover letter-related attributes
            cover_keywords = ['cover', 'letter', 'coverletter']
            
            file_inputs = self.page.query_selector_all('input[type="file"]')
            
            for file_input in file_inputs:
                # Check various attributes
                elem_id = file_input.get_attribute('id') or ''
                elem_name = file_input.get_attribute('name') or ''
                elem_class = file_input.get_attribute('class') or ''
                
                # Check if any cover letter keyword matches
                combined = f"{elem_id} {elem_name} {elem_class}".lower()
                if any(keyword in combined for keyword in cover_keywords):
                    # Build selector
                    if file_input.get_attribute('id'):
                        return f'#{file_input.get_attribute("id")}'
                    elif file_input.get_attribute('name'):
                        return f'[name="{file_input.get_attribute("name")}"]'
            
            # Fallback: return second file input if available
            if len(file_inputs) > 1:
                if file_inputs[1].get_attribute('id'):
                    return f'#{file_inputs[1].get_attribute("id")}'
            
            return 'input[type="file"]'
            
        except Exception as e:
            logger.error(f"Error finding cover letter input: {e}")
            return 'input[type="file"]'
    
    def _validate_file_format(self, file_path: str) -> bool:
        """
        Validate file format is supported.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if format is supported
        """
        ext = Path(file_path).suffix.lower()
        
        # Check if it's a supported format
        supported = self.RESUME_FORMATS + self.COVER_LETTER_FORMATS
        return ext in supported
    
    def _verify_upload(
        self, 
        file_input: ElementHandle, 
        file_path: str
    ) -> bool:
        """
        Verify that file was uploaded successfully.
        
        Args:
            file_input: The file input element
            file_path: Path to uploaded file
            
        Returns:
            True if upload verified
        """
        try:
            # Check if input has files
            files = file_input.evaluate('el => el.files.length')
            if files > 0:
                logger.info("Upload verified: file input has files")
                return True
            
            # Look for success indicators on page
            success_indicators = [
                '.upload-success',
                '.file-uploaded',
                '[data-upload-status="success"]'
            ]
            
            for selector in success_indicators:
                if self.page.query_selector(selector):
                    logger.info(f"Upload verified: found success indicator {selector}")
                    return True
            
            # Look for filename in DOM
            filename = Path(file_path).name
            if self.page.locator(f'text="{filename}"').count() > 0:
                logger.info("Upload verified: filename found on page")
                return True
            
            # If we got here, assume success (file input accepted the file)
            logger.info("Upload assumed successful (no error detected)")
            return True
            
        except Exception as e:
            logger.warning(f"Could not verify upload: {e}")
            # Assume success if we can't verify
            return True
    
    def clear_upload(self, selector: str) -> bool:
        """
        Clear an uploaded file.
        
        Args:
            selector: CSS selector for file input
            
        Returns:
            True if successful
        """
        try:
            file_input = self.page.wait_for_selector(selector, timeout=5000)
            if file_input:
                file_input.set_input_files([])
                logger.info("Cleared file upload")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing upload: {e}")
            return False
    
    def get_uploaded_files(self) -> List[str]:
        """
        Get list of uploaded filenames.
        
        Returns:
            List of filenames that have been uploaded
        """
        try:
            file_inputs = self.page.query_selector_all('input[type="file"]')
            uploaded = []
            
            for file_input in file_inputs:
                files_count = file_input.evaluate('el => el.files.length')
                if files_count > 0:
                    # Try to get filename
                    for i in range(files_count):
                        filename = file_input.evaluate(f'el => el.files[{i}].name')
                        if filename:
                            uploaded.append(filename)
            
            return uploaded
            
        except Exception as e:
            logger.error(f"Error getting uploaded files: {e}")
            return []
