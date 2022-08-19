"""nbis-admin smk: snakemake administration utilities

"""
import logging
import pathlib

from nbis.templates import add_template

from . import CommandLineError

logger = logging.getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group("add subcommand")
    group.add_argument(
        "-a",
        "--add-subcommand",
        action="store_true",
        default=False,
        help=(
            "Install snakemake subcommand templates. Will install:"
            "  1. src/<project_name>/subcommands/<subcommand>.py"
            "  2. src/snakemake/<subcommand>.smk"
        ),
    )
    group.add_argument(
        "-t",
        "--add-test",
        action="store_true",
        default=False,
        help=("Add code to deal with tests and add simple snakemake test files"),
    )
    group.add_argument(
        "-V",
        "--add-validation",
        action="store_true",
        default=False,
        help=("Add code to deal with validation and add schemas"),
    )
    parser.add_argument(
        "-p",
        "--add-profile",
        action="store_true",
        default=False,
        help=("Add local snakemake profile"),
    )


def add_subcommand(args):
    # Simple input to get subcommand name
    subcommand = input("Provide subcommand name:")
    if subcommand is None:
        raise CommandLineError("Subcommand name is required")

    # FIXME: should go with general config files
    configfile = pathlib.Path("src") / args.project_name / "config.py"
    add_template(configfile, "config.py.j2", project_name=args.project_name)
    pyfile = (
        pathlib.Path("src") / args.project_name / "subcommands" / f"{subcommand}.py"
    )
    add_template(
        pyfile,
        "subcommand.py.j2",
        project_name=args.project_name,
        subcommand=subcommand,
        test=args.add_test,
    )
    smkfile = pathlib.Path("src") / "snakemake" / f"{subcommand}.smk"
    add_template(
        smkfile,
        "subcommand.smk.j2",
        project_name=args.project_name,
        subcommand=subcommand,
        test=args.add_test,
        validation=args.add_validation,
    )


def add_local_profile(args):
    localprofile = pathlib.Path("config") / "local" / "config.yaml"
    add_template(localprofile, "profile.yaml.j2")


def main(args):
    logger.info("Running nbis-admin smk")

    if args.add_subcommand:
        add_subcommand(args)

    if args.add_profile:
        add_local_profile(args)
