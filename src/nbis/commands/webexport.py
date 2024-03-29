"""Webexport administration utilities (WIP)

All contents of folder reports/webexport will be synced to the url
defined by the 'webexport.url' configuration property.
"""

import logging
import subprocess

import click

from nbis.config import Config

__shortname__ = __name__.rsplit(".", maxsplit=1)[-1]


logger = logging.getLogger(__name__)


@click.group(help=__doc__, name=__shortname__)
def main():
    """Webexport administration utilities."""
    logger.debug("Running %s subcommand.", __shortname__)


@main.command()
@click.option("--backend", help="backend to use", default="rsync")
@click.option(
    "--rsync-options",
    multiple=True,
    help="Additional options to pass to rsync.",
    default=[],
)
@click.pass_context
def sync(ctx, backend, dry_run, **kw):
    """Initialize diary.

    Add a template diary.
    """
    logger.info("Initializing diary.")
    config = Config(file=f"{ctx.find_root().info_name}.yaml")
    arguments = [backend] + kw["rsync_options"]
    if dry_run:
        arguments.append("-n")
    arguments += [
        f"{config.webexport.builddir}/",  # pylint: disable=no-member
        f"{config.webexport.url}/",  # pylint: disable=no-member
    ]
    subprocess.run(arguments, check=True)
