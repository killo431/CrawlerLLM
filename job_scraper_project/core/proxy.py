"""Proxy rotation and stealth headers."""
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
    """Get a random proxy from the pool."""
    return random.choice(PROXIES)

def apply_stealth_headers(context):
    """Apply stealth headers to browser context."""
    context.set_extra_http_headers(STEALTH_HEADERS)
