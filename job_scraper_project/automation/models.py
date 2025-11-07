"""
Data models for application submission system.

This module contains all data classes used throughout the application submission process.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List


class SubmissionStatus(Enum):
    """Status of an application submission."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    CAPTCHA_DETECTED = "captcha_detected"
    MANUAL_INTERVENTION_REQUIRED = "manual_intervention_required"
    RATE_LIMITED = "rate_limited"
    PLATFORM_ERROR = "platform_error"


class FieldType(Enum):
    """Types of form fields."""
    TEXT = "text"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    FILE = "file"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXTAREA = "textarea"
    DATE = "date"
    NUMBER = "number"


@dataclass
class SubmissionResult:
    """
    Result of an application submission attempt.
    
    Attributes:
        success: Whether the submission was successful
        job_id: Unique identifier for the job
        platform: Platform name (linkedin, indeed, greenhouse, etc.)
        status: Current submission status
        submitted_at: Timestamp of submission
        error_message: Error message if submission failed
        screenshot_path: Path to screenshot taken during submission
        confirmation_number: Confirmation number/code from platform
        metadata: Additional platform-specific data
    """
    success: bool
    job_id: str
    platform: str
    status: SubmissionStatus = SubmissionStatus.PENDING
    submitted_at: Optional[datetime] = None
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    confirmation_number: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set submitted_at if not provided and submission was successful."""
        if self.success and self.submitted_at is None:
            self.submitted_at = datetime.now()
        if self.success:
            self.status = SubmissionStatus.SUCCESS
        elif self.status == SubmissionStatus.PENDING:
            self.status = SubmissionStatus.FAILED


@dataclass
class ApplicationData:
    """
    User profile and application data.
    
    Contains all information needed to fill out job applications.
    """
    # Personal information
    first_name: str
    last_name: str
    email: str
    phone: str
    
    # Optional personal details
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    website_url: Optional[str] = None
    
    # Address information
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    
    # Documents
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    
    # Work authorization
    work_authorized: bool = True
    require_sponsorship: bool = False
    
    # Additional fields
    years_of_experience: Optional[int] = None
    education_level: Optional[str] = None
    
    # Custom responses for screening questions
    screening_responses: Dict[str, str] = field(default_factory=dict)
    
    # Additional data for platform-specific fields
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy access."""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'phone': self.phone,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'website_url': self.website_url,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'work_authorized': self.work_authorized,
            'require_sponsorship': self.require_sponsorship,
            'years_of_experience': self.years_of_experience,
            'education_level': self.education_level,
        }


@dataclass
class FormField:
    """
    Detected form field information.
    
    Represents a single form field that was detected and needs to be filled.
    """
    # Field identification
    selector: str
    field_type: FieldType
    label: Optional[str] = None
    placeholder: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    
    # Field properties
    required: bool = False
    readonly: bool = False
    disabled: bool = False
    
    # Value information
    current_value: Optional[str] = None
    suggested_value: Optional[str] = None
    
    # For select/radio fields
    options: List[str] = field(default_factory=list)
    
    # Confidence in field detection
    confidence: float = 1.0
    
    # Field purpose (detected purpose like 'name', 'email', 'phone')
    detected_purpose: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of the field."""
        label_str = self.label or self.placeholder or self.name or self.id or "unknown"
        return f"FormField({self.field_type.value}: {label_str}, required={self.required})"


@dataclass
class NavigationState:
    """
    State tracking for multi-step form navigation.
    
    Tracks progress through multi-step application forms.
    """
    current_step: int = 0
    total_steps: int = 1
    step_titles: List[str] = field(default_factory=list)
    completed_steps: List[int] = field(default_factory=list)
    can_go_next: bool = True
    can_go_back: bool = False
    is_final_step: bool = False
    
    def advance_step(self):
        """Move to next step."""
        if self.can_go_next and self.current_step < self.total_steps - 1:
            self.completed_steps.append(self.current_step)
            self.current_step += 1
            self.is_final_step = (self.current_step == self.total_steps - 1)
    
    def go_back(self):
        """Move to previous step."""
        if self.can_go_back and self.current_step > 0:
            self.current_step -= 1
            self.is_final_step = False
    
    def __str__(self) -> str:
        """String representation."""
        return f"Step {self.current_step + 1}/{self.total_steps}"


@dataclass
class SubmissionConfig:
    """
    Configuration for application submission.
    
    Controls behavior of the submission process.
    """
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 5  # seconds
    
    # Timeouts
    page_load_timeout: int = 30  # seconds
    element_timeout: int = 10  # seconds
    
    # Screenshots
    screenshot_on_error: bool = True
    screenshot_on_success: bool = True
    screenshot_dir: str = "data/screenshots"
    
    # Browser settings
    headless: bool = False
    slow_mo: int = 100  # milliseconds - slows down actions to appear more human
    
    # Rate limiting
    delay_between_actions: float = 1.0  # seconds
    delay_between_submissions: int = 30  # seconds
    
    # CAPTCHA handling
    pause_on_captcha: bool = True
    captcha_wait_time: int = 300  # seconds to wait for manual CAPTCHA solving
    
    # Validation
    verify_submission: bool = True
    wait_for_confirmation: bool = True
    confirmation_wait_time: int = 10  # seconds
