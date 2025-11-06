"""Utility functions including retry logic."""
import time
import functools

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"[Retry] {func.__name__} failed: {e}")
                    time.sleep(delay * (backoff ** attempts))
                    attempts += 1
            print(f"[Retry] {func.__name__} failed after {max_attempts} attempts.")
            return None
        return wrapper
    return decorator
