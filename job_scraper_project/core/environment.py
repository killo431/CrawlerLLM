"""Environment variable management with validation."""
import os
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Environment:
    """Manage environment variables with defaults."""
    
    def __init__(self):
        """Initialize environment configuration."""
        self._load_env_file()
    
    def _load_env_file(self) -> None:
        """Load variables from .env file if it exists."""
        env_file = Path('.env')
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if not line or line.startswith('#'):
                            continue
                        # Parse key=value
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Don't override existing environment variables
                            if key not in os.environ:
                                os.environ[key] = value
                logger.info("Environment variables loaded from .env file")
            except Exception as e:
                logger.warning(f"Could not load .env file: {e}")
    
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Value of environment variable or default
        """
        return os.environ.get(key, default)
    
    @staticmethod
    def get_int(key: str, default: int) -> int:
        """
        Get environment variable as integer.
        
        Args:
            key: Environment variable name
            default: Default value if not found or invalid
            
        Returns:
            Integer value of environment variable or default
        """
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Invalid integer value for {key}: {value}, using default: {default}")
            return default
    
    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """
        Get environment variable as boolean.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Boolean value of environment variable or default
        """
        value = os.environ.get(key, '').lower()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
        return default
    
    @property
    def app_name(self) -> str:
        """Get application name."""
        return self.get('APP_NAME', 'job-scraper')
    
    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.get('LOG_LEVEL', 'INFO')
    
    @property
    def output_format(self) -> str:
        """Get output format."""
        return self.get('OUTPUT_FORMAT', 'json')
    
    @property
    def max_retries(self) -> int:
        """Get max retries."""
        return self.get_int('MAX_RETRIES', 3)
    
    @property
    def timeout(self) -> int:
        """Get timeout in seconds."""
        return self.get_int('TIMEOUT', 30)


# Global environment instance
_env_instance: Optional[Environment] = None


def get_env() -> Environment:
    """
    Get or create global environment instance.
    
    Returns:
        Environment instance
    """
    global _env_instance
    if _env_instance is None:
        _env_instance = Environment()
    return _env_instance
