"""
Discovery Module - Real-Time Job Discovery

This module provides continuous job monitoring with scheduled scraping,
deduplication, and real-time notifications.
"""

from discovery.scheduler import JobScheduler
from discovery.deduplicator import JobDeduplicator

__all__ = ["JobScheduler", "JobDeduplicator"]
