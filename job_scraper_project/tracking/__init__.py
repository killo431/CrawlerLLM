"""
Tracking Module - Application Tracking & Response Monitoring

This module provides comprehensive tracking of job applications and monitoring
of email responses with automatic classification.
"""

from tracking.models import Application, ApplicationEvent
from tracking.database import ApplicationDatabase

__all__ = ["Application", "ApplicationEvent", "ApplicationDatabase"]
