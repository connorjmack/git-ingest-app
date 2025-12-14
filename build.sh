#!/bin/bash

echo "Cleaning up previous build files..."
rm -rf dist build *.spec

echo "Starting PyInstaller build in ONEFILE mode..."
/usr/bin/env python -m PyInstaller --name "GitIngest" \
    --windowed \
    --onefile \
    --noconsole \
    --distpath /Applications \
    --collect-all gitingest \
    --collect-all customtkinter \
    git_ingest_app.py

if [ -f /Applications/GitIngest.app/Contents/MacOS/GitIngest ]; then
    echo "✅ SUCCESS! GitIngest.app is in /Applications"
else
    echo "❌ ERROR: Build failed."
fi