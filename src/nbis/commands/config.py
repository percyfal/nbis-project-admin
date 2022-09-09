"""Configuration administration utilities.

"""
import click
import logging
import pathlib

from nbis.templates import add_template
from nbis.click import cli

logger = logging.getLogger(__name__)

__shortname__ = __name__.split(".")[-1]

def add_config_py(args):
    """Add python configuration module"""
    configfile = pathlib.Path("src") / args.project_name / "config.py"
    add_template(configfile, "src/project/config.py.j2", project_name=args.project_name)


def add_arguments(parser):
    parser.add_argument("--dry-run", action="store_true", help="dry run")
    parser.add_argument(
        "--config-file", action="store", help="configuration file", default=None
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--init", action="store_true", help="create a configuration file"
    )
    group.add_argument("--show", action="store_true", help="show configuration")


def init(args):
    logger.info("Initializing config")


@cli.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.info(__shortname__)
