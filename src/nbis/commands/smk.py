"""Snakemake administration utilities


"""
import click
import logging
import pathlib

from nbis.templates import add_template
from nbis.cli import cli

__shortname__ = __name__.split(".")[-1]

#from .config import add_config_py

logger = logging.getLogger(__name__)


@cli.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.info(__shortname__)
