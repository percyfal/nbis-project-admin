"""Initialize snakemake files.

Will add some stuff
"""
import logging
import pathlib
import click
from . import cli

logger = logging.getLogger(__name__)


@cli.command(help=__doc__, name=__name__.split(".")[-1])
def main():
    logger.info("init")
