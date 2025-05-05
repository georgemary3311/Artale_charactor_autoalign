#!/bin/bash
# check pyinstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    pip install pyinstaller
fi
python -m PyInstaller --onefile --icon=src/artile_little_tool.ico main.py -name=Autoalign_v1.0.5