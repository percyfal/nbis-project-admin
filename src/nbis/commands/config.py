"""Configuration administration utilities.

"""
import logging
import sys

import click
import pkg_resources
import toml
from nbis.cli import pass_environment
from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)

__shortname__ = __name__.split(".")[-1]


def load_schema():
    yaml = YAML()
    schemafile = pkg_resources.resource_filename(
        "nbis", SchemaFiles.CONFIGURATION_SCHEMA
    )
    with open(schemafile) as fh:
        schemadict = yaml.load(fh)
    return Schema(schemadict)


@click.group(help=__doc__, name=__shortname__)
@pass_environment
def main(env):
    logger.debug(f"Running {__shortname__} subcommand.")


@main.command()
@click.option("--config-file", help="configuration file name")
@pass_environment
def init(env, config_file):
    """Initialize a configuration file.

    By default will save to file PROJECT_NAME.yaml in the project home
    directory, where PROJECT_NAME is derived from the project name in
    pyproject.toml.

    """
    logger.info("Initializing configuration file")
    pyproject = toml.load(env.home / "pyproject.toml")
    project_name = pyproject["project"]["name"]
    if config_file is None:
        config_file = env.home / f"{project_name}.yaml"

    schema = load_schema()
    if not config_file.exists():
        with open(config_file, "w") as fh:
            Config.from_schema(schema, file=fh, project_name=project_name)
    else:
        logger.info(f"{config_file} exists; not overwriting")


@main.command()
@pass_environment
def show(env):
    """Show an example configuration"""
    pyproject = toml.load(env.home / "pyproject.toml")
    project_name = pyproject["project"]["name"]
    schema = load_schema()
    _ = Config.from_schema(schema, file=sys.stdout, project_name=project_name)
