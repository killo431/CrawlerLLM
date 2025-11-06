"""Configuration management module with type hints and validation."""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class GlobalConfig:
    """Global configuration settings."""
    output_format: str = "json"
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 30


@dataclass
class SiteConfig:
    """Site-specific configuration."""
    base_url: str
    crawl_delay: float = 2.0
    dynamic: bool = False
    selectors: Dict[str, str] = field(default_factory=dict)


class Config:
    """Configuration manager for the job scraper."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to configuration file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.global_config: Optional[GlobalConfig] = None
        self.site_configs: Dict[str, SiteConfig] = {}
        
        self.load()
    
    def load(self) -> None:
        """Load configuration from YAML file."""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file {self.config_path} not found, using defaults")
                self._use_defaults()
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
            
            # Parse global config
            global_data = self._config.get('global', {})
            self.global_config = GlobalConfig(**global_data)
            
            # Parse site configs
            for site_name, site_data in self._config.items():
                if site_name != 'global' and isinstance(site_data, dict):
                    self.site_configs[site_name] = SiteConfig(**site_data)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            self._use_defaults()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._use_defaults()
    
    def _use_defaults(self) -> None:
        """Use default configuration."""
        self.global_config = GlobalConfig()
        self.site_configs = {
            'indeed': SiteConfig(base_url="https://www.indeed.com/jobs?q=python"),
            'linkedin': SiteConfig(
                base_url="https://www.linkedin.com/jobs/search/?keywords=python",
                crawl_delay=3.0,
                dynamic=True
            ),
            'glassdoor': SiteConfig(
                base_url="https://www.glassdoor.com/Job/python-jobs",
                dynamic=True
            ),
        }
    
    def get_site_config(self, site_name: str) -> Optional[SiteConfig]:
        """
        Get configuration for a specific site.
        
        Args:
            site_name: Name of the site (e.g., 'indeed', 'linkedin')
            
        Returns:
            SiteConfig object or None if not found
        """
        return self.site_configs.get(site_name)
    
    def get_global_config(self) -> GlobalConfig:
        """Get global configuration."""
        return self.global_config or GlobalConfig()


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: str = "config.yaml") -> Config:
    """
    Get or create global configuration instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
