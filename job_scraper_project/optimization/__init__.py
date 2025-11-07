"""
Optimization Module - ATS Optimization Engine

This module provides ATS optimization capabilities including keyword extraction,
compatibility scoring, and resume optimization.
"""

from optimization.ats_scorer import ATSScorer
from optimization.keyword_extractor import KeywordExtractor

__all__ = ["ATSScorer", "KeywordExtractor"]
