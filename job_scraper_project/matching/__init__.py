"""
Matching Module - Intelligent Job Matching Engine

This module provides AI-powered job matching capabilities with multi-dimensional
scoring to match jobs to user profiles.
"""

from matching.matcher import JobMatcher
from matching.scoring import MatchScore

__all__ = ["JobMatcher", "MatchScore"]
