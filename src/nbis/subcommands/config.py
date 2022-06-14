"""
nbis-admin config: administrate configuration
"""
import logging
import os
import subprocess

import pkg_resources
from nbis.config import Config
from nbis.config import ConfigSchema
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--init", action="store_true", help="create a configuration file"
    )
    parser.add_argument("--dry-run", action="store_true", help="dry run")
    parser.add_argument("--show", action="store_true", help="show configuration")


def init(args):
    CONFIGFILE = f"{args.cmd}.yaml"
    if os.path.exists(CONFIGFILE):
        logger.warning(f"{CONFIGFILE} exists; please edit manually")
        return
    schemafile = pkg_resources.resource_filename("nbis", ConfigSchema.PATH)
    with open(schemafile) as fh:
        schema = YAML().load(fh)
    config = ConfigSchema(schema, name=args.cmd)
    # Use project command as default
    config.properties[0].default = args.cmd
    with open(CONFIGFILE, "w") as fh:
        fh.write(str(config))


def main(args):
    logger.info("Running nbis-admin config")

    if args.init:
        init(args)
