#!/usr/bin/env python3
import os

import pytest
from click.testing import CliRunner


def pytest_configure(config):
    pytest.dname = os.path.dirname(__file__)
    pytest.project = os.path.dirname(pytest.dname)


@pytest.fixture(autouse=False)
def cd_tmp_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def project_foo(tmp_path, monkeypatch):
    p = tmp_path / "project_foo"
    p.mkdir()
    monkeypatch.chdir(p)
    return p


@pytest.fixture
def pyproject(project_foo):
    p = project_foo / "pyproject.toml"
    p.write_text('[project]\nname = "project_foo"\n')
    return project_foo


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner(mix_stderr=False)
