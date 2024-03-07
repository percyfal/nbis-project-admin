"""Test commands."""

from nbis.cli import cli


def test_add_template(runner):
    """Test adding individual template"""
    result = runner.invoke(cli, ["add", "template", "-t", "quarto", "--show"])
    assert not result.exception
