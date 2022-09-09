"""Initialize configuration files.

Will add some stuff
"""
import logging
import pathlib
import click
from . import cli
import pkg_resources
from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)

__shortname__ = __name__.split(".")[-1]


@cli.command(help=__doc__, name=__shortname__)
@click.pass_context
@click.option("--config-file")
def main(ctx, config_file):
    logger.info(__shortname__)
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
