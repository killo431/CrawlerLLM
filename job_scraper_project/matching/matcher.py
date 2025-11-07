"""
Job Matcher - Main matching engine for job-to-profile matching
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from matching.scoring import MatchScore
from matching.deal_breakers import DealBreakerChecker


@dataclass
class UserProfile:
    """User profile for job matching"""
    user_id: str
    target_titles: List[str]
    skills: Dict[str, str]  # skill -> proficiency level
    experience_years: int
    location: str
    remote_preference: str  # 'remote_only', 'hybrid', 'on_site', 'any'
    salary_min: int
    salary_max: int
    education: List[str]
    
    # Deal-breakers
    only_remote: bool = False
    minimum_salary: int = 0
    blacklisted_companies: List[str] = None
    
    def __post_init__(self):
        if self.blacklisted_companies is None:
            self.blacklisted_companies = []


class JobMatcher:
    """
    Intelligent job matching engine with multi-dimensional scoring.
    
    Scoring Dimensions:
    - Title Match (25% weight): Semantic similarity to target titles
    - Skills Match (30% weight): Required skills possessed
    - Location Match (15% weight): Location/remote compatibility
    - Salary Match (10% weight): Salary range alignment
    - Experience Match (10% weight): Years and level match
    - Company Match (5% weight): Size, industry preferences
    - Requirements Met (5% weight): Education, certifications
    
    Example:
        >>> matcher = JobMatcher()
        >>> score = matcher.calculate_match_score(job, user_profile)
        >>> if score.overall_score >= 80:
        ...     print(f"Great match! Score: {score.overall_score}")
    """
    
    def __init__(self):
        """Initialize the job matcher"""
        self.deal_breaker_checker = DealBreakerChecker()
        self.weights = {
            'title_match': 0.25,
            'skills_match': 0.30,
            'location_match': 0.15,
            'salary_match': 0.10,
            'experience_match': 0.10,
            'company_match': 0.05,
            'requirements_met': 0.05
        }
    
    def calculate_match_score(
        self,
        job: Dict[str, Any],
        user_profile: UserProfile
    ) -> MatchScore:
        """
        Calculate comprehensive match score for a job
        
        Args:
            job: Job details
            user_profile: User profile
            
        Returns:
            MatchScore object with overall score and breakdown
        """
        # Check deal-breakers first
        if self.deal_breaker_checker.has_dealbreaker(job, user_profile):
            return MatchScore(
                overall_score=0,
                breakdown={},
                is_dealbreaker=True,
                explanation="Job has deal-breaker criteria"
            )
        
        # Calculate individual scores
        scores = {
            'title_match': self._score_title_match(job, user_profile),
            'skills_match': self._score_skills_match(job, user_profile),
            'location_match': self._score_location_match(job, user_profile),
            'salary_match': self._score_salary_match(job, user_profile),
            'experience_match': self._score_experience_match(job, user_profile),
            'company_match': self._score_company_match(job, user_profile),
            'requirements_met': self._score_requirements_met(job, user_profile)
        }
        
        # Calculate weighted overall score
        overall = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return MatchScore(
            overall_score=overall,
            breakdown=scores,
            is_dealbreaker=False,
            explanation=self._generate_explanation(scores, overall)
        )
    
    def _score_title_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score job title match using semantic similarity"""
        # TODO: Implement using sentence transformers
        return 75.0
    
    def _score_skills_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score required skills match"""
        # TODO: Extract required skills from job description
        # TODO: Compare with user's skills
        return 80.0
    
    def _score_location_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score location compatibility"""
        # TODO: Implement location matching logic
        return 90.0
    
    def _score_salary_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score salary range alignment"""
        # TODO: Implement salary matching
        return 85.0
    
    def _score_experience_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score experience level match"""
        # TODO: Implement experience matching
        return 88.0
    
    def _score_company_match(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score company preferences"""
        # TODO: Implement company matching
        return 70.0
    
    def _score_requirements_met(self, job: Dict[str, Any], profile: UserProfile) -> float:
        """Score requirements fulfillment"""
        # TODO: Check education, certifications, etc.
        return 95.0
    
    def _generate_explanation(self, scores: Dict[str, float], overall: float) -> str:
        """Generate human-readable match explanation"""
        if overall >= 90:
            return "Excellent match! Highly recommended to apply."
        elif overall >= 75:
            return "Strong match with good alignment on key criteria."
        elif overall >= 60:
            return "Good match, but some gaps in requirements."
        else:
            return "Moderate match, consider if expanding search."
