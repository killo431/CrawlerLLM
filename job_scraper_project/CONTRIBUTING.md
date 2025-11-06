# Contributing to Job Scraper Project

Thank you for your interest in contributing to the Job Scraper Project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/killo431/CrawlerLLM/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach
   - Any relevant examples

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/killo431/CrawlerLLM.git
   cd CrawlerLLM/job_scraper_project
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   make install-dev
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation

5. **Run tests and linting**
   ```bash
   make test
   make lint
   make format-check
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Use conventional commit messages:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation changes
   - `test:` test additions/changes
   - `refactor:` code refactoring
   - `style:` code style changes
   - `chore:` maintenance tasks

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Ensure CI checks pass

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use black for code formatting
- Use isort for import sorting

```bash
# Format code
make format

# Check formatting
make format-check
```

### Testing

- Write unit tests for new features
- Maintain or improve code coverage
- Use pytest for testing
- Mock external dependencies

```bash
# Run tests
make test

# Run specific test file
pytest tests/test_module.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update README for significant changes
- Add inline comments for complex logic

Example docstring:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When and why this is raised
    """
    pass
```

### Type Hints

Use type hints throughout the codebase:

```python
from typing import List, Dict, Optional

def process_data(
    items: List[Dict[str, str]],
    threshold: Optional[int] = None
) -> List[str]:
    """Process data with type hints."""
    pass
```

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Don't catch exceptions silently

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise CustomException("User-friendly message") from e
```

### Logging

- Use appropriate log levels
- Include relevant context
- Don't log sensitive data

```python
logger.debug("Detailed information for debugging")
logger.info("General informational messages")
logger.warning("Warning messages for unusual situations")
logger.error("Error messages for failures")
logger.critical("Critical failures requiring immediate attention")
```

## Project Structure

When adding new features, follow the existing structure:

```
job_scraper_project/
├── adapters/          # New scrapers go here
├── core/              # Core functionality
├── scrapers/osint/    # OSINT tools
├── ai_dev/            # AI features
├── dashboard/         # UI components
├── tests/             # Test files (mirror source structure)
└── docs/              # Documentation
```

## Testing New Scrapers

When adding a new scraper:

1. Extend `BaseScraper` class
2. Implement required abstract methods
3. Add configuration to `config.yaml`
4. Write unit tests
5. Test with real and mock data
6. Update documentation

Example:
```python
from adapters.base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    """Scraper for NewSite job board."""
    
    def start_url(self) -> str:
        return "https://newsite.com/jobs"
    
    def extract_fields(self) -> List[Dict[str, Any]]:
        # Implementation
        pass
```

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow OWASP guidelines
- Report security issues privately

## Questions?

If you have questions:
1. Check existing documentation
2. Search closed issues
3. Create a new issue with `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- README.md
- Release notes
- Git commit history

Thank you for contributing! 🎉
