"""Add template to python project.

"""
import logging

import click

logger = logging.getLogger(__name__)


__shortname__ = __name__.split(".")[-1]


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running {__shortname__} subcommand.")
