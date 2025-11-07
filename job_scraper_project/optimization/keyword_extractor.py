"""
Keyword Extractor - Extracts keywords from job descriptions
"""

from typing import List, Dict, Any
from collections import Counter


class KeywordExtractor:
    """
    Extracts important keywords and skills from job descriptions.
    
    Uses TF-IDF and NLP techniques to identify the most relevant
    keywords for ATS optimization.
    """
    
    def __init__(self):
        """Initialize keyword extractor"""
        # TODO: Initialize spaCy model
        # TODO: Initialize TF-IDF vectorizer
        pass
    
    def extract_keywords(
        self,
        job_description: str,
        max_keywords: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Extract top keywords from job description
        
        Args:
            job_description: Job description text
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keywords with scores
        """
        # TODO: Implement keyword extraction
        # - Tokenize text
        # - Remove stop words
        # - Calculate TF-IDF scores
        # - Extract top keywords
        
        return [
            {'keyword': 'python', 'score': 0.95},
            {'keyword': 'software engineer', 'score': 0.90},
            {'keyword': 'agile', 'score': 0.85}
        ]
    
    def extract_skills(self, job_description: str) -> List[str]:
        """
        Extract technical skills from job description
        
        Args:
            job_description: Job description text
            
        Returns:
            List of identified skills
        """
        # Common technical skills to look for
        common_skills = {
            'python', 'java', 'javascript', 'c++', 'sql', 'aws',
            'docker', 'kubernetes', 'react', 'node.js', 'git',
            'machine learning', 'data analysis', 'api', 'rest'
        }
        
        text_lower = job_description.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        
        return found_skills
    
    def calculate_keyword_density(
        self,
        resume_text: str,
        keywords: List[str]
    ) -> float:
        """
        Calculate keyword density in resume
        
        Args:
            resume_text: Resume text
            keywords: Keywords to check for
            
        Returns:
            Keyword density (0-1)
        """
        resume_lower = resume_text.lower()
        words = resume_lower.split()
        
        keyword_count = sum(1 for word in words if word in [k.lower() for k in keywords])
        
        if len(words) == 0:
            return 0.0
        
        return keyword_count / len(words)
    
    def get_missing_keywords(
        self,
        resume_text: str,
        job_keywords: List[str]
    ) -> List[str]:
        """
        Get keywords from job description that are missing in resume
        
        Args:
            resume_text: Resume text
            job_keywords: Keywords from job description
            
        Returns:
            List of missing keywords
        """
        resume_lower = resume_text.lower()
        
        missing = [kw for kw in job_keywords if kw.lower() not in resume_lower]
        
        return missing
