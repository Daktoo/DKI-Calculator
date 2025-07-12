@echo off
setlocal enabledelayedexpansion
REM ============================================
REM Installing DKI-Calculator
REM ============================================
echo ============================================
echo Installing DKI-Calculator
echo ============================================

REM Check for curl
where curl >nul 2>nul
if errorlevel 1 (
    echo Curl is not installed
    echo Installing Curl via winget
    winget install -id curl.curl -e --source winget || goto :error
) else (
    echo Curl is already installed
)

REM Check for git
where git >nul 2>nul
if errorlevel 1 (
    echo Git is not installed
    echo Installing Git via winget
    winget install -id Git.Git -e --source winget || goto :error
) else (
    echo Git is installed.
)

REM Check for python
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed
    echo Installing Python via winget
    winget install -id Python.Python.3 -e --source winget || goto :error
) else (
    echo Python is installed
)

REM Check for pip
python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo Pip is not installed. Attempting to install pip...
    python -m ensurepip --upgrade >nul 2>nul
    if errorlevel 1 (
        echo Failed to install pip. Please install manually.
        goto :error
    )
)

REM Check for tkinter
python -c "import tkinter" >nul 2>nul
if errorlevel 1 (
    echo Tkinter is not available in your Python installation.
    echo You may need to reinstall Python from the official installer:
    echo https://www.python.org/downloads/windows/
    goto :error
)

REM Install Pillow
python -m pip install --upgrade pip >nul 2>nul
python -m pip install Pillow >nul 2>nul
if errorlevel 1 (
    echo Failed to install Pillow. Please install manually.
    goto :error
)

REM Create directory if not exists
if not exist DKI-Calculator (
    mkdir DKI-Calculator
)
cd DKI-Calculator

REM Download files only if not present
set base=https://raw.githubusercontent.com/Daktoo/DKI-Calculator/main
for %%F in (background.png dak.png dki-icon.png calc.py) do (
    if not exist %%F (
        echo Downloading %%F...
        curl -O %base%/%%F
        if errorlevel 1 (
            echo Failed to download %%F
            goto :error
        )
    ) else (
        echo %%F already exists, skipping download.
    )
)

echo.
echo Installation successful.
goto :eof

:error
echo.
echo Installation failed. Please check the above messages.
endlocal
exit /b 1

