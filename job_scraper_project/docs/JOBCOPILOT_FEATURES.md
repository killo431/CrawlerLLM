# JobCopilot Features - AI Detection Evasion System

## Overview

JobCopilot is an AI-powered application generator that creates resumes and cover letters designed to be **undetectable by AI detection systems** like Turnitin, Originality.ai, GPTZero, and Winston AI.

All features are based on peer-reviewed research from "The Detection Arms Race" paper.

## Core Features

### 1. 🚀 Stealth Engine (Model Selection)

**Purpose**: Use AI models with lowest baseline detectability.

**Implementation**:
- Default model: Google Gemini 2.5 Pro (53% detection rate)
- Alternative models: GPT-4, Claude 3.5 Sonnet, Llama 3.1
- Automatic model selection based on detectability

**Why It Works**: Research shows Gemini 2.5 Pro has "stealth by architecture" - its reasoning-first approach naturally produces more human-like text patterns.

**Usage**:
```python
from ai_dev.text_generator import StealthEngine, GenerationConfig

config = GenerationConfig(
    model="gemini-2.5-pro",  # Lowest detection rate
    temperature=0.7,
    perplexity_level="medium",
    burstiness_level="dynamic"
)

engine = StealthEngine(config)
resume = engine.generate_resume(user_profile)
cover_letter = engine.generate_cover_letter(user_profile, job_posting)
```

**Detection Rates**:
- Gemini 2.5 Pro: 53% (BEST)
- GPT-4: 95%
- Claude 3.5 Sonnet: 99%
- Llama 3.1: 100% (unless fine-tuned)

---

### 2. 📊 Application Stealth Score

**Purpose**: Real-time AI detection risk analysis.

**Implementation**:
- Analyzes text for AI markers
- Calculates detection probability (0-100%)
- Provides risk level and actionable suggestions

**Scoring Criteria**:
1. AI-fingerprint words (leverage, delve, embrace, etc.)
2. Burstiness (sentence length variation)
3. Perplexity (text predictability)
4. Grammar perfection (too perfect = suspicious)

**Usage**:
```python
from ai_dev.stealth_scorer import score_application_document

score = score_application_document(text)

print(f"Score: {score.score:.1f}%")
print(f"Risk Level: {score.risk_level}")
print(f"Safe to submit: {score.is_safe()}")

for issue in score.issues:
    print(f"- {issue}")
```

**Risk Thresholds**:
- 0-20%: ✅ Safe (Low Risk) - Ready to submit
- 20-50%: ⚠️ Medium Risk - Consider polishing
- 50-80%: 🚨 High Risk - Polish required
- 80-100%: 🛑 Very High Risk - Major revision needed

---

### 3. 🎨 Authenticity Polish Wizard

**Purpose**: Guided manual editing to eliminate AI markers.

**Why It Works**: Research shows "manual post-editing is the only universally foolproof method."

**Three-Step Process**:

#### Step 1: Fix Burstiness
- **Issue**: AI generates sentences of uniform length
- **Solution**: Vary sentence lengths dramatically
- **Example**: Mix short punchy sentences with longer, flowing ones

#### Step 2: Fix Perplexity
- **Issue**: AI text is too predictable, lacks personal touches
- **Solution**: Add specific examples, anecdotes, personal voice
- **Example**: Replace "extensive experience" with "In my five years at TechCorp, I built..."

#### Step 3: Fix Stylometry
- **Issue**: AI uses fingerprint words (leverage, delve, embrace)
- **Solution**: Replace with natural alternatives
- **Example**: "leverage" → "use", "delve" → "explore"

**Usage**:
```python
from ai_dev.authenticity_polish import quick_polish_analysis

steps = quick_polish_analysis(text)

for step in steps:
    print(f"\n{step['step']}: {step['description']}")
    for suggestion in step['suggestions']:
        print(f"- Issue: {suggestion['issue']}")
        print(f"- Fix: {suggestion['suggestion']}")
```

---

### 4. 🎤 AI Voice Cloning

**Purpose**: Create personalized model trained on your writing style.

**Why It Works**: Research shows fine-tuned models have unique fingerprints unknown to public detectors. While Llama 3.1 is 100% detectable by default, fine-tuning creates an undetectable private variant.

**Process**:

1. **Upload Samples**: Provide 3-5 writing samples
   - Old cover letters
   - Professional emails
   - Reports or essays
   - Any professional writing

2. **Train Model**: Fine-tune on your style
   - Analyzes sentence patterns
   - Learns vocabulary preferences
   - Captures personal voice

3. **Generate**: Use personalized model
   - Output matches your style
   - Unique fingerprint
   - Undetectable by public systems

**Usage**:
```python
from ai_dev.voice_cloning import VoiceCloningEngine

engine = VoiceCloningEngine()

# Add writing samples
engine.add_writing_sample(user_id, sample_text, "cover_letter")
engine.add_writing_sample(user_id, sample_text_2, "email")
engine.add_writing_sample(user_id, sample_text_3, "report")

# Train personalized model
success = engine.train_model(user_id)

# Generate with personal voice
text = engine.generate_with_voice(user_id, prompt, base_text)
```

**Status Tracking**:
```python
status = engine.get_profile_status(user_id)

print(f"Samples: {status['sample_count']}")
print(f"Words: {status['total_words']}")
print(f"Trained: {status['is_trained']}")
print(f"Recommendation: {status['recommendation']}")
```

---

### 5. 🎛️ Advanced Style Controls

**Purpose**: Fine-tune text generation parameters for maximum stealth.

**Parameters**:

#### Perplexity (Complexity)
- **Simple**: Clear, direct language with common words
- **Medium**: Mix of simple and sophisticated language
- **Complex**: Nuanced, sophisticated vocabulary

#### Burstiness (Variation)
- **Uniform**: Consistent sentence lengths (formal)
- **Dynamic**: Varied rhythm with short and long sentences (human-like)

#### Tone
- **Professional**: Formal business tone
- **Casual**: Friendly, conversational
- **Witty**: Clever, engaging
- **Academic**: Scholarly, research-oriented

#### Human Imperfections
- **Enabled**: Adds contractions (it's, don't), colloquialisms, natural style
- **Disabled**: More formal, perfect grammar

**Usage**:
```python
config = GenerationConfig(
    model="gemini-2.5-pro",
    perplexity_level="complex",
    burstiness_level="dynamic",
    tone="professional",
    add_imperfections=True,
    temperature=0.8,
    max_tokens=1000
)

engine = StealthEngine(config)
```

---

## Complete Workflow

### Recommended Process:

```
1. ONBOARDING
   └─> Upload 3-5 writing samples
   └─> Train voice model
   └─> Analyze writing style

2. GENERATION
   └─> Configure style parameters
   └─> Generate with Stealth Engine (Gemini 2.5 Pro)
   └─> Apply voice cloning

3. VERIFICATION
   └─> Calculate Stealth Score
   └─> Review issues and suggestions
   └─> Check if score < 20%

4. POLISHING (if needed)
   └─> Run Authenticity Wizard
   └─> Fix burstiness
   └─> Fix perplexity
   └─> Fix stylometry

5. FINAL CHECK
   └─> Recalculate Stealth Score
   └─> Verify score < 20%
   └─> Ready to submit!
```

---

## API Reference

### Text Generator

```python
from ai_dev.text_generator import (
    StealthEngine,
    GenerationConfig,
    generate_application_documents
)

# Generate both resume and cover letter
results = generate_application_documents(
    user_profile={
        "name": "John Doe",
        "title": "Software Engineer",
        "experience": "5 years",
        "skills": ["Python", "JavaScript"],
        "education": "B.S. Computer Science"
    },
    job_posting={
        "title": "Senior Developer",
        "company": "TechCorp",
        "requirements": "5+ years experience"
    },
    config=GenerationConfig(model="gemini-2.5-pro")
)

resume = results["resume"]
cover_letter = results["cover_letter"]
model_info = results["model_info"]
```

### Stealth Scorer

```python
from ai_dev.stealth_scorer import StealthScorer

scorer = StealthScorer()
score = scorer.score_text(text)

# Get polish recommendations
recommendations = scorer.generate_polish_recommendations(text, score)

for step in recommendations["steps"]:
    print(step["step"], step["action"])
```

### Voice Cloning

```python
from ai_dev.voice_cloning import (
    VoiceCloningEngine,
    quick_add_sample,
    quick_train,
    quick_status
)

# Quick functions
quick_add_sample(user_id, text, "cover_letter")
quick_train(user_id)
status = quick_status(user_id)

# Full API
engine = VoiceCloningEngine()
profile = engine.create_profile(user_id)
profile = engine.add_writing_sample(user_id, text, "email")
success = engine.train_model(user_id)
text = engine.generate_with_voice(user_id, prompt, base_text)
analysis = engine.analyze_writing_style(user_id)
```

### Authenticity Polish

```python
from ai_dev.authenticity_polish import (
    AuthenticityPolishWizard,
    quick_polish_analysis
)

# Get wizard steps
wizard = AuthenticityPolishWizard()
suggestions = wizard.analyze_and_suggest(text)
steps = wizard.get_wizard_steps(text)

# Apply edits
updated = wizard.apply_suggestion(text, suggestion, user_edit)
```

---

## Dashboard Usage

### Running the JobCopilot Dashboard

```bash
cd job_scraper_project
streamlit run dashboard/jobcopilot_app.py
```

### Features:

1. **Generate Application**: Create resume and cover letter
2. **Authenticity Polish**: Get step-by-step improvement suggestions
3. **Voice Cloning**: Upload samples and train personal model
4. **Stealth Score**: Analyze detection risk
5. **Advanced Settings**: Fine-tune generation parameters
6. **About**: Documentation and research background

---

## Best Practices

### For Lowest Detection Rate:

1. ✅ **Always use Gemini 2.5 Pro** as primary model
2. ✅ **Train voice model** with 3-5 quality samples
3. ✅ **Target score < 20%** before submission
4. ✅ **Use Authenticity Polish** if score > 20%
5. ✅ **Enable imperfections** for natural tone
6. ✅ **Set burstiness to "dynamic"** for variation
7. ✅ **Add personal anecdotes** in cover letters
8. ✅ **Replace all AI-fingerprint words** manually
9. ✅ **Vary sentence lengths** dramatically
10. ✅ **Include contractions** (it's, don't, can't)

### Red Flags to Avoid:

1. ❌ Using Claude or GPT-4 without polishing (>95% detection)
2. ❌ Keeping AI-fingerprint words (leverage, delve, embrace)
3. ❌ Uniform sentence lengths throughout
4. ❌ No personal pronouns or anecdotes
5. ❌ Perfect grammar with no contractions
6. ❌ Generic claims without specific examples
7. ❌ Repetitive sentence starters
8. ❌ Overly long paragraphs
9. ❌ Formal tone in cover letters
10. ❌ Submitting with score > 20%

---

## Research Background

**Paper**: "The Detection Arms Race" (2024)

**Key Findings**:
- Different models have vastly different detection rates
- Gemini 2.5 Pro: 53% baseline detectability
- Manual editing is universally foolproof
- Fine-tuning creates undetectable private fingerprints
- Burstiness and perplexity are key indicators
- AI-fingerprint words are easily detected

**Detection Systems Studied**:
- Turnitin
- Originality.ai
- GPTZero
- Winston AI
- Copyleaks
- Sapling

---

## Security & Ethics

### Privacy:
- All writing samples stored locally
- Fine-tuned models are private
- No data shared with third parties
- User data never leaves your control

### Ethical Use:
- Designed for legitimate job applications
- Not for academic dishonesty
- Not for deceptive content
- Should reflect your actual skills/experience

### Compliance:
- Follow employer guidelines
- Respect job posting terms
- Use AI as writing assistant, not replacement
- Ensure accuracy of all claims

---

## Support

For issues, questions, or feature requests:
- Check documentation in `docs/`
- Review research paper summary
- Run tests: `pytest tests/`
- Check logs in `logs/`

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**License**: MIT
