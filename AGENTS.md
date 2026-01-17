# Repository Guidelines

## Project Structure & Module Organization
- `git_ingest_app.py`: CustomTkinter desktop UI; handles repo URL input, threading, ingest orchestration, and clipboard actions.
- `txt_files/`: Default output directory when running locally; frozen builds save under `~/Documents/GitHub/git-ingest-output`.
- `build.sh`, `GitIngest.spec`, `hook-customtkinter.py`, `hooks/`: PyInstaller packaging helpers; macOS build drops `/Applications/GitIngest.app`.
- `.github/workflows/claude*.yml`: Claude automation for PR reviews and comment-triggered assistance.
- `requirements.txt` / `environment.yml`: Runtime and build dependencies; `logo.png`/`logo.icns` app assets; `build/` holds generated bundles.

## Build, Test, and Development Commands
- Create env (Conda): `conda env create -f environment.yml && conda activate gitingest-app`.
- Create env (venv): `python -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt` (includes pytest tooling).
- Run locally: `python git_ingest_app.py` (opens GUI; outputs files under `txt_files/` by default).
- Package macOS app: `./build.sh` (cleans dist/build/spec and runs PyInstaller onefile GUI build to `/Applications/GitIngest.app`).
- Tests: `pytest` or `pytest --cov=app_utils --cov=git_ingest_app` (markers: `slow`, `gui`).
- Lint/format: follow PEP 8; no enforced tool yet—use `ruff`/`black` locally if you prefer.

## Coding Style & Naming Conventions
- Target Python 3.11; 4-space indentation; keep modules single-purpose and small.
- Functions/methods/variables: `lower_snake_case`; classes: `CapWords`; constants: `UPPER_SNAKE`.
- Keep UI strings concise; align new UI elements with existing CustomTkinter styling (dark theme, green call-to-action accents).
- Prefer type hints for new public helpers; keep imports ordered standard lib → third-party → local.

## Testing Guidelines
- Automated: pytest lives in `tests/`; unit helpers cover output-path logic (`app_utils.py`). Add markers `@pytest.mark.gui` for UI/display-bound cases and `@pytest.mark.slow` for long-running ingest checks.
- Manual smoke before PRs: run app, ingest `https://github.com/cyclotruc/gitingest`, verify file card appears, "Copy Path" and "Copy Content" operate, and Finder reveal works on macOS.
- If changing the build pipeline, confirm `./build.sh` completes and the resulting app launches without a console window.

## Commit & Pull Request Guidelines
- Commit messages: short, imperative, scoped (e.g., "Add output card hover state"); group related changes per commit.
- PRs: include summary, testing notes or manual steps, screenshots/GIFs for UI tweaks, and linked issues if applicable.
- Keep branches up to date with `main`; expect Claude review workflow on PRs when opened/synced—address raised findings before merge.
