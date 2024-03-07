"""Test commands."""

from nbis.cli import cli


def test_add_template(runner):
    """Test adding individual template"""
    result = runner.invoke(cli, ["add", "template", "-t", "quarto", "--show"])
    assert not result.exception


def test_add_tool(runner):
    """Test adding tool"""
    result = runner.invoke(cli, ["add", "tool", "snakemake", "--show"])
    print(result.stdout)
    assert not result.exception
