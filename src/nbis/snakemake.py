"""Snakemake utilities"""
import logging
import re

import click

logger = logging.getLogger(__name__)


def get_profile(uri, config):
    """Retrieve snakemake profile from config"""
    try:
        uri = config["snakemake_profiles"][uri]
    except TypeError as e:
        logger.debug(f"TypeError: '{e}'")
    except KeyError as e:
        logger.debug(f"KeyError: no such snakemake-profiles key {e}")
    finally:
        logger.debug(f"trying snakemake profile at uri '{uri}'")
    return uri


def profile_opt(default_profile="local"):
    """Add snakemake profile option"""
    func = click.option(
        "--profile",
        help=(
            "snakemake profile, either defined as key:value pair in config"
            " or a URI pointing to profile directory"
        ),
        default=default_profile,
    )
    return func


def jobs_opt():
    """Add jobs option"""
    return click.option("--jobs", "-j", type=int, default=1, help="snakemake jobs")


def test_opt():
    """Add test option"""
    return click.option(
        "--test", is_flag=True, help="run workflow on small test data set"
    )


def directory_opt():
    """Add snakemake directory option"""
    return click.option(
        "--directory/-d",
        help=(
            "Specify working directory (relative paths in the snakefile will "
            "use this as their origin). (default: project directory)"
        ),
    )


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
    with open(smkfile) as fh:
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
