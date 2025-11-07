"""
Deal Breaker Checker - Fast filtering for disqualifying criteria
"""

from typing import Dict, Any


class DealBreakerChecker:
    """
    Checks for deal-breaker criteria that immediately disqualify a job.
    
    This is run before expensive matching calculations to quickly filter
    jobs that don't meet mandatory requirements.
    """
    
    def has_dealbreaker(self, job: Dict[str, Any], user_profile: Any) -> bool:
        """
        Check if job has any deal-breaker criteria
        
        Args:
            job: Job details
            user_profile: User profile with preferences
            
        Returns:
            True if job has deal-breaker, False otherwise
        """
        # Check location deal-breaker
        if self._check_location_dealbreaker(job, user_profile):
            return True
        
        # Check salary deal-breaker
        if self._check_salary_dealbreaker(job, user_profile):
            return True
        
        # Check blacklisted company
        if self._check_company_blacklist(job, user_profile):
            return True
        
        # Check other requirements
        if self._check_requirement_dealbreakers(job, user_profile):
            return True
        
        return False
    
    def _check_location_dealbreaker(self, job: Dict[str, Any], profile: Any) -> bool:
        """Check location compatibility"""
        if profile.only_remote:
            return not job.get('is_remote', False)
        return False
    
    def _check_salary_dealbreaker(self, job: Dict[str, Any], profile: Any) -> bool:
        """Check salary requirements"""
        if profile.minimum_salary > 0:
            job_max_salary = job.get('salary_max', 0)
            if job_max_salary > 0 and job_max_salary < profile.minimum_salary:
                return True
        return False
    
    def _check_company_blacklist(self, job: Dict[str, Any], profile: Any) -> bool:
        """Check if company is blacklisted"""
        company = job.get('company', '').lower()
        blacklist = [c.lower() for c in profile.blacklisted_companies]
        return company in blacklist
    
    def _check_requirement_dealbreakers(self, job: Dict[str, Any], profile: Any) -> bool:
        """Check other mandatory requirements"""
        # TODO: Check security clearance, work authorization, etc.
        return False
