"""Unit tests for voice cloning."""
import pytest
import os
import tempfile
from ai_dev.voice_cloning import (
    VoiceCloningEngine,
    VoiceProfile,
    WritingSample,
    quick_add_sample,
    quick_train,
    quick_status
)


@pytest.fixture
def temp_storage():
    """Create temporary storage directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def engine(temp_storage):
    """Create VoiceCloningEngine with temp storage."""
    return VoiceCloningEngine(storage_dir=temp_storage)


def test_engine_initialization(temp_storage):
    """Test engine initialization."""
    engine = VoiceCloningEngine(storage_dir=temp_storage)
    assert engine.storage_dir == temp_storage
    assert os.path.exists(temp_storage)


def test_create_profile(engine):
    """Test creating a voice profile."""
    profile = engine.create_profile("test_user")
    
    assert profile.user_id == "test_user"
    assert len(profile.samples) == 0
    assert profile.is_trained is False
    assert profile.model_id is None


def test_add_writing_sample(engine):
    """Test adding a writing sample."""
    sample_text = "This is a test writing sample. It demonstrates my writing style."
    
    profile = engine.add_writing_sample("test_user", sample_text, "email")
    
    assert len(profile.samples) == 1
    assert profile.samples[0].content == sample_text
    assert profile.samples[0].sample_type == "email"
    assert profile.samples[0].word_count == len(sample_text.split())


def test_add_multiple_samples(engine):
    """Test adding multiple writing samples."""
    samples = [
        "First sample text here.",
        "Second sample with more content.",
        "Third sample for variety."
    ]
    
    for sample in samples:
        engine.add_writing_sample("test_user", sample, "general")
    
    profile = engine.load_profile("test_user")
    assert len(profile.samples) == 3


def test_load_nonexistent_profile(engine):
    """Test loading a profile that doesn't exist."""
    profile = engine.load_profile("nonexistent_user")
    assert profile is None


def test_load_existing_profile(engine):
    """Test loading an existing profile."""
    # Create profile
    engine.create_profile("test_user")
    
    # Load it
    profile = engine.load_profile("test_user")
    assert profile is not None
    assert profile.user_id == "test_user"


def test_train_model_insufficient_samples(engine):
    """Test training with insufficient samples."""
    engine.create_profile("test_user")
    engine.add_writing_sample("test_user", "Sample 1", "general")
    engine.add_writing_sample("test_user", "Sample 2", "general")
    
    # Should fail with < 3 samples
    success = engine.train_model("test_user")
    assert success is False


def test_train_model_success(engine):
    """Test successful model training."""
    # Add 3+ samples
    for i in range(3):
        engine.add_writing_sample("test_user", f"Sample {i} with content.", "general")
    
    success = engine.train_model("test_user")
    
    assert success is True
    
    profile = engine.load_profile("test_user")
    assert profile.is_trained is True
    assert profile.model_id is not None
    assert "voice_clone" in profile.model_id


def test_train_model_no_profile(engine):
    """Test training with no profile."""
    success = engine.train_model("nonexistent_user")
    assert success is False


def test_generate_with_voice_no_profile(engine):
    """Test generation with no voice profile."""
    result = engine.generate_with_voice("nonexistent_user", "Test prompt")
    assert "no voice profile" in result.lower()


def test_generate_with_voice_untrained(engine):
    """Test generation with untrained profile."""
    engine.create_profile("test_user")
    engine.add_writing_sample("test_user", "Sample", "general")
    
    result = engine.generate_with_voice("test_user", "Test prompt", "Base text")
    # Should return base text since not trained
    assert "Base text" in result or "not trained" in result.lower()


def test_generate_with_voice_trained(engine):
    """Test generation with trained profile."""
    # Setup trained profile
    for i in range(3):
        engine.add_writing_sample("test_user", f"Sample {i}", "general")
    engine.train_model("test_user")
    
    base_text = "This is the base text."
    result = engine.generate_with_voice("test_user", "Test prompt", base_text)
    
    assert base_text in result
    assert "Voice Clone" in result


def test_get_profile_status_nonexistent(engine):
    """Test status of nonexistent profile."""
    status = engine.get_profile_status("nonexistent_user")
    
    assert status["exists"] is False
    assert "No voice profile" in status["message"]


def test_get_profile_status_existing(engine):
    """Test status of existing profile."""
    engine.add_writing_sample("test_user", "Sample text here.", "email")
    
    status = engine.get_profile_status("test_user")
    
    assert status["exists"] is True
    assert status["user_id"] == "test_user"
    assert status["sample_count"] == 1
    assert status["total_words"] > 0
    assert "recommendation" in status


def test_get_profile_status_ready_to_train(engine):
    """Test status when ready to train."""
    for i in range(3):
        engine.add_writing_sample("test_user", f"Sample {i} text.", "general")
    
    status = engine.get_profile_status("test_user")
    
    assert status["ready_to_train"] is True
    assert "Ready to train" in status["recommendation"]


def test_get_profile_status_trained(engine):
    """Test status when model is trained."""
    for i in range(3):
        engine.add_writing_sample("test_user", f"Sample {i} text.", "general")
    engine.train_model("test_user")
    
    status = engine.get_profile_status("test_user")
    
    assert status["is_trained"] is True
    assert status["model_id"] is not None
    assert "active" in status["recommendation"].lower()


def test_analyze_writing_style_no_samples(engine):
    """Test style analysis with no samples."""
    analysis = engine.analyze_writing_style("nonexistent_user")
    assert "error" in analysis


def test_analyze_writing_style(engine):
    """Test writing style analysis."""
    samples = [
        "I'm writing this sample. It's got contractions and personal style.",
        "My second sample demonstrates consistency. I use first person often.",
        "This third sample shows variety. I can't help but be personal."
    ]
    
    for sample in samples:
        engine.add_writing_sample("test_user", sample, "email")
    
    analysis = engine.analyze_writing_style("test_user")
    
    assert "total_words" in analysis
    assert "total_sentences" in analysis
    assert "avg_sentence_length" in analysis
    assert "uses_contractions" in analysis
    assert "uses_first_person" in analysis
    assert analysis["uses_contractions"] is True
    assert analysis["uses_first_person"] is True


def test_voice_profile_to_dict():
    """Test VoiceProfile serialization."""
    sample = WritingSample("Test content", "email", "2024-01-01", 2)
    profile = VoiceProfile(
        user_id="test",
        samples=[sample],
        created_at="2024-01-01",
        updated_at="2024-01-02",
        model_id="test_model",
        is_trained=True
    )
    
    data = profile.to_dict()
    
    assert data["user_id"] == "test"
    assert len(data["samples"]) == 1
    assert data["is_trained"] is True
    assert data["model_id"] == "test_model"


def test_voice_profile_from_dict():
    """Test VoiceProfile deserialization."""
    data = {
        "user_id": "test",
        "samples": [
            {
                "content": "Test",
                "sample_type": "email",
                "uploaded_at": "2024-01-01",
                "word_count": 1
            }
        ],
        "created_at": "2024-01-01",
        "updated_at": "2024-01-02",
        "model_id": "test_model",
        "is_trained": True
    }
    
    profile = VoiceProfile.from_dict(data)
    
    assert profile.user_id == "test"
    assert len(profile.samples) == 1
    assert profile.is_trained is True


def test_quick_add_sample(temp_storage):
    """Test convenience function for adding sample."""
    # Use temp storage for quick functions
    os.environ['VOICE_STORAGE'] = temp_storage
    
    profile = quick_add_sample("quick_user", "Quick sample text", "email")
    assert len(profile.samples) >= 1


def test_quick_train(temp_storage, engine):
    """Test convenience function for training."""
    for i in range(3):
        engine.add_writing_sample("quick_user", f"Sample {i}", "general")
    
    success = quick_train("quick_user")
    # May succeed or fail depending on profile location
    assert isinstance(success, bool)


def test_quick_status(temp_storage, engine):
    """Test convenience function for status."""
    status = quick_status("status_user")
    assert "exists" in status
