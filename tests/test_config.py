"""Test configuration."""

import re

import pytest

from nbis.cli import cli
from nbis.config import Config, PropertyDict


@pytest.fixture(name="data")
def fdata():
    """Data fixture."""
    d = {"project_name": "foo", "docs": {"src": "docs"}}
    return d


def test_config(data):
    """Test configuration."""
    conf = Config(data)
    assert isinstance(conf, PropertyDict)
    assert isinstance(conf.docs, PropertyDict)  # pylint: disable=no-member


def test_config_init(runner, pyproject):
    """Test initialization of configuration file."""
    out = pyproject
    result = runner.invoke(cli, ["config", "init"])
    assert not result.exception
    p = out / "project_foo.yaml"
    assert re.search(r"project_name: project_foo", p.read_text())
