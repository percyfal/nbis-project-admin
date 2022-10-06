import logging
import re

from nbis.cli import cli


def test_cli(runner):
    result = runner.invoke(cli, [])
    assert not result.exception
    assert (
        re.search(
            r"--debug    Print debugging information.\n\s+"
            r"--help     Show this message and exit.\n\n",
            result.output,
        )
        is not None
    )
    assert (
        re.search(
            r"Commands:\n\s+"
            r"\s+add        Add template to python project.\n"
            r"\s+config     Configuration administration utilities.\n",
            result.output,
        )
        is not None
    )


def test_cli_debug(runner, caplog):
    caplog.set_level(logging.DEBUG)
    result = runner.invoke(cli, ["--debug", "diary", "init", "-n"])
    assert not result.exception
    assert caplog.records[0].levelname == "DEBUG"
    assert re.search(r"(DRY RUN)", result.output) is not None
