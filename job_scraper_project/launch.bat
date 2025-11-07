@echo off
REM JobCopilot One-Click Launch Script for Windows
REM This script installs dependencies and launches the application

echo ==========================================
echo  JobCopilot One-Click Launch
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed
    echo Please install Python 3.11 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed
    pause
    exit /b 1
)

echo [OK] pip detected
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
)

echo.

REM Install Playwright browsers if needed
if not exist "%USERPROFILE%\.cache\ms-playwright" (
    echo Installing Playwright browsers...
    python -m playwright install chromium
    if errorlevel 1 (
        echo [WARNING] Failed to install Playwright browsers
        echo Job scraping features may not work
    ) else (
        echo [OK] Playwright browsers installed
    )
) else (
    echo [OK] Playwright browsers already installed
)

REM Create .env file if it doesn't exist
if not exist .env (
    if exist .env.example (
        echo Creating .env file from template...
        copy .env.example .env >nul
        echo [OK] .env file created
        echo [NOTE] Edit .env file to add your API keys
    )
)

echo.
echo ==========================================
echo Select application to launch:
echo ==========================================
echo 1. Home Page (Recommended)
echo 2. Configuration Wizard
echo 3. Main Dashboard (JobCopilot)
echo 4. Job Scraping Dashboard
echo 5. Demo Script
echo.

set /p choice="Enter your choice [1-5]: "

if "%choice%"=="1" (
    echo.
    echo Launching Home Page...
    echo.
    echo ==========================================
    echo Access the application at:
    echo http://localhost:8501
    echo ==========================================
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run dashboard/home.py
) else if "%choice%"=="2" (
    echo.
    echo Launching Configuration Wizard...
    echo.
    echo ==========================================
    echo Access the wizard at:
    echo http://localhost:8501
    echo ==========================================
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run dashboard/copilot_wizard.py
) else if "%choice%"=="3" (
    echo.
    echo Launching Main Dashboard...
    echo.
    echo ==========================================
    echo Access the dashboard at:
    echo http://localhost:8501
    echo ==========================================
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run dashboard/jobcopilot_app.py
) else if "%choice%"=="4" (
    echo.
    echo Launching Job Scraping Dashboard...
    echo.
    echo ==========================================
    echo Access the dashboard at:
    echo http://localhost:8501
    echo ==========================================
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run dashboard/app.py
) else if "%choice%"=="5" (
    echo.
    echo Running Demo Script...
    echo.
    python demo_jobcopilot.py
    pause
) else (
    echo [ERROR] Invalid choice. Exiting.
    pause
    exit /b 1
)
