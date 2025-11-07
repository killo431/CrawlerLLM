"""AI detection scoring module (Application Stealth Score)."""
import re
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from core.logger import setup_logger

logger = setup_logger("stealth_scorer")


@dataclass
class StealthScore:
    """Stealth score result."""
    score: float  # 0-100, where 0 is undetectable and 100 is obviously AI
    risk_level: str  # "Safe", "Medium Risk", "High Risk", "Very High Risk"
    issues: List[str]  # List of detected issues
    suggestions: List[str]  # List of improvement suggestions
    
    def is_safe(self) -> bool:
        """Check if the score is below safe threshold (<20%)."""
        return self.score < 20


class StealthScorer:
    """
    AI detection scorer for application documents.
    
    Based on "The Detection Arms Race" research, this analyzes:
    1. Perplexity (text predictability)
    2. Burstiness (sentence length variation)
    3. Stylometric markers (AI-fingerprint words)
    
    Thresholds:
    - 0-20%: Safe (Low Risk)
    - 20-50%: Medium Risk
    - 50-80%: High Risk
    - 80-100%: Very High Risk
    """
    
    # AI-fingerprint words from the research paper
    AI_FINGERPRINT_WORDS = [
        "delve", "leverage", "embrace", "harness", "navigate", "landscape",
        "dive deep", "cutting-edge", "cutting edge", "robust", "holistic",
        "paradigm", "synergy", "utilize", "facilitate", "endeavor",
        "seamlessly", "transformative", "innovative", "revolutionary",
        "game-changing", "state-of-the-art", "best-in-class", "world-class"
    ]
    
    def __init__(self):
        """Initialize the stealth scorer."""
        logger.info("Initialized Stealth Scorer")
    
    def score_text(self, text: str) -> StealthScore:
        """
        Calculate stealth score for given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            StealthScore object with score and analysis
        """
        issues = []
        suggestions = []
        scores = []
        
        # Check 1: AI-fingerprint words
        fingerprint_score, fp_issues, fp_suggestions = self._check_fingerprint_words(text)
        scores.append(fingerprint_score)
        issues.extend(fp_issues)
        suggestions.extend(fp_suggestions)
        
        # Check 2: Burstiness (sentence length variation)
        burstiness_score, b_issues, b_suggestions = self._check_burstiness(text)
        scores.append(burstiness_score)
        issues.extend(b_issues)
        suggestions.extend(b_suggestions)
        
        # Check 3: Perplexity indicators (repetitive patterns)
        perplexity_score, p_issues, p_suggestions = self._check_perplexity(text)
        scores.append(perplexity_score)
        issues.extend(p_issues)
        suggestions.extend(p_suggestions)
        
        # Check 4: Grammatical perfection (too perfect is suspicious)
        grammar_score, g_issues, g_suggestions = self._check_grammar_perfection(text)
        scores.append(grammar_score)
        issues.extend(g_issues)
        suggestions.extend(g_suggestions)
        
        # Calculate overall score (weighted average)
        overall_score = sum(scores) / len(scores)
        
        # Determine risk level
        if overall_score < 20:
            risk_level = "Safe"
        elif overall_score < 50:
            risk_level = "Medium Risk"
        elif overall_score < 80:
            risk_level = "High Risk"
        else:
            risk_level = "Very High Risk"
        
        logger.info(f"Stealth score calculated: {overall_score:.1f}% ({risk_level})")
        
        return StealthScore(
            score=overall_score,
            risk_level=risk_level,
            issues=issues,
            suggestions=suggestions
        )
    
    def _check_fingerprint_words(self, text: str) -> Tuple[float, List[str], List[str]]:
        """Check for AI-fingerprint words."""
        text_lower = text.lower()
        found_words = []
        
        for word in self.AI_FINGERPRINT_WORDS:
            if word in text_lower:
                found_words.append(word)
        
        # Score based on frequency
        word_count = len(text.split())
        fingerprint_ratio = len(found_words) / max(word_count / 100, 1)  # Per 100 words
        score = min(fingerprint_ratio * 30, 100)  # Max 100
        
        issues = []
        suggestions = []
        
        if found_words:
            issues.append(f"Found {len(found_words)} AI-fingerprint words: {', '.join(found_words[:5])}")
            suggestions.append("Replace AI-fingerprint words with more natural alternatives")
            
            # Provide specific replacements
            replacements = {
                "leverage": "use",
                "delve": "explore",
                "embrace": "adopt",
                "harness": "use",
                "robust": "strong/reliable",
                "utilize": "use",
                "facilitate": "help/enable"
            }
            
            for word in found_words[:3]:
                if word in replacements:
                    suggestions.append(f"Replace '{word}' with '{replacements[word]}'")
        
        return score, issues, suggestions
    
    def _check_burstiness(self, text: str) -> Tuple[float, List[str], List[str]]:
        """Check sentence length variation (burstiness)."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return 0, [], []
        
        # Calculate sentence lengths
        lengths = [len(s.split()) for s in sentences]
        
        # Calculate coefficient of variation (std dev / mean)
        mean_length = sum(lengths) / len(lengths)
        variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
        std_dev = variance ** 0.5
        cv = std_dev / mean_length if mean_length > 0 else 0
        
        # Low CV indicates uniform sentences (AI-like)
        # Human writing typically has CV > 0.5
        issues = []
        suggestions = []
        
        if cv < 0.3:
            score = 40
            issues.append(f"Sentences are too uniform (variation: {cv:.2f})")
            suggestions.append("Vary sentence lengths dramatically - mix short punchy sentences with longer flowing ones")
        elif cv < 0.5:
            score = 20
            issues.append(f"Sentence variation could be improved (variation: {cv:.2f})")
            suggestions.append("Add more variety to sentence lengths")
        else:
            score = 0
        
        return score, issues, suggestions
    
    def _check_perplexity(self, text: str) -> Tuple[float, List[str], List[str]]:
        """Check for low perplexity indicators (repetitive patterns)."""
        issues = []
        suggestions = []
        score = 0
        
        # Check for repetitive sentence starters
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) >= 3:
            starters = [s.split()[0].lower() if s.split() else "" for s in sentences]
            unique_starters = len(set(starters))
            repetition_ratio = 1 - (unique_starters / len(starters))
            
            if repetition_ratio > 0.5:
                score += 30
                issues.append("Many sentences start with the same words")
                suggestions.append("Vary your sentence beginnings")
        
        # Check for repetitive phrases
        words = text.lower().split()
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
        
        # Count repeated bigrams/trigrams
        repeated_bigrams = len(bigrams) - len(set(bigrams))
        repeated_trigrams = len(trigrams) - len(set(trigrams))
        
        if repeated_trigrams > 2:
            score += 20
            issues.append("Repeated phrases detected")
            suggestions.append("Use more varied expressions and avoid repeating phrases")
        
        return score, issues, suggestions
    
    def _check_grammar_perfection(self, text: str) -> Tuple[float, List[str], List[str]]:
        """Check if text is too grammatically perfect (AI indicator)."""
        issues = []
        suggestions = []
        score = 0
        
        # Check for contractions (human writing often has them)
        contractions = ["don't", "can't", "won't", "it's", "i'm", "you're", "isn't", "aren't"]
        has_contractions = any(c in text.lower() for c in contractions)
        
        # Check for informal markers
        informal_markers = [
            " I ", " I've ", " I'd ", " really ", " just ", " actually ",
            " basically ", " honestly ", " truly "
        ]
        has_informal = any(m in text for m in informal_markers)
        
        # Perfectly formal with no contractions is suspicious for cover letters
        if not has_contractions and not has_informal and len(text.split()) > 100:
            score = 25
            issues.append("Text is too formally perfect")
            suggestions.append("Consider adding natural contractions (it's, don't) for authenticity")
        
        # Check for overly long paragraphs (AI often generates these)
        paragraphs = text.split('\n\n')
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 100]
        
        if len(long_paragraphs) > len(paragraphs) * 0.6:
            score += 15
            issues.append("Paragraphs are consistently long")
            suggestions.append("Break up long paragraphs for more natural flow")
        
        return score, issues, suggestions
    
    def generate_polish_recommendations(self, text: str, score: StealthScore) -> Dict[str, Any]:
        """
        Generate specific polish recommendations for Authenticity Wizard.
        
        Args:
            text: Original text
            score: Current stealth score
            
        Returns:
            Dictionary with step-by-step recommendations
        """
        recommendations = {
            "current_score": score.score,
            "target_score": 15,  # Target <20% for safe
            "steps": []
        }
        
        # Step 1: Fix AI-fingerprint words
        fingerprint_words = [
            word for word in self.AI_FINGERPRINT_WORDS 
            if word in text.lower()
        ]
        
        if fingerprint_words:
            recommendations["steps"].append({
                "step": "Fix Stylometry",
                "issue": f"Found AI-fingerprint words: {', '.join(fingerprint_words[:3])}",
                "action": "Replace these words with more natural alternatives",
                "words_to_replace": fingerprint_words[:5]
            })
        
        # Step 2: Fix burstiness
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) >= 3:
            lengths = [len(s.split()) for s in sentences]
            mean_length = sum(lengths) / len(lengths)
            std_dev = (sum((x - mean_length) ** 2 for x in lengths) / len(lengths)) ** 0.5
            cv = std_dev / mean_length if mean_length > 0 else 0
            
            if cv < 0.5:
                recommendations["steps"].append({
                    "step": "Fix Burstiness",
                    "issue": "Sentences are too uniform in length",
                    "action": "Vary sentence lengths - make some very short, others longer",
                    "example_section": sentences[0] if sentences else ""
                })
        
        # Step 3: Add personal touches
        if "I" not in text or "my" not in text.lower():
            recommendations["steps"].append({
                "step": "Fix Perplexity",
                "issue": "Text lacks personal anecdotes",
                "action": "Add a brief personal story or specific example from your experience"
            })
        
        return recommendations


# Convenience function
def score_application_document(text: str) -> StealthScore:
    """
    Quick function to score a document.
    
    Args:
        text: Document text to score
        
    Returns:
        StealthScore object
    """
    scorer = StealthScorer()
    return scorer.score_text(text)
