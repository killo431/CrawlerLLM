"""Browser automation with stealth capabilities."""
from playwright.sync_api import sync_playwright

def launch_stealth_browser():
    """Launch a browser with stealth patches to avoid detection."""
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        # Create new context
        context = browser.new_context()
        
        # Create new page
        page = context.new_page()
        
        # Apply stealth patches (navigator.webdriver masking, etc.)
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        return page
