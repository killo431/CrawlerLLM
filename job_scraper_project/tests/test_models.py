"""Unit tests for automation models."""
import pytest
from datetime import datetime
from automation.models import (
    SubmissionResult,
    SubmissionStatus,
    ApplicationData,
    FormField,
    FieldType,
    NavigationState,
    SubmissionConfig
)


def test_submission_result_creation():
    """Test SubmissionResult creation."""
    result = SubmissionResult(
        success=True,
        job_id='test_job_123',
        platform='linkedin',
        status=SubmissionStatus.SUCCESS
    )
    
    assert result.success == True
    assert result.job_id == 'test_job_123'
    assert result.platform == 'linkedin'
    assert result.status == SubmissionStatus.SUCCESS
    assert result.submitted_at is not None


def test_submission_result_failure():
    """Test SubmissionResult for failure case."""
    result = SubmissionResult(
        success=False,
        job_id='test_job_456',
        platform='indeed',
        error_message='Connection timeout'
    )
    
    assert result.success == False
    assert result.error_message == 'Connection timeout'
    assert result.status == SubmissionStatus.FAILED


def test_application_data_creation():
    """Test ApplicationData creation."""
    data = ApplicationData(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='555-0123'
    )
    
    assert data.first_name == 'John'
    assert data.last_name == 'Doe'
    assert data.email == 'john.doe@example.com'
    assert data.phone == '555-0123'


def test_application_data_to_dict():
    """Test ApplicationData to_dict method."""
    data = ApplicationData(
        first_name='Jane',
        last_name='Smith',
        email='jane@example.com',
        phone='555-9999',
        city='San Francisco',
        state='CA'
    )
    
    data_dict = data.to_dict()
    
    assert data_dict['first_name'] == 'Jane'
    assert data_dict['last_name'] == 'Smith'
    assert data_dict['full_name'] == 'Jane Smith'
    assert data_dict['email'] == 'jane@example.com'
    assert data_dict['city'] == 'San Francisco'
    assert data_dict['state'] == 'CA'


def test_application_data_optional_fields():
    """Test ApplicationData with optional fields."""
    data = ApplicationData(
        first_name='Test',
        last_name='User',
        email='test@example.com',
        phone='555-0000',
        linkedin_url='https://linkedin.com/in/testuser',
        github_url='https://github.com/testuser',
        years_of_experience=5
    )
    
    assert data.linkedin_url == 'https://linkedin.com/in/testuser'
    assert data.github_url == 'https://github.com/testuser'
    assert data.years_of_experience == 5


def test_navigation_state_initialization():
    """Test NavigationState initialization."""
    state = NavigationState()
    
    assert state.current_step == 0
    assert state.total_steps == 1
    assert state.can_go_next == True
    assert state.can_go_back == False
    assert state.is_final_step == False


def test_navigation_state_advance():
    """Test NavigationState advance_step."""
    state = NavigationState(total_steps=3)
    
    assert state.current_step == 0
    
    state.advance_step()
    assert state.current_step == 1
    assert 0 in state.completed_steps
    
    state.advance_step()
    assert state.current_step == 2
    assert state.is_final_step == True


def test_navigation_state_go_back():
    """Test NavigationState go_back."""
    state = NavigationState(total_steps=3, current_step=2)
    state.can_go_back = True
    
    state.go_back()
    assert state.current_step == 1
    assert state.is_final_step == False


def test_navigation_state_string():
    """Test NavigationState __str__ method."""
    state = NavigationState(current_step=1, total_steps=5)
    
    state_str = str(state)
    assert '2/5' in state_str  # current_step is 0-indexed


def test_submission_config_defaults():
    """Test SubmissionConfig default values."""
    config = SubmissionConfig()
    
    assert config.max_retries == 3
    assert config.retry_delay == 5
    assert config.page_load_timeout == 30
    assert config.element_timeout == 10
    assert config.screenshot_on_error == True
    assert config.screenshot_on_success == True
    assert config.headless == False
    assert config.slow_mo == 100


def test_submission_config_custom():
    """Test SubmissionConfig with custom values."""
    config = SubmissionConfig(
        max_retries=5,
        headless=True,
        screenshot_on_error=False,
        slow_mo=200
    )
    
    assert config.max_retries == 5
    assert config.headless == True
    assert config.screenshot_on_error == False
    assert config.slow_mo == 200


def test_submission_status_enum():
    """Test all SubmissionStatus enum values."""
    assert SubmissionStatus.PENDING.value == 'pending'
    assert SubmissionStatus.IN_PROGRESS.value == 'in_progress'
    assert SubmissionStatus.SUCCESS.value == 'success'
    assert SubmissionStatus.FAILED.value == 'failed'
    assert SubmissionStatus.CAPTCHA_DETECTED.value == 'captcha_detected'
    assert SubmissionStatus.MANUAL_INTERVENTION_REQUIRED.value == 'manual_intervention_required'
    assert SubmissionStatus.RATE_LIMITED.value == 'rate_limited'
    assert SubmissionStatus.PLATFORM_ERROR.value == 'platform_error'


def test_field_type_enum():
    """Test all FieldType enum values."""
    assert FieldType.TEXT.value == 'text'
    assert FieldType.EMAIL.value == 'email'
    assert FieldType.PHONE.value == 'phone'
    assert FieldType.URL.value == 'url'
    assert FieldType.FILE.value == 'file'
    assert FieldType.SELECT.value == 'select'
    assert FieldType.CHECKBOX.value == 'checkbox'
    assert FieldType.RADIO.value == 'radio'
    assert FieldType.TEXTAREA.value == 'textarea'
    assert FieldType.DATE.value == 'date'
    assert FieldType.NUMBER.value == 'number'
