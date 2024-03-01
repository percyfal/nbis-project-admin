"""Test commands."""

from nbis.cli import cli


def test_init_diary(runner):
    """Test initialization of diary."""
    result = runner.invoke(cli, ["diary"])
    print(result.stdout)
    print(result)
