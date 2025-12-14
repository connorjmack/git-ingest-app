# GitIngest Pro Local GUI

**GitIngest Pro** is a clean, native desktop application providing a simple graphical interface for the powerful [GitIngest](https://github.com/cyclotruc/gitingest) tool.

This application allows developers, researchers, and LLM enthusiasts to quickly process any public GitHub repository URL into a single, structured text file containing the entire codebase's summary, directory tree, and file contents. This format is optimized for ingestion by large language models (LLMs) like Claude, Gemini, or ChatGPT.

<img src="https://path/to/your/app/screenshot.png" alt="Screenshot of the GitIngest Pro desktop application in dark mode" width="800">

## ✨ Features

* **Modern Native UI:** Built with CustomTkinter to deliver a clean, modern, and native dark-mode experience on macOS and other platforms.
* **Asynchronous Processing:** Long-running operations (cloning and ingesting) are executed on a separate thread using `threading` and `asyncio`, ensuring the UI remains responsive and never freezes.
* **Smart Output Handling:**
    * Automatically saves the output file with a timestamped filename (e.g., `repo-name_YYYYMMDD_HHMMSS.txt`).
    * Defaults to a safe, easily accessible location (`~/Documents/GitHub/git-ingest-output`).
    * Allows users to easily select a custom output folder.
* **One-Click Actions:** Instantly copy the output file path or the entire file content (ready for LLM pasting) to the clipboard upon completion.

## 🚀 Installation & Setup

We recommend using `conda` for the easiest environment setup, but standard `venv` and `pip` instructions are also provided.

### Option 1: Using Conda (Recommended)

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/connorjmack/git-ingest-app.git](https://github.com/connorjmack/git-ingest-app.git)
    cd git-ingest-app
    ```
2.  **Create and Activate the Environment:**
    ```bash
    conda env create -f environment.yml
    conda activate gitingest-app
    ```
3.  **Run the Application:**
    ```bash
    python git_ingest_app.py
    ```

### Option 2: Using venv + pip

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/connorjmack/git-ingest-app.git](https://github.com/connorjmack/git-ingest-app.git)
    cd git-ingest-app
    ```
2.  **Create and Activate the Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Application:**
    ```bash
    python git_ingest_app.py
    ```

## 🛠️ Usage

1.  **Run the Application** using one of the methods above.
2.  **Paste** a valid GitHub repository URL (e.g., `https://github.com/cyclotruc/gitingest`) into the input field.
3.  **(Optional) Click "Change Folder"** to select a custom output directory.
4.  **Click "Ingest Repository"**. The application will clone the repo and process the contents in the background.
5.  Once complete, the file path will appear, and you can use the **Copy File Path** or **Copy File Content** buttons to easily access the generated text file.

## 📦 Building a Standalone macOS App

If you wish to create a self-contained `.app` bundle for macOS, you can use the included build script with PyInstaller:

**Prerequisites:** Ensure you have PyInstaller installed (`pip install pyinstaller`) and are running on a macOS environment.

```bash
# Run the build script
./build.sh