"""
Form field detection and mapping module.

This module provides intelligent form field detection using heuristics and pattern matching.
"""
import re
from typing import List, Dict, Optional, Any
from playwright.sync_api import Page, ElementHandle
from automation.models import FormField, FieldType
from core.logger import setup_logger

logger = setup_logger("form_mapper")


class FormMapper:
    """
    Intelligent form field detector and mapper.
    
    Detects form fields on a page and maps them to known purposes (name, email, phone, etc.)
    using label matching, placeholder analysis, and field attributes.
    """
    
    # Pattern definitions for field detection
    NAME_PATTERNS = [
        r'\bfirst\s*name\b',
        r'\bgiven\s*name\b',
        r'\blast\s*name\b',
        r'\bfamily\s*name\b',
        r'\bfull\s*name\b',
        r'\bname\b'
    ]
    
    EMAIL_PATTERNS = [
        r'\bemail\b',
        r'\be-mail\b',
        r'\bmail\b'
    ]
    
    PHONE_PATTERNS = [
        r'\bphone\b',
        r'\btelephone\b',
        r'\bmobile\b',
        r'\bcell\b',
        r'\bcontact\s*number\b'
    ]
    
    ADDRESS_PATTERNS = [
        r'\baddress\b',
        r'\bstreet\b',
        r'\bcity\b',
        r'\bstate\b',
        r'\bzip\b',
        r'\bpostal\b',
        r'\bcountry\b'
    ]
    
    URL_PATTERNS = [
        r'\burl\b',
        r'\bwebsite\b',
        r'\blinkedin\b',
        r'\bgithub\b',
        r'\bportfolio\b'
    ]
    
    def __init__(self, page: Page):
        """
        Initialize the form mapper.
        
        Args:
            page: Playwright page object
        """
        self.page = page
    
    def detect_all_fields(self) -> List[FormField]:
        """
        Detect all form fields on the current page.
        
        Returns:
            List of detected FormField objects
        """
        fields = []
        
        # Detect text inputs
        fields.extend(self._detect_text_inputs())
        
        # Detect email inputs
        fields.extend(self._detect_email_inputs())
        
        # Detect phone inputs
        fields.extend(self._detect_phone_inputs())
        
        # Detect file inputs
        fields.extend(self._detect_file_inputs())
        
        # Detect select dropdowns
        fields.extend(self._detect_select_fields())
        
        # Detect textareas
        fields.extend(self._detect_textareas())
        
        # Detect checkboxes
        fields.extend(self._detect_checkboxes())
        
        logger.info(f"Detected {len(fields)} form fields on page")
        return fields
    
    def _detect_text_inputs(self) -> List[FormField]:
        """Detect text input fields."""
        fields = []
        try:
            inputs = self.page.query_selector_all('input[type="text"], input:not([type])')
            
            for input_elem in inputs:
                field = self._create_field_from_element(input_elem, FieldType.TEXT)
                if field:
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting text inputs: {e}")
        
        return fields
    
    def _detect_email_inputs(self) -> List[FormField]:
        """Detect email input fields."""
        fields = []
        try:
            inputs = self.page.query_selector_all('input[type="email"]')
            
            for input_elem in inputs:
                field = self._create_field_from_element(input_elem, FieldType.EMAIL)
                if field:
                    field.detected_purpose = 'email'
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting email inputs: {e}")
        
        return fields
    
    def _detect_phone_inputs(self) -> List[FormField]:
        """Detect phone input fields."""
        fields = []
        try:
            inputs = self.page.query_selector_all('input[type="tel"], input[type="phone"]')
            
            for input_elem in inputs:
                field = self._create_field_from_element(input_elem, FieldType.PHONE)
                if field:
                    field.detected_purpose = 'phone'
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting phone inputs: {e}")
        
        return fields
    
    def _detect_file_inputs(self) -> List[FormField]:
        """Detect file upload inputs."""
        fields = []
        try:
            inputs = self.page.query_selector_all('input[type="file"]')
            
            for input_elem in inputs:
                field = self._create_field_from_element(input_elem, FieldType.FILE)
                if field:
                    # Try to determine if it's for resume or cover letter
                    label_text = (field.label or field.placeholder or '').lower()
                    if 'resume' in label_text or 'cv' in label_text:
                        field.detected_purpose = 'resume'
                    elif 'cover' in label_text or 'letter' in label_text:
                        field.detected_purpose = 'cover_letter'
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting file inputs: {e}")
        
        return fields
    
    def _detect_select_fields(self) -> List[FormField]:
        """Detect select dropdown fields."""
        fields = []
        try:
            selects = self.page.query_selector_all('select')
            
            for select_elem in selects:
                field = self._create_field_from_element(select_elem, FieldType.SELECT)
                if field:
                    # Extract options
                    options = select_elem.query_selector_all('option')
                    field.options = [opt.text_content() for opt in options if opt.text_content()]
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting select fields: {e}")
        
        return fields
    
    def _detect_textareas(self) -> List[FormField]:
        """Detect textarea fields."""
        fields = []
        try:
            textareas = self.page.query_selector_all('textarea')
            
            for textarea_elem in textareas:
                field = self._create_field_from_element(textarea_elem, FieldType.TEXTAREA)
                if field:
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting textareas: {e}")
        
        return fields
    
    def _detect_checkboxes(self) -> List[FormField]:
        """Detect checkbox fields."""
        fields = []
        try:
            checkboxes = self.page.query_selector_all('input[type="checkbox"]')
            
            for checkbox_elem in checkboxes:
                field = self._create_field_from_element(checkbox_elem, FieldType.CHECKBOX)
                if field:
                    fields.append(field)
        except Exception as e:
            logger.error(f"Error detecting checkboxes: {e}")
        
        return fields
    
    def _create_field_from_element(
        self, 
        element: ElementHandle, 
        field_type: FieldType
    ) -> Optional[FormField]:
        """
        Create a FormField object from an HTML element.
        
        Args:
            element: The HTML element
            field_type: The type of field
            
        Returns:
            FormField object or None if creation fails
        """
        try:
            # Get element attributes
            elem_id = element.get_attribute('id')
            elem_name = element.get_attribute('name')
            placeholder = element.get_attribute('placeholder')
            required = element.get_attribute('required') is not None
            readonly = element.get_attribute('readonly') is not None
            disabled = element.get_attribute('disabled') is not None
            
            # Try to find associated label
            label = self._find_label_for_element(element, elem_id)
            
            # Create selector - prefer ID, fall back to name, then other attributes
            if elem_id:
                selector = f'#{elem_id}'
            elif elem_name:
                selector = f'[name="{elem_name}"]'
            else:
                selector = self._generate_unique_selector(element)
            
            # Get current value
            current_value = element.get_attribute('value')
            
            # Create field
            field = FormField(
                selector=selector,
                field_type=field_type,
                label=label,
                placeholder=placeholder,
                name=elem_name,
                id=elem_id,
                required=required,
                readonly=readonly,
                disabled=disabled,
                current_value=current_value
            )
            
            # Detect purpose
            field.detected_purpose = self._detect_field_purpose(field)
            
            return field
            
        except Exception as e:
            logger.error(f"Error creating field from element: {e}")
            return None
    
    def _find_label_for_element(
        self, 
        element: ElementHandle, 
        elem_id: Optional[str]
    ) -> Optional[str]:
        """
        Find the label associated with an element.
        
        Args:
            element: The form element
            elem_id: Element ID if available
            
        Returns:
            Label text or None
        """
        try:
            # Try to find label by 'for' attribute
            if elem_id:
                label = self.page.query_selector(f'label[for="{elem_id}"]')
                if label:
                    return label.text_content().strip()
            
            # Try to find parent label
            parent = element.evaluate('el => el.parentElement')
            if parent:
                parent_elem = element.evaluate_handle('el => el.parentElement')
                if parent_elem:
                    tag_name = parent_elem.evaluate('el => el.tagName.toLowerCase()')
                    if tag_name == 'label':
                        return parent_elem.evaluate('el => el.textContent').strip()
            
            return None
            
        except Exception as e:
            logger.debug(f"Could not find label: {e}")
            return None
    
    def _generate_unique_selector(self, element: ElementHandle) -> str:
        """
        Generate a unique CSS selector for an element.
        
        Args:
            element: The element to generate selector for
            
        Returns:
            CSS selector string
        """
        try:
            # Use Playwright's built-in selector generation
            selector = element.evaluate('''
                el => {
                    let path = [];
                    while (el.parentElement) {
                        let selector = el.tagName.toLowerCase();
                        if (el.className) {
                            selector += '.' + el.className.split(' ').join('.');
                        }
                        path.unshift(selector);
                        el = el.parentElement;
                    }
                    return path.join(' > ');
                }
            ''')
            return selector
        except Exception as e:
            logger.warning(f"Could not generate selector: {e}")
            return 'input'
    
    def _detect_field_purpose(self, field: FormField) -> Optional[str]:
        """
        Detect the purpose of a field based on its attributes.
        
        Args:
            field: The FormField to analyze
            
        Returns:
            Detected purpose string or None
        """
        # Combine all text that might indicate purpose
        text_to_check = ' '.join(filter(None, [
            field.label,
            field.placeholder,
            field.name,
            field.id
        ])).lower()
        
        # Check for name fields
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in self.NAME_PATTERNS):
            if 'first' in text_to_check:
                return 'first_name'
            elif 'last' in text_to_check:
                return 'last_name'
            else:
                return 'full_name'
        
        # Check for email
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in self.EMAIL_PATTERNS):
            return 'email'
        
        # Check for phone
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in self.PHONE_PATTERNS):
            return 'phone'
        
        # Check for URL/website fields
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in self.URL_PATTERNS):
            if 'linkedin' in text_to_check:
                return 'linkedin_url'
            elif 'github' in text_to_check:
                return 'github_url'
            elif 'portfolio' in text_to_check:
                return 'portfolio_url'
            else:
                return 'website_url'
        
        # Check for address fields
        if any(re.search(pattern, text_to_check, re.IGNORECASE) for pattern in self.ADDRESS_PATTERNS):
            if 'city' in text_to_check:
                return 'city'
            elif 'state' in text_to_check:
                return 'state'
            elif 'zip' in text_to_check or 'postal' in text_to_check:
                return 'zip_code'
            elif 'country' in text_to_check:
                return 'country'
            else:
                return 'address'
        
        return None
    
    def map_fields_to_data(
        self, 
        fields: List[FormField], 
        data: Dict[str, Any]
    ) -> Dict[FormField, Any]:
        """
        Map detected form fields to user data.
        
        Args:
            fields: List of detected FormField objects
            data: Dictionary of user data
            
        Returns:
            Dictionary mapping FormField to values
        """
        mapping = {}
        
        for field in fields:
            if field.detected_purpose and field.detected_purpose in data:
                value = data[field.detected_purpose]
                if value is not None:
                    field.suggested_value = str(value)
                    mapping[field] = value
        
        logger.info(f"Mapped {len(mapping)}/{len(fields)} fields to user data")
        return mapping
    
    def score_field_confidence(self, field: FormField) -> float:
        """
        Calculate confidence score for field detection.
        
        Args:
            field: The FormField to score
            
        Returns:
            Confidence score between 0 and 1
        """
        score = 0.5  # Base score
        
        # Increase confidence if we have a clear label
        if field.label:
            score += 0.2
        
        # Increase if we detected a purpose
        if field.detected_purpose:
            score += 0.2
        
        # Increase if field has a good ID or name
        if field.id or field.name:
            score += 0.1
        
        return min(score, 1.0)
