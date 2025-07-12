#!/bin/bash

set -e

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
if [[ "$PKG_MANAGER" != "brew" && "$EUID" -ne 0 ]]; then
    echo "Please rerun this script using sudo"
    echo "  sudo $0"
    exit 1
fi

if ! command_exists curl; then
    echo "Installing curl..."
    case $PKG_MANAGER in
        apt) apt update && apt install -y curl ;;
        dnf) dnf install -y curl ;;
        yum) yum install -y curl ;;
        pacman) pacman -Sy --noconfirm curl ;;
        zypper) zypper install -y curl ;;
        brew) brew install curl ;;
        pkg) pkg install curl ;;
        *) echo "Unsupported package manager. Please install curl manually."; exit 1 ;;
    esac
fi

if ! command_exists git; then
    echo "Installing git..."
    case $PKG_MANAGER in
        apt) apt update && apt install -y git ;;
        dnf) dnf install -y git ;;
        yum) yum install -y git ;;
        pacman) pacman -Sy --noconfirm git ;;
        zypper) zypper install -y git ;;
        brew) brew install git ;;
        pkg) pkg install git ;;
        *) echo "Unsupported package manager. Please install git manually."; exit 1 ;;
    esac
fi

if ! command_exists python3; then
    echo "Installing python3..."
    case $PKG_MANAGER in
        apt) apt update && apt install -y python3 ;;
        dnf) dnf install -y python3 ;;
        yum) yum install -y python3 ;;
        pacman) pacman -Sy --noconfirm python ;;
        zypper) zypper install -y python3 ;;
        brew) brew install python3 ;;
        pkg) pkg install python3 ;;
        *) echo "Unsupported package manager. Please install python3 manually."; exit 1 ;;
    esac
fi

echo "Checking for Pillow..."
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "Installing Pillow..."
    case $PKG_MANAGER in
        apt) apt install -y python3-pillow ;;
        dnf) dnf install -y python3-pillow ;;
        yum) yum install -y python3-pillow ;;
        pacman) pacman -Sy --noconfirm python-pillow ;;
        zypper) zypper install -y python3-pillow ;;
        brew) pip3 install Pillow ;;
        pkg) pkg install python3-pillow ;;
        *) echo "Unsupported package manager. Please install Pillow manually."; exit 1 ;;
    esac
fi

echo "Checking for Tkinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Installing Tkinter..."
    case $PKG_MANAGER in
        apt) apt install -y python3-tk ;;
        dnf) dnf install -y python3-tkinter ;;
        yum) yum install -y python3-tkinter ;;
        pacman) pacman -Sy --noconfirm tk ;;
        zypper) zypper install -y python3-tk ;;
        brew) pip3 install tk ;;
        pkg) pkg install python3-tk ;;
        *) echo "Unsupported package manager. Please install Tkinter manually."; exit 1 ;;
    esac
fi

mkdir -p DKI-Calculator
cd DKI-Calculator
echo "Downloading files..."
base_url="https://raw.githubusercontent.com/Daktoo/DKI-Calculator/main"
curl -O "$base_url/background.png"
curl -O "$base_url/dak.png"
curl -O "$base_url/dki-icon.png"
curl -O "$base_url/calc.py"

echo "Installation completed successfully. You can run the calculator at ~/DKI-Calculator/calc.py"
