"""
Adaptive rate limiting module.

Provides intelligent rate limiting that adapts to platform responses.
"""
import time
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from core.logger import setup_logger

logger = setup_logger("rate_limiter")


class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that learns from platform responses.
    
    Features:
    1. Per-platform rate limiting
    2. Adaptive delays based on success/failure rates
    3. Exponential backoff on errors
    4. Random jitter to appear more human
    """
    
    def __init__(
        self,
        default_rate: int = 10,  # applications per hour
        min_delay: int = 30,  # minimum seconds between submissions
        max_delay: int = 300,  # maximum seconds between submissions
    ):
        """
        Initialize the rate limiter.
        
        Args:
            default_rate: Default applications per hour
            min_delay: Minimum delay between submissions (seconds)
            max_delay: Maximum delay between submissions (seconds)
        """
        self.default_rate = default_rate
        self.min_delay = min_delay
        self.max_delay = max_delay
        
        # Track submissions per platform
        self.platform_history: Dict[str, List[float]] = {}
        
        # Track errors per platform
        self.platform_errors: Dict[str, int] = {}
        
        # Adaptive delays per platform
        self.platform_delays: Dict[str, int] = {}
        
        # Last submission time per platform
        self.last_submission: Dict[str, float] = {}
    
    def record_submission(
        self,
        platform: str,
        success: bool = True,
        error_type: Optional[str] = None
    ):
        """
        Record a submission attempt.
        
        Args:
            platform: Platform name
            success: Whether submission was successful
            error_type: Type of error if failed
        """
        current_time = time.time()
        
        # Initialize platform history if needed
        if platform not in self.platform_history:
            self.platform_history[platform] = []
            self.platform_errors[platform] = 0
            self.platform_delays[platform] = self.min_delay
        
        # Record submission
        self.platform_history[platform].append(current_time)
        self.last_submission[platform] = current_time
        
        # Handle errors
        if not success:
            self.platform_errors[platform] += 1
            
            # Adjust delay based on error type
            if error_type == 'rate_limited':
                # Increase delay significantly
                self.platform_delays[platform] = min(
                    self.platform_delays[platform] * 2,
                    self.max_delay
                )
                logger.warning(f"Rate limit hit on {platform}, increased delay to {self.platform_delays[platform]}s")
            elif error_type == 'captcha':
                # Moderate increase
                self.platform_delays[platform] = min(
                    int(self.platform_delays[platform] * 1.5),
                    self.max_delay
                )
                logger.warning(f"CAPTCHA on {platform}, increased delay to {self.platform_delays[platform]}s")
            else:
                # Small increase for other errors
                self.platform_delays[platform] = min(
                    self.platform_delays[platform] + 10,
                    self.max_delay
                )
        else:
            # Successful submission - gradually reduce delay if it was increased
            if self.platform_delays[platform] > self.min_delay:
                self.platform_delays[platform] = max(
                    int(self.platform_delays[platform] * 0.9),
                    self.min_delay
                )
            
            # Reset error count on success
            self.platform_errors[platform] = max(0, self.platform_errors[platform] - 1)
    
    def check_rate_limit(self, platform: str) -> bool:
        """
        Check if we're within rate limits for a platform.
        
        Args:
            platform: Platform name
            
        Returns:
            True if within limits, False if rate limited
        """
        if platform not in self.platform_history:
            return True
        
        current_time = time.time()
        cutoff_time = current_time - 3600  # 1 hour ago
        
        # Remove old submissions
        self.platform_history[platform] = [
            t for t in self.platform_history[platform]
            if t > cutoff_time
        ]
        
        # Check rate
        submission_count = len(self.platform_history[platform])
        
        if submission_count >= self.default_rate:
            logger.warning(f"Rate limit reached for {platform}: {submission_count}/{self.default_rate} per hour")
            return False
        
        return True
    
    def get_required_delay(self, platform: str) -> float:
        """
        Get the required delay before next submission.
        
        Args:
            platform: Platform name
            
        Returns:
            Delay in seconds (with random jitter)
        """
        base_delay = self.platform_delays.get(platform, self.min_delay)
        
        # Add random jitter (±20%)
        jitter = random.uniform(-0.2, 0.2) * base_delay
        delay = base_delay + jitter
        
        # Ensure within bounds
        delay = max(self.min_delay, min(delay, self.max_delay))
        
        # Check last submission time
        if platform in self.last_submission:
            time_since_last = time.time() - self.last_submission[platform]
            if time_since_last < delay:
                return delay - time_since_last
        
        return delay
    
    def wait_if_needed(self, platform: str) -> float:
        """
        Wait if necessary before next submission.
        
        Args:
            platform: Platform name
            
        Returns:
            Actual wait time in seconds
        """
        required_delay = self.get_required_delay(platform)
        
        if required_delay > 0:
            logger.info(f"Waiting {required_delay:.1f}s before next {platform} submission")
            time.sleep(required_delay)
            return required_delay
        
        return 0
    
    def get_platform_stats(self, platform: str) -> Dict:
        """
        Get statistics for a platform.
        
        Args:
            platform: Platform name
            
        Returns:
            Dictionary with platform statistics
        """
        if platform not in self.platform_history:
            return {
                'total_submissions': 0,
                'submissions_last_hour': 0,
                'error_count': 0,
                'current_delay': self.min_delay,
                'rate_limit_status': 'OK'
            }
        
        current_time = time.time()
        cutoff_time = current_time - 3600
        
        recent_submissions = [
            t for t in self.platform_history[platform]
            if t > cutoff_time
        ]
        
        rate_limit_status = 'OK'
        if len(recent_submissions) >= self.default_rate:
            rate_limit_status = 'RATE_LIMITED'
        elif len(recent_submissions) >= self.default_rate * 0.8:
            rate_limit_status = 'WARNING'
        
        return {
            'total_submissions': len(self.platform_history[platform]),
            'submissions_last_hour': len(recent_submissions),
            'error_count': self.platform_errors.get(platform, 0),
            'current_delay': self.platform_delays.get(platform, self.min_delay),
            'rate_limit_status': rate_limit_status,
            'remaining_quota': self.default_rate - len(recent_submissions)
        }
    
    def reset_platform(self, platform: str):
        """
        Reset rate limiting for a platform.
        
        Args:
            platform: Platform name
        """
        if platform in self.platform_history:
            self.platform_history[platform] = []
        if platform in self.platform_errors:
            self.platform_errors[platform] = 0
        if platform in self.platform_delays:
            self.platform_delays[platform] = self.min_delay
        if platform in self.last_submission:
            del self.last_submission[platform]
        
        logger.info(f"Reset rate limiter for {platform}")
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """
        Get statistics for all platforms.
        
        Returns:
            Dictionary mapping platform to stats
        """
        stats = {}
        for platform in self.platform_history.keys():
            stats[platform] = self.get_platform_stats(platform)
        return stats
    
    def suggest_optimal_timing(self, platform: str) -> str:
        """
        Suggest optimal timing for submissions.
        
        Args:
            platform: Platform name
            
        Returns:
            Human-readable suggestion
        """
        stats = self.get_platform_stats(platform)
        
        if stats['rate_limit_status'] == 'RATE_LIMITED':
            # Calculate when quota will reset
            oldest_submission = min(self.platform_history[platform]) if self.platform_history[platform] else time.time()
            reset_time = oldest_submission + 3600
            wait_minutes = int((reset_time - time.time()) / 60)
            
            return f"Rate limit reached. Wait {wait_minutes} minutes for quota reset."
        
        elif stats['rate_limit_status'] == 'WARNING':
            return f"Approaching rate limit ({stats['submissions_last_hour']}/{self.default_rate}). Consider slowing down."
        
        else:
            remaining = stats['remaining_quota']
            delay = stats['current_delay']
            
            return f"OK to submit. {remaining} submissions remaining this hour. Current delay: {delay}s"
