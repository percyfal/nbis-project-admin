"""Pytest configuration file."""

import os

import pytest
from click.testing import CliRunner


def pytest_configure():
    """Add project and dname to pytest configuration."""
    pytest.dname = os.path.dirname(__file__)
    pytest.project = os.path.dirname(pytest.dname)


@pytest.fixture(autouse=False)
def cd_tmp_path(tmp_path, monkeypatch):
    """Monkeypatch change directory to tmp_path."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture(name="project_foo")
def fproject_foo(tmp_path, monkeypatch):
    """Project foo fixture."""
    p = tmp_path / "project_foo"
    p.mkdir()
    monkeypatch.chdir(p)
    return p


@pytest.fixture
def pyproject(project_foo):
    """pyproject.toml fixture."""
    p = project_foo / "pyproject.toml"
    p.write_text('[project]\nname = "project_foo"\n')
    return project_foo


@pytest.fixture(scope="function")
def runner():
    """Base client runner."""
    return CliRunner(mix_stderr=False)
