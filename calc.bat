@echo off
setlocal enabledelayedexpansion
echo ============================================
echo Installing DKI-Calculator
echo ============================================
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
if exist DKI-Calculator (
    echo Repo already exists: DKI-Calculator
) else (
    echo Cloning GitHub repo...
    git clone https://github.com/Daktoo/DKI-Calculator
)

echo.
echo Installation successfull.

