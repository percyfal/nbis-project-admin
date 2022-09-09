"""Snakemake administration utilities


"""
import logging

import click
from nbis.cli import cli

__shortname__ = __name__.split(".")[-1]

logger = logging.getLogger(__name__)


@cli.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running subcommand {__shortname__}")


@main.command()
@click.pass_context
def init(ctx):
    """Initialize snakemake files.

    Info here
    """
    pass


@main.command()
@click.pass_context
def add(ctx):
    """Add snakefile and python helper code.

    Add snakefile and possibly subcommand code. Options to add tests
    and validation.
    """
    pass
