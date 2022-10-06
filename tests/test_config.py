import re

import pytest
from nbis.cli import cli
from nbis.config import Config
from nbis.config import PropertyDict


@pytest.fixture
def data():
    d = dict(project_name="foo", docs=dict(src="docs"))
    return d


def test_config(data):
    conf = Config(data)
    assert isinstance(conf, PropertyDict)
    assert isinstance(conf.docs, PropertyDict)


def test_config_init(runner, pyproject):
    out = pyproject
    result = runner.invoke(cli, ["config", "init"])
    assert not result.exception
    p = out / "project_foo.yaml"
    assert re.search(r"project_name: project_foo", p.read_text())
