"""Adapter benchmarking and performance metrics."""
import time
from core.logger import setup_logger

logger = setup_logger("benchmark")

def benchmark_adapter(adapter_class):
    """Benchmark a scraper adapter."""
    scraper = adapter_class()
    start = time.time()
    try:
        scraper.run()
        duration = time.time() - start
        logger.info(f"{adapter_class.__name__} completed in {duration:.2f}s")
        return {"adapter": adapter_class.__name__, "duration": duration}
    except Exception as e:
        logger.error(f"{adapter_class.__name__} failed: {e}")
        return {"adapter": adapter_class.__name__, "error": str(e)}
