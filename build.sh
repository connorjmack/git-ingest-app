#!/bin/bash

# --- Clean up previous builds ---
echo "Cleaning up previous build files..."
rm -rf dist build *.spec

# --- Build the application ---
echo "Starting PyInstaller build in ONEDIR mode (Recommended for macOS)..."
# ADDED --collect-all flags to fix launch crashes
/usr/bin/env python -m PyInstaller --name "GitIngest" \
    --windowed \
    --onedir \
    --noconsole \
    --distpath /Applications \
    --additional-hooks-dir=hooks \
    --collect-all gitingest \
    --collect-all customtkinter \
    git_ingest_app.py

# --- Verify and provide instructions ---
if [ -d /Applications/GitIngest.app ]; then
    echo " "
    echo "========================================================"
    echo "✅ SUCCESS! GitIngest.app is located in /Applications"
    echo "========================================================"
    echo " "
else
    echo " "
    echo "❌ ERROR: Build failed. Check the output above."
fi