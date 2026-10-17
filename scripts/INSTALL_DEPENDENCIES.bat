@echo off
title Installing Dependencies - Ahrefs Auto Scraper v3.5
chcp 65001 >nul
cd /d "%~dp0\.."
cls

echo ===============================================================================
echo                Ahrefs Auto Scraper v3.5 - Dependency Installer
echo                         Engineered by Al Hossain Rifat
echo ===============================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [*] Python detected:
python --version
echo.
echo [*] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [*] Installing required packages from config\requirements.txt...
if exist config\requirements.txt (
    python -m pip install -r config\requirements.txt
) else (
    python -m pip install -r requirements.txt
)

echo.
echo ===============================================================================
echo [✓] All dependencies have been successfully installed!
echo You can now double-click "LAUNCH_SCRAPER.bat" to start keyword research.
echo ===============================================================================
echo.
pause
