"""AI Voice Cloning module for personalized text generation."""
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from core.logger import setup_logger

logger = setup_logger("voice_cloning")


@dataclass
class WritingSample:
    """User's writing sample."""
    content: str
    sample_type: str  # "cover_letter", "email", "report", etc.
    uploaded_at: str
    word_count: int


@dataclass
class VoiceProfile:
    """User's voice profile for fine-tuning."""
    user_id: str
    samples: List[WritingSample]
    created_at: str
    updated_at: str
    model_id: Optional[str] = None  # ID of fine-tuned model
    is_trained: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "user_id": self.user_id,
            "samples": [asdict(s) for s in self.samples],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "model_id": self.model_id,
            "is_trained": self.is_trained
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceProfile":
        """Create from dictionary."""
        samples = [WritingSample(**s) for s in data.get("samples", [])]
        return cls(
            user_id=data["user_id"],
            samples=samples,
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            model_id=data.get("model_id"),
            is_trained=data.get("is_trained", False)
        )


class VoiceCloningEngine:
    """
    AI Voice Cloning Engine for personalized text generation.
    
    Based on "The Detection Arms Race" research:
    - Open-source models (Llama 3.1) are 100% detectable by default
    - Fine-tuning on user's writing creates unique fingerprint
    - Private fingerprints are undetectable by public detectors
    
    This module manages:
    1. Collection of user writing samples
    2. Profile creation and storage
    3. Fine-tuning orchestration (placeholder for actual implementation)
    4. Personalized text generation
    """
    
    def __init__(self, storage_dir: str = "data/voice_profiles"):
        """
        Initialize the Voice Cloning Engine.
        
        Args:
            storage_dir: Directory to store voice profiles
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        logger.info(f"Initialized Voice Cloning Engine (storage: {storage_dir})")
    
    def create_profile(self, user_id: str) -> VoiceProfile:
        """
        Create a new voice profile for a user.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            New VoiceProfile
        """
        profile = VoiceProfile(
            user_id=user_id,
            samples=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self._save_profile(profile)
        logger.info(f"Created voice profile for user: {user_id}")
        
        return profile
    
    def add_writing_sample(
        self, 
        user_id: str, 
        content: str, 
        sample_type: str = "general"
    ) -> VoiceProfile:
        """
        Add a writing sample to user's profile.
        
        Args:
            user_id: User identifier
            content: Writing sample text
            sample_type: Type of sample (cover_letter, email, report, etc.)
            
        Returns:
            Updated VoiceProfile
        """
        profile = self.load_profile(user_id)
        
        if not profile:
            profile = self.create_profile(user_id)
        
        sample = WritingSample(
            content=content,
            sample_type=sample_type,
            uploaded_at=datetime.now().isoformat(),
            word_count=len(content.split())
        )
        
        profile.samples.append(sample)
        profile.updated_at = datetime.now().isoformat()
        profile.is_trained = False  # Need to retrain with new sample
        
        self._save_profile(profile)
        logger.info(f"Added writing sample for user {user_id} ({sample.word_count} words)")
        
        return profile
    
    def load_profile(self, user_id: str) -> Optional[VoiceProfile]:
        """
        Load a user's voice profile.
        
        Args:
            user_id: User identifier
            
        Returns:
            VoiceProfile if exists, None otherwise
        """
        profile_path = os.path.join(self.storage_dir, f"{user_id}.json")
        
        if not os.path.exists(profile_path):
            return None
        
        try:
            with open(profile_path, 'r') as f:
                data = json.load(f)
            
            profile = VoiceProfile.from_dict(data)
            logger.info(f"Loaded voice profile for user: {user_id}")
            return profile
            
        except Exception as e:
            logger.error(f"Failed to load profile for {user_id}: {e}")
            return None
    
    def _save_profile(self, profile: VoiceProfile) -> bool:
        """Save voice profile to disk."""
        profile_path = os.path.join(self.storage_dir, f"{profile.user_id}.json")
        
        try:
            with open(profile_path, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
            
            logger.info(f"Saved voice profile for user: {profile.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save profile for {profile.user_id}: {e}")
            return False
    
    def train_model(self, user_id: str) -> bool:
        """
        Train a personalized model for the user.
        
        This is a placeholder for actual fine-tuning implementation.
        In production, this would:
        1. Prepare training data from writing samples
        2. Call fine-tuning API (e.g., Llama, GPT-4)
        3. Store model ID
        4. Update profile
        
        Args:
            user_id: User identifier
            
        Returns:
            True if training successful
        """
        profile = self.load_profile(user_id)
        
        if not profile:
            logger.error(f"No profile found for user: {user_id}")
            return False
        
        if len(profile.samples) < 3:
            logger.warning(f"Need at least 3 samples to train. User {user_id} has {len(profile.samples)}")
            return False
        
        # Mock training process
        logger.info(f"Starting model training for user: {user_id}")
        logger.info(f"Training on {len(profile.samples)} samples ({sum(s.word_count for s in profile.samples)} total words)")
        
        # In production, call actual fine-tuning API here
        # For now, just simulate with a mock model ID
        profile.model_id = f"voice_clone_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        profile.is_trained = True
        profile.updated_at = datetime.now().isoformat()
        
        self._save_profile(profile)
        
        logger.info(f"Model training completed for user: {user_id} (model_id: {profile.model_id})")
        return True
    
    def generate_with_voice(
        self, 
        user_id: str, 
        prompt: str,
        base_text: Optional[str] = None
    ) -> str:
        """
        Generate text using user's personalized voice model.
        
        Args:
            user_id: User identifier
            prompt: Generation prompt
            base_text: Optional base text to refine
            
        Returns:
            Generated/refined text
        """
        profile = self.load_profile(user_id)
        
        if not profile:
            logger.warning(f"No profile for user {user_id}, using generic generation")
            return base_text or "[Generated text - no voice profile]"
        
        if not profile.is_trained:
            logger.warning(f"Profile for user {user_id} not trained yet")
            return base_text or "[Generated text - voice not trained]"
        
        # Mock voice-cloned generation
        logger.info(f"Generating with voice model: {profile.model_id}")
        
        # In production, this would call the fine-tuned model API
        # For now, add a marker to indicate it was voice-cloned
        result = base_text if base_text else "[Voice-cloned generated text]"
        result += f"\n\n[Generated with Voice Clone: {profile.model_id}]"
        
        return result
    
    def get_profile_status(self, user_id: str) -> Dict[str, Any]:
        """
        Get status of user's voice profile.
        
        Args:
            user_id: User identifier
            
        Returns:
            Status dictionary
        """
        profile = self.load_profile(user_id)
        
        if not profile:
            return {
                "exists": False,
                "message": "No voice profile found. Upload writing samples to get started."
            }
        
        sample_count = len(profile.samples)
        total_words = sum(s.word_count for s in profile.samples)
        
        status = {
            "exists": True,
            "user_id": user_id,
            "sample_count": sample_count,
            "total_words": total_words,
            "is_trained": profile.is_trained,
            "model_id": profile.model_id,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at
        }
        
        # Recommendation
        if sample_count < 3:
            status["recommendation"] = f"Upload {3 - sample_count} more sample(s) to enable voice cloning"
            status["ready_to_train"] = False
        elif not profile.is_trained:
            status["recommendation"] = "Ready to train! Click 'Train Voice Model' to personalize your AI"
            status["ready_to_train"] = True
        else:
            status["recommendation"] = "Voice model active! Your applications will use your personal writing style"
            status["ready_to_train"] = False
        
        return status
    
    def analyze_writing_style(self, user_id: str) -> Dict[str, Any]:
        """
        Analyze user's writing style from samples.
        
        Args:
            user_id: User identifier
            
        Returns:
            Style analysis dictionary
        """
        profile = self.load_profile(user_id)
        
        if not profile or not profile.samples:
            return {"error": "No samples to analyze"}
        
        # Combine all samples
        all_text = " ".join(s.content for s in profile.samples)
        
        # Basic style metrics
        sentences = [s.strip() for s in all_text.split('.') if s.strip()]
        words = all_text.split()
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        # Detect common patterns
        uses_contractions = any(c in all_text.lower() for c in ["don't", "can't", "i'm", "it's"])
        uses_first_person = "I" in all_text or "my" in all_text.lower()
        
        return {
            "total_words": len(words),
            "total_sentences": len(sentences),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_word_length": round(avg_word_length, 1),
            "uses_contractions": uses_contractions,
            "uses_first_person": uses_first_person,
            "sample_types": list(set(s.sample_type for s in profile.samples))
        }


# Convenience functions
def quick_add_sample(user_id: str, content: str, sample_type: str = "general") -> VoiceProfile:
    """Quick function to add a writing sample."""
    engine = VoiceCloningEngine()
    return engine.add_writing_sample(user_id, content, sample_type)


def quick_train(user_id: str) -> bool:
    """Quick function to train a voice model."""
    engine = VoiceCloningEngine()
    return engine.train_model(user_id)


def quick_status(user_id: str) -> Dict[str, Any]:
    """Quick function to get profile status."""
    engine = VoiceCloningEngine()
    return engine.get_profile_status(user_id)
