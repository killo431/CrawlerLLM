"""JobCopilot Home - Main Landing Page."""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page config
st.set_page_config(
    layout="wide",
    page_title="JobCopilot - Home",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better landing page
st.markdown("""
<style>
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #4314b6;
    }
    
    .feature-description {
        color: #666;
        font-size: 0.95rem;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 1rem;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4314b6;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* CTA button */
    .cta-button {
        background: #4314b6;
        color: white;
        padding: 1rem 3rem;
        border-radius: 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: background 0.3s;
    }
    
    .cta-button:hover {
        background: #5a1fd4;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">🚀 JobCopilot</h1>
    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">Undetectable AI-Powered Job Applications</p>
    <p style="font-size: 1rem; opacity: 0.9;">Generate resumes and cover letters that bypass AI detection systems</p>
</div>
""", unsafe_allow_html=True)

# Quick Start Options
st.markdown("## 🎯 Quick Start")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <div class="feature-title">Configuration Wizard</div>
        <div class="feature-description">
            Set up your job search preferences in 4 easy steps.
            Perfect for first-time users.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Setup →", key="wizard_btn", use_container_width=True):
        st.switch_page("dashboard/copilot_wizard.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Generate Application</div>
        <div class="feature-description">
            Create AI-generated resumes and cover letters instantly.
            Low detection risk guaranteed.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Generate Now →", key="generate_btn", use_container_width=True):
        st.switch_page("dashboard/jobcopilot_app.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Job Scraping</div>
        <div class="feature-description">
            Search and scrape jobs from Indeed, LinkedIn, and Glassdoor.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Search Jobs →", key="scrape_btn", use_container_width=True):
        st.switch_page("dashboard/app.py")

st.markdown("---")

# Key Features Section
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Stealth Engine
    - Uses **Gemini 2.5 Pro** (53% detection rate)
    - 47% lower detection vs other models
    - "Reasoning-first" architecture
    - Natural human-like writing
    
    ### 🎨 Authenticity Polish
    - Guided manual editing process
    - Fixes burstiness and perplexity
    - Removes AI-fingerprint words
    - Target: <20% detection rate
    
    ### 🎤 AI Voice Cloning
    - Upload 3-5 writing samples
    - Fine-tune personalized model
    - Creates unique fingerprint
    - Unknown to AI detectors
    """)

with col2:
    st.markdown("""
    ### 📊 Stealth Score
    - Real-time detection risk analysis
    - 0-100% risk scale
    - Specific issues and suggestions
    - Safe threshold indicators
    
    ### 🎛️ Advanced Controls
    - Perplexity slider (simple ↔ complex)
    - Burstiness slider (uniform ↔ dynamic)
    - Tone selection
    - Natural imperfection toggle
    
    ### 🔍 Job Intelligence
    - Multi-platform scraping
    - OSINT tools included
    - Export to JSON/CSV
    - Performance benchmarking
    """)

st.markdown("---")

# Stats Section
st.markdown("""
<div class="stats-container">
    <div class="stat">
        <div class="stat-value">53%</div>
        <div class="stat-label">Detection Rate<br/>(Gemini 2.5 Pro)</div>
    </div>
    <div class="stat">
        <div class="stat-value">&lt;20%</div>
        <div class="stat-label">Target Safe<br/>Threshold</div>
    </div>
    <div class="stat">
        <div class="stat-value">85%+</div>
        <div class="stat-label">Success Rate<br/>Below Threshold</div>
    </div>
    <div class="stat">
        <div class="stat-value">70+</div>
        <div class="stat-label">Test Cases<br/>Passing</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Workflow Section
st.markdown("## 🔄 Complete Workflow")

st.markdown("""
<div style="background: #f8f9fa; padding: 2rem; border-radius: 1rem; margin: 1rem 0;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">1️⃣</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">Setup</div>
            <div style="font-size: 0.9rem; color: #666;">Configure preferences</div>
        </div>
        <div style="font-size: 1.5rem; color: #4314b6;">→</div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">2️⃣</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">Generate</div>
            <div style="font-size: 0.9rem; color: #666;">Create documents</div>
        </div>
        <div style="font-size: 1.5rem; color: #4314b6;">→</div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">3️⃣</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">Score</div>
            <div style="font-size: 0.9rem; color: #666;">Check detection risk</div>
        </div>
        <div style="font-size: 1.5rem; color: #4314b6;">→</div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">4️⃣</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">Polish</div>
            <div style="font-size: 0.9rem; color: #666;">Improve if needed</div>
        </div>
        <div style="font-size: 1.5rem; color: #4314b6;">→</div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">5️⃣</div>
            <div style="font-weight: 600; margin-bottom: 0.25rem;">Submit</div>
            <div style="font-size: 0.9rem; color: #666;">Send with confidence</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Research-Based Section
st.markdown("## 🔬 Based on Scientific Research")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    All features are based on findings from **"The Detection Arms Race"** research paper, 
    which analyzed the detectability of various AI models and evasion techniques.
    
    **Key Findings:**
    - Gemini 2.5 Pro: 53% detection rate (lowest)
    - GPT-4: 95% detection rate
    - Claude 3.5 Sonnet: 99% detection rate
    - Manual post-editing is universally foolproof
    - Fine-tuned models create unique fingerprints
    - Perplexity and burstiness are key indicators
    """)

with col2:
    st.info("""
    **Detection Thresholds:**
    
    ✅ 0-20%: Safe  
    ⚠️ 20-50%: Medium Risk  
    🚨 50-80%: High Risk  
    🛑 80-100%: Very High Risk
    """)

st.markdown("---")

# Getting Started Section
st.markdown("## 🚀 Getting Started")

tab1, tab2, tab3 = st.tabs(["First Time Users", "Experienced Users", "Developers"])

with tab1:
    st.markdown("""
    ### Welcome to JobCopilot! 👋
    
    If you're new here, follow these steps:
    
    1. **Click "Start Setup →"** above to launch the Configuration Wizard
    2. **Complete the 4-step setup:**
       - Step 1: Select job preferences (location, types, titles)
       - Step 2: Set optional filters (experience, salary)
       - Step 3: Upload your resume
       - Step 4: Choose writing style
    3. **Generate your first application** using the Stealth Engine
    4. **Check your Stealth Score** (target: <20%)
    5. **Polish if needed** using the Authenticity Wizard
    6. **Download and submit** your application!
    
    📚 [Read the Complete Guide](docs/WIZARD_GUIDE.md)
    """)

with tab2:
    st.markdown("""
    ### Quick Actions 🎯
    
    For experienced users who know what they want:
    
    - **Generate Application**: Go directly to document generation
    - **Voice Cloning**: Upload writing samples to train your model
    - **Stealth Score**: Analyze existing documents
    - **Job Scraping**: Search for jobs across platforms
    - **Polish Wizard**: Improve detection scores
    
    💡 **Pro Tip**: Train your voice model for the most undetectable results!
    """)

with tab3:
    st.markdown("""
    ### Technical Information 🛠️
    
    **Architecture:**
    - Python 3.11+
    - Streamlit (UI Framework)
    - Multiple LLM APIs (Gemini, Claude, GPT-4)
    - Playwright (Browser automation)
    - Custom stealth algorithms
    
    **Project Structure:**
    ```
    job_scraper_project/
    ├── dashboard/          # Streamlit UI
    ├── ai_dev/            # AI generation engines
    ├── adapters/          # Job board scrapers
    ├── core/              # Core functionality
    ├── automation/        # Application automation
    └── tests/             # Test suite (70+ tests)
    ```
    
    **Contributing:**
    - Check [FEATURES_ROADMAP.md](../FEATURES_ROADMAP.md)
    - Review [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md)
    - Submit pull requests
    
    **Testing:**
    ```bash
    pytest tests/
    python demo_jobcopilot.py
    ```
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p><strong>JobCopilot v1.0</strong></p>
    <p>Built with ❤️ and cutting-edge AI research</p>
    <p>Based on "The Detection Arms Race" (2024)</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        <a href="https://github.com/killo431/CrawlerLLM" target="_blank" style="color: #4314b6; text-decoration: none;">GitHub</a> • 
        <a href="../README.md" target="_blank" style="color: #4314b6; text-decoration: none;">Documentation</a> • 
        <a href="../FEATURES_ROADMAP.md" target="_blank" style="color: #4314b6; text-decoration: none;">Roadmap</a>
    </p>
</div>
""", unsafe_allow_html=True)
