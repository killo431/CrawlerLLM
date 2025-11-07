# Multi-stage build for production-ready Docker image
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 scraper && \
    mkdir -p /app /app/data/output /app/logs && \
    chown -R scraper:scraper /app

# Install runtime dependencies including playwright browsers
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY --chown=scraper:scraper . .

# Install playwright browsers (as root, before switching to scraper user)
RUN python -m playwright install --with-deps chromium

# Switch to non-root user
USER scraper

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command - Launch home page (can be overridden)
CMD ["streamlit", "run", "dashboard/home.py", "--server.address", "0.0.0.0"]
