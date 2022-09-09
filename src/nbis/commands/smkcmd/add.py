"""Add snakefile and python helper code.

Add snakefile and possibly subcommand code. Options to add tests and
validation.

"""
import logging
import pathlib
import click
from . import cli

logger = logging.getLogger(__name__)


@cli.command(help=__doc__, name=__name__.split(".")[-1])
def main():
    logger.info(__name__)
