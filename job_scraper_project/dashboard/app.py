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

# Tab 2: Phone Lookup
with tabs[1]:
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

# Tab 3: Digital Footprint
with tabs[2]:
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

# Tab 4: Breach Checker
with tabs[3]:
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

# Tab 5: AI Feature Developer
with tabs[4]:
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

# Tab 6: About
with tabs[5]:
    st.header("📚 About")
    st.markdown("""
    ## OSINT + Job Scraping Dashboard
    
    This is a modular, stealth-capable scraping agent designed to extract job listings 
    from multiple career sites. The system includes:
    
    - **Scraping Adapters**: Indeed, LinkedIn, Glassdoor
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
