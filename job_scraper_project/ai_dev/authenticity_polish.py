"""Authenticity Polish wizard for guided manual editing."""
import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from core.logger import setup_logger

logger = setup_logger("authenticity_polish")


@dataclass
class PolishSuggestion:
    """A single polish suggestion."""
    step_name: str  # "Fix Burstiness", "Fix Perplexity", "Fix Stylometry"
    issue: str
    suggestion: str
    target_text: Optional[str] = None  # Specific text to highlight/replace
    replacement: Optional[str] = None  # Suggested replacement


class AuthenticityPolishWizard:
    """
    Guided manual editing wizard for authenticity polish.
    
    Based on "The Detection Arms Race" research:
    "Manual post-editing is the only universally foolproof method."
    
    This wizard guides users through 3 steps:
    1. Fix Burstiness - Vary sentence lengths
    2. Fix Perplexity - Add personal touches
    3. Fix Stylometry - Remove AI-fingerprint words
    """
    
    # AI-fingerprint words with suggested replacements
    FINGERPRINT_REPLACEMENTS = {
        "leverage": ["use", "apply", "utilize"],
        "delve": ["explore", "examine", "look into"],
        "embrace": ["adopt", "accept", "welcome"],
        "harness": ["use", "tap into", "employ"],
        "navigate": ["handle", "manage", "deal with"],
        "landscape": ["environment", "field", "space"],
        "robust": ["strong", "reliable", "solid"],
        "holistic": ["complete", "comprehensive", "full"],
        "paradigm": ["model", "approach", "framework"],
        "synergy": ["collaboration", "teamwork", "cooperation"],
        "utilize": ["use", "employ", "apply"],
        "facilitate": ["help", "enable", "support"],
        "endeavor": ["effort", "project", "work"],
        "seamlessly": ["smoothly", "easily", "naturally"],
        "transformative": ["significant", "major", "important"],
        "innovative": ["new", "creative", "novel"],
        "cutting-edge": ["advanced", "modern", "latest"],
        "state-of-the-art": ["advanced", "modern", "current"],
        "game-changing": ["important", "significant", "major"],
        "revolutionary": ["groundbreaking", "major", "significant"]
    }
    
    def __init__(self):
        """Initialize the Authenticity Polish Wizard."""
        logger.info("Initialized Authenticity Polish Wizard")
    
    def analyze_and_suggest(self, text: str) -> List[PolishSuggestion]:
        """
        Analyze text and generate polish suggestions.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of PolishSuggestion objects
        """
        suggestions = []
        
        # Step 1: Fix Burstiness
        burstiness_suggestions = self._suggest_burstiness_fixes(text)
        suggestions.extend(burstiness_suggestions)
        
        # Step 2: Fix Perplexity
        perplexity_suggestions = self._suggest_perplexity_fixes(text)
        suggestions.extend(perplexity_suggestions)
        
        # Step 3: Fix Stylometry
        stylometry_suggestions = self._suggest_stylometry_fixes(text)
        suggestions.extend(stylometry_suggestions)
        
        logger.info(f"Generated {len(suggestions)} polish suggestions")
        return suggestions
    
    def _suggest_burstiness_fixes(self, text: str) -> List[PolishSuggestion]:
        """Suggest fixes for burstiness (sentence length variation)."""
        suggestions = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return suggestions
        
        # Calculate sentence lengths
        lengths = [len(s.split()) for s in sentences]
        mean_length = sum(lengths) / len(lengths)
        
        # Find consecutive sentences of similar length
        for i in range(len(sentences) - 2):
            len1, len2, len3 = lengths[i], lengths[i+1], lengths[i+2]
            
            # If three consecutive sentences are similar length
            if abs(len1 - mean_length) < 3 and abs(len2 - mean_length) < 3 and abs(len3 - mean_length) < 3:
                target_text = f"{sentences[i]}. {sentences[i+1]}. {sentences[i+2]}"
                
                suggestions.append(PolishSuggestion(
                    step_name="Fix Burstiness",
                    issue="Three consecutive sentences have similar length",
                    suggestion="Vary the rhythm: Make the first sentence shorter (cut unnecessary words) and combine the last two sentences into one longer, flowing sentence.",
                    target_text=target_text
                ))
                break  # Only suggest once
        
        # If no consecutive similar-length found, but overall low variation
        if not suggestions:
            std_dev = (sum((x - mean_length) ** 2 for x in lengths) / len(lengths)) ** 0.5
            cv = std_dev / mean_length if mean_length > 0 else 0
            
            if cv < 0.4:
                # Find a medium-length sentence to split
                for i, (sentence, length) in enumerate(zip(sentences, lengths)):
                    if length > mean_length * 1.2 and ',' in sentence:
                        suggestions.append(PolishSuggestion(
                            step_name="Fix Burstiness",
                            issue="Sentences are too uniform in length",
                            suggestion="Break this longer sentence into two shorter ones at the comma for better rhythm.",
                            target_text=sentence
                        ))
                        break
        
        return suggestions
    
    def _suggest_perplexity_fixes(self, text: str) -> List[PolishSuggestion]:
        """Suggest fixes for perplexity (add personal touches)."""
        suggestions = []
        
        # Check for lack of personal pronouns
        personal_markers = ['I ', 'my ', 'My ', "I've ", "I'd ", "I'm "]
        has_personal = any(marker in text for marker in personal_markers)
        
        if not has_personal:
            suggestions.append(PolishSuggestion(
                step_name="Fix Perplexity",
                issue="Text lacks personal voice",
                suggestion="Add a brief personal anecdote or specific example from your experience. Start a sentence with 'I' or 'In my experience' to make it more authentic.",
                target_text=None
            ))
        
        # Check for generic claims that could use examples
        generic_phrases = [
            "extensive experience",
            "proven track record",
            "strong background",
            "highly skilled",
            "excellent communication"
        ]
        
        for phrase in generic_phrases:
            if phrase.lower() in text.lower():
                # Find the sentence containing this phrase
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    if phrase.lower() in sentence.lower():
                        suggestions.append(PolishSuggestion(
                            step_name="Fix Perplexity",
                            issue=f"Generic claim: '{phrase}'",
                            suggestion=f"This sounds robotic. Add a concrete example: What specific project or achievement demonstrates this? Use real numbers or details.",
                            target_text=sentence.strip()
                        ))
                        break
                break  # Only one perplexity fix at a time
        
        # Check for repetitive sentence starters
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) >= 3:
            starters = [s.split()[0] if s.split() else "" for s in sentences]
            starter_counts = {}
            for starter in starters:
                starter_counts[starter] = starter_counts.get(starter, 0) + 1
            
            for starter, count in starter_counts.items():
                if count >= 3 and starter:
                    suggestions.append(PolishSuggestion(
                        step_name="Fix Perplexity",
                        issue=f"Multiple sentences start with '{starter}'",
                        suggestion=f"Vary your sentence beginnings. Try starting some sentences differently to create more natural flow.",
                        target_text=None
                    ))
                    break
        
        return suggestions
    
    def _suggest_stylometry_fixes(self, text: str) -> List[PolishSuggestion]:
        """Suggest fixes for stylometry (AI-fingerprint words)."""
        suggestions = []
        
        text_lower = text.lower()
        
        # Find AI-fingerprint words
        found_words = []
        for word, replacements in self.FINGERPRINT_REPLACEMENTS.items():
            if word in text_lower:
                found_words.append((word, replacements))
        
        # Suggest replacements for first few words found
        for word, replacements in found_words[:3]:
            # Find the actual occurrence in text (with original case)
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            match = pattern.search(text)
            
            if match:
                original_word = match.group()
                replacement = replacements[0]
                
                # Try to match the case
                if original_word[0].isupper():
                    replacement = replacement.capitalize()
                
                suggestions.append(PolishSuggestion(
                    step_name="Fix Stylometry",
                    issue=f"AI-fingerprint word detected: '{original_word}'",
                    suggestion=f"Replace '{original_word}' with a more natural alternative like '{replacement}', '{replacements[1] if len(replacements) > 1 else replacement}', or '{replacements[2] if len(replacements) > 2 else replacement}'.",
                    target_text=original_word,
                    replacement=replacement
                ))
        
        # Check for overly formal tone (no contractions)
        contractions = ["don't", "can't", "won't", "it's", "i'm", "you're"]
        has_contractions = any(c in text_lower for c in contractions)
        
        if not has_contractions and len(text.split()) > 100:
            # Find potential contraction opportunities
            formal_phrases = {
                "do not": "don't",
                "cannot": "can't",
                "will not": "won't",
                "it is": "it's",
                "I am": "I'm",
                "you are": "you're"
            }
            
            for formal, contraction in formal_phrases.items():
                if formal in text:
                    suggestions.append(PolishSuggestion(
                        step_name="Fix Stylometry",
                        issue="Text is too formally perfect",
                        suggestion=f"Consider making the tone more natural. For example, change '{formal}' to '{contraction}' for authenticity.",
                        target_text=formal,
                        replacement=contraction
                    ))
                    break
        
        return suggestions
    
    def apply_suggestion(self, text: str, suggestion: PolishSuggestion, user_edit: str) -> str:
        """
        Apply a user's edit based on a suggestion.
        
        Args:
            text: Original text
            suggestion: The suggestion being applied
            user_edit: User's edited text
            
        Returns:
            Updated text
        """
        if suggestion.target_text and suggestion.target_text in text:
            # Replace the target text with user's edit
            updated = text.replace(suggestion.target_text, user_edit, 1)
            logger.info(f"Applied polish: {suggestion.step_name}")
            return updated
        
        # If no specific target, assume user is appending/modifying
        logger.info(f"Applied polish: {suggestion.step_name} (manual edit)")
        return user_edit
    
    def get_wizard_steps(self, text: str) -> List[Dict[str, Any]]:
        """
        Get wizard steps for UI display.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of step dictionaries for UI
        """
        suggestions = self.analyze_and_suggest(text)
        
        # Group by step name
        steps = {}
        for suggestion in suggestions:
            if suggestion.step_name not in steps:
                steps[suggestion.step_name] = []
            steps[suggestion.step_name].append({
                "issue": suggestion.issue,
                "suggestion": suggestion.suggestion,
                "target_text": suggestion.target_text,
                "replacement": suggestion.replacement
            })
        
        # Format for wizard
        wizard_steps = []
        
        step_order = ["Fix Burstiness", "Fix Perplexity", "Fix Stylometry"]
        step_descriptions = {
            "Fix Burstiness": "Let's vary the rhythm of your sentences",
            "Fix Perplexity": "Let's add a personal touch",
            "Fix Stylometry": "Let's remove common AI-fingerprint words"
        }
        
        for step_name in step_order:
            if step_name in steps:
                wizard_steps.append({
                    "step": step_name,
                    "description": step_descriptions[step_name],
                    "suggestions": steps[step_name]
                })
        
        return wizard_steps


# Convenience function
def quick_polish_analysis(text: str) -> List[Dict[str, Any]]:
    """Quick function to get polish suggestions."""
    wizard = AuthenticityPolishWizard()
    return wizard.get_wizard_steps(text)
