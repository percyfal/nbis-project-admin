"""
nbis-admin diary: manage diary entries
"""
import logging
import os
import sys
from datetime import date

from nbis.templates import env

from . import SubcommandError

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument("--init", help="init empty diary", action="store_true")
    parser.add_argument(
        "--diary-file",
        "-d",
        help="diary file name",
        action="store",
        default="docs/diary.md",
    )


def init_diary(args):
    if os.path.exists(args.diary_file):
        logger.warning(f"{args.diary_file} already exists; skipping init")
        raise SubcommandError
    try:
        with open(args.diary_file, "w") as fh:
            sysargs = " ".join(sys.argv[1:])
            template = env.get_template("diary.md.j2")
            fh.write(
                template.render(
                    project_name=args.project_name, args=sysargs, date=date.today()
                )
            )
    except FileNotFoundError:
        logger.error(f"Make sure parent directory exists: {args.diary_file}")
        raise


def main(args):
    logger.info("Running nbis-admin diary")

    if args.init:
        init_diary(args)
