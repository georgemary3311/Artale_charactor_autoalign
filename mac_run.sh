#!/bin/bash

REPO_NAME="Artale_charactor_autoalign"
REPO_URL="https://github.com/georgemary3311/Artale_charactor_autoalign.git"

# Clone the repository only if it hasn't been cloned
if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
else
    echo "Repository already cloned."
fi

cd "$REPO_NAME" || exit

# Function to check and install Python package
check_and_install() {
    PACKAGE=$1
    IMPORT_NAME=$2
    python3 -c "import $IMPORT_NAME" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "$PACKAGE not found. Installing..."
        pip3 install "$PACKAGE"
    else
        echo "$PACKAGE is already installed."
    fi
}

# Check and install psd-tools (imported as psd_tools)
check_and_install psd-tools psd_tools

# Check and install opencv-python (imported as cv2)
check_and_install opencv-python cv2

check_and_install colorama colorama

# Run the main script
python3 main.py