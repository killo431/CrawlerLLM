"""Unit tests for configuration management."""
import pytest
from pathlib import Path
from core.config import Config, GlobalConfig, SiteConfig


def test_global_config_defaults():
    """Test GlobalConfig with default values."""
    config = GlobalConfig()
    assert config.output_format == "json"
    assert config.log_level == "INFO"
    assert config.max_retries == 3


def test_site_config_creation():
    """Test SiteConfig creation."""
    config = SiteConfig(
        base_url="https://example.com",
        crawl_delay=2.5,
        dynamic=True
    )
    assert config.base_url == "https://example.com"
    assert config.crawl_delay == 2.5
    assert config.dynamic is True


def test_config_use_defaults():
    """Test Config falls back to defaults when file not found."""
    config = Config(config_path="nonexistent.yaml")
    assert config.global_config is not None
    assert len(config.site_configs) > 0


def test_config_get_site_config():
    """Test retrieving site-specific config."""
    config = Config(config_path="nonexistent.yaml")
    indeed_config = config.get_site_config('indeed')
    
    assert indeed_config is not None
    assert isinstance(indeed_config, SiteConfig)
    assert 'indeed.com' in indeed_config.base_url


def test_config_get_missing_site():
    """Test retrieving config for non-existent site."""
    config = Config(config_path="nonexistent.yaml")
    missing = config.get_site_config('nonexistent_site')
    
    assert missing is None


def test_config_global_config():
    """Test getting global configuration."""
    config = Config(config_path="nonexistent.yaml")
    global_config = config.get_global_config()
    
    assert isinstance(global_config, GlobalConfig)
    assert global_config.output_format == "json"
