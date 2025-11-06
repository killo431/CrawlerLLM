# Makefile for common development tasks

.PHONY: help install install-dev test lint format clean docker-build docker-run

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt
	playwright install chromium

install-dev:  ## Install development dependencies
	pip install -r requirements.txt -r requirements-dev.txt
	playwright install chromium
	pre-commit install

test:  ## Run tests with coverage
	pytest tests/ -v --cov=. --cov-report=term --cov-report=html

lint:  ## Run linters
	flake8 .
	mypy . --ignore-missing-imports

format:  ## Format code with black and isort
	black .
	isort .

format-check:  ## Check code formatting
	black --check --diff .
	isort --check-only --diff .

clean:  ## Clean build artifacts and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

docker-build:  ## Build Docker image
	docker build -t job-scraper:latest .

docker-run:  ## Run Docker container
	docker-compose up -d

docker-stop:  ## Stop Docker container
	docker-compose down

docker-logs:  ## Show Docker logs
	docker-compose logs -f

run:  ## Run the CLI scraper
	python main.py

dashboard:  ## Run the Streamlit dashboard
	streamlit run dashboard/app.py

.DEFAULT_GOAL := help
