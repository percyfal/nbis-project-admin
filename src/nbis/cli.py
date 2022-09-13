"""Console script for nbis based on click."""
import logging

import click
from nbis import decorators
from nbis.commands import *  # noqa: F405, F403

from . import __version__

__author__ = "Per Unneberg"


logger = logging.getLogger(__name__)


@click.group(help=__doc__)
@click.version_option(version=__version__)
@decorators.debug_option()
@click.pass_context
def cli(ctx):
    """Cli help"""
    ctx.ensure_object(dict)
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s [%(name)s:%(funcName)s]: %(message)s"
    )
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)


def main():
    cli(obj={})


cli.add_command(config.main)  # noqa: F405
cli.add_command(diary.main)  # noqa: F405
cli.add_command(docs.main)  # noqa: F405
cli.add_command(smk.main)  # noqa: F405
cli.add_command(webexport.main)  # noqa: F405
