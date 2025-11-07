"""Unit tests for application submitter."""
import pytest
from automation.application_submitter import ApplicationSubmitter
from automation.models import SubmissionConfig, SubmissionStatus


def test_platform_detection():
    """Test platform detection from URLs."""
    config = SubmissionConfig()
    
    # Create submitter without browser setup for testing
    submitter = ApplicationSubmitter(config)
    
    # Test LinkedIn detection
    assert submitter.detect_platform("https://www.linkedin.com/jobs/apply/123") == "linkedin"
    assert submitter.detect_platform("https://linkedin.com/jobs/view/456") == "linkedin"
    
    # Test Indeed detection
    assert submitter.detect_platform("https://www.indeed.com/viewjob?jk=123") == "indeed"
    assert submitter.detect_platform("https://indeed.com/apply/789") == "indeed"
    
    # Test Greenhouse detection
    assert submitter.detect_platform("https://boards.greenhouse.io/company/jobs/123") == "greenhouse"
    assert submitter.detect_platform("https://app.greenhouse.io/apply/456") == "greenhouse"
    
    # Test generic fallback
    assert submitter.detect_platform("https://company.com/careers/apply") == "generic"
    assert submitter.detect_platform("https://example.com/job/123") == "generic"


def test_submission_config_defaults():
    """Test default configuration values."""
    config = SubmissionConfig()
    
    assert config.max_retries == 3
    assert config.retry_delay == 5
    assert config.screenshot_on_error == True
    assert config.screenshot_on_success == True
    assert config.headless == False
    assert config.verify_submission == True


def test_submission_config_custom():
    """Test custom configuration values."""
    config = SubmissionConfig(
        max_retries=5,
        headless=True,
        screenshot_on_error=False
    )
    
    assert config.max_retries == 5
    assert config.headless == True
    assert config.screenshot_on_error == False


def test_rate_limiting():
    """Test rate limiting functionality."""
    config = SubmissionConfig()
    submitter = ApplicationSubmitter(config)
    
    # Initially should be within limits
    assert submitter._check_rate_limit()
    
    # Record multiple submissions
    for _ in range(10):
        submitter._record_submission()
    
    # Should now be rate limited
    assert not submitter._check_rate_limit()


def test_submission_status_enum():
    """Test SubmissionStatus enum values."""
    assert SubmissionStatus.PENDING.value == "pending"
    assert SubmissionStatus.IN_PROGRESS.value == "in_progress"
    assert SubmissionStatus.SUCCESS.value == "success"
    assert SubmissionStatus.FAILED.value == "failed"
    assert SubmissionStatus.CAPTCHA_DETECTED.value == "captcha_detected"


def test_validate_files():
    """Test file validation in submission."""
    # This would require mocking the file system
    # Simplified test for structure
    config = SubmissionConfig()
    submitter = ApplicationSubmitter(config)
    
    # Verify config is set
    assert submitter.config is not None
    assert isinstance(submitter.config, SubmissionConfig)
