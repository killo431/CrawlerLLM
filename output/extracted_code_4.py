# Entry point for the stealth scraping agent
from core.browser import launch_stealth_browser
from core.behavior import simulate_human_interaction
from core.proxy import configure_proxy
from core.session import persist_session, load_session
from core.llm_brain import suggest_selector

def run_scraper():
    # Launch browser with stealth patches
    page = launch_stealth_browser()

    # Simulate human-like behavior to reduce bot detection
    simulate_human_interaction(page)

    # Navigate to target job board
    page.goto("https://www.example-job-board.com")

    # Extract HTML for LLM-based selector suggestion
    html = page.content()
    selector = suggest_selector(html, "job_title", model="gpt-4")

    # Use selector to extract job title
    job_title = page.locator(selector).inner_text()
    print("Extracted Job Title:", job_title)

    # Save session for reuse
    persist_session(page.context)

if __name__ == "__main__":
    run_scraper()
