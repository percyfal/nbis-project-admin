"""nbis-admin smk: snakemake administration utilities

"""
import logging
import pathlib

from nbis.templates import add_template

from .config import add_config_py

logger = logging.getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group("add subcommand")
    group.add_argument(
        "-a",
        "--add-subcommand",
        action="store",
        help=(
            "Install snakemake subcommand templates. Will install:"
            "  1. src/<project_name>/subcommands/<subcommand>.py"
            "  2. src/snakemake/rules/<subcommand>.smk"
        ),
        dest="subcommand",
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
    parser.add_argument(
        "--init",
        action="store_true",
        default=False,
        help=(
            "Install minimal config, sample and schema files. "
            "Will install config/config.yaml, resources/samples.tsv, "
            "schemas/config.schema.yaml and schemas/samples.schema.yaml."
        ),
    )


def add_subcommand_smk_py(args):
    pyfile = (
        pathlib.Path("src")
        / args.project_name
        / "subcommands"
        / f"{args.subcommand}.py"
    )
    add_template(
        pyfile,
        "src/project/subcommands/subcommand.smk.py.j2",
        project_name=args.project_name,
        subcommand=args.subcommand,
        test=args.add_test,
    )


def add_subcommand_smk(args):
    smkfile = pathlib.Path("src") / "snakemake" / "rules" / f"{args.subcommand}.smk"
    add_template(
        smkfile,
        "src/snakemake/rules/subcommand.smk.j2",
        project_name=args.project_name,
        subcommand=args.subcommand,
        test=args.add_test,
        validation=args.add_validation,
    )


def add_test_config(args):
    smkfile = pathlib.Path("src") / "snakemake" / "rules" / "test-config.smk"
    add_template(
        smkfile,
        "src/snakemake/rules/test-config.smk.j2",
    )


def add_test_smk_setup(args):
    smkfile = (
        pathlib.Path("src")
        / "snakemake"
        / "rules"
        / f"test-{args.subcommand}-setup.smk"
    )
    add_template(
        smkfile, "src/snakemake/rules/test-setup.smk.j2", subcommand=args.subcommand
    )


def add_config_yaml(args):
    yamlconf = pathlib.Path("config") / "config.yaml"
    add_template(yamlconf, "config/config.yaml.j2")


def add_config_schema_yaml(args):
    confschema = pathlib.Path("schemas") / "config.schema.yaml"
    add_template(confschema, "schemas/config.schema.yaml.j2")


def add_samples_schema_yaml(args):
    sampleschema = pathlib.Path("schemas") / "samples.schema.yaml"
    add_template(sampleschema, "schemas/samples.schema.yaml.j2")


def add_samples_tsv(args):
    samplestsv = pathlib.Path("resources") / "samples.tsv"
    add_template(samplestsv, "resources/samples.tsv.j2")


def add_subcommand(args):
    add_config_py(args)
    add_subcommand_smk_py(args)
    add_subcommand_smk(args)
    if args.add_test:
        add_test_config(args)
        add_test_smk_setup(args)


def init(args):
    add_config_yaml(args)
    add_config_schema_yaml(args)
    add_samples_schema_yaml(args)
    add_samples_tsv(args)


def add_local_profile(args):
    localprofile = pathlib.Path("config") / "local" / "config.yaml"
    add_template(localprofile, "profile.yaml.j2")


def main(args):
    logger.info("Running nbis-admin smk")

    if args.subcommand is not None:
        add_subcommand(args)

    if args.add_profile:
        add_local_profile(args)

    if args.init:
        init(args)
