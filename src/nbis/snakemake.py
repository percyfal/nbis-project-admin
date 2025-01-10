"""Snakemake utilities"""

import logging
import re
from pathlib import Path
from typing import Callable

import click
from click.decorators import FC

from nbis.env import Environment

logger = logging.getLogger(__name__)


def snakemake_argument_list() -> Callable[[FC], FC]:
    """Add snakemake argument list."""

    return click.argument("snakemake_args", nargs=-1, type=click.UNPROCESSED)


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
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: str,
    ) -> str:
        """Profile callback."""
        env = ctx.ensure_object(Environment)
        if ctx.params.get("no_profile"):
            return []
        is_report = ctx.params.get("report", [])
        if len(is_report) > 0:
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
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: int,
    ) -> int:
        """Verbose callback."""
        log_level = max(3 - value, 0) * 10
        logging.basicConfig(
            level=log_level,
            format=(
                "%(asctime)s; %(levelname)s " "[%(name)s:%(funcName)s]: %(message)s"
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
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: int,
    ) -> int:
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
        default=default,
        callback=cores_callback,
        type=int,
    )


def jobs_option(default=None) -> Callable[[FC], FC]:
    """Add jobs option."""

    def jobs_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: int,
    ) -> int:
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


def threads_option(default=None) -> Callable[[FC], FC]:
    """Add threads option."""

    def threads_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: int,
    ) -> int:
        """Threads callback."""
        if value is None:
            return []
        if value < 1:
            logging.error("Threads must be greater than 0")
            raise ValueError("Threads must be greater than 0")
        return ["--threads", str(value)]

    return click.option(
        "-t",
        "--threads",
        help="number of threads",
        default=default,
        callback=threads_callback,
        type=click.IntRange(
            1,
        ),
    )


def test_option(
    config: list[str] = None,
    options: list[str] = None,
    test_profile: str = None,
) -> Callable[[FC], FC]:
    """Add test option with callback."""

    def test_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: int,
    ) -> int:
        """Callback for test option"""
        ret = []
        if value:
            if options:
                ret = ret + options
            if test_profile:
                ret = ret + ["--profile", test_profile]
            ret = ret + ["--config", "__test__=True"]
            if config:
                ret = ret + config
        return ret

    return click.option(
        "--test",
        is_flag=True,
        help="run workflow on small test data set",
        callback=test_callback,
    )


def directory_option(
    default: str = None,
    expose_value: bool = True,
) -> Callable[[FC], FC]:
    """Add snakemake directory option"""

    def directory_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: str,
    ) -> str:
        """Directory callback"""
        env = ctx.ensure_object(Environment)
        if value is None:
            try:
                value = env.home
            except AttributeError:
                pass
        if value is None:
            return []
        return ["--directory", str(value)]

    return click.option(
        "-d",
        "--directory",
        help=(
            "Specify working directory (relative paths in the snakefile will "
            "use this as their origin). (default: project directory). Will fallback"
            "on project environment home directory if available."
        ),
        default=default,
        callback=directory_callback,
        expose_value=expose_value,
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
    )


def envmodules_config_option(
    default: str = None,
    envmodules_config: str = "envmodules.yaml",
    expose_value: bool = True,
) -> Callable[[FC], FC]:
    """Add snakemake envmodules yaml config file option."""

    def envmodules_config_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: str,
    ) -> str:
        """Envmodules config callback."""
        env = ctx.ensure_object(Environment)
        try:
            directory = ctx.params.get("directory", env.home)
        except AttributeError:
            directory = None
        if value is not None:
            configfile = value
            if directory is not None:
                configfile = Path(directory) / value
            return ["--configfile", str(configfile)]
        try:
            value = env.home
        except AttributeError:
            value = None
        if value is not None:
            configfile = Path(value) / envmodules_config
        else:
            configfile = Path(envmodules_config)
        if not configfile.exists():
            logger.warning("envmodules config file %s does not exist", configfile)
            return []
        return ["--configfile", str(configfile)]

    return click.option(
        "--envmodules-configfile",
        help=("Specify environment modules configuration file."),
        default=default,
        callback=envmodules_config_callback,
        expose_value=expose_value,
        type=click.Path(exists=True, file_okay=True, dir_okay=False),
    )


def report_option(
    report_file: str = "report.html",
) -> Callable[[FC], FC]:
    """Add snakemake report option"""

    def report_callback(
        ctx: click.core.Context,  # pylint: disable=unused-argument
        param: click.core.Option,  # pylint: disable=unused-argument
        value: bool,
    ) -> int:
        """Callback for report option"""
        ret = []
        if value:
            ret = ["--report", report_file]
        return ret

    func = click.option(
        "--report",
        help=("generate snakemake report"),
        is_flag=True,
        default=False,
        callback=report_callback,
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
