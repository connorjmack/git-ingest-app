#!/bin/bash

# --- Clean up previous builds ---
echo "Cleaning up previous build files..."
rm -rf dist build *.spec

# --- Build the application ---
echo "Starting PyInstaller build in ONEDIR mode (Recommended for macOS)..."
# We use the full python path from the active virtual environment to ensure isolation
/usr/bin/env python -m PyInstaller --name "GitIngest" \
    --windowed \
    --onedir \
    --noconsole \
    --distpath /Applications \
    ingest_app.py

# --- Verify and provide instructions ---
# Check for a directory (folder) since onedir creates a folder structure
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