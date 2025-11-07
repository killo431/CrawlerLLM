"""AI text generation module with multi-model support (Stealth Engine)."""
import os
from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass
from core.logger import setup_logger

logger = setup_logger("text_generator")


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    model: str = "gemini-2.5-pro"  # Default to stealth model
    temperature: float = 0.7
    max_tokens: int = 1000
    perplexity_level: str = "medium"  # simple, medium, complex
    burstiness_level: str = "dynamic"  # uniform, dynamic
    tone: str = "professional"  # professional, casual, witty, academic
    add_imperfections: bool = False


class StealthEngine:
    """
    Stealth Engine for generating undetectable AI text.
    
    Based on "The Detection Arms Race" research:
    - Gemini 2.5 Pro: 53% detection rate (BEST)
    - Claude 3.5 Sonnet: 99% detection rate
    - Llama 3.1: 100% detection rate
    """
    
    SUPPORTED_MODELS = {
        "gemini-2.5-pro": {
            "detection_rate": 0.53,
            "api_key_env": "GEMINI_API_KEY",
            "description": "Reasoning-first model with stealth by architecture"
        },
        "claude-3.5-sonnet": {
            "detection_rate": 0.99,
            "api_key_env": "ANTHROPIC_API_KEY",
            "description": "High quality but easily detectable"
        },
        "llama-3.1": {
            "detection_rate": 1.00,
            "api_key_env": "LLAMA_API_KEY",
            "description": "Open-source, 100% detectable unless fine-tuned"
        },
        "gpt-4": {
            "detection_rate": 0.95,
            "api_key_env": "OPENAI_API_KEY",
            "description": "General purpose, high detection rate"
        }
    }
    
    def __init__(self, config: Optional[GenerationConfig] = None):
        """Initialize the Stealth Engine."""
        self.config = config or GenerationConfig()
        self.model_info = self.SUPPORTED_MODELS.get(self.config.model, {})
        logger.info(f"Initialized Stealth Engine with model: {self.config.model}")
    
    def _build_stealth_prompt(self, base_prompt: str) -> str:
        """
        Build an enhanced prompt with stealth parameters.
        
        Based on research: stacked prompt engineering reduces detection.
        """
        # Perplexity instructions
        perplexity_map = {
            "simple": "Write in clear, simple language. Use short sentences and common words.",
            "medium": "Write naturally with moderate complexity. Mix simple and sophisticated language.",
            "complex": "Use nuanced, sophisticated language with varied vocabulary and complex sentence structures."
        }
        
        # Burstiness instructions
        burstiness_map = {
            "uniform": "Keep sentence lengths consistent and formal.",
            "dynamic": "Vary sentence lengths dramatically. Mix very short sentences with longer, flowing ones. Create natural rhythm."
        }
        
        # Imperfection instructions
        imperfection_text = ""
        if self.config.add_imperfections:
            imperfection_text = (
                "\n- Use occasional contractions (it's, don't, can't)"
                "\n- Include natural colloquialisms"
                "\n- Add subtle, natural imperfections in style"
            )
        
        stealth_prompt = f"""
{base_prompt}

IMPORTANT STYLE REQUIREMENTS:
- Tone: {self.config.tone}
- Complexity Level: {perplexity_map.get(self.config.perplexity_level, perplexity_map['medium'])}
- Sentence Variation: {burstiness_map.get(self.config.burstiness_level, burstiness_map['dynamic'])}
{imperfection_text}

AVOID these AI-fingerprint words: delve, leverage, embrace, harness, navigate, landscape, dive deep, cutting-edge, robust

Write as if you are a real person sharing genuine professional experience. Make it sound human, not robotic.
"""
        return stealth_prompt
    
    def generate_resume(self, user_profile: Dict[str, Any]) -> str:
        """
        Generate a resume using the Stealth Engine.
        
        Args:
            user_profile: Dictionary with user's professional information
            
        Returns:
            Generated resume text
        """
        base_prompt = f"""
Create a professional resume for this profile:

Name: {user_profile.get('name', 'Professional')}
Title: {user_profile.get('title', 'Software Engineer')}
Experience: {user_profile.get('experience', '5 years')}
Skills: {', '.join(user_profile.get('skills', []))}
Education: {user_profile.get('education', 'Bachelor\'s Degree')}

Include:
- Professional summary
- Work experience with accomplishments
- Skills section
- Education
"""
        
        stealth_prompt = self._build_stealth_prompt(base_prompt)
        logger.info("Generating resume with Stealth Engine")
        
        # Mock generation for now - will be replaced with actual API calls
        return self._mock_generate(stealth_prompt, "resume")
    
    def generate_cover_letter(
        self, 
        user_profile: Dict[str, Any], 
        job_posting: Dict[str, Any]
    ) -> str:
        """
        Generate a cover letter using the Stealth Engine.
        
        Args:
            user_profile: Dictionary with user's professional information
            job_posting: Dictionary with job details
            
        Returns:
            Generated cover letter text
        """
        base_prompt = f"""
Create a compelling cover letter for this application:

Applicant: {user_profile.get('name', 'Professional')}
Current Role: {user_profile.get('title', 'Software Engineer')}
Experience: {user_profile.get('experience', '5 years')}

Job Position: {job_posting.get('title', 'Software Engineer')}
Company: {job_posting.get('company', 'Tech Company')}
Requirements: {job_posting.get('requirements', 'Software development skills')}

Create a personalized cover letter that:
- Shows genuine interest in the position
- Highlights relevant experience
- Connects skills to job requirements
- Includes specific examples of achievements
"""
        
        stealth_prompt = self._build_stealth_prompt(base_prompt)
        logger.info("Generating cover letter with Stealth Engine")
        
        # Mock generation for now - will be replaced with actual API calls
        return self._mock_generate(stealth_prompt, "cover_letter")
    
    def _mock_generate(self, prompt: str, doc_type: str) -> str:
        """
        Mock text generation (placeholder for actual API integration).
        
        In production, this will call the actual model API.
        """
        if doc_type == "resume":
            return f"""JOHN DOE
Senior Software Engineer

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years building scalable applications. I've worked on everything from small startups to enterprise systems. My focus is on clean code and solving real problems.

EXPERIENCE

Senior Software Engineer | TechCorp | 2020-Present
• Built microservices that handle 1M+ daily requests
• Led team of 4 developers on e-commerce platform
• Cut API response times by 60% through optimization

Software Engineer | StartupXYZ | 2018-2020
• Developed React-based dashboard used by 10k+ users
• Created automated testing suite, reducing bugs by 40%
• Worked directly with customers to understand their needs

SKILLS
Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL

EDUCATION
B.S. Computer Science | State University | 2018

[Generated with Stealth Engine - Model: {self.config.model}, Detection Rate: {self.model_info.get('detection_rate', 'N/A'):.0%}]
"""
        else:  # cover_letter
            return f"""Dear Hiring Manager,

I'm excited to apply for the Software Engineer position at your company. What draws me to this role isn't just the tech stack. It's the mission.

Over the past five years, I've built systems that matter. At TechCorp, I led a team that created a platform handling over a million requests daily. The work was challenging. We had to scale fast. But we did it right.

What I love most about software engineering is solving real problems for real people. When I worked at StartupXYZ, I spent time with customers. I watched them use our product. That feedback shaped everything we built. The result? A dashboard that 10,000 users rely on every day.

Your job description mentions needing someone who can work across the stack. That's exactly what I do. I've written Python backends and React frontends. I've deployed on AWS and optimized databases. But more than that, I can communicate with everyone—from engineers to executives to end users.

I'd love to discuss how my experience aligns with your needs. Let's talk about how I can contribute to your team.

Best regards,
John Doe

[Generated with Stealth Engine - Model: {self.config.model}, Detection Rate: {self.model_info.get('detection_rate', 'N/A'):.0%}]
"""
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "model": self.config.model,
            "detection_rate": self.model_info.get("detection_rate", "Unknown"),
            "description": self.model_info.get("description", "Unknown model"),
            "config": {
                "temperature": self.config.temperature,
                "perplexity_level": self.config.perplexity_level,
                "burstiness_level": self.config.burstiness_level,
                "tone": self.config.tone,
                "add_imperfections": self.config.add_imperfections
            }
        }


# Convenience function
def generate_application_documents(
    user_profile: Dict[str, Any],
    job_posting: Dict[str, Any],
    config: Optional[GenerationConfig] = None
) -> Dict[str, str]:
    """
    Generate both resume and cover letter in one call.
    
    Args:
        user_profile: User's professional information
        job_posting: Job details
        config: Optional generation configuration
        
    Returns:
        Dictionary with 'resume' and 'cover_letter' keys
    """
    engine = StealthEngine(config)
    
    return {
        "resume": engine.generate_resume(user_profile),
        "cover_letter": engine.generate_cover_letter(user_profile, job_posting),
        "model_info": engine.get_model_info()
    }
