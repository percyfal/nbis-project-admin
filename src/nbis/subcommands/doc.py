"""
nbis-admin doc: manage documentation
"""
import logging
import os
import pathlib

from nbis.config import Config

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--path", help="work on path only", action="store", default=None
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", help="build documentation", action="store_true")
    group.add_argument("--init", help="init documentation", action="store_true")


def build(args):
    """Build documentation folders"""
    config = Config(args.config_file)
    if args.path is not None:
        sources = [pathlib.Path(args.path)]
    else:
        for fn in os.listdir(config.docs.src):
            fn = pathlib.Path(os.path.join(config.docs.src, fn))
            if fn.isdir:
                sources.append(fn)


def init(args):
    """Initialize documentation folders"""
    pass


def main(args):
    logger.info("Running nbis-admin docs")

    if args.build:
        build(args)

    if args.init:
        init(args)
