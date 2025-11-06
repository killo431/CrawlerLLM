"""Centralized logging module."""
import logging
import os

def setup_logger(name="scraper", level=logging.INFO, log_dir="logs"):
    """Set up a logger with file and console handlers."""
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    fh = logging.FileHandler(f"{log_dir}/{name}.log")
    fh.setLevel(level)
    
    # Console handler (only errors)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
