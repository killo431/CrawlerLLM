"""Centralized logging module with improved error handling and type hints."""
import logging
import os
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "scraper",
    level: int = logging.INFO,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.
    
    Args:
        name: Logger name (used for log file name)
        level: Logging level (default: logging.INFO)
        log_dir: Directory to store log files
        
    Returns:
        Configured logger instance
        
    Raises:
        OSError: If log directory cannot be created
    """
    try:
        # Create log directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger(name)
        
        # Avoid adding handlers multiple times
        if logger.hasHandlers():
            return logger
            
        logger.setLevel(level)
        
        # File handler with rotation
        log_file = log_path / f"{name}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(level)
        
        # Console handler (info and above)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Detailed formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        logger.info(f"Logger '{name}' initialized successfully")
        return logger
        
    except Exception as e:
        # Fallback to console-only logger if file logging fails
        fallback_logger = logging.getLogger(name)
        fallback_logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fallback_logger.addHandler(ch)
        fallback_logger.error(f"Failed to setup file logging: {e}")
        return fallback_logger
