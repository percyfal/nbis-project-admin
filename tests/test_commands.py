"""Test commands."""

from nbis.cli import cli


def test_init_diary(runner):
    """Test initialization of diary."""
    result = runner.invoke(cli, ["add", "diary", "--show"])
    assert not result.exception
