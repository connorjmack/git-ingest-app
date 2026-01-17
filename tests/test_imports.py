import pytest


def test_git_ingest_app_imports():
    pytest.importorskip("customtkinter")
    import git_ingest_app  # noqa: F401
