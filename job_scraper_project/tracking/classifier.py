"""
Email Classifier - Classifies job application response emails
"""

from typing import Dict, Any
from enum import Enum


class EmailClassification(Enum):
    """Email classification types"""
    REJECTION = "rejection"
    INTERVIEW = "interview"
    OFFER = "offer"
    UPDATE = "update"
    UNKNOWN = "unknown"


class EmailClassifier:
    """
    Classifies job application response emails using keyword matching
    and optional LLM fallback for complex cases.
    """
    
    # Keyword patterns for classification
    REJECTION_KEYWORDS = [
        'unfortunately', 'not moving forward', 'other candidates',
        'not selected', 'position has been filled', 'pursuing other',
        'decided to move forward with', 'not the right fit'
    ]
    
    INTERVIEW_KEYWORDS = [
        'schedule', 'interview', 'speak with you', 'next steps',
        'phone screen', 'video call', 'meet with', 'available to talk',
        'discuss your application', 'conversation', 'screening call'
    ]
    
    OFFER_KEYWORDS = [
        'pleased to offer', 'offer letter', 'congratulations',
        'welcome to', 'job offer', 'extend an offer', 'offer of employment',
        'accept this position', 'joining our team'
    ]
    
    def classify(
        self,
        email_subject: str,
        email_body: str,
        sender: str = ""
    ) -> Dict[str, Any]:
        """
        Classify an email message
        
        Args:
            email_subject: Email subject line
            email_body: Email body text
            sender: Sender email address
            
        Returns:
            Classification result with type and confidence
        """
        text = f"{email_subject} {email_body}".lower()
        
        # Check for rejection patterns
        rejection_score = self._count_keywords(text, self.REJECTION_KEYWORDS)
        
        # Check for interview patterns
        interview_score = self._count_keywords(text, self.INTERVIEW_KEYWORDS)
        
        # Check for offer patterns
        offer_score = self._count_keywords(text, self.OFFER_KEYWORDS)
        
        # Determine classification
        max_score = max(rejection_score, interview_score, offer_score)
        
        if max_score == 0:
            classification = EmailClassification.UNKNOWN
            confidence = 0.0
        elif rejection_score == max_score:
            classification = EmailClassification.REJECTION
            confidence = min(rejection_score * 0.3, 0.95)
        elif interview_score == max_score:
            classification = EmailClassification.INTERVIEW
            confidence = min(interview_score * 0.3, 0.95)
        elif offer_score == max_score:
            classification = EmailClassification.OFFER
            confidence = min(offer_score * 0.3, 0.95)
        else:
            classification = EmailClassification.UNKNOWN
            confidence = 0.0
        
        return {
            'classification': classification,
            'confidence': confidence,
            'scores': {
                'rejection': rejection_score,
                'interview': interview_score,
                'offer': offer_score
            }
        }
    
    def _count_keywords(self, text: str, keywords: list) -> int:
        """Count how many keywords appear in text"""
        return sum(1 for keyword in keywords if keyword in text)
    
    async def classify_with_llm(
        self,
        email_subject: str,
        email_body: str
    ) -> Dict[str, Any]:
        """
        Classify email using LLM for complex cases
        
        Args:
            email_subject: Email subject
            email_body: Email body
            
        Returns:
            Classification result with high confidence
        """
        # TODO: Implement LLM-based classification
        # - Use GPT-4 or similar
        # - Provide classification prompt
        # - Parse response
        return {
            'classification': EmailClassification.UNKNOWN,
            'confidence': 0.0
        }
