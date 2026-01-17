from pathlib import Path

import pytest

from app_utils import default_output_dir, ensure_directory


def test_default_output_dir_local(tmp_path):
    base_file = tmp_path / "git_ingest_app.py"
    base_file.write_text("")

    result = default_output_dir(base_file, frozen=False)

    assert result == base_file.parent / "txt_files"


def test_default_output_dir_frozen(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    base_file = Path("/tmp/fake_app")

    result = default_output_dir(base_file, frozen=True)

    assert result == tmp_path / "Documents" / "GitHub" / "git-ingest-output"


def test_ensure_directory_creates_nested(tmp_path):
    target = tmp_path / "nested" / "dir"

    created = ensure_directory(target)

    assert created == target
    assert target.exists()
    assert target.is_dir()


def test_ensure_directory_idempotent(tmp_path):
    target = tmp_path / "already" / "exists"
    target.mkdir(parents=True)

    created = ensure_directory(target)

    assert created == target
