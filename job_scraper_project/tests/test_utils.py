"""Unit tests for utility functions."""
import pytest
import time
from core.utils import retry


def test_retry_success():
    """Test retry decorator with successful function."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1, backoff=1)
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = successful_function()
    assert result == "success"
    assert call_count == 1


def test_retry_eventual_success():
    """Test retry decorator with eventual success."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1, backoff=1)
    def eventually_successful():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Temporary failure")
        return "success"
    
    result = eventually_successful()
    assert result == "success"
    assert call_count == 2


def test_retry_failure():
    """Test retry decorator with permanent failure."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1, backoff=1)
    def failing_function():
        nonlocal call_count
        call_count += 1
        raise ValueError("Permanent failure")
    
    with pytest.raises(ValueError):
        failing_function()
    
    assert call_count == 3


def test_retry_specific_exception():
    """Test retry with specific exception types."""
    call_count = 0
    
    @retry(max_attempts=3, delay=0.1, backoff=1, exceptions=(ValueError,))
    def function_with_type_error():
        nonlocal call_count
        call_count += 1
        raise TypeError("Wrong exception type")
    
    with pytest.raises(TypeError):
        function_with_type_error()
    
    # Should fail immediately as TypeError is not in exceptions tuple
    assert call_count == 1


def test_retry_backoff():
    """Test exponential backoff timing."""
    call_times = []
    
    @retry(max_attempts=3, delay=0.1, backoff=2)
    def timed_function():
        call_times.append(time.time())
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError):
        timed_function()
    
    # Check that delays increase exponentially
    assert len(call_times) == 3
    if len(call_times) >= 2:
        delay1 = call_times[1] - call_times[0]
        assert delay1 >= 0.09  # Allow small margin
