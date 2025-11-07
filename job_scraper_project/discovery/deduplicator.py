"""
Job Deduplicator - Detects and removes duplicate job listings
"""

import hashlib
from typing import List, Dict, Any, Set


class JobDeduplicator:
    """
    Deduplicates job listings across multiple sources.
    
    Uses fingerprinting and fuzzy matching to identify duplicate
    jobs even when posted on different platforms.
    """
    
    def __init__(self):
        """Initialize deduplicator"""
        self.seen_fingerprints: Set[str] = set()
    
    def generate_fingerprint(self, job: Dict[str, Any]) -> str:
        """
        Generate unique fingerprint for a job
        
        Args:
            job: Job details
            
        Returns:
            Fingerprint hash
        """
        # Normalize data
        company = job.get('company', '').lower().strip()
        title = job.get('title', '').lower().strip()
        location = self._normalize_location(job.get('location', ''))
        
        # Create fingerprint
        fingerprint_str = f"{company}:{title}:{location}"
        
        # Hash for storage
        return hashlib.md5(fingerprint_str.encode()).hexdigest()
    
    def is_duplicate(
        self,
        job: Dict[str, Any],
        existing_jobs: List[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if job is a duplicate
        
        Args:
            job: Job to check
            existing_jobs: Optional list of existing jobs to check against
            
        Returns:
            True if duplicate, False if unique
        """
        # Check fingerprint
        fingerprint = self.generate_fingerprint(job)
        
        if fingerprint in self.seen_fingerprints:
            return True
        
        # Check against existing jobs with fuzzy matching
        if existing_jobs:
            for existing in existing_jobs:
                if self._calculate_similarity(job, existing) > 0.9:
                    return True
        
        return False
    
    def add_job(self, job: Dict[str, Any]) -> str:
        """
        Add job to seen set
        
        Args:
            job: Job to add
            
        Returns:
            Job fingerprint
        """
        fingerprint = self.generate_fingerprint(job)
        self.seen_fingerprints.add(fingerprint)
        return fingerprint
    
    def deduplicate_batch(
        self,
        jobs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Deduplicate a batch of jobs
        
        Args:
            jobs: List of jobs to deduplicate
            
        Returns:
            List of unique jobs
        """
        unique_jobs = []
        
        for job in jobs:
            if not self.is_duplicate(job, unique_jobs):
                unique_jobs.append(job)
                self.add_job(job)
        
        return unique_jobs
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location string"""
        return location.lower().strip().replace(',', '').replace('.', '')
    
    def _calculate_similarity(
        self,
        job1: Dict[str, Any],
        job2: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between two jobs
        
        Args:
            job1: First job
            job2: Second job
            
        Returns:
            Similarity score (0-1)
        """
        # TODO: Implement Levenshtein distance or similar
        # For now, simple comparison
        if (job1.get('company') == job2.get('company') and
            job1.get('title') == job2.get('title')):
            return 1.0
        return 0.0
