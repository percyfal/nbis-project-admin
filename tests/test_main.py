import pytest
from nbis.__main__ import main


def test_main():
    with pytest.raises(SystemExit):
        main(["--help"])


def test_subcommand():
    with pytest.raises(SystemExit):
        main(["webexport", "--help"])
