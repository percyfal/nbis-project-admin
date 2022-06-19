"""
nbis-admin config: administrate configuration
"""
import logging

import pkg_resources
from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


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

    yaml = YAML()
    schemafile = pkg_resources.resource_filename(
        "nbis", SchemaFiles.CONFIGURATION_SCHEMA
    )
    with open(schemafile) as fh:
        schemadict = yaml.load(fh)
    schema = Schema(schemadict)
    with open(args.config_file, "w") as fh:
        Config.from_schema(schema, file=fh)


def main(args):
    logger.info("Running nbis-admin config")

    if args.config_file is None:
        args.config_file = f"{args.prog}.yaml"

    if args.init:
        init(args)
