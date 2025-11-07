"""Streamlit dashboard for OSINT and job scraping."""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.export_manager import export_data

st.set_page_config(layout="wide", page_title="OSINT + Job Scraping Dashboard")
st.title("🧠 OSINT + Job Scraping Dashboard")

tabs = st.tabs([
    "Job Scraping",
    "Application Submission",
    "Phone Lookup", 
    "Footprint Trace", 
    "Breach Checker",
    "AI Feature Developer", 
    "About"
])

# Tab 1: Job Scraping
with tabs[0]:
    st.header("🧳 Job Scraper")
    
    site = st.selectbox("Select Job Board", ["Indeed", "LinkedIn", "Glassdoor"])
    
    if st.button("Start Scraping"):
        with st.spinner(f"Scraping {site}..."):
            if site == "Indeed":
                from adapters.indeed import IndeedScraper
                scraper = IndeedScraper()
            elif site == "LinkedIn":
                from adapters.linkedin import LinkedInScraper
                scraper = LinkedInScraper()
            else:
                from adapters.glassdoor import GlassdoorScraper
                scraper = GlassdoorScraper()
            
            jobs = scraper.run()
            
            if jobs:
                export_data(jobs, f"{site.lower()}_jobs", "json")
                export_data(jobs, f"{site.lower()}_jobs", "csv")
                st.success(f"✅ Scraped {len(jobs)} jobs from {site}")
                st.dataframe(jobs)
            else:
                st.warning("No jobs found")

# Tab 2: Application Submission
with tabs[1]:
    st.header("📝 Automated Application Submission")
    
    st.markdown("""
    Submit job applications automatically across multiple platforms.
    Supports LinkedIn Easy Apply, Indeed, Greenhouse ATS, and generic applications.
    """)
    
    # Application details
    st.subheader("Job Details")
    col1, col2 = st.columns(2)
    
    with col1:
        job_url = st.text_input("Job Application URL*", placeholder="https://...")
        job_id = st.text_input("Job ID (optional)", placeholder="Unique identifier")
    
    with col2:
        platform = st.selectbox(
            "Platform",
            ["Auto-detect", "LinkedIn", "Indeed", "Greenhouse", "Generic"]
        )
    
    # User profile
    st.subheader("Your Information")
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name*")
        last_name = st.text_input("Last Name*")
        email = st.text_input("Email*", placeholder="your.email@example.com")
        phone = st.text_input("Phone*", placeholder="555-0123")
    
    with col2:
        linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/...")
        github_url = st.text_input("GitHub URL", placeholder="https://github.com/...")
        city = st.text_input("City")
        state = st.text_input("State/Province")
    
    # Documents
    st.subheader("Documents")
    col1, col2 = st.columns(2)
    
    with col1:
        resume_file = st.file_uploader("Resume/CV*", type=['pdf', 'doc', 'docx'])
    
    with col2:
        cover_letter_file = st.file_uploader("Cover Letter (optional)", type=['pdf', 'doc', 'docx'])
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        headless = st.checkbox("Run in headless mode (no browser window)", value=False)
        screenshot = st.checkbox("Capture screenshots", value=True)
        retry_attempts = st.slider("Retry attempts", 1, 5, 3)
    
    # Submit button
    if st.button("🚀 Submit Application", type="primary"):
        # Validate required fields
        if not all([job_url, first_name, last_name, email, phone, resume_file]):
            st.error("Please fill in all required fields (*)")
        else:
            import asyncio
            import tempfile
            from pathlib import Path
            from automation.application_submitter import ApplicationSubmitter
            from automation.models import SubmissionConfig
            
            with st.spinner("Submitting application..."):
                try:
                    # Save uploaded files temporarily
                    with tempfile.TemporaryDirectory() as temp_dir:
                        resume_path = Path(temp_dir) / resume_file.name
                        with open(resume_path, 'wb') as f:
                            f.write(resume_file.getvalue())
                        
                        cover_letter_path = None
                        if cover_letter_file:
                            cover_letter_path = Path(temp_dir) / cover_letter_file.name
                            with open(cover_letter_path, 'wb') as f:
                                f.write(cover_letter_file.getvalue())
                        
                        # Create job dictionary
                        job = {
                            'id': job_id or 'dashboard_job',
                            'application_url': job_url
                        }
                        
                        # Create user profile
                        user_profile = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone': phone,
                            'linkedin_url': linkedin_url,
                            'github_url': github_url,
                            'city': city,
                            'state': state
                        }
                        
                        # Create config
                        config = SubmissionConfig(
                            headless=headless,
                            screenshot_on_error=screenshot,
                            screenshot_on_success=screenshot,
                            max_retries=retry_attempts
                        )
                        
                        # Submit application
                        async def submit():
                            with ApplicationSubmitter(config) as submitter:
                                return await submitter.submit_application(
                                    job=job,
                                    resume=str(resume_path),
                                    cover_letter=str(cover_letter_path) if cover_letter_path else None,
                                    user_profile=user_profile
                                )
                        
                        result = asyncio.run(submit())
                        
                        # Display result
                        if result.success:
                            st.success("✅ Application submitted successfully!")
                            st.info(f"**Platform:** {result.platform}")
                            st.info(f"**Job ID:** {result.job_id}")
                            if result.confirmation_number:
                                st.info(f"**Confirmation:** {result.confirmation_number}")
                            if result.screenshot_path:
                                st.info(f"**Screenshot:** {result.screenshot_path}")
                                try:
                                    from PIL import Image
                                    img = Image.open(result.screenshot_path)
                                    st.image(img, caption="Application Screenshot", use_column_width=True)
                                except:
                                    pass
                        else:
                            st.error("❌ Application submission failed")
                            st.error(f"**Error:** {result.error_message}")
                            st.info(f"**Platform:** {result.platform}")
                            st.info(f"**Status:** {result.status.value}")
                            if result.screenshot_path:
                                st.info(f"**Screenshot:** {result.screenshot_path}")
                                try:
                                    from PIL import Image
                                    img = Image.open(result.screenshot_path)
                                    st.image(img, caption="Error Screenshot", use_column_width=True)
                                except:
                                    pass
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())

# Tab 3: Phone Lookup
with tabs[2]:
    st.header("📞 Phone Lookup")
    from scrapers.osint.phone_lookup import lookup_phone, export_phone_result
    
    phone = st.text_input("Enter phone number")
    if st.button("Lookup Phone"):
        if phone:
            result = lookup_phone(phone)
            export_phone_result(result, phone)
            st.json(result)
        else:
            st.warning("Please enter a phone number")

# Tab 4: Digital Footprint
with tabs[3]:
    st.header("🕵️ Digital Footprint Trace")
    from scrapers.osint.footprint_trace import trace_footprint, export_footprint_result
    
    name = st.text_input("Enter full name")
    if st.button("Trace Footprint"):
        if name:
            result = trace_footprint(name)
            export_footprint_result(result, name)
            st.json(result)
        else:
            st.warning("Please enter a name")

# Tab 5: Breach Checker
with tabs[4]:
    st.header("🛡️ Email Breach Checker")
    from scrapers.osint.breach_checker import check_email_breach, export_breach_result
    
    email = st.text_input("Enter email address")
    if st.button("Check Breaches"):
        if email:
            result = check_email_breach(email)
            export_breach_result(result, email)
            st.json(result)
        else:
            st.warning("Please enter an email address")

# Tab 6: AI Feature Developer
with tabs[5]:
    st.header("🧠 AI Feature Developer")
    from ai_dev.feature_developer import generate_adapter
    
    site = st.text_input("Target site/domain (e.g., monster, ziprecruiter)")
    field = st.text_input("Field to extract (e.g., salary, benefits)")
    
    if st.button("Generate Adapter"):
        if site and field:
            code = generate_adapter(site, field)
            st.code(code, language="python")
            
            # Option to save
            save_path = f"adapters/{site}.py"
            if st.button("Save Adapter"):
                with open(save_path, "w") as f:
                    f.write(code)
                st.success(f"Adapter saved to {save_path}")
        else:
            st.warning("Please fill in all fields")

# Tab 7: About
with tabs[6]:
    st.header("📚 About")
    st.markdown("""
    ## OSINT + Job Scraping Dashboard
    
    This is a modular, stealth-capable scraping agent designed to extract job listings 
    from multiple career sites and automate application submissions. The system includes:
    
    - **Scraping Adapters**: Indeed, LinkedIn, Glassdoor
    - **Application Automation**: LinkedIn Easy Apply, Indeed, Greenhouse ATS, Generic
    - **OSINT Tools**: Phone lookup, digital footprint trace, breach checker
    - **AI Features**: LLM-powered adapter generation
    - **Stealth Capabilities**: Proxy rotation, fingerprint masking
    
    ### Features
    - Modular adapter system
    - Retry logic with fallback
    - Export to JSON/CSV
    - Centralized logging
    - Benchmark tracking
    
    ### Tech Stack
    - Python 3.11+
    - Streamlit
    - Playwright (for browser automation)
    - Pydantic (for data validation)
    
    Built for cybersecurity research and OSINT automation.
    """)
