#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

detect_package_manager() {
    if command_exists apt; then
        echo "apt"
    elif command_exists dnf; then
        echo "dnf"
    elif command_exists yum; then
        echo "yum"
    elif command_exists pacman; then
        echo "pacman"
    elif command_exists zypper; then
        echo "zypper"
    elif command_exists brew; then
        echo "brew"
    elif command_exists pkg; then
        echo "pkg"
    else
        echo "unknown"
    fi
}

echo "Beginning installation for Dakto INC Calculator..."

PKG_MANAGER=$(detect_package_manager)
if [[ "$PKG_MANGER" != "brew" && "$EUID" -ne 0 ]]; then
    echo "Please rerun this script using sudo"
    echo "  sudo $0"
    exit 1
fi

if ! command_exists git; then
    echo "Installing git..."
    case  $PKG_MANAGER in
        apt) apt update && apt install -y git ;;
        dnf) dnf install -y git ;;
        yum) yum install -y git ;;
        pacman) pacman -Sy --noconfirm git ;;
        zypper) zypper install -y git ;;
        brew) brew install git ;;
        pkg) pkg install git ;;
        *) echo "Unsupported package manager. Please install python3 manually."; exit 1 ;;
    esac
else
    echo "Successfully installed Python3."
fi

echo "Checking for Tkinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Installing Tkinter..."
    case $PKG_MANAGER in
        apt) apt install -y python3-tk ;;
        dnf) dnf install -y python3-tkinter ;;
        yum) yum install -y tkinter ;;
        pacman) pacman -Sy --noconfirm tk ;;
        zypper) zypper install -y python3-tk ;;
        brew) brew install python-tk ;;
        pkg) pkg install python3-tk ;;
        *) echo "Unsupported package manager. Please install tkinter manually."; exit 1 ;;
    esac
else
    echo "Successfully installed Tkinter."
fi

REPO_URL="https://github.com/Daktoo/DKI-Calculator"
TARGET_DIR="DKI-Calculator"

if [[ -d "$TARGER_DIR" ]]; then
    echo "Repo already exists: $TARGER_DIR"
else
    echo "Cloning repo from $REPO_URL..."
    git clone "$REPO_URL"
fi

echo "Installation completed successfully. You can run the calculator at ~/DKI-Calculator/calc.py"
