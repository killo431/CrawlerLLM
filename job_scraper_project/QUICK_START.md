# Quick Start Guide - JobCopilot

## Installation

```bash
# Clone the repository
git clone https://github.com/killo431/CrawlerLLM.git
cd CrawlerLLM/job_scraper_project

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Running the Application

### Option 1: Home Page (Recommended)
```bash
streamlit run dashboard/home.py
```

This launches the main landing page with quick access to:
- Configuration Wizard
- Application Generator
- Job Scraping

### Option 2: Configuration Wizard (First-Time Setup)
```bash
streamlit run dashboard/copilot_wizard.py
```

Complete the 4-step setup:
1. Job preferences (location, types, titles)
2. Optional filters (experience, salary)
3. Resume upload
4. Writing style preferences

### Option 3: Main Dashboard (Experienced Users)
```bash
streamlit run dashboard/jobcopilot_app.py
```

Direct access to:
- Application generation
- Stealth scoring
- Voice cloning
- Authenticity polish

### Option 4: Job Scraping Dashboard
```bash
streamlit run dashboard/app.py
```

For job scraping and OSINT tools.

## Features Overview

### 🆕 NEW: Configuration Wizard
Multi-step guided setup based on AiCopilotCFG UX pattern:
- Progressive disclosure (4 steps)
- Input validation
- Progress indicators
- Configuration persistence

### 🎯 Core Features
- **Stealth Engine**: Gemini 2.5 Pro (53% detection rate)
- **Stealth Score**: Real-time AI detection analysis
- **Voice Cloning**: Personalized writing models
- **Authenticity Polish**: Guided document improvement
- **Job Scraping**: Indeed, LinkedIn, Glassdoor

## Quick Usage Examples

### Generate Your First Application

1. **Launch the home page:**
   ```bash
   streamlit run dashboard/home.py
   ```

2. **Click "Start Setup →"** to launch the Configuration Wizard

3. **Complete the 4 steps:**
   - Step 1: Select job preferences
   - Step 2: Set optional filters (can skip)
   - Step 3: Upload your resume
   - Step 4: Choose writing style

4. **Generate application** from the main dashboard

5. **Check Stealth Score** (target: <20%)

6. **Polish if needed** using Authenticity Wizard

7. **Download and submit!**

### Scrape Jobs

1. **Launch dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

2. **Select job board** (Indeed, LinkedIn, Glassdoor)

3. **Click "Start Scraping"**

4. **Export results** to JSON or CSV

### Train Voice Model

1. **Go to Voice Cloning tab** in main dashboard

2. **Upload 3-5 writing samples:**
   - Old cover letters
   - Professional emails
   - Reports or essays

3. **Click "Train Voice Model"**

4. **Use trained model** for personalized applications

## File Structure

```
job_scraper_project/
├── dashboard/
│   ├── home.py              # 🆕 Landing page
│   ├── copilot_wizard.py    # 🆕 Configuration wizard
│   ├── jobcopilot_app.py    # Main dashboard
│   └── app.py               # Job scraping dashboard
├── docs/
│   ├── WIZARD_GUIDE.md      # 🆕 Wizard documentation
│   └── UX_IMPROVEMENTS.md   # 🆕 UX design decisions
├── .streamlit/
│   └── config.toml          # 🆕 Theme configuration
└── README.md                # Full documentation
```

## Common Commands

### Development
```bash
# Run tests
pytest tests/

# Run demo
python demo_jobcopilot.py

# Format code
black .

# Lint code
flake8
```

### Production
```bash
# Docker build
docker-compose up

# Run in production mode
streamlit run dashboard/home.py --server.port 8501
```

## Configuration

### Environment Variables
Create a `.env` file:
```env
# API Keys (optional)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Browser settings
HEADLESS_MODE=true
SCREENSHOT_ON_ERROR=true

# Database (optional)
DATABASE_URL=sqlite:///jobcopilot.db
```

### Streamlit Configuration
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Playwright not installed" error
```bash
playwright install
```

### Port already in use
```bash
# Use different port
streamlit run dashboard/home.py --server.port 8502
```

### Session state issues
- Refresh browser (Ctrl+R / Cmd+R)
- Clear browser cache
- Restart Streamlit server

## Getting Help

- 📖 [Full Documentation](README.md)
- 🎯 [Wizard Guide](docs/WIZARD_GUIDE.md)
- 🎨 [UX Improvements](docs/UX_IMPROVEMENTS.md)
- 🗺️ [Feature Roadmap](../FEATURES_ROADMAP.md)
- 📋 [Implementation Plan](../IMPLEMENTATION_PLAN.md)

## What's New in v1.1

### 🆕 New Features
- ⚙️ Multi-step Configuration Wizard (4 steps)
- 🏠 Professional Home/Landing Page
- 🎨 Custom theme matching AiCopilotCFG design
- 📊 Enhanced statistics and metrics display
- 🔄 Improved workflow visualization

### 🔧 Improvements
- Better navigation between pages
- Clearer progress indicators
- Enhanced form validation
- Improved mobile responsiveness
- Better error messages

### 📚 Documentation
- Comprehensive wizard guide
- UX improvement documentation
- Quick start guide (this file)
- Updated README

## Next Steps

1. ✅ Complete wizard setup
2. ✅ Generate first application
3. ✅ Check stealth score
4. ✅ Train voice model (3-5 samples)
5. ✅ Polish documents if needed
6. ✅ Submit applications!

---

**Version**: 1.1.0  
**Last Updated**: November 2025  
**Status**: Production Ready

For more information, see the [Full README](README.md)
