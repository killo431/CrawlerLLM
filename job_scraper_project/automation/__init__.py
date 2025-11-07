"""
Automation Module - Application Submission Engine

This module provides automated application submission capabilities across
multiple job platforms including LinkedIn Easy Apply, Indeed, and ATS systems.
"""

from automation.application_submitter import ApplicationSubmitter
from automation.models import (
    SubmissionResult,
    SubmissionStatus,
    ApplicationData,
    FormField,
    FieldType,
    NavigationState,
    SubmissionConfig
)

__all__ = [
    "ApplicationSubmitter",
    "SubmissionResult",
    "SubmissionStatus",
    "ApplicationData",
    "FormField",
    "FieldType",
    "NavigationState",
    "SubmissionConfig"
]
