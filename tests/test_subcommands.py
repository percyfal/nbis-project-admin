import pytest
from nbis.subcommands import config
from nbis.subcommands import diary


class Namespace:
    prog = "nbis"
    project_name = "nbis"
    diary_file = "diary.md"
    config_file = None


@pytest.fixture
def namespace():
    return Namespace()


def test_config_init(namespace, cd_tmp_path):
    config.init(namespace)


def test_init_diary(namespace, cd_tmp_path):
    diary.init_diary(namespace)
