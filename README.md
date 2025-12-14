# GitIngest Local GUI

A clean, dark-mode macOS GUI application for [GitIngest](https://github.com/cyclotruc/gitingest). 

This tool allows you to paste a GitHub repository URL and locally generate a single text file containing the entire repository's summary, directory tree, and file contents—perfect for feeding codebases into LLMs (ChatGPT, Claude, Gemini).

<img src="https://via.placeholder.com/800x500.png?text=Add+Your+Screenshot+Here" alt="App Screenshot" width="100%">

## Features
* **Modern UI:** Built with CustomTkinter for a native macOS dark-mode feel.
* **Async Processing:** Runs on a separate thread so the UI never freezes during large downloads.
* **One-Click Copy:** Automatically generates a copy-ready file path.
* **Smart Saving:** Auto-saves files with timestamps to your local `Documents/GitHub/git_ingest_summaries` folder.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/gitingest-gui.git](https://github.com/yourusername/gitingest-gui.git)
    cd gitingest-gui
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

**Run via Python:**
```bash
python ingest_app.py