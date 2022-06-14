"""
nbis-admin config: administrate configuration
"""
import logging

from nbis.config import Config

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--init", action="store_true", help="create a configuration file"
    )
    parser.add_argument("--dry-run", action="store_true", help="dry run")
    parser.add_argument("--show", action="store_true", help="show configuration")


def init(args):
    Config.init(prog=args.prog)


def main(args):
    logger.info("Running nbis-admin config")

    if args.init:
        init(args)
