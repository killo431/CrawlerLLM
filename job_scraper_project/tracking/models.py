"""
Tracking Models - Data models for application tracking
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ApplicationStatus(Enum):
    """Application status values"""
    SUBMITTED = "submitted"
    VIEWED = "viewed"
    REJECTED = "rejected"
    INTERVIEW_REQUESTED = "interview_requested"
    OFFER_RECEIVED = "offer_received"
    WITHDRAWN = "withdrawn"


class ResponseType(Enum):
    """Email response types"""
    NONE = "none"
    REJECTION = "rejection"
    INTERVIEW = "interview"
    OFFER = "offer"
    UPDATE = "update"


@dataclass
class Application:
    """
    Represents a job application.
    
    Tracks the complete lifecycle of an application from submission
    through final outcome.
    """
    id: str
    user_id: str
    job_id: str
    
    # Job details
    job_title: str
    company: str
    application_url: str
    
    # Application details
    submitted_at: datetime
    resume_version: str
    cover_letter_version: Optional[str]
    match_score: float
    
    # Status tracking
    status: ApplicationStatus
    status_updated_at: datetime
    
    # Response tracking
    response_received: bool = False
    response_at: Optional[datetime] = None
    response_type: Optional[ResponseType] = None
    response_email_id: Optional[str] = None
    
    # Interview details (if applicable)
    interview_requested: bool = False
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None  # 'phone', 'video', 'in_person'
    
    # Metadata
    confirmation_screenshot: Optional[str] = None
    confirmation_number: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'company': self.company,
            'application_url': self.application_url,
            'submitted_at': self.submitted_at.isoformat(),
            'resume_version': self.resume_version,
            'cover_letter_version': self.cover_letter_version,
            'match_score': self.match_score,
            'status': self.status.value,
            'status_updated_at': self.status_updated_at.isoformat(),
            'response_received': self.response_received,
            'response_at': self.response_at.isoformat() if self.response_at else None,
            'response_type': self.response_type.value if self.response_type else None,
            'response_email_id': self.response_email_id,
            'interview_requested': self.interview_requested,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'interview_type': self.interview_type,
            'confirmation_screenshot': self.confirmation_screenshot,
            'confirmation_number': self.confirmation_number,
            'notes': self.notes
        }


@dataclass
class ApplicationEvent:
    """
    Represents an event in an application's lifecycle.
    
    Used for detailed tracking of all state changes and actions.
    """
    id: str
    application_id: str
    event_type: str  # 'submitted', 'viewed', 'response_received', etc.
    event_timestamp: datetime
    event_data: dict
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'event_type': self.event_type,
            'event_timestamp': self.event_timestamp.isoformat(),
            'event_data': self.event_data
        }
