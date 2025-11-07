"""JobCopilot Configuration Wizard - Multi-step Setup Interface.

Based on the AiCopilotCFG UX pattern with 4-step wizard flow.
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page config
st.set_page_config(
    layout="centered",
    page_title="Copilot Configuration",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the AiCopilotCFG design
st.markdown("""
<style>
    /* Hide default streamlit elements for cleaner wizard UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Wizard container styling */
    .wizard-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Progress indicator */
    .step-indicator {
        text-align: center;
        margin: 2rem 0;
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .section-description {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 2rem;
        padding: 0.75rem 2rem;
        font-weight: 500;
    }
    
    /* Navigation buttons */
    .nav-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
        justify-content: space-between;
    }
    
    /* Exit button styling */
    .exit-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: 1px solid #333;
        border-radius: 2rem;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    /* Checkbox/toggle styling */
    .stCheckbox {
        padding: 0.5rem 0;
    }
    
    /* Card styling */
    .option-card {
        border: 1px solid #ddd;
        border-radius: 1.5rem;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .option-card.selected {
        background-color: #4314b6;
        color: white;
        border-color: #4314b6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'config' not in st.session_state:
    st.session_state.config = {
        'include_remote': False,
        'remote_locations': ['Worldwide'],
        'include_physical': False,
        'physical_locations': [],
        'job_types': [],
        'job_titles': [],
        'experience_level': [],
        'salary_min': 0,
        'salary_max': 200000,
        'resume_path': None,
        'writing_style': 'professional',
        'tone': 'balanced',
        'perplexity': 'medium',
        'burstiness': 'dynamic'
    }

def go_to_step(step_num):
    """Navigate to a specific step."""
    st.session_state.current_step = step_num

def render_progress_indicator():
    """Render the progress indicator showing current step."""
    current = st.session_state.current_step
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="font-size: 0.9rem; color: #666;">Step {current} of 4</p>
    </div>
    """, unsafe_allow_html=True)

def render_exit_button():
    """Render the exit button."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Exit", key="exit_btn"):
            st.switch_page("dashboard/jobcopilot_app.py")

# ====================
# STEP 1: Job Preferences
# ====================
def render_step_1():
    """Step 1: Work Location, Job Types, and Job Titles."""
    st.markdown("<h1 style='text-align: center;'>Copilot Configuration</h1>", unsafe_allow_html=True)
    render_exit_button()
    render_progress_indicator()
    
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>First, select the Work Location and Jobs you are looking for</p>", unsafe_allow_html=True)
    
    # Work Location Section
    st.markdown("### Work Location")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>Are you looking for jobs that are remote, have a physical location, or both?</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        include_remote = st.checkbox(
            "Remote Jobs",
            value=st.session_state.config['include_remote'],
            key="include_remote_cb"
        )
        st.session_state.config['include_remote'] = include_remote
        
        if include_remote:
            remote_locs = st.multiselect(
                "Remote Locations",
                ["Worldwide", "USA Only", "Europe", "Asia Pacific", "Latin America"],
                default=st.session_state.config['remote_locations'],
                key="remote_locs"
            )
            st.session_state.config['remote_locations'] = remote_locs
    
    with col2:
        include_physical = st.checkbox(
            "On-site Jobs / Hybrid",
            value=st.session_state.config['include_physical'],
            key="include_physical_cb"
        )
        st.session_state.config['include_physical'] = include_physical
        
        if include_physical:
            physical_locs = st.multiselect(
                "Physical Locations",
                ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", "Boston, MA", "Chicago, IL"],
                default=st.session_state.config['physical_locations'],
                key="physical_locs"
            )
            st.session_state.config['physical_locations'] = physical_locs
    
    st.markdown("---")
    
    # Job Types Section
    st.markdown("### Job Types")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>What job types are you looking for? Select at least one.</p>", unsafe_allow_html=True)
    
    job_types_options = ["Fulltime", "Part-Time", "Contractor / Temp", "Internship"]
    selected_types = []
    
    cols = st.columns(4)
    for i, job_type in enumerate(job_types_options):
        with cols[i]:
            if st.checkbox(job_type, value=job_type in st.session_state.config['job_types'], key=f"job_type_{i}"):
                selected_types.append(job_type)
    
    st.session_state.config['job_types'] = selected_types
    
    st.markdown("---")
    
    # Job Titles Section
    st.markdown("### Job Titles")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>What job titles are you looking for? Type in and select up to 5</p>", unsafe_allow_html=True)
    
    job_titles = st.text_input(
        "Enter job titles (comma-separated)",
        value=", ".join(st.session_state.config['job_titles']),
        placeholder="e.g., Software Engineer, Data Scientist, Product Manager",
        key="job_titles_input"
    )
    
    if job_titles:
        titles_list = [t.strip() for t in job_titles.split(',') if t.strip()]
        st.session_state.config['job_titles'] = titles_list[:5]
        
        if len(titles_list) > 5:
            st.warning("⚠️ Maximum 5 job titles allowed. Only the first 5 will be saved.")
        
        # Display selected titles as tags
        if titles_list:
            st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
            for title in titles_list[:5]:
                st.markdown(f"<span style='background: #4314b6; color: white; padding: 0.5rem 1rem; border-radius: 1.5rem; margin: 0.25rem; display: inline-block;'>{title}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("Next Step →", type="primary", key="step1_next"):
            # Validation
            if not st.session_state.config['include_remote'] and not st.session_state.config['include_physical']:
                st.error("⚠️ Please select at least one work location option")
            elif not st.session_state.config['job_types']:
                st.error("⚠️ Please select at least one job type")
            elif not st.session_state.config['job_titles']:
                st.error("⚠️ Please enter at least one job title")
            else:
                go_to_step(2)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ====================
# STEP 2: Optional Filters
# ====================
def render_step_2():
    """Step 2: Additional filters for narrowing search."""
    st.markdown("<h1 style='text-align: center;'>Copilot Configuration</h1>", unsafe_allow_html=True)
    render_exit_button()
    render_progress_indicator()
    
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>Next, narrow your search with optional filters</p>", unsafe_allow_html=True)
    
    # Experience Level
    st.markdown("### Experience Level")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>Select all that apply</p>", unsafe_allow_html=True)
    
    experience_options = ["Internship", "Entry Level", "Mid Level", "Senior Level", "Lead/Principal", "Executive"]
    selected_exp = []
    
    cols = st.columns(3)
    for i, exp in enumerate(experience_options):
        with cols[i % 3]:
            if st.checkbox(exp, value=exp in st.session_state.config['experience_level'], key=f"exp_{i}"):
                selected_exp.append(exp)
    
    st.session_state.config['experience_level'] = selected_exp
    
    st.markdown("---")
    
    # Salary Range
    st.markdown("### Salary Range")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>Filter by expected salary (USD per year)</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        salary_min = st.number_input(
            "Minimum Salary",
            min_value=0,
            max_value=500000,
            value=st.session_state.config['salary_min'],
            step=5000,
            key="salary_min"
        )
        st.session_state.config['salary_min'] = salary_min
    
    with col2:
        salary_max = st.number_input(
            "Maximum Salary",
            min_value=0,
            max_value=500000,
            value=st.session_state.config['salary_max'],
            step=5000,
            key="salary_max"
        )
        st.session_state.config['salary_max'] = salary_max
    
    if salary_min > salary_max:
        st.warning("⚠️ Minimum salary should be less than maximum salary")
    
    # Navigation
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", key="step2_back"):
            go_to_step(1)
            st.rerun()
    with col3:
        if st.button("Next Step →", type="primary", key="step2_next"):
            go_to_step(3)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ====================
# STEP 3: Resume Upload
# ====================
def render_step_3():
    """Step 3: Confirm the CV/Resume to use."""
    st.markdown("<h1 style='text-align: center;'>Copilot Configuration</h1>", unsafe_allow_html=True)
    render_exit_button()
    render_progress_indicator()
    
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>Confirm the CV/Resume you would like to use</p>", unsafe_allow_html=True)
    
    st.markdown("### Upload Your Resume")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>Upload your resume or CV in PDF, DOC, or DOCX format</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'doc', 'docx'],
        key="resume_upload",
        help="Supported formats: PDF, DOC, DOCX"
    )
    
    if uploaded_file:
        # Save the file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.config['resume_path'] = tmp_file.name
        
        st.success(f"✅ Resume uploaded: {uploaded_file.name}")
        st.info(f"📄 File size: {len(uploaded_file.getvalue()) / 1024:.1f} KB")
    
    st.markdown("---")
    
    # Option to use existing resume
    st.markdown("### Or Use Existing Resume")
    
    # TODO: Replace with actual database query for user's uploaded resumes
    # This is placeholder data for demonstration purposes
    existing_resumes = []  # In production, fetch from database
    
    if existing_resumes:
        selected_existing = st.selectbox(
            "Select from previously uploaded resumes",
            ["None"] + existing_resumes,
            key="existing_resume"
        )
        
        if selected_existing != "None":
            st.session_state.config['resume_path'] = f"/uploads/{selected_existing}"
            st.info(f"📄 Using: {selected_existing}")
    else:
        st.info("💡 No previously uploaded resumes found. Upload a new resume above.")
    
    # Navigation
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", key="step3_back"):
            go_to_step(2)
            st.rerun()
    with col3:
        if st.button("Next Step →", type="primary", key="step3_next"):
            if not st.session_state.config['resume_path']:
                st.error("⚠️ Please upload or select a resume")
            else:
                go_to_step(4)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ====================
# STEP 4: Writing Style
# ====================
def render_step_4():
    """Step 4: Configure writing style and AI generation preferences."""
    st.markdown("<h1 style='text-align: center;'>Copilot Configuration</h1>", unsafe_allow_html=True)
    render_exit_button()
    render_progress_indicator()
    
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>Final Step!</p>", unsafe_allow_html=True)
    
    st.markdown("### Writing Style")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>Choose how you want your cover letters and applications to be written</p>", unsafe_allow_html=True)
    
    # Writing Style
    writing_style = st.radio(
        "Select your preferred writing style",
        ["Professional", "Casual", "Witty", "Academic"],
        index=["professional", "casual", "witty", "academic"].index(st.session_state.config['writing_style'].lower()),
        key="writing_style_radio",
        horizontal=True
    )
    st.session_state.config['writing_style'] = writing_style.lower()
    
    st.markdown("---")
    
    # Tone
    st.markdown("### Tone")
    st.markdown("<p style='color: #666; font-size: 0.9rem;'>How formal or casual should the tone be?</p>", unsafe_allow_html=True)
    
    tone_map = {0: "very_formal", 1: "formal", 2: "balanced", 3: "casual", 4: "very_casual"}
    tone_labels = ["Very Formal", "Formal", "Balanced", "Casual", "Very Casual"]
    
    current_tone_index = 2  # Default to balanced
    for idx, val in tone_map.items():
        if val == st.session_state.config['tone']:
            current_tone_index = idx
            break
    
    tone_slider = st.select_slider(
        "Tone Scale",
        options=tone_labels,
        value=tone_labels[current_tone_index],
        key="tone_slider"
    )
    st.session_state.config['tone'] = tone_map[tone_labels.index(tone_slider)]
    
    st.markdown("---")
    
    # Advanced Settings
    with st.expander("⚙️ Advanced Style Settings"):
        st.markdown("### Text Complexity")
        
        perplexity = st.select_slider(
            "Perplexity (Complexity)",
            options=["simple", "medium", "complex"],
            value=st.session_state.config['perplexity'],
            key="perplexity_slider",
            help="Simple = clear and direct, Complex = nuanced and sophisticated"
        )
        st.session_state.config['perplexity'] = perplexity
        
        st.markdown("### Sentence Variation")
        
        burstiness = st.select_slider(
            "Burstiness (Variation)",
            options=["uniform", "dynamic"],
            value=st.session_state.config['burstiness'],
            key="burstiness_slider",
            help="Uniform = consistent sentences, Dynamic = varied rhythm"
        )
        st.session_state.config['burstiness'] = burstiness
    
    # Summary of configuration
    st.markdown("---")
    st.markdown("### 📋 Configuration Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Job Preferences:**")
        st.write(f"• Job Types: {', '.join(st.session_state.config['job_types'])}")
        titles = st.session_state.config['job_titles']
        titles_display = ', '.join(titles[:3]) + ('...' if len(titles) > 3 else '')
        st.write(f"• Job Titles: {titles_display}")
        st.write(f"• Remote: {'✓' if st.session_state.config['include_remote'] else '✗'}")
        st.write(f"• On-site: {'✓' if st.session_state.config['include_physical'] else '✗'}")
    
    with col2:
        st.markdown("**Style Preferences:**")
        st.write(f"• Writing Style: {st.session_state.config['writing_style'].title()}")
        st.write(f"• Tone: {st.session_state.config['tone'].replace('_', ' ').title()}")
        st.write(f"• Complexity: {st.session_state.config['perplexity'].title()}")
        st.write(f"• Variation: {st.session_state.config['burstiness'].title()}")
    
    # Navigation
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", key="step4_back"):
            go_to_step(3)
            st.rerun()
    with col3:
        if st.button("🚀 Complete Setup", type="primary", key="step4_complete"):
            # Save configuration
            st.success("✅ Configuration saved successfully!")
            st.balloons()
            
            # In a real app, save config to database or file
            # For now, configuration is stored in session state
            
            # Reset wizard and go to main app
            st.session_state.current_step = 1
            st.info("✨ Redirecting to dashboard...")
            st.switch_page("dashboard/jobcopilot_app.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ====================
# Main App Router
# ====================
def main():
    """Main application router."""
    current_step = st.session_state.current_step
    
    if current_step == 1:
        render_step_1()
    elif current_step == 2:
        render_step_2()
    elif current_step == 3:
        render_step_3()
    elif current_step == 4:
        render_step_4()
    else:
        # Fallback
        st.error("Invalid step. Resetting to step 1.")
        st.session_state.current_step = 1
        st.rerun()

if __name__ == "__main__":
    main()
