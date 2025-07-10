@echo off
setlocal enabledelayedexpansion
echo ============================================
echo Installing DKI-Calculator
echo ============================================
where curl >nul 2>nul
if errorlevel 1 (
    echo Curl is not installed
    echo Installing Curl via winget
    winget install -id curl.curl -e --source winget
) else (
    echo Curl is already installed
)
where git >nul 2>nul
if errorlevel 1 (
    echo Git is not installed
    echo Installing Git via winget
    winget install -id Git.Git -e --source winget
) else (
    echo Git is installed.
)
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed
    echo Installing Python via winget
    winget install -id Python.Python.3 -e --source winget
) else (
    echo Python is installed
)
echo Checking for tkinter support
python -c "import tkinter" >nul 2>nul
if errorlevel 1 (
    echo Tkinter is not available in your Python installation.
    echo You may need to reinstall Python from the official installer:
    echo https://www.python.org/downloads/windows/
    echo.
    pause
)
echo Installing Pillow module
python -m pip install --upgrade pip
python -m pip install Pillow

if not exist DKI-Calculator (
    mkdir DKI-Calculator
)
cd DKI-Calculator
echo "Downloading files..."
set base=https://raw.githubusercontent.com/Daktoo/DKI-Calculator/main
curl -O %base%/background.png
curl -O %base%/dak.png
curl -O %base%/dki-icon.png
curl -O %base%/calc.python

echo.
echo Installation successfull.

