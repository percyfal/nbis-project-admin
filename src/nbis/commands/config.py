"""Configuration administration utilities.

"""
import logging
import pathlib

import click
import pkg_resources
from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles
from nbis.templates import add_template
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)

__shortname__ = __name__.split(".")[-1]


def add_config_py(ctx):
    """Add python configuration module"""
    configfile = pathlib.Path("src") / ctx.info_name / "config.py"
    add_template(configfile, "src/project/config.py.j2", project_name=ctx.info_name)


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running {__shortname__} subcommand.")


@main.command()
@click.option("--config-file", help="configuration file name")
@click.pass_context
def init(ctx, config_file):
    logger.info("Initializing configuration file")
    if config_file is None:
        config_file = pathlib.Path(f"{ctx.parent.parent.info_name}.yaml")

    yaml = YAML()
    schemafile = pkg_resources.resource_filename(
        "nbis", SchemaFiles.CONFIGURATION_SCHEMA
    )
    with open(schemafile) as fh:
        schemadict = yaml.load(fh)
    schema = Schema(schemadict)
    if not config_file.exists():
        with open(config_file, "w") as fh:
            Config.from_schema(schema, file=fh)
    else:
        logger.info(f"{config_file} exists; not overwriting")


@main.command()
def show(ctx):
    pass
