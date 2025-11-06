# Add this to main.py to support multiple adapters
from adapters.indeed import IndeedScraper
from adapters.linkedin import LinkedInScraper
from adapters.glassdoor import GlassdoorScraper

def get_scraper(site: str, page):
    if site == "indeed":
        return IndeedScraper(page)
    elif site == "linkedin":
        return LinkedInScraper(page)
    elif site == "glassdoor":
        return GlassdoorScraper(page)
    else:
        raise ValueError(f"Unsupported site: {site}")

🧩 CLI or Config-Based Site Selection

Update main.py to accept a site name from CLI or config:

import sys

# Get site name from CLI or default to 'indeed'
site = sys.argv[1] if len(sys.argv) > 1 else "indeed"
scraper = get_scraper(site, page)

🧠 LLM Fallback Logic in llm_brain.py
def suggest_selector(html: str, field_name: str) -> str:
    try:
        prompt = f"Given this HTML, find the best CSS selector for '{field_name}':\n{html}"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        selector = response.json()["response"].strip()
        if not selector or "error" in selector.lower():
            raise ValueError("Invalid selector from LLM")
        return selector
    except Exception as e:
        print(f"LLM fallback triggered: {e}")
        return ".default-selector"  # fallback static selector
