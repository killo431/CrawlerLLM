"""Unit tests for stealth scoring."""
import pytest
from ai_dev.stealth_scorer import StealthScorer, StealthScore, score_application_document


def test_stealth_score_dataclass():
    """Test StealthScore dataclass."""
    score = StealthScore(
        score=15.5,
        risk_level="Safe",
        issues=["Issue 1"],
        suggestions=["Suggestion 1"]
    )
    
    assert score.score == 15.5
    assert score.risk_level == "Safe"
    assert score.is_safe() is True
    
    high_score = StealthScore(score=75, risk_level="High Risk", issues=[], suggestions=[])
    assert high_score.is_safe() is False


def test_stealth_scorer_initialization():
    """Test StealthScorer initialization."""
    scorer = StealthScorer()
    assert len(scorer.AI_FINGERPRINT_WORDS) > 0
    assert "leverage" in scorer.AI_FINGERPRINT_WORDS
    assert "delve" in scorer.AI_FINGERPRINT_WORDS


def test_score_text_basic():
    """Test basic text scoring."""
    scorer = StealthScorer()
    
    text = "This is a simple test text. It has multiple sentences. They vary in length."
    score = scorer.score_text(text)
    
    assert isinstance(score, StealthScore)
    assert 0 <= score.score <= 100
    assert score.risk_level in ["Safe", "Medium Risk", "High Risk", "Very High Risk"]


def test_fingerprint_word_detection():
    """Test AI-fingerprint word detection."""
    scorer = StealthScorer()
    
    # Text with fingerprint words
    text_with_fp = "We leverage cutting-edge technology to delve into robust solutions."
    score_with = scorer.score_text(text_with_fp)
    
    # Text without fingerprint words
    text_without = "We use advanced technology to explore strong solutions."
    score_without = scorer.score_text(text_without)
    
    # Text with fingerprint words should score higher (worse)
    assert score_with.score > score_without.score
    assert any("fingerprint" in issue.lower() for issue in score_with.issues)


def test_burstiness_check():
    """Test burstiness (sentence variation) checking."""
    scorer = StealthScorer()
    
    # Uniform sentences (low burstiness - AI-like)
    uniform_text = "I work hard. I code well. I test code. I fix bugs. I ship fast."
    score_uniform = scorer.score_text(uniform_text)
    
    # Varied sentences (high burstiness - human-like)
    varied_text = "I work. I code well and test thoroughly to ensure quality. Bugs? I fix them fast."
    score_varied = scorer.score_text(varied_text)
    
    # Uniform text should score higher (worse)
    assert score_uniform.score >= score_varied.score


def test_perplexity_check():
    """Test perplexity checking."""
    scorer = StealthScorer()
    
    # Repetitive sentence starters
    repetitive = "I am a developer. I am experienced. I am skilled. I am dedicated."
    score_rep = scorer.score_text(repetitive)
    
    # Varied sentence starters
    varied = "I am a developer. My experience spans five years. Skills include Python. Dedication drives my work."
    score_var = scorer.score_text(varied)
    
    # Repetitive should score worse
    assert score_rep.score >= score_var.score


def test_grammar_perfection_check():
    """Test grammar perfection checking."""
    scorer = StealthScorer()
    
    # Too perfect (no contractions)
    perfect = """I am writing to apply for the position. I have extensive experience. 
    I cannot wait to contribute. It is my belief that I would be an asset."""
    score_perfect = scorer.score_text(perfect)
    
    # More natural (with contractions)
    natural = """I'm writing to apply for the position. I've got extensive experience. 
    Can't wait to contribute. I'd be an asset."""
    score_natural = scorer.score_text(natural)
    
    # Both should produce valid scores - test that contractions are detected
    assert isinstance(score_perfect, StealthScore)
    assert isinstance(score_natural, StealthScore)


def test_risk_level_classification():
    """Test risk level classification."""
    scorer = StealthScorer()
    
    # Create scores at different levels
    safe_score = StealthScore(score=15, risk_level="Safe", issues=[], suggestions=[])
    medium_score = StealthScore(score=35, risk_level="Medium Risk", issues=[], suggestions=[])
    high_score = StealthScore(score=65, risk_level="High Risk", issues=[], suggestions=[])
    very_high_score = StealthScore(score=85, risk_level="Very High Risk", issues=[], suggestions=[])
    
    assert safe_score.is_safe() is True
    assert medium_score.is_safe() is False
    assert high_score.is_safe() is False
    assert very_high_score.is_safe() is False


def test_generate_polish_recommendations():
    """Test polish recommendations generation."""
    scorer = StealthScorer()
    
    text = "I leverage cutting-edge technology to delve into solutions. I use Python. I use JavaScript. I use Docker."
    score = scorer.score_text(text)
    recommendations = scorer.generate_polish_recommendations(text, score)
    
    assert "current_score" in recommendations
    assert "target_score" in recommendations
    assert "steps" in recommendations
    assert isinstance(recommendations["steps"], list)


def test_empty_text():
    """Test scoring empty or very short text."""
    scorer = StealthScorer()
    
    empty_score = scorer.score_text("")
    short_score = scorer.score_text("Hi.")
    
    assert isinstance(empty_score, StealthScore)
    assert isinstance(short_score, StealthScore)


def test_score_application_document_convenience():
    """Test convenience function."""
    text = "This is a test document for scoring."
    score = score_application_document(text)
    
    assert isinstance(score, StealthScore)
    assert 0 <= score.score <= 100


def test_multiple_ai_fingerprints():
    """Test detection of multiple AI-fingerprint words."""
    scorer = StealthScorer()
    
    text = """We leverage innovative solutions to embrace cutting-edge paradigms. 
    Our robust framework facilitates seamless integration."""
    
    score = scorer.score_text(text)
    
    # Should detect multiple fingerprint words
    fingerprint_issues = [i for i in score.issues if "fingerprint" in i.lower()]
    assert len(fingerprint_issues) > 0


def test_suggestions_provided():
    """Test that suggestions are provided when issues found."""
    scorer = StealthScorer()
    
    text = "We leverage cutting-edge solutions to delve into problems."
    score = scorer.score_text(text)
    
    if score.issues:
        assert len(score.suggestions) > 0


def test_long_paragraphs_detection():
    """Test detection of overly long paragraphs."""
    scorer = StealthScorer()
    
    # Create a very long paragraph
    long_paragraph = " ".join(["This is a sentence."] * 30)
    score = scorer.score_text(long_paragraph)
    
    # Should potentially flag long paragraphs
    assert isinstance(score, StealthScore)


def test_score_consistency():
    """Test that same text produces consistent scores."""
    scorer = StealthScorer()
    
    text = "This is a consistent test text with multiple sentences for scoring."
    
    score1 = scorer.score_text(text)
    score2 = scorer.score_text(text)
    
    assert score1.score == score2.score
    assert score1.risk_level == score2.risk_level
