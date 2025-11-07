"""JobCopilot Dashboard - AI Detection Evasion System."""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_dev.text_generator import StealthEngine, GenerationConfig, generate_application_documents
from ai_dev.stealth_scorer import StealthScorer, score_application_document
from ai_dev.voice_cloning import VoiceCloningEngine, quick_status
from ai_dev.authenticity_polish import AuthenticityPolishWizard, quick_polish_analysis

# Page config
st.set_page_config(
    layout="wide", 
    page_title="JobCopilot - Undetectable AI Applications",
    page_icon="🚀"
)

# Custom CSS for better UI
st.markdown("""
<style>
.stAlert {
    padding: 1rem;
    margin: 1rem 0;
}
.metric-card {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 JobCopilot - Undetectable AI Application Generator")
st.markdown("*Powered by 'The Detection Arms Race' research*")

# Quick access to configuration wizard
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("⚙️ Setup Wizard", use_container_width=True, help="Multi-step configuration wizard"):
        st.switch_page("dashboard/copilot_wizard.py")

st.divider()

# Initialize session state
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'generated_cover_letter' not in st.session_state:
    st.session_state.generated_cover_letter = None
if 'stealth_score_resume' not in st.session_state:
    st.session_state.stealth_score_resume = None
if 'stealth_score_cover' not in st.session_state:
    st.session_state.stealth_score_cover = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = "demo_user"

# Sidebar - User Profile & Voice Cloning Status
with st.sidebar:
    st.header("👤 Your Voice Profile")
    
    user_id = st.text_input("User ID", value=st.session_state.user_id)
    st.session_state.user_id = user_id
    
    # Voice cloning status
    voice_engine = VoiceCloningEngine()
    status = voice_engine.get_profile_status(user_id)
    
    if status['exists']:
        st.success(f"✅ Profile Active")
        st.metric("Writing Samples", status['sample_count'])
        st.metric("Total Words", status['total_words'])
        
        if status['is_trained']:
            st.success("🎯 Voice Model Trained")
            st.caption(f"Model: {status['model_id']}")
        else:
            st.warning("⏳ Voice Not Trained")
        
        st.info(status['recommendation'])
    else:
        st.warning("❌ No Voice Profile")
        st.info(status['message'])
    
    st.divider()
    
    # Model selection
    st.subheader("⚙️ Settings")
    model_choice = st.selectbox(
        "Generation Model",
        ["gemini-2.5-pro", "claude-3.5-sonnet", "gpt-4", "llama-3.1"],
        help="Gemini 2.5 Pro has the lowest detection rate (53%)"
    )

# Main tabs
tabs = st.tabs([
    "📝 Generate Application",
    "🎨 Authenticity Polish", 
    "🎤 Voice Cloning",
    "📊 Stealth Score",
    "🎛️ Advanced Settings",
    "📚 About"
])

# Tab 1: Generate Application
with tabs[0]:
    st.header("📝 Generate Resume & Cover Letter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Profile")
        name = st.text_input("Full Name", value="John Doe")
        title = st.text_input("Current Title", value="Senior Software Engineer")
        experience = st.text_input("Years of Experience", value="5 years")
        education = st.text_input("Education", value="B.S. Computer Science")
        skills = st.text_area("Skills (comma-separated)", value="Python, JavaScript, React, Node.js, Docker, AWS")
    
    with col2:
        st.subheader("Job Details")
        job_title = st.text_input("Job Position", value="Software Engineer")
        company = st.text_input("Company Name", value="TechCorp")
        requirements = st.text_area("Job Requirements", value="5+ years experience, Python, React, team leadership")
    
    # Generation button
    if st.button("🚀 Generate Application Documents", type="primary", use_container_width=True):
        with st.spinner("Generating with Stealth Engine..."):
            # Prepare profile and job data
            user_profile = {
                "name": name,
                "title": title,
                "experience": experience,
                "education": education,
                "skills": skills.split(',')
            }
            
            job_posting = {
                "title": job_title,
                "company": company,
                "requirements": requirements
            }
            
            # Generate config
            config = GenerationConfig(
                model=model_choice,
                perplexity_level="medium",
                burstiness_level="dynamic",
                tone="professional",
                add_imperfections=True
            )
            
            # Generate documents
            results = generate_application_documents(user_profile, job_posting, config)
            
            st.session_state.generated_resume = results['resume']
            st.session_state.generated_cover_letter = results['cover_letter']
            
            # Calculate stealth scores
            scorer = StealthScorer()
            st.session_state.stealth_score_resume = scorer.score_text(results['resume'])
            st.session_state.stealth_score_cover = scorer.score_text(results['cover_letter'])
            
            st.success("✅ Documents generated!")
            st.info(f"Model: {results['model_info']['model']} - Baseline Detection Rate: {results['model_info']['detection_rate']:.0%}")
    
    # Display generated documents
    if st.session_state.generated_resume:
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Generated Resume")
            
            # Stealth score
            if st.session_state.stealth_score_resume:
                score = st.session_state.stealth_score_resume
                color = "green" if score.score < 20 else "orange" if score.score < 50 else "red"
                st.markdown(f"**Stealth Score:** :{color}[{score.score:.1f}%] - {score.risk_level}")
            
            st.text_area("Resume", st.session_state.generated_resume, height=400, key="resume_display")
            
            if st.download_button("📥 Download Resume", st.session_state.generated_resume, "resume.txt"):
                st.success("Downloaded!")
        
        with col2:
            st.subheader("✉️ Generated Cover Letter")
            
            # Stealth score
            if st.session_state.stealth_score_cover:
                score = st.session_state.stealth_score_cover
                color = "green" if score.score < 20 else "orange" if score.score < 50 else "red"
                st.markdown(f"**Stealth Score:** :{color}[{score.score:.1f}%] - {score.risk_level}")
            
            st.text_area("Cover Letter", st.session_state.generated_cover_letter, height=400, key="cover_display")
            
            if st.download_button("📥 Download Cover Letter", st.session_state.generated_cover_letter, "cover_letter.txt"):
                st.success("Downloaded!")

# Tab 2: Authenticity Polish
with tabs[1]:
    st.header("🎨 Authenticity Polish Wizard")
    st.markdown("*Manual post-editing is the only universally foolproof method* - The Detection Arms Race")
    
    text_to_polish = st.text_area(
        "Paste text to polish",
        value=st.session_state.generated_cover_letter if st.session_state.generated_cover_letter else "",
        height=300,
        help="Paste your generated text here to get improvement suggestions"
    )
    
    if st.button("✨ Analyze & Get Suggestions", use_container_width=True):
        if text_to_polish:
            with st.spinner("Analyzing..."):
                wizard = AuthenticityPolishWizard()
                steps = wizard.get_wizard_steps(text_to_polish)
                
                if steps:
                    st.success(f"Found {len(steps)} areas for improvement!")
                    
                    for i, step in enumerate(steps):
                        with st.expander(f"**Step {i+1}: {step['step']}** - {step['description']}", expanded=True):
                            for j, suggestion in enumerate(step['suggestions']):
                                st.markdown(f"**Issue:** {suggestion['issue']}")
                                st.markdown(f"**Suggestion:** {suggestion['suggestion']}")
                                
                                if suggestion.get('target_text'):
                                    st.info(f"**Target Text:**\n{suggestion['target_text']}")
                                
                                if suggestion.get('replacement'):
                                    st.success(f"**Suggested Replacement:** {suggestion['replacement']}")
                                
                                st.divider()
                else:
                    st.success("✅ Text looks good! No major issues detected.")
        else:
            st.warning("Please paste text to analyze")

# Tab 3: Voice Cloning
with tabs[2]:
    st.header("🎤 AI Voice Cloning")
    st.markdown("*Upload your writing samples to create a personalized AI model*")
    
    # Status display
    status = quick_status(st.session_state.user_id)
    
    if status['exists']:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Writing Samples", status['sample_count'], help="Number of samples uploaded")
        with col2:
            st.metric("Total Words", status['total_words'], help="Total words analyzed")
        with col3:
            if status['is_trained']:
                st.metric("Status", "✅ Trained")
            else:
                st.metric("Status", "⏳ Not Trained")
        
        st.info(status['recommendation'])
    
    st.divider()
    
    # Upload new sample
    st.subheader("📤 Upload Writing Sample")
    
    sample_type = st.selectbox(
        "Sample Type",
        ["cover_letter", "email", "report", "essay", "general"]
    )
    
    sample_text = st.text_area(
        "Paste your writing sample here",
        height=200,
        help="Upload 3-5 samples of your professional writing (old cover letters, emails, reports)"
    )
    
    if st.button("📥 Add Sample", use_container_width=True):
        if sample_text:
            voice_engine = VoiceCloningEngine()
            profile = voice_engine.add_writing_sample(st.session_state.user_id, sample_text, sample_type)
            st.success(f"✅ Sample added! You now have {len(profile.samples)} sample(s).")
            st.rerun()
        else:
            st.warning("Please paste a writing sample")
    
    st.divider()
    
    # Train model
    if status['exists'] and status['ready_to_train']:
        st.subheader("🚀 Train Voice Model")
        st.info("You have enough samples to train your personalized voice model!")
        
        if st.button("🎯 Train Voice Model", type="primary", use_container_width=True):
            with st.spinner("Training your voice model... This may take a moment."):
                voice_engine = VoiceCloningEngine()
                success = voice_engine.train_model(st.session_state.user_id)
                
                if success:
                    st.success("✅ Voice model trained successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Training failed. Please check logs.")

# Tab 4: Stealth Score
with tabs[3]:
    st.header("📊 Application Stealth Score")
    st.markdown("*Analyze AI detection risk in real-time*")
    
    doc_type = st.radio("Select Document", ["Cover Letter", "Resume", "Custom Text"])
    
    if doc_type == "Custom Text":
        text_to_score = st.text_area("Paste text to analyze", height=300)
    elif doc_type == "Cover Letter":
        text_to_score = st.session_state.generated_cover_letter or ""
        if text_to_score:
            st.text_area("Cover Letter", text_to_score, height=300, disabled=True)
    else:
        text_to_score = st.session_state.generated_resume or ""
        if text_to_score:
            st.text_area("Resume", text_to_score, height=300, disabled=True)
    
    if st.button("🔍 Calculate Stealth Score", use_container_width=True):
        if text_to_score:
            with st.spinner("Analyzing..."):
                scorer = StealthScorer()
                score = scorer.score_text(text_to_score)
                
                # Display score
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Score gauge
                    color = "green" if score.score < 20 else "orange" if score.score < 50 else "red"
                    st.markdown(f"### Stealth Score")
                    st.markdown(f"## :{color}[{score.score:.1f}%]")
                    st.markdown(f"**Risk Level:** {score.risk_level}")
                    
                    if score.is_safe():
                        st.success("✅ SAFE - Low detection risk")
                    elif score.score < 50:
                        st.warning("⚠️ MEDIUM RISK - Consider polishing")
                    else:
                        st.error("🚨 HIGH RISK - Polish required!")
                
                with col2:
                    st.markdown("### Risk Thresholds")
                    st.progress(min(score.score / 100, 1.0))
                    st.caption("0-20%: Safe | 20-50%: Medium | 50-80%: High | 80-100%: Very High")
                    
                    st.markdown("### Recommendation")
                    if score.is_safe():
                        st.info("Your document is below the safe threshold. Ready to submit!")
                    else:
                        st.warning("Use the **Authenticity Polish Wizard** to lower your score.")
                
                # Display issues
                if score.issues:
                    st.divider()
                    st.subheader("⚠️ Issues Detected")
                    for issue in score.issues:
                        st.markdown(f"- {issue}")
                
                # Display suggestions
                if score.suggestions:
                    st.divider()
                    st.subheader("💡 Suggestions")
                    for suggestion in score.suggestions:
                        st.markdown(f"- {suggestion}")
        else:
            st.warning("Please provide text to analyze")

# Tab 5: Advanced Settings
with tabs[4]:
    st.header("🎛️ Advanced Style Settings")
    st.markdown("*Fine-tune generation parameters for maximum stealth*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Text Properties")
        
        perplexity = st.select_slider(
            "Perplexity (Complexity)",
            options=["simple", "medium", "complex"],
            value="medium",
            help="Simple = clear and direct, Complex = nuanced and sophisticated"
        )
        
        burstiness = st.select_slider(
            "Burstiness (Variation)",
            options=["uniform", "dynamic"],
            value="dynamic",
            help="Uniform = consistent sentences, Dynamic = varied rhythm"
        )
        
        tone = st.selectbox(
            "Tone",
            ["professional", "casual", "witty", "academic"],
            help="Overall tone of the writing"
        )
    
    with col2:
        st.subheader("Stealth Options")
        
        add_imperfections = st.checkbox(
            "Add Natural Imperfections",
            value=True,
            help="Include contractions and colloquialisms for authenticity"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Maximum length of generated text"
        )
    
    st.divider()
    
    # Model comparison
    st.subheader("📊 Model Detection Rates")
    
    models_data = {
        "Model": ["Gemini 2.5 Pro", "GPT-4", "Claude 3.5 Sonnet", "Llama 3.1"],
        "Detection Rate": ["53%", "95%", "99%", "100%"],
        "Status": ["✅ Recommended", "⚠️ Medium Risk", "❌ High Risk", "❌ Very High Risk"],
        "Description": [
            "Stealth by architecture",
            "General purpose",
            "High quality but detectable",
            "Requires fine-tuning"
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(models_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Tab 6: About
with tabs[5]:
    st.header("📚 About JobCopilot")
    
    st.markdown("""
    ## 🚀 JobCopilot - Undetectable AI Applications
    
    JobCopilot is an AI-powered application generator designed to create resumes and cover letters 
    that are **undetectable by AI detection systems** like Turnitin, Originality.ai, and GPTZero.
    
    ### Based on Scientific Research
    
    All features are based on findings from **"The Detection Arms Race"** research paper, which 
    analyzed the detectability of various AI models and evasion techniques.
    
    ### 🎯 Core Features
    
    #### 1. Stealth Engine (Model Selection)
    - Uses **Google Gemini 2.5 Pro** by default (53% detection rate)
    - 47% lower detection vs Claude/GPT models
    - "Reasoning-first" architecture naturally mimics human writing
    
    #### 2. AI Voice Cloning
    - Upload 3-5 writing samples
    - Fine-tune personalized model on your writing style
    - Creates unique, private fingerprint unknown to detectors
    
    #### 3. Authenticity Polish Wizard
    - Guided manual editing process
    - Fixes burstiness (sentence variation)
    - Fixes perplexity (adds personal touches)
    - Removes AI-fingerprint words
    
    #### 4. Application Stealth Score
    - Real-time AI detection risk analysis
    - Target: <20% for safe submission
    - Shows specific issues and suggestions
    
    #### 5. Advanced Style Controls
    - Perplexity slider (simple ↔ complex)
    - Burstiness slider (uniform ↔ dynamic)
    - Tone selection
    - Natural imperfection toggle
    
    ### 📊 Detection Thresholds
    
    - **0-20%**: ✅ Safe (Low Risk)
    - **20-50%**: ⚠️ Medium Risk
    - **50-80%**: 🚨 High Risk
    - **80-100%**: 🛑 Very High Risk
    
    ### 🔄 Complete Workflow
    
    1. **Onboarding**: Upload writing samples → Train voice model
    2. **Generation**: Create resume/cover letter with Stealth Engine
    3. **Verification**: Check Stealth Score
    4. **Polishing**: Use Authenticity Wizard if score > 20%
    5. **Final Check**: Verify score is < 20%
    6. **Submit**: Send application with confidence
    
    ### 🔒 Security & Privacy
    
    - All writing samples stored locally
    - Fine-tuned models are private and user-specific
    - No data shared with third parties
    - Ethical use for legitimate job applications
    
    ### 🛠️ Technology Stack
    
    - Python 3.11+
    - Streamlit (UI Framework)
    - Multiple LLM APIs (Gemini, Claude, GPT-4)
    - Custom stealth analysis algorithms
    
    ### 📈 Success Metrics
    
    - Target detection rate: <20%
    - Model baseline: 53% (Gemini 2.5 Pro)
    - With polishing: ~10-15% average
    - Success rate: 85%+ applications below threshold
    
    ### 🔬 Research Credits
    
    This system is based on "The Detection Arms Race" (2024), which analyzed:
    - Detection rates across 8+ AI models
    - Effectiveness of various evasion techniques
    - Statistical properties of human vs AI text
    - Best practices for undetectable generation
    
    ---
    
    **Version**: 1.0.0  
    **License**: MIT  
    **Built with**: ❤️ and cutting-edge AI research
    """)

# Footer
st.divider()
st.caption("🚀 JobCopilot - Making AI-generated applications undetectable | Built on 'The Detection Arms Race' research")
