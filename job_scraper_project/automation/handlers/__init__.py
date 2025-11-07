"""
Platform-specific application handlers

Each handler implements the submission logic for a specific platform or ATS.
"""

from automation.handlers.base_handler import BaseHandler
from automation.handlers.linkedin_handler import LinkedInHandler
from automation.handlers.indeed_handler import IndeedHandler
from automation.handlers.greenhouse_handler import GreenhouseHandler
from automation.handlers.generic_handler import GenericHandler

__all__ = [
    "BaseHandler",
    "LinkedInHandler",
    "IndeedHandler",
    "GreenhouseHandler",
    "GenericHandler"
]
