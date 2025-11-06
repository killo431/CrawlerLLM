"""Health check and monitoring utilities for production deployment."""
import time
import psutil
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class HealthCheck:
    """System health check for production monitoring."""
    
    def __init__(self):
        """Initialize health check system."""
        self.start_time = time.time()
        self.checks_performed = 0
    
    def get_uptime(self) -> float:
        """
        Get system uptime in seconds.
        
        Returns:
            Uptime in seconds
        """
        return time.time() - self.start_time
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get current memory usage statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        memory = psutil.virtual_memory()
        return {
            "total_mb": memory.total / (1024 * 1024),
            "available_mb": memory.available / (1024 * 1024),
            "used_mb": memory.used / (1024 * 1024),
            "percent": memory.percent
        }
    
    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage percentage.
        
        Returns:
            CPU usage percentage
        """
        return psutil.cpu_percent(interval=1)
    
    def get_disk_usage(self, path: str = "/") -> Dict[str, float]:
        """
        Get disk usage statistics.
        
        Args:
            path: Path to check disk usage for
            
        Returns:
            Dictionary with disk statistics
        """
        try:
            disk = psutil.disk_usage(path)
            return {
                "total_gb": disk.total / (1024 ** 3),
                "used_gb": disk.used / (1024 ** 3),
                "free_gb": disk.free / (1024 ** 3),
                "percent": disk.percent
            }
        except Exception as e:
            logger.error(f"Failed to get disk usage: {e}")
            return {"error": str(e)}
    
    def check_health(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Dictionary with health status and metrics
        """
        self.checks_performed += 1
        
        try:
            status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "uptime_seconds": self.get_uptime(),
                "checks_performed": self.checks_performed,
                "system": {
                    "memory": self.get_memory_usage(),
                    "cpu_percent": self.get_cpu_usage(),
                    "disk": self.get_disk_usage()
                }
            }
            
            # Check if system is under stress
            memory = self.get_memory_usage()
            cpu = self.get_cpu_usage()
            
            if memory["percent"] > 90 or cpu > 90:
                status["status"] = "degraded"
                status["warnings"] = []
                if memory["percent"] > 90:
                    status["warnings"].append(f"High memory usage: {memory['percent']:.1f}%")
                if cpu > 90:
                    status["warnings"].append(f"High CPU usage: {cpu:.1f}%")
            
            logger.info(f"Health check performed: {status['status']}")
            return status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


# Global health check instance
_health_check: HealthCheck = None


def get_health_check() -> HealthCheck:
    """
    Get or create global health check instance.
    
    Returns:
        HealthCheck instance
    """
    global _health_check
    if _health_check is None:
        _health_check = HealthCheck()
    return _health_check
