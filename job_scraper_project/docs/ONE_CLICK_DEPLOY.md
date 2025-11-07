# One-Click Deployment & Launch Guide

## Overview

JobCopilot provides multiple one-click deployment options for quick setup and launch on any platform. Choose the method that best fits your environment.

---

## 🚀 Quick Start (Recommended)

### Option 1: Launch Script (Easiest)

#### On Linux/Mac:
```bash
cd job_scraper_project
./launch.sh
```

#### On Windows:
```cmd
cd job_scraper_project
launch.bat
```

**Features:**
- ✅ Automatic dependency installation
- ✅ Interactive menu to choose application
- ✅ Checks system requirements
- ✅ Installs Playwright browsers
- ✅ Creates .env file from template
- ✅ Launches selected application

**Menu Options:**
1. Home Page (Recommended) - http://localhost:8501
2. Configuration Wizard - http://localhost:8501
3. Main Dashboard - http://localhost:8501
4. Job Scraping Dashboard - http://localhost:8501
5. Demo Script

---

### Option 2: Make Commands (For Developers)

```bash
# Show all available commands
make help

# One-click launch with interactive menu
make launch

# Launch specific application
make home          # Home page
make wizard        # Configuration wizard
make main          # Main dashboard
make dashboard     # Job scraping dashboard
make demo          # Demo script

# Docker one-click
make docker-launch       # Launch home page in Docker
make docker-launch-all   # Launch all services
```

---

### Option 3: Docker Compose (For Production)

#### Launch Home Page Only (Default):
```bash
docker-compose up -d
```
Access at: http://localhost:8501

#### Launch All Applications:
```bash
docker-compose --profile wizard --profile dashboard --profile scraper up -d
```

**Port Mapping:**
- Home Page: http://localhost:8501
- Configuration Wizard: http://localhost:8502
- Main Dashboard: http://localhost:8503
- Job Scraping: http://localhost:8504

#### Stop All Services:
```bash
docker-compose down
```

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **pip**: Latest version
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum
- **Disk**: 1GB free space

### Optional (for Docker)
- **Docker**: 20.10 or higher
- **Docker Compose**: 1.29 or higher

---

## 🛠️ Installation Methods

### Method 1: Automated Installation (launch.sh)

The launch script handles everything automatically:
```bash
./launch.sh
```

**What it does:**
1. Checks Python version (3.11+)
2. Installs dependencies from requirements.txt
3. Installs Playwright browsers
4. Creates .env file if missing
5. Launches selected application

### Method 2: Manual Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Playwright browsers
python -m playwright install chromium

# 3. Create .env file (optional)
cp .env.example .env

# 4. Launch application
streamlit run dashboard/home.py
```

### Method 3: Docker Installation

```bash
# 1. Build image
docker-compose build

# 2. Launch
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f
```

---

## 🎯 Launch Options Explained

### 1. Home Page (Recommended)
**File:** `dashboard/home.py`  
**Port:** 8501  
**Best for:** All users, first-time setup

**Features:**
- Professional landing page
- Quick access to all features
- Feature highlights and statistics
- Getting started guide by user type

**Launch:**
```bash
# Script
./launch.sh
# Select option 1

# Direct
streamlit run dashboard/home.py

# Make
make home

# Docker
docker-compose up -d
```

---

### 2. Configuration Wizard
**File:** `dashboard/copilot_wizard.py`  
**Port:** 8502 (Docker) / 8501 (local)  
**Best for:** First-time users, guided setup

**Features:**
- 4-step guided configuration
- Job preferences setup
- Resume upload
- Writing style configuration

**Launch:**
```bash
# Script
./launch.sh
# Select option 2

# Direct
streamlit run dashboard/copilot_wizard.py

# Make
make wizard

# Docker
docker-compose --profile wizard up -d
```

---

### 3. Main Dashboard (JobCopilot)
**File:** `dashboard/jobcopilot_app.py`  
**Port:** 8503 (Docker) / 8501 (local)  
**Best for:** Experienced users, application generation

**Features:**
- AI application generation
- Stealth scoring
- Voice cloning
- Authenticity polish
- Advanced settings

**Launch:**
```bash
# Script
./launch.sh
# Select option 3

# Direct
streamlit run dashboard/jobcopilot_app.py

# Make
make main

# Docker
docker-compose --profile dashboard up -d
```

---

### 4. Job Scraping Dashboard
**File:** `dashboard/app.py`  
**Port:** 8504 (Docker) / 8501 (local)  
**Best for:** Job scraping, OSINT tools

**Features:**
- Job board scraping (Indeed, LinkedIn, Glassdoor)
- OSINT tools
- Export to JSON/CSV
- Application submission automation

**Launch:**
```bash
# Script
./launch.sh
# Select option 4

# Direct
streamlit run dashboard/app.py

# Make
make dashboard

# Docker
docker-compose --profile scraper up -d
```

---

### 5. Demo Script
**File:** `demo_jobcopilot.py`  
**Best for:** Testing features, CLI workflow

**Features:**
- Complete workflow demonstration
- AI generation example
- Stealth scoring example
- Voice cloning example

**Launch:**
```bash
# Script
./launch.sh
# Select option 5

# Direct
python demo_jobcopilot.py

# Make
make demo
```

---

## 🐳 Docker Deployment Details

### Single Service (Home Page)
```bash
docker-compose up -d
```

### Specific Service
```bash
# Wizard
docker-compose --profile wizard up -d

# Dashboard
docker-compose --profile dashboard up -d

# Scraper
docker-compose --profile scraper up -d
```

### All Services
```bash
docker-compose --profile wizard --profile dashboard --profile scraper up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f jobcopilot-home
docker-compose logs -f jobcopilot-wizard
docker-compose logs -f jobcopilot-dashboard
docker-compose logs -f job-scraper
```

### Stop Services
```bash
# Stop all
docker-compose down

# Stop specific
docker-compose stop jobcopilot-home
```

### Rebuild After Changes
```bash
docker-compose build
docker-compose up -d
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file (automatically created by launch script):
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

# Logging
LOG_LEVEL=INFO
```

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize:
```toml
[theme]
primaryColor = "#4314b6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
port = 8501
address = "0.0.0.0"
```

---

## 🌐 Network Access

### Local Access
- Home Page: http://localhost:8501
- Wizard: http://localhost:8502 (Docker)
- Dashboard: http://localhost:8503 (Docker)
- Scraper: http://localhost:8504 (Docker)

### Network Access
Replace `localhost` with your machine's IP address:
- Find IP: `ip addr show` (Linux) or `ipconfig` (Windows)
- Example: http://192.168.1.100:8501

### Cloud Deployment
For cloud deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📊 Health Checks

### Check Application Status
```bash
# Local
curl http://localhost:8501

# Docker
docker-compose ps
docker-compose logs jobcopilot-home
```

### Check Dependencies
```bash
pip list | grep streamlit
python -c "import streamlit; print(streamlit.__version__)"
```

### Check Playwright
```bash
python -m playwright --version
ls ~/.cache/ms-playwright/
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8501  # Mac/Linux
netstat -ano | findstr :8501  # Windows

# Use different port
streamlit run dashboard/home.py --server.port 8502
```

### Dependencies Not Installing
```bash
# Upgrade pip
pip install --upgrade pip

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Playwright Not Working
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright

# Install browsers with dependencies
python -m playwright install --with-deps chromium
```

### Docker Build Fails
```bash
# Clean build
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
```

### Permission Denied (launch.sh)
```bash
chmod +x launch.sh
./launch.sh
```

---

## 🚀 Production Deployment

### Best Practices
1. **Use Docker** for production
2. **Set environment variables** for API keys
3. **Enable HTTPS** with reverse proxy (nginx)
4. **Set resource limits** in docker-compose
5. **Configure logging** properly
6. **Set up monitoring** with healthchecks

### Example Production Setup
```yaml
# docker-compose.prod.yml
services:
  jobcopilot-home:
    build: .
    restart: always
    environment:
      - LOG_LEVEL=WARNING
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

Launch production:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 📈 Performance Optimization

### For Better Performance:
1. **Increase resources** (memory, CPU)
2. **Use SSD** for Docker volumes
3. **Enable caching** in Streamlit
4. **Limit concurrent users** if needed
5. **Use CDN** for static assets

### Monitoring
```bash
# Check resource usage
docker stats

# Check logs
docker-compose logs -f --tail=100

# Health check
curl http://localhost:8501/_stcore/health
```

---

## 🔒 Security Considerations

### Production Security:
1. **Change default ports**
2. **Use HTTPS/TLS**
3. **Set strong passwords**
4. **Restrict network access**
5. **Keep dependencies updated**
6. **Use secrets management**
7. **Enable rate limiting**

### Example nginx reverse proxy:
```nginx
server {
    listen 80;
    server_name jobcopilot.example.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 Additional Resources

- [Quick Start Guide](../QUICK_START.md)
- [Wizard Guide](WIZARD_GUIDE.md)
- [Full Documentation](../README.md)
- [Deployment Guide](../DEPLOYMENT.md)
- [Feature Roadmap](../../FEATURES_ROADMAP.md)

---

## 💡 Tips & Tricks

### Quick Commands
```bash
# Status check
make help

# Quick launch
./launch.sh

# Docker quick start
make docker-launch

# View all logs
make docker-logs

# Stop everything
make docker-stop
```

### Keyboard Shortcuts
- **Ctrl+C**: Stop server
- **Ctrl+R**: Refresh browser
- **R**: Rerun Streamlit app

### Development Mode
```bash
# Auto-reload on changes
streamlit run dashboard/home.py --server.runOnSave true

# Debug mode
streamlit run dashboard/home.py --logger.level debug
```

---

## 🎉 Success!

Once launched, you should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

Visit the URL in your browser to start using JobCopilot!

---

**Version**: 1.1.0  
**Last Updated**: November 2025  
**Status**: Production Ready

For help or issues, open a GitHub issue or check the documentation.
