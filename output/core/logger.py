import time
from core.logger import setup_logger

logger = setup_logger("benchmark")

def benchmark_adapter(adapter_class):
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

📊 Dashboard Benchmark Tab
tab9 = st.tabs(["Adapter Benchmark"])[0]

with tab9:
    st.header("📈 Adapter Benchmark")
    from adapters.indeed import IndeedScraper
    from adapters.linkedin import LinkedInScraper
    from adapters.glassdoor import GlassdoorScraper
    from core.benchmark import benchmark_adapter

    if st.button("Run Benchmarks"):
        results = []
        for adapter in [IndeedScraper, LinkedInScraper, GlassdoorScraper]:
            result = benchmark_adapter(adapter)
            results.append(result)
        st.json(results)
