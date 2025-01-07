"""Configuration administration utilities.

"""

import logging
import sys

import click
try:
    import pkg_resources
except ImportError:
    from importlib import resources as pkg_resources
import toml

import nbis
from nbis.cli import pass_environment
from nbis.config import Config
from nbis.config import SchemaFiles
from nbis.config import get_schema

logger = logging.getLogger(__name__)

__shortname__ = __name__.rsplit(".", maxsplit=1)[-1]


@click.group(help=__doc__, name=__shortname__)
def main():
    """Configuration administration utilities."""
    logger.debug("Running %s subcommand.", __shortname__)


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

    schema = get_schema()
    if not config_file.exists():
        with open(config_file, "w", encoding="utf-8") as fh:
            Config.from_schema(schema, file=fh, project_name=project_name)
    else:
        logger.info("%s exists; not overwriting", config_file)


@main.command()
@pass_environment
def show(env):
    """Show an example configuration"""
    pyproject = toml.load(env.home / "pyproject.toml")
    project_name = pyproject["project"]["name"]
    schema = get_schema()
    _ = Config.from_schema(schema, file=sys.stdout, project_name=project_name)


@main.command()
@click.argument(
    "configuration",
    type=click.Choice(("main", "profile")),
    default="main",
)
@pass_environment
def example(env, configuration):
    """Show example configuration files."""
    conf_map = {
        "main": "CONFIGURATION_SCHEMA",
        "profile": "SNAKEMAKE_PROFILE_SCHEMA",
    }
    kwargs = {}
    schema = get_schema(conf_map[configuration])
    try:
        schemafile = pkg_resources.resource_filename(
            "nbis", str(getattr(SchemaFiles, conf_map[configuration]))
        )
    except AttributeError:
        schemafile = pkg_resources.files(nbis) / "schemas" / conf_map[configuration]

    required = schema.schema.get("required", None)
    if configuration == "main":
        kwargs = {"project_name": env.home.name}

    print()
    print(f"#\n# Showing example configuration for schema {conf_map[configuration]}")
    print(f"# See schema file {schemafile} for more details.\n#")
    if required is not None:
        print(f"# Required fields: {','.join(required)}\n#")
    print()

    Config.from_schema(schema, file=sys.stdout, example=True, **kwargs)
    print()
