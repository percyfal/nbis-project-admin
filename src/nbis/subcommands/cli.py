"""nbis-admin cli: cli administration utilities

"""
import logging
import pathlib

from nbis.templates import add_template

from .config import add_config_py

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "-a",
        "--add-subcommand",
        action="store",
        help=(
            "Install subcommand template src/<project_name>/subcommands/<subcommand>.py"
        ),
        dest="subcommand",
    )
    parser.add_argument(
        "-c",
        "--add-config",
        action="store_true",
        default=False,
        help="Install config module",
    )


def add_subcommand_py(args):
    pyfile = (
        pathlib.Path("src")
        / args.project_name
        / "subcommands"
        / f"{args.subcommand}.py"
    )
    add_template(
        pyfile,
        "src/project/subcommands/subcommand.py.j2",
        project_name=args.project_name,
        subcommand=args.subcommand,
    )


def main(args):
    logger.info("Running nbis-admin cli")

    if args.subcommand is not None:
        add_subcommand_py(args)

    if args.add_config:
        add_config_py(args)
