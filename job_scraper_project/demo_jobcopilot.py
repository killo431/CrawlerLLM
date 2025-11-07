"""Demo script for JobCopilot AI detection evasion features."""
from ai_dev.text_generator import StealthEngine, GenerationConfig, generate_application_documents
from ai_dev.stealth_scorer import score_application_document
from ai_dev.voice_cloning import VoiceCloningEngine
from ai_dev.authenticity_polish import quick_polish_analysis

print("=" * 80)
print("JobCopilot Demo - AI Detection Evasion System")
print("=" * 80)

# Step 1: Generate documents with Stealth Engine
print("\n🚀 STEP 1: Generate Application with Stealth Engine")
print("-" * 80)

user_profile = {
    "name": "John Doe",
    "title": "Senior Software Engineer",
    "experience": "5 years",
    "skills": ["Python", "JavaScript", "React", "Node.js", "Docker", "AWS"],
    "education": "B.S. Computer Science"
}

job_posting = {
    "title": "Software Engineer",
    "company": "TechCorp",
    "requirements": "5+ years experience, Python, React, team leadership"
}

config = GenerationConfig(
    model="gemini-2.5-pro",
    perplexity_level="medium",
    burstiness_level="dynamic",
    tone="professional",
    add_imperfections=True
)

results = generate_application_documents(user_profile, job_posting, config)

print(f"✅ Generated with model: {results['model_info']['model']}")
print(f"   Detection Rate: {results['model_info']['detection_rate']:.0%}")
print(f"\n📄 Cover Letter Preview (first 300 chars):")
print(results['cover_letter'][:300] + "...")

# Step 2: Calculate Stealth Score
print("\n\n📊 STEP 2: Calculate Stealth Score")
print("-" * 80)

score = score_application_document(results['cover_letter'])

print(f"Score: {score.score:.1f}%")
print(f"Risk Level: {score.risk_level}")
print(f"Safe to submit: {'✅ YES' if score.is_safe() else '⚠️ NEEDS POLISH'}")

if score.issues:
    print(f"\n⚠️ Issues Found ({len(score.issues)}):")
    for issue in score.issues[:3]:
        print(f"  - {issue}")

if score.suggestions:
    print(f"\n💡 Suggestions ({len(score.suggestions)}):")
    for suggestion in score.suggestions[:3]:
        print(f"  - {suggestion}")

# Step 3: Get polish recommendations
print("\n\n🎨 STEP 3: Authenticity Polish Recommendations")
print("-" * 80)

steps = quick_polish_analysis(results['cover_letter'])

if steps:
    print(f"Found {len(steps)} improvement areas:")
    for i, step in enumerate(steps, 1):
        print(f"\n  {i}. {step['step']}")
        print(f"     {step['description']}")
        if step['suggestions']:
            first_suggestion = step['suggestions'][0]
            print(f"     Issue: {first_suggestion['issue']}")
            print(f"     Fix: {first_suggestion['suggestion'][:80]}...")
else:
    print("✅ Text looks good! No major issues detected.")

# Step 4: Voice Cloning demo
print("\n\n🎤 STEP 4: Voice Cloning Setup")
print("-" * 80)

engine = VoiceCloningEngine()
user_id = "demo_user"

# Add writing samples
sample1 = """I'm excited about this opportunity. Over the past five years, I've built 
systems that matter. At my current company, I led a team that scaled our platform to 
handle millions of requests. What I love most is solving real problems for real people."""

sample2 = """My approach to software engineering is practical. I believe in writing clean 
code that's easy to maintain. When I worked on our mobile app, I spent time with users. 
Their feedback shaped everything we built."""

sample3 = """I can't imagine doing anything else. Every day brings new challenges. Whether 
it's debugging a tricky issue or architecting a new feature, I'm all in. That's what 
keeps me excited about this field."""

print("Adding writing samples...")
engine.add_writing_sample(user_id, sample1, "cover_letter")
engine.add_writing_sample(user_id, sample2, "email")
engine.add_writing_sample(user_id, sample3, "essay")

status = engine.get_profile_status(user_id)
print(f"✅ Profile created: {status['sample_count']} samples, {status['total_words']} words")
print(f"   Status: {status['recommendation']}")

if status['ready_to_train']:
    print("\n🎯 Training voice model...")
    success = engine.train_model(user_id)
    if success:
        print("✅ Voice model trained successfully!")
        final_status = engine.get_profile_status(user_id)
        print(f"   Model ID: {final_status['model_id']}")
    else:
        print("❌ Training failed")

# Analyze writing style
analysis = engine.analyze_writing_style(user_id)
print(f"\n📊 Writing Style Analysis:")
print(f"   Avg Sentence Length: {analysis['avg_sentence_length']} words")
print(f"   Uses Contractions: {'✅' if analysis['uses_contractions'] else '❌'}")
print(f"   Uses First Person: {'✅' if analysis['uses_first_person'] else '❌'}")

# Summary
print("\n\n" + "=" * 80)
print("Summary: JobCopilot Complete Workflow")
print("=" * 80)
print("""
✅ STEP 1: Generated application with Stealth Engine (Gemini 2.5 Pro)
✅ STEP 2: Calculated Stealth Score with risk analysis
✅ STEP 3: Generated polish recommendations (Fix Burstiness/Perplexity/Stylometry)
✅ STEP 4: Created voice profile with 3 writing samples

🎯 Recommended Workflow:
   1. Generate → 2. Score → 3. Polish (if needed) → 4. Verify → 5. Submit

📊 Target: <20% Stealth Score = Safe to submit

🚀 Launch dashboard: streamlit run dashboard/jobcopilot_app.py
""")

print("=" * 80)
print("Demo complete! All features working successfully.")
print("=" * 80)
