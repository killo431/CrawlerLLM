"""
Match Scoring - Data structures and utilities for match scores
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class MatchScore:
    """
    Represents a job match score with breakdown.
    
    Attributes:
        overall_score: Overall match score (0-100)
        breakdown: Dictionary of individual dimension scores
        is_dealbreaker: Whether job has deal-breaker criteria
        explanation: Human-readable explanation of the match
    """
    overall_score: float
    breakdown: Dict[str, float]
    is_dealbreaker: bool
    explanation: str
    
    def is_good_match(self, threshold: float = 75.0) -> bool:
        """Check if this is a good match based on threshold"""
        return not self.is_dealbreaker and self.overall_score >= threshold
    
    def get_risk_level(self) -> str:
        """Get risk level based on score"""
        if self.is_dealbreaker:
            return "DEALBREAKER"
        elif self.overall_score >= 90:
            return "EXCELLENT"
        elif self.overall_score >= 75:
            return "GOOD"
        elif self.overall_score >= 60:
            return "MODERATE"
        else:
            return "LOW"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'overall_score': self.overall_score,
            'breakdown': self.breakdown,
            'is_dealbreaker': self.is_dealbreaker,
            'explanation': self.explanation,
            'risk_level': self.get_risk_level()
        }
