"""Snakemake utilities"""

import logging
import re
from typing import Callable

import click
from click.decorators import FC

from nbis.env import Environment

logger = logging.getLogger(__name__)


def get_profile(uri, config):
    """Retrieve snakemake profile from config"""
    try:
        uri = config["snakemake_profiles"][uri]
    except TypeError as e:
        logger.debug("TypeError: '%s'", e)
    except KeyError as e:
        logger.debug("KeyError: no such snakemake-profiles key %s", e)
    finally:
        logger.debug("trying snakemake profile at uri '%s'", uri)
    return uri


def profile_option(
        default: str = "local", expose_value: bool = True
) -> Callable[[FC], FC]:
    """Add profile option with callback."""

    def profile_callback(
        ctx: click.core.Context, param: click.core.Option, value: str
    ) -> str:  # pylint: disable=unused-argument
        """Profile callback."""
        env = ctx.ensure_object(Environment)
        if ctx.params.get("no_profile"):
            return []
        if value is None:
            value = default
        return ["--profile", get_profile(value, env.config)]

    return click.option(
        "--profile",
        help="Set the profile",
        callback=profile_callback,
        expose_value=expose_value,
        is_eager=False,
        default=default,
    )


def no_profile_option() -> Callable[[FC], FC]:
    """Add no profile option with callback."""

    return click.option(
        "--no-profile",
        help="Do not use a profile",
        is_flag=True,
        expose_value=True,
        is_eager=True,
        default=False,
    )


def verbose_option(expose_value: bool = False) -> Callable[[FC], FC]:
    """Add verbose option with callback."""

    def verbose_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Verbose callback."""
        log_level = max(3 - value, 0) * 10
        logging.basicConfig(
            level=log_level,
            format=(
                "%(asctime)s; %(levelname)s "
                "[%(name)s:%(funcName)s]: %(message)s"
            ),
        )
        return log_level

    return click.option(
        "--verbose",
        "-v",
        "logger",
        help="Set the verbosity level",
        count=True,
        callback=verbose_callback,
        expose_value=expose_value,
        is_eager=True,
        default=0,
    )


def cores_option(default=None) -> Callable[[FC], FC]:
    """Add cores option."""

    def cores_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Cores callback."""
        if value is None:
            return []
        if value < 1:
            logging.error("Cores must be greater than 0")
            raise ValueError("Cores must be greater than 0")
        return ["--cores", str(value)]

    return click.option(
        "-c",
        "--cores",
        help="number of cores",
        default=None,
        callback=cores_callback,
        type=int,
    )


def jobs_option(default=None) -> Callable[[FC], FC]:
    """Add jobs option."""

    def jobs_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Jobs callback."""
        if value is None:
            return []
        if value < 1:
            logging.error("Jobs must be greater than 0")
            raise ValueError("Jobs must be greater than 0")
        return ["--jobs", str(value)]

    return click.option(
        "-j",
        "--jobs",
        help="number of jobs",
        default=default,
        callback=jobs_callback,
        type=int,
    )


def threads_option() -> Callable[[FC], FC]:
    """Add threads option."""

    return click.option(
        "-t",
        "--threads",
        help="number of threads",
        default=1,
        type=click.IntRange(
            1,
        ),
    )


def test_option() -> Callable[[FC], FC]:
    """Add test option"""

    def test_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Callback for test option"""
        if value:
            return ["--config", "__test__=True"]
        return []

    return click.option(
        "--test", is_flag=True, help="run workflow on small test data set",
        callback=test_callback
    )


def directory_option():
    """Add snakemake directory option"""
    return click.option(
        "--directory/-d",
        help=(
            "Specify working directory (relative paths in the snakefile will "
            "use this as their origin). (default: project directory)"
        ),
    )


def report_option() -> Callable[[FC], FC]:
    """Add snakemake report option"""
    func = click.option(
        "--report",
        help=("generate snakemake report"),
        is_flag=True,
        default=False,
    )
    return func


def format_snakemake_help(smkfile, *, default=None):
    """Return docstring from snakemake file.

    Provided that a document starts with triple quotes,
    the document is read and split on that delimiter. This
    will produce a list where the first entry is the empty
    string, so the function returns the second entry in the
    list.

    Use in command function:

        @cli.command(context_settings=dict(ignore_unknown_options=True),
                    help=format_snakemake_help(config.SNAKEMAKE_ROOT / smkfile))
    """
    with open(smkfile, encoding="utf-8") as fh:
        file_contents = "".join(fh.readlines())
    text = default
    if re.match('^"""', file_contents):
        m = re.split('"""', file_contents)
        text = m[1]
    else:
        if default is None:
            return None, None
        text = default
    try:
        title, body = text.split("\n", maxsplit=1)
    except ValueError:
        title = default
        body = default
    return title, body
