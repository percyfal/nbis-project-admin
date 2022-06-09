import pkg_resources
import pytest
from nbis.__main__ import main


def test_main():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["--help"])


def test_subcommand():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["webexport", "--help"])

