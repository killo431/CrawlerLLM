#!/usr/bin/env python3
"""
Script to analyze page_text (1).txt and separate it into distinct project components.
This will parse the conversation and extract:
1. Project requirements
2. Architecture/design documents
3. Code scaffolds and implementations
4. Configuration files
5. Documentation
"""

import os
import re
from pathlib import Path

def read_page_text(filename):
    """Read the page_text file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def identify_sections(lines):
    """Identify distinct sections in the conversation."""
    sections = {
        'requirements': [],
        'architecture': [],
        'code_python': [],
        'code_yaml': [],
        'documentation': [],
        'checklists': [],
        'project_structure': []
    }
    
    current_section = None
    buffer = []
    in_code_block = False
    code_language = None
    context_buffer = []  # Store previous lines for context
    
    for i, line in enumerate(lines):
        # Keep last 5 lines for context
        context_buffer.append(line)
        if len(context_buffer) > 5:
            context_buffer.pop(0)
        
        # Detect code blocks with various patterns
        # Pattern 1: Triple backticks
        if '```' in line:
            if not in_code_block:
                in_code_block = True
                # Extract language if specified
                lang_match = re.search(r'```(\w+)', line)
                if lang_match:
                    code_language = lang_match.group(1).lower()
                else:
                    # Try to infer language from context
                    context_str = ' '.join(context_buffer)
                    if any(word in context_str.lower() for word in ['python', '.py', 'def ', 'import ']):
                        code_language = 'python'
                    elif any(word in context_str.lower() for word in ['yaml', '.yaml', '.yml']):
                        code_language = 'yaml'
                continue
            else:
                in_code_block = False
                # Save accumulated code
                if buffer:
                    if not code_language:
                        # Try to infer from content
                        content = '\n'.join(buffer)
                        if any(keyword in content for keyword in ['def ', 'import ', 'class ', 'from ']):
                            code_language = 'python'
                    
                    if code_language in ['python', 'py', None]:  # Default to Python if unknown
                        sections['code_python'].append({
                            'line_start': i - len(buffer),
                            'content': '\n'.join(buffer),
                            'context': ' '.join(context_buffer[:3])  # Store context
                        })
                    elif code_language in ['yaml', 'yml']:
                        sections['code_yaml'].append({
                            'line_start': i - len(buffer),
                            'content': '\n'.join(buffer)
                        })
                buffer = []
                code_language = None
                continue
        
        # Pattern 2: "Python" or "Code" followed by "Copy"
        if line.strip() in ['Python', 'Code', 'Bash', 'JavaScript', 'Yaml', 'Http']:
            if i + 1 < len(lines) and lines[i+1].strip() == 'Copy':
                in_code_block = True
                code_language = line.strip().lower()
                continue
        
        # Pattern 3: Lines starting with "Copy" after a code indicator
        if line.strip() == 'Copy' and not in_code_block:
            # Check if previous line was a language indicator
            if i > 0:
                prev = lines[i-1].strip()
                if prev in ['Python', 'Code', 'Bash', 'JavaScript', 'Yaml']:
                    in_code_block = True
                    code_language = prev.lower()
            continue
        
        if in_code_block:
            # Skip "Copy" lines within code blocks
            if line.strip() == 'Copy':
                continue
            # End code block on certain markers
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                if line.strip().startswith('📁') or line.strip().startswith('✅'):
                    # This marks end of code
                    in_code_block = False
                    if buffer:
                        content = '\n'.join(buffer)
                        if any(keyword in content for keyword in ['def ', 'import ', 'class ', 'from ', '=']):
                            code_language = 'python'
                        sections['code_python'].append({
                            'line_start': i - len(buffer),
                            'content': content,
                            'context': ' '.join(context_buffer[:3])
                        })
                        buffer = []
                        code_language = None
                    continue
            buffer.append(line.rstrip())
            continue
        
        # Detect requirements sections
        if 'Requirements Gathering' in line or 'requirements.md' in line:
            current_section = 'requirements'
        elif 'Architecture' in line or 'Project Structure' in line:
            current_section = 'architecture'
        elif '[ ]' in line or '[x]' in line or '☐' in line or '✅' in line:
            current_section = 'checklists'
        elif re.match(r'^[\w\-_]+/', line):  # Project structure lines like "core/"
            current_section = 'project_structure'
        elif 'Documentation' in line or 'README' in line:
            current_section = 'documentation'
        
        # Accumulate content for current section
        if current_section and line.strip():
            sections[current_section].append(line.rstrip())
    
    return sections

def extract_project_structure(lines):
    """Extract the project file structure from the text."""
    structure = {}
    in_structure = False
    current_path = []
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        # Look for directory/file patterns
        if re.match(r'^[\w\-_]+/', line) or re.match(r'^├──|└──', line):
            in_structure = True
            
            # Parse tree structure
            depth = len(re.findall(r'[├└]──|│   ', line))
            name = re.sub(r'[├└]──|│   ', '', line).strip()
            
            if name:
                structure[name] = {
                    'depth': depth,
                    'type': 'directory' if name.endswith('/') else 'file'
                }
    
    return structure

def extract_code_files(sections):
    """Extract and organize code files from sections."""
    code_files = {}
    
    for i, code_block in enumerate(sections['code_python']):
        content = code_block['content']
        
        # Try to identify file name from context
        filename = f"extracted_code_{i}.py"
        
        # Look for file path comments or imports to deduce the file
        if 'dashboard/app.py' in content or 'streamlit' in content:
            filename = 'dashboard/app.py'
        elif 'core/browser.py' in content or 'playwright' in content:
            filename = 'core/browser.py'
        elif 'core/proxy.py' in content or 'PROXIES' in content:
            filename = 'core/proxy.py'
        elif 'core/logger.py' in content or 'setup_logger' in content:
            filename = 'core/logger.py'
        elif 'core/export_manager.py' in content or 'export_data' in content:
            filename = 'core/export_manager.py'
        elif 'core/benchmark.py' in content or 'benchmark_adapter' in content:
            filename = 'core/benchmark.py'
        elif 'adapters/base_scraper.py' in content or 'BaseScraper' in content:
            filename = 'adapters/base_scraper.py'
        elif 'adapters/indeed.py' in content or 'IndeedScraper' in content:
            filename = 'adapters/indeed.py'
        elif 'adapters/linkedin.py' in content or 'LinkedInScraper' in content:
            filename = 'adapters/linkedin.py'
        elif 'adapters/glassdoor.py' in content or 'GlassdoorScraper' in content:
            filename = 'adapters/glassdoor.py'
        elif 'ai_dev/feature_developer.py' in content or 'generate_adapter' in content:
            filename = 'ai_dev/feature_developer.py'
        elif 'phone_lookup' in content:
            filename = 'scrapers/osint/phone_lookup.py'
        elif 'footprint_trace' in content or 'trace_footprint' in content:
            filename = 'scrapers/osint/footprint_trace.py'
        elif 'breach_checker' in content or 'check_email_breach' in content:
            filename = 'scrapers/osint/breach_checker.py'
        
        code_files[filename] = content
    
    return code_files

def create_output_structure(base_dir='output'):
    """Create output directory structure."""
    dirs = [
        'core',
        'adapters',
        'scrapers/osint',
        'dashboard',
        'ai_dev',
        'data/output',
        'logs',
        'docs'
    ]
    
    for dir_path in dirs:
        Path(os.path.join(base_dir, dir_path)).mkdir(parents=True, exist_ok=True)
    
    return base_dir

def write_files(code_files, base_dir='output'):
    """Write extracted code files to disk."""
    created_files = []
    
    for filename, content in code_files.items():
        filepath = os.path.join(base_dir, filename)
        
        # Create parent directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(filepath)
        print(f"[Created] {filepath}")
    
    return created_files

def generate_readme(sections, base_dir='output'):
    """Generate a comprehensive README from documentation sections."""
    readme_content = """# OSINT + Job Scraping Dashboard

This project was automatically extracted and reconstructed from conversation data.

## Overview

This is a modular, stealth-capable scraping agent designed to extract job listings from multiple career sites. The system includes:

- **Scraping Adapters**: Indeed, LinkedIn, Glassdoor
- **OSINT Tools**: Phone lookup, digital footprint trace, breach checker
- **Dashboard**: Streamlit-based UI for all tools
- **AI Features**: LLM-powered adapter generation
- **Stealth Capabilities**: Proxy rotation, fingerprint masking

## Project Structure

"""
    
    # Add project structure if available
    if sections['project_structure']:
        readme_content += "\n```\n"
        readme_content += "\n".join(sections['project_structure'][:50])  # First 50 lines
        readme_content += "\n```\n\n"
    
    readme_content += """
## Requirements

```
streamlit
playwright
pydantic
loguru
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. Run the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## Features

### Job Scraping
- Modular adapter system for multiple job boards
- Retry logic with LLM fallback for broken selectors
- Export to JSON/CSV

### OSINT Tools
- Phone number lookup
- Digital footprint tracing
- Email breach checking

### Stealth Features
- Proxy rotation
- Custom headers
- Fingerprint masking
- Human behavior simulation

## Documentation

See the `docs/` directory for detailed documentation on:
- Adding new scraping adapters
- Configuration options
- Troubleshooting guide

## License

MIT License
"""
    
    readme_path = os.path.join(base_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"[Created] {readme_path}")
    return readme_path

def generate_requirements_txt(base_dir='output'):
    """Generate requirements.txt file."""
    requirements = """streamlit
playwright
pydantic
loguru
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
requests
beautifulsoup4
lxml
"""
    
    req_path = os.path.join(base_dir, 'requirements.txt')
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print(f"[Created] {req_path}")
    return req_path

def main():
    """Main execution function."""
    print("=" * 60)
    print("Analyzing page_text (1).txt")
    print("=" * 60)
    
    # Read the input file
    lines = read_page_text('page_text (1).txt')
    print(f"\n[Info] Read {len(lines)} lines from page_text (1).txt")
    
    # Identify sections
    print("\n[Info] Identifying sections...")
    sections = identify_sections(lines)
    
    for section, content in sections.items():
        if content:
            print(f"  - {section}: {len(content)} items")
    
    # Extract code files
    print("\n[Info] Extracting code files...")
    code_files = extract_code_files(sections)
    print(f"  - Found {len(code_files)} code files")
    
    # Create output structure
    print("\n[Info] Creating output directory structure...")
    base_dir = create_output_structure()
    
    # Write files
    print("\n[Info] Writing files...")
    created_files = write_files(code_files, base_dir)
    
    # Generate documentation
    print("\n[Info] Generating documentation...")
    generate_readme(sections, base_dir)
    generate_requirements_txt(base_dir)
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully created {len(created_files) + 2} files in '{base_dir}/' directory")
    print("=" * 60)
    print("\nProject structure has been rebuilt and organized!")
    print(f"Check the '{base_dir}/' directory for all extracted files.")

if __name__ == '__main__':
    main()
