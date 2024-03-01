"""Test CLI."""

import logging
import re

from nbis.cli import cli


def test_cli(runner):
    """Test CLI."""
    result = runner.invoke(cli, [])
    assert not result.exception
    assert (
        re.search(
            r"--debug\s+Print debugging information.\n\s+"
            r"--help\s+Show this message and exit.\n\n",
            result.output,
        )
        is not None
    )
    assert (
        re.search(
            r"Commands:\n\s+"
            r"\s+add\s+Add template to a project.\n"
            r"\s+config\s+Configuration administration utilities.\n",
            result.output,
        )
        is not None
    )


def test_cli_debug(runner, caplog):
    """Test CLI debug."""
    caplog.set_level(logging.DEBUG)
    result = runner.invoke(cli, ["--debug", "add", "diary", "--show"])
    assert not result.exception
    assert caplog.records[0].levelname == "DEBUG"
    assert re.search(r"title:", result.output) is not None
