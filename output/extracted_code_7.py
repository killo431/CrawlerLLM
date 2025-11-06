# Configures proxy settings for stealth scraping
def configure_proxy():
    # Example proxy configuration
    proxy = {
        "server": "http://proxy.example.com:8000",
        "username": "user",
        "password": "pass"
    }

    # Inject proxy into browser context (to be used in browser.py)
    return proxy
