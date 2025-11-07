"""Unit tests for text generation (Stealth Engine)."""
import pytest
from ai_dev.text_generator import (
    StealthEngine, 
    GenerationConfig, 
    generate_application_documents
)


def test_generation_config_defaults():
    """Test default generation configuration."""
    config = GenerationConfig()
    assert config.model == "gemini-2.5-pro"
    assert config.temperature == 0.7
    assert config.perplexity_level == "medium"
    assert config.burstiness_level == "dynamic"
    assert config.tone == "professional"
    assert config.add_imperfections is False


def test_stealth_engine_initialization():
    """Test Stealth Engine initialization."""
    engine = StealthEngine()
    assert engine.config.model == "gemini-2.5-pro"
    assert engine.model_info["detection_rate"] == 0.53


def test_stealth_engine_custom_config():
    """Test Stealth Engine with custom config."""
    config = GenerationConfig(
        model="gpt-4",
        perplexity_level="complex",
        burstiness_level="uniform",
        tone="casual",
        add_imperfections=True
    )
    engine = StealthEngine(config)
    assert engine.config.model == "gpt-4"
    assert engine.config.tone == "casual"
    assert engine.model_info["detection_rate"] == 0.95


def test_generate_resume():
    """Test resume generation."""
    engine = StealthEngine()
    
    user_profile = {
        "name": "Test User",
        "title": "Software Engineer",
        "experience": "5 years",
        "skills": ["Python", "JavaScript"],
        "education": "B.S. Computer Science"
    }
    
    resume = engine.generate_resume(user_profile)
    
    assert isinstance(resume, str)
    assert len(resume) > 0
    assert "Software Engineer" in resume or "EXPERIENCE" in resume


def test_generate_cover_letter():
    """Test cover letter generation."""
    engine = StealthEngine()
    
    user_profile = {
        "name": "Test User",
        "title": "Software Engineer",
        "experience": "5 years"
    }
    
    job_posting = {
        "title": "Senior Developer",
        "company": "TechCorp",
        "requirements": "5+ years experience"
    }
    
    cover_letter = engine.generate_cover_letter(user_profile, job_posting)
    
    assert isinstance(cover_letter, str)
    assert len(cover_letter) > 0


def test_stealth_prompt_building():
    """Test stealth prompt enhancement."""
    config = GenerationConfig(
        perplexity_level="complex",
        burstiness_level="dynamic",
        add_imperfections=True
    )
    
    engine = StealthEngine(config)
    base_prompt = "Create a resume"
    stealth_prompt = engine._build_stealth_prompt(base_prompt)
    
    assert "Create a resume" in stealth_prompt
    assert "Tone:" in stealth_prompt
    assert "AVOID these AI-fingerprint words" in stealth_prompt


def test_model_info():
    """Test getting model information."""
    engine = StealthEngine()
    info = engine.get_model_info()
    
    assert "model" in info
    assert "detection_rate" in info
    assert "config" in info
    assert info["model"] == "gemini-2.5-pro"
    assert info["detection_rate"] == 0.53


def test_generate_application_documents():
    """Test convenience function for generating both documents."""
    user_profile = {
        "name": "Test User",
        "title": "Developer",
        "experience": "3 years",
        "skills": ["Python"],
        "education": "Bachelor's"
    }
    
    job_posting = {
        "title": "Software Engineer",
        "company": "TestCorp",
        "requirements": "Python skills"
    }
    
    results = generate_application_documents(user_profile, job_posting)
    
    assert "resume" in results
    assert "cover_letter" in results
    assert "model_info" in results
    assert isinstance(results["resume"], str)
    assert isinstance(results["cover_letter"], str)


def test_supported_models():
    """Test all supported models are configured."""
    assert "gemini-2.5-pro" in StealthEngine.SUPPORTED_MODELS
    assert "claude-3.5-sonnet" in StealthEngine.SUPPORTED_MODELS
    assert "llama-3.1" in StealthEngine.SUPPORTED_MODELS
    assert "gpt-4" in StealthEngine.SUPPORTED_MODELS
    
    # Check detection rates
    assert StealthEngine.SUPPORTED_MODELS["gemini-2.5-pro"]["detection_rate"] == 0.53
    assert StealthEngine.SUPPORTED_MODELS["llama-3.1"]["detection_rate"] == 1.00


def test_perplexity_levels():
    """Test different perplexity levels produce different prompts."""
    base_prompt = "Write text"
    
    config_simple = GenerationConfig(perplexity_level="simple")
    engine_simple = StealthEngine(config_simple)
    prompt_simple = engine_simple._build_stealth_prompt(base_prompt)
    
    config_complex = GenerationConfig(perplexity_level="complex")
    engine_complex = StealthEngine(config_complex)
    prompt_complex = engine_complex._build_stealth_prompt(base_prompt)
    
    assert "simple language" in prompt_simple.lower()
    assert "sophisticated language" in prompt_complex.lower()
    assert prompt_simple != prompt_complex


def test_imperfections_toggle():
    """Test imperfections toggle affects prompt."""
    base_prompt = "Write text"
    
    config_no_imp = GenerationConfig(add_imperfections=False)
    engine_no_imp = StealthEngine(config_no_imp)
    prompt_no_imp = engine_no_imp._build_stealth_prompt(base_prompt)
    
    config_imp = GenerationConfig(add_imperfections=True)
    engine_imp = StealthEngine(config_imp)
    prompt_imp = engine_imp._build_stealth_prompt(base_prompt)
    
    assert "contraction" not in prompt_no_imp.lower()
    assert "contraction" in prompt_imp.lower()
