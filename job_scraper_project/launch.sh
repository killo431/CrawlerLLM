#!/bin/bash
# JobCopilot One-Click Launch Script
# This script installs dependencies and launches the application

set -e  # Exit on error

echo "=========================================="
echo "🚀 JobCopilot One-Click Launch"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.11 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python 3.11 or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip3 detected${NC}"

# Function to check if package is installed
check_package() {
    python3 -c "import $1" 2>/dev/null
}

# Install dependencies if not already installed
echo ""
echo -e "${YELLOW}Checking dependencies...${NC}"

if check_package "streamlit"; then
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
else
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${RED}Error: Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Install Playwright browsers if needed
echo ""
echo -e "${YELLOW}Checking Playwright browsers...${NC}"

if [ ! -d "$HOME/.cache/ms-playwright" ]; then
    echo -e "${YELLOW}Installing Playwright browsers (this may take a few minutes)...${NC}"
    python3 -m playwright install chromium
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Playwright browsers installed${NC}"
    else
        echo -e "${YELLOW}Warning: Failed to install Playwright browsers${NC}"
        echo -e "${YELLOW}Job scraping features may not work${NC}"
    fi
else
    echo -e "${GREEN}✓ Playwright browsers already installed${NC}"
fi

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo ""
        echo -e "${YELLOW}Creating .env file from template...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo -e "${YELLOW}Note: Edit .env file to add your API keys${NC}"
    fi
fi

# Ask which app to launch
echo ""
echo "=========================================="
echo "Select application to launch:"
echo "=========================================="
echo "1) Home Page (Recommended)"
echo "2) Configuration Wizard"
echo "3) Main Dashboard (JobCopilot)"
echo "4) Job Scraping Dashboard"
echo "5) Demo Script"
echo ""
read -p "Enter your choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Launching Home Page...${NC}"
        echo ""
        echo "=========================================="
        echo "Access the application at:"
        echo "http://localhost:8501"
        echo "=========================================="
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        streamlit run dashboard/home.py
        ;;
    2)
        echo ""
        echo -e "${GREEN}⚙️ Launching Configuration Wizard...${NC}"
        echo ""
        echo "=========================================="
        echo "Access the wizard at:"
        echo "http://localhost:8501"
        echo "=========================================="
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        streamlit run dashboard/copilot_wizard.py
        ;;
    3)
        echo ""
        echo -e "${GREEN}📝 Launching Main Dashboard...${NC}"
        echo ""
        echo "=========================================="
        echo "Access the dashboard at:"
        echo "http://localhost:8501"
        echo "=========================================="
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        streamlit run dashboard/jobcopilot_app.py
        ;;
    4)
        echo ""
        echo -e "${GREEN}🔍 Launching Job Scraping Dashboard...${NC}"
        echo ""
        echo "=========================================="
        echo "Access the dashboard at:"
        echo "http://localhost:8501"
        echo "=========================================="
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        streamlit run dashboard/app.py
        ;;
    5)
        echo ""
        echo -e "${GREEN}🎯 Running Demo Script...${NC}"
        echo ""
        python3 demo_jobcopilot.py
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac
