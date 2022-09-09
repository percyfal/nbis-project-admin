#!/usr/bin/env python3
import importlib
import os

import nbis.cli as cli
import pytest
from click.testing import CliRunner
from nbis import commands


def pytest_configure(config):
    pytest.dname = os.path.dirname(__file__)
    pytest.project = os.path.dirname(pytest.dname)


@pytest.fixture(autouse=False)
def cd_tmp_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


@pytest.fixture(scope="session")
def load(request):
    package = commands
    _ = importlib.import_module(".", package.__name__)
    cli.add_subcommands(package)


@pytest.fixture(scope="function")
def runner(request, load):
    return CliRunner()


@pytest.fixture(scope="function")
def main(request):
    from nbis.cli import cli

    return cli
