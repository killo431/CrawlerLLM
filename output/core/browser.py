import random

PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080"
]

STEALTH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}

def get_random_proxy():
    return random.choice(PROXIES)

def apply_stealth_headers(context):
    context.set_extra_http_headers(STEALTH_HEADERS)

🔁 Integration in core/browser.py
from core.proxy import get_random_proxy, apply_stealth_headers

proxy = get_random_proxy()
browser = playwright.chromium.launch(headless=False, proxy={"server": proxy})
context = browser.new_context()
apply_stealth_headers(context)
