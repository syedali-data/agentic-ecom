import time
import logging
from functools import wraps

def retry(max_attempts=3, delay=2, exceptions=(Exception,), logger=None):
    """
    Universal retry decorator with exponential backoff.
    Usage: @retry(max_attempts=5, delay=2)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    wait = delay * (2 ** (attempt - 1))  # exponential backoff
                    msg = f"[RETRY {attempt}] {func.__name__} failed: {e} - retrying in {wait:.2f}s"
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    if attempt == max_attempts:
                        raise
                    time.sleep(wait)
                    attempt += 1
        return wrapper
    return decorator
